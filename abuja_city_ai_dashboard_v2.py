"""
Abuja City AI Dashboard v2.0
Enhanced with: Predictive Analytics, Crime Heatmap, Smart Recommendations, 
Multi-language Support, Data Export, and API Simulation

Deployment-ready for Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import random
import time
from datetime import datetime, timedelta
import json
import base64

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Abuja City AI Dashboard v2.0",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ENHANCED CSS
# ============================================
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .main { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); color: #e2e8f0; }
    .glass-card { background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 24px; margin: 12px 0; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); transition: transform 0.3s ease, box-shadow 0.3s ease; }
    .glass-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4); border-color: rgba(34, 197, 94, 0.3); }
    .metric-card { background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%); border-left: 4px solid #22c55e; border-radius: 12px; padding: 20px; margin: 8px 0; }
    .metric-label { font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { background: linear-gradient(90deg, #22c55e, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800 !important; font-size: 2.5rem !important; margin-bottom: 0.5rem !important; }
    .section-title { color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 10px; }
    .chat-container { background: rgba(15, 23, 42, 0.6); border-radius: 16px; padding: 20px; height: 500px; overflow-y: auto; }
    .chat-message-user { background: linear-gradient(135deg, #22c55e, #16a34a); color: white; border-radius: 16px 16px 4px 16px; padding: 12px 16px; margin: 8px 0; max-width: 80%; float: right; clear: both; }
    .chat-message-bot { background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; border-radius: 16px 16px 16px 4px; padding: 12px 16px; margin: 8px 0; max-width: 80%; float: left; clear: both; }
    .stButton>button { background: linear-gradient(135deg, #22c55e, #16a34a) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 12px 24px !important; font-weight: 600 !important; transition: all 0.3s ease !important; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3) !important; }
    .stButton>button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4) !important; }
    .sidebar .sidebar-content { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%); }
    .status-indicator { display: inline-block; width: 8px; height: 8px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite; margin-right: 8px; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    .footer { text-align: center; padding: 24px; color: #64748b; font-size: 0.85rem; border-top: 1px solid rgba(255, 255, 255, 0.1); margin-top: 40px; }
    .recommendation-card { background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(168, 85, 247, 0.1)); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 16px; margin: 8px 0; }
    .prediction-badge { display: inline-block; background: rgba(34, 197, 94, 0.2); color: #22c55e; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ============================================
# DATA & KNOWLEDGE BASE
# ============================================
ABUJA_KNOWLEDGE = {
    "history": "Abuja became Nigeria's capital on December 12, 1991, replacing Lagos. It was chosen for its central location and ethnic neutrality.",
    "population": "Abuja has approximately 3.8 million residents (2024 estimate) and is one of the fastest-growing cities in Africa.",
    "landmarks": ["Aso Rock - Iconic 400m monolith", "National Mosque - National Islamic center", "National Christian Centre - National church", "Millennium Park - Largest public park", "Jabi Lake - Recreational lake", "Zuma Rock - Gateway to Abuja", "Eagle Square - National events venue"],
    "districts": ["Wuse", "Maitama", "Asokoro", "Garki", "Gwarinpa", "Jabi", "Kubwa", "Lugbe", "Katampe"],
    "economy": "Abuja's economy is driven by government services, real estate, telecommunications, and a growing tech startup ecosystem.",
    "climate": "Tropical savanna climate with distinct wet (April-October) and dry (November-March) seasons. Average temp: 25-30°C.",
    "transport": "Nnamdi Azikiwe International Airport (ABJ), Abuja Light Rail, major highways, and ride-sharing services.",
    "culture": "Home to diverse ethnic groups including Hausa, Yoruba, Igbo, and over 250 other Nigerian ethnicities.",
    "education": "University of Abuja, Nile University, Baze University, African University of Science and Technology.",
    "tech": "Growing tech hub with innovation centers like the Abuja Technology Village and numerous startups.",
    "food": "Famous for Suya (spiced grilled meat), Pounded Yam, Egusi Soup, Jollof Rice, and Masa (rice cakes).",
    "nightlife": "Wuse 2 and Maitama offer vibrant nightlife with clubs, lounges, and live music venues.",
    "safety": "Generally safer than many Nigerian cities, with dedicated police and security presence in major districts.",
    "healthcare": "National Hospital Abuja, private hospitals like Cedarcrest, and numerous clinics across districts."
}

DISTRICT_COORDS = {
    "Wuse": [9.0765, 7.3986], "Maitama": [9.0833, 7.5167], "Asokoro": [9.0333, 7.5333],
    "Garki": [9.0167, 7.4833], "Gwarinpa": [9.1167, 7.4167], "Jabi": [9.0667, 7.4167],
    "Kubwa": [9.1667, 7.3333], "Lugbe": [8.9667, 7.3667], "Katampe": [9.0833, 7.4667],
    "Central Business District": [9.0667, 7.4833]
}

# ============================================
# AI CHATBOT WITH MULTI-LANGUAGE
# ============================================
class AbujaAIBot:
    def __init__(self):
        self.context = []
    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        if any(word in user_input for word in ["hola", "buenos", "como"]):
            return "Hola! Bienvenido al Abuja City AI. Puedo ayudarte a explorar la capital de Nigeria."
        if any(word in user_input for word in ["bonjour", "salut", "comment"]):
            return "Bonjour! Bienvenue à Abuja City AI. Je peux vous aider à explorer la capitale du Nigeria."
        if any(word in user_input for word in ["hallo", "guten", "wie"]):
            return "Hallo! Willkommen beim Abuja City AI. Ich kann Ihnen helfen, die Hauptstadt Nigerias zu erkunden."
        if any(word in user_input for word in ["ciao", "buongiorno", "come"]):
            return "Ciao! Benvenuto ad Abuja City AI. Posso aiutarti a esplorare la capitale della Nigeria."
        greetings = ["hello", "hi", "hey", "greetings", "salutations", "good morning", "good afternoon", "good evening"]
        if any(g in user_input for g in greetings):
            return "Hello! Welcome to Abuja City AI. I can help you explore Nigeria's capital. Ask me about landmarks, districts, culture, food, or anything about Abuja!"
        if any(word in user_input for word in ["help", "what can you do", "capabilities", "features"]):
            return """I can help you with:
  Historical facts about Abuja
  Information about districts and landmarks
  Real-time city analytics and data
  Weather updates and forecasts
  Traffic conditions and routes
  Economic and demographic insights
  Cultural events and attractions
  Food and restaurant recommendations
  Real estate and housing info
  Safety and security information"""

Try asking something specific!"
        if any(word in user_input for word in ["landmark", "places", "visit", "see", "tourist", "attraction", "monument"]):
            landmarks = "\n".join([f"• {lm}" for lm in ABUJA_KNOWLEDGE["landmarks"]])
            return f"Here are Abuja's top landmarks you should visit:\n\n{landmarks}\n\nWould you like details about any specific place?"
        if any(word in user_input for word in ["district", "area", "neighborhood", "zone", "where"]):
            districts = ", ".join(ABUJA_KNOWLEDGE["districts"])
            return f"Abuja's major districts include: {districts}.\n\nMaitama and Asokoro are upscale residential areas, Wuse is the commercial hub, Gwarinpa is the largest housing estate in West Africa, and the CBD houses government offices."
        if any(word in user_input for word in ["food", "eat", "cuisine", "restaurant", "dish", "meal", "suya", "jollof"]):
            return f"Abuja's culinary scene is amazing! {ABUJA_KNOWLEDGE['food']}\n\nTop spots: Nkoyo (local cuisine), BluCabana (continental), Wakkis (Indian), and street food at Wuse Market."
        if any(word in user_input for word in ["history", "capital", "when", "built", "founded", "created"]):
            return f"{ABUJA_KNOWLEDGE['history']} The city was master-planned by Japanese architect Kenzo Tange. It sits in the center of Nigeria, symbolizing national unity."
        if any(word in user_input for word in ["population", "people", "residents", "live", "how many"]):
            return f"{ABUJA_KNOWLEDGE['population']} The city continues to attract people from all over Nigeria and West Africa."
        if any(word in user_input for word in ["economy", "business", "job", "work", "money", "industry", "tech", "startup"]):
            return f"{ABUJA_KNOWLEDGE['economy']} The city is also emerging as a fintech hub with companies like Flutterwave and Paystack having significant presence."
        if any(word in user_input for word in ["weather", "climate", "rain", "hot", "cold", "temperature", "season"]):
            return f"{ABUJA_KNOWLEDGE['climate']} The harmattan season (December-February) brings dusty winds from the Sahara. Pack light clothing and an umbrella!"
        if any(word in user_input for word in ["transport", "airport", "flight", "train", "road", "bus", "move", "travel"]):
            return f"{ABUJA_KNOWLEDGE['transport']} The Abuja Light Rail connects the airport to the city center. Uber, Bolt, and local taxis are readily available."
        if any(word in user_input for word in ["culture", "people", "ethnic", "tribe", "language", "diversity"]):
            return f"{ABUJA_KNOWLEDGE['culture']} This diversity creates a rich cultural tapestry with festivals like the Abuja Carnival celebrating all ethnic groups."
        if any(word in user_input for word in ["school", "university", "education", "study", "learn", "college"]):
            return f"{ABUJA_KNOWLEDGE['education']} The city also has excellent secondary schools and international schools like the American International School."
        if any(word in user_input for word in ["nightlife", "club", "bar", "party", "fun", "entertainment", "drink"]):
            return f"{ABUJA_KNOWLEDGE['nightlife']} Popular spots include Play Lounge, The Cube, and Sky Bar at the Transcorp Hilton."
        if any(word in user_input for word in ["safe", "safety", "security", "danger", "crime", "police"]):
            return f"{ABUJA_KNOWLEDGE['safety']} However, as with any major city, exercise standard precautions especially at night and in less populated areas."
        if any(word in user_input for word in ["health", "hospital", "doctor", "medical", "clinic", "pharmacy"]):
            return f"{ABUJA_KNOWLEDGE['healthcare']} The city has excellent medical facilities compared to other Nigerian cities."
        default_responses = [
            "That's an interesting question about Abuja! While I don't have specific information on that, I can tell you about Abuja's landmarks, districts, food, culture, or economy. What would you like to know?",
            "Great question! Abuja is a fascinating city. I can help you with information about visiting, living, working, or exploring Abuja. What specific aspect interests you?",
            "I'd love to help you explore Abuja! Ask me about the best places to visit, where to eat, the tech scene, or the different districts. I'm here to guide you!"
        ]
        return random.choice(default_responses)

if 'abuja_bot' not in st.session_state:
    st.session_state.abuja_bot = AbujaAIBot()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# ============================================
# SIMULATION FUNCTIONS
# ============================================
def generate_weather_data():
    current_hour = datetime.now().hour
    base_temp = 28 + 4 * np.sin((current_hour - 6) * np.pi / 12)
    return {"temperature": round(base_temp + random.uniform(-2, 2), 1), "feels_like": round(base_temp + random.uniform(-1, 3), 1), "humidity": random.randint(45, 85), "wind_speed": round(random.uniform(5, 20), 1), "condition": random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Light Rain"]), "uv_index": random.randint(3, 11), "visibility": random.randint(8, 10), "pressure": random.randint(1008, 1015)}

def generate_traffic_data():
    districts = list(DISTRICT_COORDS.keys())
    traffic_data = []
    for district in districts:
        base_congestion = random.uniform(20, 60)
        if district in ["Central Business District", "Wuse"]:
            base_congestion += 25
        elif district in ["Maitama", "Asokoro"]:
            base_congestion -= 10
        traffic_data.append({"District": district, "Congestion": min(100, round(base_congestion + random.uniform(-10, 10), 1)), "Avg_Speed_kmh": round(random.uniform(15, 60), 1), "Incidents": random.randint(0, 5), "Road_Quality": random.randint(60, 95)})
    return pd.DataFrame(traffic_data)

def generate_population_data():
    years = list(range(2000, 2026))
    population = []
    base = 800000
    for year in years:
        growth_rate = random.uniform(0.05, 0.09)
        base = int(base * (1 + growth_rate))
        population.append({"Year": year, "Population": base, "Growth_Rate": round(growth_rate * 100, 2)})
    return pd.DataFrame(population)

def generate_sentiment_data():
    topics = ["Infrastructure", "Security", "Cost of Living", "Traffic", "Nightlife", "Food", "Weather", "Job Market", "Housing", "Entertainment"]
    sentiment_data = []
    for topic in topics:
        sentiment_data.append({"Topic": topic, "Positive": random.randint(40, 85), "Neutral": random.randint(10, 30), "Negative": random.randint(5, 25)})
    return pd.DataFrame(sentiment_data)

def generate_real_estate_data():
    districts = ["Maitama", "Asokoro", "Wuse", "Garki", "Jabi", "Gwarinpa", "Kubwa", "Lugbe"]
    real_estate = []
    for district in districts:
        base_price = random.uniform(300000, 1500000)
        if district in ["Maitama", "Asokoro"]:
            base_price *= 2.5
        elif district in ["Wuse", "Garki"]:
            base_price *= 1.5
        real_estate.append({"District": district, "Avg_Price_NGN": int(base_price), "Price_per_sqm": int(base_price / 200), "YoY_Change": round(random.uniform(-5, 25), 1), "Rental_Yield": round(random.uniform(3, 8), 1)})
    return pd.DataFrame(real_estate)

def generate_crime_data():
    districts = list(DISTRICT_COORDS.keys())
    crime_types = ["Theft", "Assault", "Fraud", "Traffic Violation", "Vandalism"]
    crime_data = []
    for district in districts:
        for crime in crime_types:
            crime_data.append({"District": district, "Crime_Type": crime, "Incidents": random.randint(5, 80), "Resolution_Rate": round(random.uniform(40, 95), 1)})
    return pd.DataFrame(crime_data)

def generate_predictive_data():
    months = pd.date_range(start='2024-01-01', periods=12, freq='M')
    predictive_data = []
    for i, month in enumerate(months):
        predictive_data.append({"Month": month.strftime("%b %Y"), "Predicted_Traffic": round(50 + 20 * np.sin(i * np.pi / 6) + random.uniform(-5, 5), 1), "Predicted_Population": round(3.8 + 0.05 * i + random.uniform(-0.02, 0.02), 2), "Predicted_Rent": round(1.2 + 0.1 * i + random.uniform(-0.05, 0.05), 2), "Confidence": round(random.uniform(75, 95), 1)})
    return pd.DataFrame(predictive_data)

def create_abuja_map():
    m = folium.Map(location=[9.0765, 7.3986], zoom_start=12, tiles="CartoDB dark_matter")
    for district, coords in DISTRICT_COORDS.items():
        folium.Marker(coords, popup=f"<b>{district}</b><br>Major District of Abuja", tooltip=district, icon=folium.Icon(color="green", icon="info-sign")).add_to(m)
    landmarks = {"Aso Rock": [9.0833, 7.5167], "National Mosque": [9.0579, 7.4951], "National Christian Centre": [9.0579, 7.4951], "Millennium Park": [9.0765, 7.4986], "Zuma Rock": [9.1333, 7.2333], "Eagle Square": [9.0667, 7.4833], "Jabi Lake": [9.0667, 7.4167]}
    for name, coords in landmarks.items():
        folium.Marker(coords, popup=f"<b>{name}</b><br>Popular Landmark", tooltip=name, icon=folium.Icon(color="blue", icon="star")).add_to(m)
    heat_data = [[coords[0], coords[1], random.randint(50, 100)] for coords in DISTRICT_COORDS.values()]
    HeatMap(heat_data).add_to(m)
    return m

def create_crime_heatmap():
    m = folium.Map(location=[9.0765, 7.3986], zoom_start=12, tiles="CartoDB dark_matter")
    crime_points = []
    for district, coords in DISTRICT_COORDS.items():
        intensity = random.randint(20, 80)
        if district in ["Wuse", "Central Business District"]:
            intensity += 20
        crime_points.append([coords[0], coords[1], intensity])
    HeatMap(crime_points, radius=25, blur=15, max_zoom=13).add_to(m)
    return m

# ============================================
# DATA EXPORT FUNCTIONS
# ============================================
def get_csv_download_link(df, filename="data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="background: linear-gradient(135deg, #22c55e, #16a34a); color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600;">📥 Download CSV</a>'

def get_json_download_link(data, filename="data.json"):
    json_str = json.dumps(data, indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    return f'<a href="data:application/json;base64,{b64}" download="{filename}" style="background: linear-gradient(135deg, #3b82f6, #2563eb); color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600;">📥 Download JSON</a>'

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2rem; margin-bottom: 0;">🏛️</h1>
        <h2 style="background: linear-gradient(90deg, #22c55e, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">Abuja AI</h2>
        <p style="color: #64748b; font-size: 0.85rem;">Smart City Dashboard v2.0</p>
    </div>
    """)
    st.markdown("---")
    page = st.radio("Navigate", ["🏠 Home", "🗺️ Interactive Map", "📊 Analytics", "🔮 Predictions", "🤖 AI City Guide", "🏘️ Districts", "📈 Real Estate", "🚨 Crime Monitor", "💾 Data Export"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
    <div class="glass-card" style="padding: 16px;">
        <p style="margin: 0; font-size: 0.9rem;"><span class="status-indicator"></span><strong style="color: #22c55e;">System Online</strong></p>
        <p style="margin: 8px 0 0 0; font-size: 0.75rem; color: #64748b;">Data refreshed: {}<br>AI Model: AbujaBot v2.1<br>API Status: Active</p>
    </div>
    """.format(datetime.now().strftime("%H:%M:%S")), unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="padding: 10px;">
        <p style="color: #64748b; font-size: 0.8rem; margin-bottom: 8px;">QUICK STATS</p>
        <p style="margin: 4px 0; font-size: 0.9rem;">📍 9 Districts</p>
        <p style="margin: 4px 0; font-size: 0.9rem;">🏛️ 7 Landmarks</p>
        <p style="margin: 4px 0; font-size: 0.9rem;">🌡️ 28°C Avg</p>
        <p style="margin: 4px 0; font-size: 0.9rem;">👥 3.8M People</p>
    </div>
    """)

# ============================================
# MAIN CONTENT
# ============================================

if page == "🏠 Home":
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 16px;">
            <span style="background: linear-gradient(90deg, #22c55e, #3b82f6, #22c55e); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Abuja City AI v2.0</span>
        </h1>
        <p style="font-size: 1.25rem; color: #94a3b8; max-width: 600px; margin: 0 auto 32px;">Experience Nigeria's capital through AI-powered insights, interactive visualizations, and intelligent city exploration.</p>
        <div style="display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;">
            <span style="background: rgba(34, 197, 94, 0.1); color: #22c55e; padding: 8px 16px; border-radius: 20px; font-size: 0.85rem;">🤖 AI-Powered</span>
            <span style="background: rgba(59, 130, 246, 0.1); color: #3b82f6; padding: 8px 16px; border-radius: 20px; font-size: 0.85rem;">📊 Real-time Data</span>
            <span style="background: rgba(168, 85, 247, 0.1); color: #a855f7; padding: 8px 16px; border-radius: 20px; font-size: 0.85rem;">🗺️ Interactive Maps</span>
            <span style="background: rgba(249, 115, 22, 0.1); color: #f97316; padding: 8px 16px; border-radius: 20px; font-size: 0.85rem;">🔮 Predictions</span>
        </div>
    </div>
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><p class="metric-label">Population</p><p class="metric-value">3.8M</p><p style="color: #22c55e; font-size: 0.85rem;">▲ +6.2% YoY</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><p class="metric-label">Area</p><p class="metric-value">1,769</p><p style="color: #94a3b8; font-size: 0.85rem;">km²</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><p class="metric-label">Elevation</p><p class="metric-value">360</p><p style="color: #94a3b8; font-size: 0.85rem;">meters</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><p class="metric-label">Founded</p><p class="metric-value">1991</p><p style="color: #3b82f6; font-size: 0.85rem;">Capital since</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">🌤️ Live Weather</p>', unsafe_allow_html=True)
    weather = generate_weather_data()
    wcol1, wcol2, wcol3, wcol4, wcol5 = st.columns(5)
    with wcol1:
        st.markdown(f'<div class="glass-card" style="text-align: center;"><p style="font-size: 2.5rem; margin: 0;">🌡️</p><p style="font-size: 1.8rem; font-weight: 700; color: #f97316; margin: 8px 0;">{weather["temperature"]}°C</p><p style="color: #94a3b8; font-size: 0.85rem;">Temperature</p></div>', unsafe_allow_html=True)
    with wcol2:
        st.markdown(f'<div class="glass-card" style="text-align: center;"><p style="font-size: 2.5rem; margin: 0;">💧</p><p style="font-size: 1.8rem; font-weight: 700; color: #3b82f6; margin: 8px 0;">{weather["humidity"]}%</p><p style="color: #94a3b8; font-size: 0.85rem;">Humidity</p></div>', unsafe_allow_html=True)
    with wcol3:
        st.markdown(f'<div class="glass-card" style="text-align: center;"><p style="font-size: 2.5rem; margin: 0;">💨</p><p style="font-size: 1.8rem; font-weight: 700; color: #a855f7; margin: 8px 0;">{weather["wind_speed"]} km/h</p><p style="color: #94a3b8; font-size: 0.85rem;">Wind Speed</p></div>', unsafe_allow_html=True)
    with wcol4:
        st.markdown(f'<div class="glass-card" style="text-align: center;"><p style="font-size: 2.5rem; margin: 0;">☀️</p><p style="font-size: 1.8rem; font-weight: 700; color: #fbbf24; margin: 8px 0;">{weather["uv_index"]}</p><p style="color: #94a3b8; font-size: 0.85rem;">UV Index</p></div>', unsafe_allow_html=True)
    with wcol5:
        st.markdown(f'<div class="glass-card" style="text-align: center;"><p style="font-size: 2.5rem; margin: 0;">👁️</p><p style="font-size: 1.8rem; font-weight: 700; color: #22c55e; margin: 8px 0;">{weather["visibility"]} km</p><p style="color: #94a3b8; font-size: 0.85rem;">Visibility</p></div>', unsafe_allow_html=True)

elif page == "🗺️ Interactive Map":
    st.markdown('<p class="section-title">🗺️ Interactive City Map</p>', unsafe_allow_html=True)
    map_col1, map_col2 = st.columns([3, 1])
    with map_col1:
        abuja_map = create_abuja_map()
        st_folium(abuja_map, width=900, height=600, returned_objects=[])
    with map_col2:
        st.markdown('<div class="glass-card"><p style="color: #22c55e; font-weight: 600; margin-bottom: 12px;">📍 LEGEND</p><p style="margin: 8px 0; font-size: 0.9rem;">🟢 <strong>Green Markers:</strong> Districts</p><p style="margin: 8px 0; font-size: 0.9rem;">🔵 <strong>Blue Stars:</strong> Landmarks</p><p style="margin: 8px 0; font-size: 0.9rem;">🔴 <strong>Heatmap:</strong> Activity Zones</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card"><p style="color: #3b82f6; font-weight: 600; margin-bottom: 12px;">🏛️ TOP LANDMARKS</p><p style="margin: 8px 0; font-size: 0.85rem;">• Aso Rock (400m monolith)</p><p style="margin: 8px 0; font-size: 0.85rem;">• National Mosque</p><p style="margin: 8px 0; font-size: 0.85rem;">• National Christian Centre</p><p style="margin: 8px 0; font-size: 0.85rem;">• Millennium Park</p><p style="margin: 8px 0; font-size: 0.85rem;">• Zuma Rock</p><p style="margin: 8px 0; font-size: 0.85rem;">• Eagle Square</p><p style="margin: 8px 0; font-size: 0.85rem;">• Jabi Lake</p></div>', unsafe_allow_html=True)

elif page == "📊 Analytics":
    st.markdown('<p class="section-title">📊 City Analytics Dashboard</p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📈 Population", "🚦 Traffic", "😊 Sentiment"])
    with tab1:
        pop_data = generate_population_data()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=pop_data['Year'], y=pop_data['Population'], name="Population", line=dict(color="#22c55e", width=3), fill='tozeroy', fillcolor='rgba(34, 197, 94, 0.1)'), secondary_y=False)
        fig.add_trace(go.Bar(x=pop_data['Year'], y=pop_data['Growth_Rate'], name="Growth Rate %", marker_color="#3b82f6", opacity=0.7), secondary_y=True)
        fig.update_layout(title="Abuja Population Growth (2000-2025)", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        traffic_data = generate_traffic_data()
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Traffic Congestion by District", "Road Quality Index"))
        fig.add_trace(go.Bar(x=traffic_data['District'], y=traffic_data['Congestion'], marker_color=traffic_data['Congestion'], marker_colorscale='RdYlGn_r', name="Congestion %"), row=1, col=1)
        fig.add_trace(go.Bar(x=traffic_data['District'], y=traffic_data['Road_Quality'], marker_color=traffic_data['Road_Quality'], marker_colorscale='RdYlGn', name="Quality Score"), row=1, col=2)
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with tab3:
        sentiment_data = generate_sentiment_data()
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Positive', x=sentiment_data['Topic'], y=sentiment_data['Positive'], marker_color='#22c55e'))
        fig.add_trace(go.Bar(name='Neutral', x=sentiment_data['Topic'], y=sentiment_data['Neutral'], marker_color='#94a3b8'))
        fig.add_trace(go.Bar(name='Negative', x=sentiment_data['Topic'], y=sentiment_data['Negative'], marker_color='#ef4444'))
        fig.update_layout(barmode='stack', title="Social Media Sentiment Analysis - Abuja Topics", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
        st.plotly_chart(fig, use_container_width=True)

elif page == "🔮 Predictions":
    st.markdown('<p class="section-title">🔮 AI Predictive Analytics</p>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card" style="margin-bottom: 20px;"><p style="color: #cbd5e1;">🤖 <strong>AI-Powered Predictions:</strong> Our machine learning models analyze historical data to forecast future trends in traffic, population, and real estate prices with confidence intervals.</p></div>', unsafe_allow_html=True)
    pred_data = generate_predictive_data()
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Traffic Congestion Forecast", "Population Growth Prediction", "Rent Price Trend", "Model Confidence"))
    fig.add_trace(go.Scatter(x=pred_data['Month'], y=pred_data['Predicted_Traffic'], mode='lines+markers', line=dict(color="#ef4444", width=3), name="Traffic %"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pred_data['Month'], y=pred_data['Predicted_Population'], mode='lines+markers', line=dict(color="#22c55e", width=3), name="Population (M)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=pred_data['Month'], y=pred_data['Predicted_Rent'], mode='lines+markers', line=dict(color="#3b82f6", width=3), name="Rent (M₦)"), row=2, col=1)
    fig.add_trace(go.Bar(x=pred_data['Month'], y=pred_data['Confidence'], marker_color='#a855f7', name="Confidence %"), row=2, col=2)
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=700, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<p class="section-title">📋 Detailed Predictions</p>', unsafe_allow_html=True)
    st.dataframe(pred_data, use_container_width=True, hide_index=True)
    st.markdown('<p class="section-title">💡 AI Insights</p>', unsafe_allow_html=True)
    insights = ["📈 <strong>Population:</strong> Expected to reach 4.2M by end of 2025 based on current migration patterns.", "🚗 <strong>Traffic:</strong> Peak congestion predicted for July-August due to rainy season delays.", "🏠 <strong>Real Estate:</strong> Maitama and Asokoro rents projected to increase 15-20% annually.", "🌧️ <strong>Weather:</strong> Above-average rainfall expected in Q3 2024, affecting outdoor activities.", "💼 <strong>Employment:</strong> Tech sector job growth predicted at 25% YoY, highest in Jabi district."]
    for insight in insights:
        st.markdown(f'<div class="recommendation-card"><p style="color: #cbd5e1; margin: 0;">{insight}</p><span class="prediction-badge">AI Generated</span></div>', unsafe_allow_html=True)

elif page == "🤖 AI City Guide":
    st.markdown('<p class="section-title">🤖 AI City Guide - AbujaBot</p>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card" style="margin-bottom: 20px;"><p style="color: #cbd5e1;">🤖 <strong>AbujaBot</strong> is your intelligent guide to Nigeria's capital. Ask about landmarks, districts, food, culture, transportation, or anything about living in and visiting Abuja!</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message-bot">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask AbujaBot anything...", placeholder="e.g., What are the best places to visit in Abuja?")
        submit = st.form_submit_button("Send Message 💬")
        if submit and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("AbujaBot is thinking..."):
                time.sleep(0.5)
                response = st.session_state.abuja_bot.get_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="color: #64748b; font-size: 0.9rem;">💡 Try asking:</p>', unsafe_allow_html=True)
    suggestions = ["What are the top landmarks?", "Tell me about Abuja's districts", "What food should I try?", "How's the tech scene?", "Is Abuja safe?", "What's the weather like?"]
    sug_col1, sug_col2, sug_col3 = st.columns(3)
    for i, suggestion in enumerate(suggestions):
        col = [sug_col1, sug_col2, sug_col3][i % 3]
        with col:
            if st.button(suggestion, key=f"sug_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": suggestion})
                response = st.session_state.abuja_bot.get_response(suggestion)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

elif page == "🏘️ Districts":
    st.markdown('<p class="section-title">🏘️ District Explorer</p>', unsafe_allow_html=True)
    districts_info = {
        "Maitama": {"type": "Upscale Residential", "description": "Abuja's most exclusive district, home to embassies, high-end residences, and luxury hotels.", "highlights": ["Transcorp Hilton", "Embassy Row", "Maitama Park", "Upscale Restaurants"], "avg_rent": "₦3M - ₦15M/year", "safety": "★★★★★"},
        "Asokoro": {"type": "Government/Residential", "description": "High-security district housing the Presidential Villa, Aso Rock, and government officials.", "highlights": ["Aso Rock", "Presidential Villa", "National Mosque", "Eagle Square"], "avg_rent": "₦2.5M - ₦12M/year", "safety": "★★★★★"},
        "Wuse": {"type": "Commercial Hub", "description": "The bustling commercial heart of Abuja with markets, malls, restaurants, and nightlife.", "highlights": ["Wuse Market", "Silverbird Cinema", "Nightlife", "Shopping Malls"], "avg_rent": "₦1.5M - ₦6M/year", "safety": "★★★★☆"},
        "Garki": {"type": "Mixed-Use", "description": "One of the oldest districts with government offices, businesses, and residential areas.", "highlights": ["Garki Market", "International Conference Centre", "Hotels", "Restaurants"], "avg_rent": "₦1M - ₦5M/year", "safety": "★★★★☆"},
        "Gwarinpa": {"type": "Residential", "description": "Home to the largest housing estate in West Africa. Popular with middle-class families.", "highlights": ["Gwarinpa Estate", "Family-friendly", "Schools", "Local Markets"], "avg_rent": "₦800K - ₦3M/year", "safety": "★★★★☆"},
        "Jabi": {"type": "Mixed-Use", "description": "Vibrant district known for Jabi Lake, shopping centers, and diverse residential options.", "highlights": ["Jabi Lake Mall", "Jabi Lake", "Parks", "Tech Hubs"], "avg_rent": "₦1M - ₦4M/year", "safety": "★★★★☆"},
        "Kubwa": {"type": "Suburban", "description": "Fast-growing satellite town with affordable housing and a large population.", "highlights": ["Affordable Housing", "Kubwa Market", "Growing Infrastructure", "Families"], "avg_rent": "₦400K - ₦1.5M/year", "safety": "★★★☆☆"},
        "Lugbe": {"type": "Emerging", "description": "Rapidly developing area near the airport with new estates and commercial developments.", "highlights": ["Airport Proximity", "New Developments", "Lower Costs", "Future Growth"], "avg_rent": "₦500K - ₦2M/year", "safety": "★★★☆☆"}
    }
    for district, info in districts_info.items():
        with st.expander(f"🏘️ {district} - {info['type']}"):
            dcol1, dcol2 = st.columns([2, 1])
            with dcol1:
                st.markdown(f'<div class="glass-card"><p style="color: #cbd5e1; line-height: 1.7;">{info["description"]}</p><p style="color: #22c55e; font-weight: 600; margin-top: 12px;">✨ Highlights:</p><ul style="color: #94a3b8; margin-top: 8px;">{"".join([f"<li>{h}</li>" for h in info["highlights"]])}</ul></div>', unsafe_allow_html=True)
            with dcol2:
                st.markdown(f'<div class="glass-card"><p style="color: #3b82f6; font-weight: 600;">💰 Average Rent</p><p style="font-size: 1.2rem; font-weight: 700; color: #f8fafc;">{info["avg_rent"]}</p><p style="color: #22c55e; font-weight: 600; margin-top: 16px;">🛡️ Safety Rating</p><p style="font-size: 1.5rem;">{info["safety"]}</p></div>', unsafe_allow_html=True)

elif page == "📈 Real Estate":
    st.markdown('<p class="section-title">📈 Real Estate Market</p>', unsafe_allow_html=True)
    re_data = generate_real_estate_data()
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Average Property Prices", "Price per sqm", "Year-over-Year Change", "Rental Yield %"))
    fig.add_trace(go.Bar(x=re_data['District'], y=re_data['Avg_Price_NGN']/1000000, marker_color='#22c55e', name="Price (M₦)"), row=1, col=1)
    fig.add_trace(go.Bar(x=re_data['District'], y=re_data['Price_per_sqm'], marker_color='#3b82f6', name="Price/sqm"), row=1, col=2)
    colors = ['#22c55e' if x > 0 else '#ef4444' for x in re_data['YoY_Change']]
    fig.add_trace(go.Bar(x=re_data['District'], y=re_data['YoY_Change'], marker_color=colors, name="YoY %"), row=2, col=1)
    fig.add_trace(go.Bar(x=re_data['District'], y=re_data['Rental_Yield'], marker_color='#a855f7', name="Yield %"), row=2, col=2)
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=700, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="glass-card"><p style="color: #22c55e; font-weight: 600; margin-bottom: 12px;">🏠 MARKET INSIGHTS</p><p style="color: #cbd5e1; line-height: 1.8;">Abuja's real estate market is one of the most dynamic in West Africa. Maitama and Asokoro command premium prices due to their exclusivity and security. Wuse offers the best commercial value, while Gwarinpa and Kubwa provide affordable family housing. The market has shown resilience with consistent year-over-year growth, making it attractive for both local and international investors.</p></div>', unsafe_allow_html=True)

elif page == "🚨 Crime Monitor":
    st.markdown('<p class="section-title">🚨 Crime Monitor & Safety Analytics</p>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card" style="margin-bottom: 20px;"><p style="color: #cbd5e1;">🛡️ <strong>Safety Analytics:</strong> Real-time crime monitoring across Abuja districts with heatmap visualization and incident resolution tracking.</p></div>', unsafe_allow_html=True)
    crime_data = generate_crime_data()
    st.markdown('<p class="section-title">🗺️ Crime Heatmap</p>', unsafe_allow_html=True)
    crime_map = create_crime_heatmap()
    st_folium(crime_map, width=900, height=500, returned_objects=[])
    st.markdown('<p class="section-title">📊 Crime Statistics by District</p>', unsafe_allow_html=True)
    crime_summary = crime_data.groupby('District').agg({'Incidents': 'sum', 'Resolution_Rate': 'mean'}).reset_index()
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Total Incidents by District", "Average Resolution Rate"))
    fig.add_trace(go.Bar(x=crime_summary['District'], y=crime_summary['Incidents'], marker_color='#ef4444', name="Incidents"), row=1, col=1)
    fig.add_trace(go.Bar(x=crime_summary['District'], y=crime_summary['Resolution_Rate'], marker_color='#22c55e', name="Resolution %"), row=1, col=2)
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<p class="section-title">📋 Crime Type Breakdown</p>', unsafe_allow_html=True)
    crime_type_summary = crime_data.groupby('Crime_Type').agg({'Incidents': 'sum', 'Resolution_Rate': 'mean'}).reset_index()
    st.dataframe(crime_type_summary, use_container_width=True, hide_index=True)

elif page == "💾 Data Export":
    st.markdown('<p class="section-title">💾 Data Export Center</p>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card" style="margin-bottom: 20px;"><p style="color: #cbd5e1;">📥 <strong>Export all city data</strong> in CSV or JSON format for your own analysis and reporting.</p></div>', unsafe_allow_html=True)

    export_tab1, export_tab2, export_tab3, export_tab4 = st.tabs(["📊 Population Data", "🚦 Traffic Data", "🏠 Real Estate Data", "🚨 Crime Data"])

    with export_tab1:
        pop_data = generate_population_data()
        st.dataframe(pop_data, use_container_width=True, hide_index=True)
        st.markdown(get_csv_download_link(pop_data, "abuja_population.csv"), unsafe_allow_html=True)
    with export_tab2:
        traffic_data = generate_traffic_data()
        st.dataframe(traffic_data, use_container_width=True, hide_index=True)
        st.markdown(get_csv_download_link(traffic_data, "abuja_traffic.csv"), unsafe_allow_html=True)
    with export_tab3:
        re_data = generate_real_estate_data()
        st.dataframe(re_data, use_container_width=True, hide_index=True)
        st.markdown(get_csv_download_link(re_data, "abuja_real_estate.csv"), unsafe_allow_html=True)
    with export_tab4:
        crime_data = generate_crime_data()
        st.dataframe(crime_data, use_container_width=True, hide_index=True)
        st.markdown(get_csv_download_link(crime_data, "abuja_crime_data.csv"), unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <p>🏛️ <strong>Abuja City AI Dashboard v2.0</strong> | Built with Streamlit & AI</p>
    <p style="margin-top: 8px;">Portfolio Project | Data simulated for demonstration purposes</p>
    <p style="margin-top: 8px; color: #475569;">© 2024 | Powered by Python, Plotly, Folium & Machine Learning</p>
</div>
""", unsafe_allow_html=True)
