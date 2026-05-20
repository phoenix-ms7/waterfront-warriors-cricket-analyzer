import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai

# 1. Page Setup
st.set_page_config(page_title="Waterfront Warriors AI", layout="wide")
st.title("🏏 Waterfront Warriors AI Strategist")
st.write("Pulling the latest player stats from CricClubs...")

# 2. Set up Google Gemini AI using the hidden Streamlit Secrets
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# 3. Your CricClubs URL (2026 Weekenders Tournament)
url = "https://cricclubs.com/NJSBCL/viewTeam.do?teamId=3613&clubId=2690"

# 4. The "Disguise" to bypass the 403 Forbidden error
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    # Fetch the webpage using the disguise
    response = requests.get(url, headers=headers)
    
    # Pass the HTML to Pandas to find the tables
    tables = pd.read_html(response.text, flavor="lxml")
    
    if len(tables) > 1:
        st.success("✅ Successfully pulled live stats from CricClubs!")
        
        # Usually, batting and bowling stats are the first two tables 
        batting_df = tables[0]
        bowling_df = tables[1]
        
        # Show the Data in two columns on the screen
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏏 Batting Stats")
            st.dataframe(batting_df.head(10)) # Shows the top 10 rows
            
        with col2:
            st.subheader("⚾ Bowling Stats")
            st.dataframe(bowling_df.head(10))
            
        # The AI Strategy Section
        st.divider() # Draws a neat line across the screen
        st.subheader("🤖 AI Game Plan Generator")
        
        if st.button("Generate Strategy for Next Match"):
            with st.spinner("Coach Gemini is analyzing the numbers..."):
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # The instructions we secretly send to the AI
                prompt = f"""
                You are an expert cricket coach. Analyze this batting data: 
                {batting_df.head(10).to_string()}
                
                And this bowling data:
                {bowling_df.head(10).to_string()}
                
                Based on these numbers, give me a 3-paragraph strategy for our next match. 
                Suggest an ideal batting order and which bowlers to rely on for the powerplay and death overs.
                """
                
                strategy = model.generate_content(prompt)
                st.success("Strategy Ready!")
                st.write(strategy.text)
                
        # Bonus: YouTube Integration
        st.divider()
        st.subheader("📺 Latest Match Highlights")
        st.write("Watch our recent matches from our YouTube channel.")
        # Just replace this link inside the quotes with your team's YouTube video!
        st.video("https://www.youtube.com/@WaterfrontWarriors")

    else:
        st.warning("Could not find the stats tables on this page.")

except Exception as e:
    st.error(f"Error scraping data: {e}")
