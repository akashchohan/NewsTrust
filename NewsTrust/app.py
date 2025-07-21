import streamlit as st
import time
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="NewsTrust",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Coffee Theme ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Create a css file 'style.css' and add the css code below
# Or create the file dynamically
css = """
/* Main page background */
.main {
    background-color: #F5EFE6; /* <-- CHANGE THIS for a different shade of light brown */
    color: #4E342E;
}

/* Text input box */
.stTextInput > div > div > input {
    background-color: #EBE3D5;
    color: #4E342E !important;
    border-color: #A47551;
}

/* Select box */
.stSelectbox > div > div {
    background-color: #EBE3D5;
    border-color: #A47551;
}

/* Button styling */
.stButton > button {
    background-color: #6D4C41; /* Dark brown */
    color: #FFFFFF;
    border-radius: 12px;
    border: 2px solid #5D4037;
    font-weight: bold;
    transition: all 0.2s;
}

.stButton > button {
    background-color: #6D4C41; /* <-- CHANGE THIS for a different dark brown */
    color: #FFFFFF;
    border-radius: 12px;      /* <-- INCREASE this for rounder corners (e.g., 20px) */
    border: 2px solid #5D4037;
    font-weight: bold;
}

/* Section headers */
h1, h2, h3 {
    color: #4E342E; /* Dark brown for headers */
}

/* Animation styling */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.report-container {
    animation: fadeIn 1s;
    background-color: #EBE3D5; /* Lighter shade for the report card */
    padding: 2rem;
    border-radius: 15px;
    border: 2px solid #D7C0AE;
}

"""

# Create the style.css file
with open("style.css", "w") as f:
    f.write(css)

local_css("style.css")

# --- MOCKUP BACKEND FUNCTIONS ---
# In a real project, these functions would perform API calls and NLP analysis.

def get_trusted_sources_for_country(country):
    """Returns a list of trusted news sources for a given country."""
    # In a real app, this would come from a database or a config file.
    sources = {
        "USA": ["nytimes.com", "apnews.com", "reuters.com", "pbs.org/newshour"],
        "India": ["thehindu.com", "pib.gov.in", "indianexpress.com", "ndtv.com"],
        "UK": ["bbc.co.uk/news", "reuters.com/world/uk", "theguardian.com/uk"],
        "Canada": ["cbc.ca/news", "ctvnews.ca", "theglobeandmail.com"],
    }
    return sources.get(country, [])

def fetch_and_analyze_news(headline, country):
    """
    MOCKUP: Simulates fetching news, analyzing it with SBERT, and returning results.
    """
    # 1. Fetch real news from trusted sources (replace this with a real API call).
    # 2. Use SBERT to compare user's headline with fetched headlines.
    # 3. Calculate a score based on similarity.

    # This is a dummy response for demonstration.
    time.sleep(2) # Simulate network delay and analysis time

    # Let's pretend we found some matches
    if "election" in headline.lower() and country == "USA":
        return {
            "trust_score": 92,
            "sources": [
                {"title": "Official Election Results Certified by National Board", "url": "https://apnews.com/elections", "source": "AP News"},
                {"title": "Election Day sees record turnout, results pending", "url": "https://www.reuters.com/elections", "source": "Reuters"}
            ],
            "summary": "High confidence. Similar reports were found on multiple high-authority news sites."
        }
    elif "monsoon" in headline.lower() and country == "India":
         return {
            "trust_score": 85,
            "sources": [
                {"title": "Monsoon covers entire country, says IMD", "url": "https://pib.gov.in/imd-report", "source": "Press Information Bureau"},
                {"title": "Heavy rains lash coastal regions as monsoon intensifies", "url": "https://www.thehindu.com/weather", "source": "The Hindu"}
            ],
            "summary": "Good confidence. The topic is actively being reported by official government sources and major national newspapers."
        }
    else:
        return {
            "trust_score": 15,
            "sources": [],
            "summary": "Low confidence. We could not find any matching reports from trusted national sources. This could be misinformation or a very new, unverified event."
        }


# --- UI LAYOUT ---

st.title("☕ NewsTrust Verification")
st.markdown("Enter a news headline to check its authenticity against trusted sources.")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    country = st.selectbox(
        "Select Country of Origin",
        ("USA", "India", "UK", "Canada"),
        index=0
    )

with col2:
    user_headline = st.text_input(
        "Enter Headline Here",
        placeholder="e.g., Are the recent election results official?"
    )

if st.button("🔍 Verify Headline", use_container_width=True):
    if user_headline and country:
        with st.spinner(f"Analyzing headline against trusted sources in {country}..."):
            report = fetch_and_analyze_news(user_headline, country)

        st.markdown("---")
        st.header("Verification Report")

        # Display the report in a styled container
        with st.container():
            st.markdown('<div class="report-container">', unsafe_allow_html=True)

            score = report['trust_score']

            if score > 75:
                st.subheader(f"Trust Score: {score}% (High Confidence)")
                st.success(report['summary'])
            elif score > 40:
                st.subheader(f"Trust Score: {score}% (Moderate Confidence)")
                st.warning(report['summary'])
            else:
                st.subheader(f"Trust Score: {score}% (Low Confidence)")
                st.error(report['summary'])

            if report['sources']:
                st.markdown("#### Found on Trusted Sources:")
                for source in report['sources']:
                    st.markdown(f"- **[{source['title']}]({source['url']})** on *{source['source']}*")
            else:
                 st.markdown("#### No matching articles found on major sources.")

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a headline and select a country.")

st.markdown(
    "<br><br><div style='text-align: center; color: #A47551;'>Powered by Streamlit & AI</div>",
    unsafe_allow_html=True
)