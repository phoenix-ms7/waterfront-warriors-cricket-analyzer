import streamlit as st
import pandas as pd
import cloudscraper
import google.generativeai as genai
from bs4 import BeautifulSoup

st.set_page_config(page_title="Waterfront Warriors AI", layout="wide")
st.title("🏏 Waterfront Warriors AI Strategist")
st.write("Bypassing security and pulling live stats from CricClubs...")

# Set up Google Gemini AI
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

url = "https://cricclubs.com/NJSBCL/viewTeam.do?teamId=3613&clubId=2690"

try:
    # Upgrade the Disguise: Create a Cloudscraper instance to mimic a real Chrome browser
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
    response = scraper.get(url)
    
    # Check if Cloudflare blocked us again or if we got through
    if "Just a moment..." in response.text:
        st.error("🚨 Cloudflare security block is still active. CricClubs security is set very high right now.")
    else:
        # We got through! Read the tables.
        tables = pd.read_html(response.text, flavor="lxml")
        
        if len(tables) > 1:
            st.success("✅ Successfully bypassed Cloudflare and pulled live stats!")
            
            batting_df = tables[0]
            bowling_df = tables[1]
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🏏 Batting Stats")
                st.dataframe(batting_df.head(10))
            with col2:
                st.subheader("⚾ Bowling Stats")
                st.dataframe(bowling_df.head(10))
                
            st.divider()
            st.subheader("🤖 AI Game Plan Generator")
            
            if st.button("Generate Strategy"):
                with st.spinner("Coach Gemini is analyzing..."):
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = f"Analyze batting: {batting_df.head(10).to_string()} and bowling: {bowling_df.head(10).to_string()}. Give a 3-paragraph match strategy."
                    strategy = model.generate_content(prompt)
                    st.write(strategy.text)
                    
        else:
            st.warning("Bypassed security, but couldn't find the data tables.")

except Exception as e:
    st.error(f"Error: {e}")
