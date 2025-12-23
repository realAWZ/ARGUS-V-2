import streamlit as st
import json
import urllib.request
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="ARGUS", page_icon="👁️", layout="wide")

# --- CUSTOM "ARGUS" STYLE ---
st.markdown("""
<style>
    .big-font { font-size:40px !important; font-family: 'Courier New'; font-weight: bold; color: #00ff00; }
    .stApp { background-color: #000000; color: #00ff00; }
    .stButton>button { border: 1px solid #00ff00; color: #00ff00; background-color: #0e1117; font-family: 'Courier New'; }
    .stButton>button:hover { background-color: #00ff00; color: black; border: 1px solid white; }
    .stTextInput>div>div>input { color: #00ff00; background-color: #0e1117; font-family: 'Courier New'; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([1, 4])
with col1:
    st.write("# 👁️")
with col2:
    st.markdown('<p class="big-font">ARGUS SYSTEM ONLINE</p>', unsafe_allow_html=True)

st.caption("A.R.G.U.S. // AUTH: ZOSCHE")
st.divider()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📡 TACTICAL RADAR", "🔐 SECURE COMMS", "💪 BIO-METRICS"])

# --- TAB 1: RADAR (Zero-Dependency) ---
with tab1:
    st.markdown("### 🛰️ GLOBAL SECTOR SCAN")
    city_input = st.text_input("ENTER COORDINATES (CITY):", "Newton")
    
    if st.button("INITIATE SCAN"):
        try:
            # 1. Geocode (Using standard urllib)
            # We encode the city name to handle spaces (e.g. "New York")
            safe_city = urllib.parse.quote(city_input)
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={safe_city}&count=1&language=en&format=json"
            
            with urllib.request.urlopen(geo_url) as response:
                geo_data = json.loads(response.read().decode())
            
            if "results" in geo_data:
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]
                name = geo_data["results"][0]["name"]
                
                # 2. Weather Scan
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,rain&temperature_unit=fahrenheit&wind_speed_unit=mph"
                
                with urllib.request.urlopen(weather_url) as w_response:
                    w_data = json.loads(w_response.read().decode())
                
                curr = w_data['current']
                
                # 3. Display
                st.success(f"📡 LOCKED ON: {name.upper()}")
                c1, c2, c3 = st.columns(3)
                c1.metric("THERMAL", f"{curr['temperature_2m']}°F")
                c2.metric("VELOCITY", f"{curr['wind_speed_10m']} MPH")
                c3.metric("PRECIP", f"{curr['rain']} MM")
                
            else:
                st.error("❌ TARGET LOST.")
                
        except Exception as e:
            st.error(f"❌ LINK FAILURE: {e}")

# --- TAB 2: COMMS ---
with tab2:
    st.markdown("### 🔐 CRYPTOGRAPHIC RELAY")
    mode = st.radio("SELECT PROTOCOL:", ["ENCRYPT", "DECRYPT"], horizontal=True)
    text_input = st.text_area("DATA INPUT:")
    
    if st.button("EXECUTE"):
        if text_input:
            if mode == "ENCRYPT":
                encoded = base64.b64encode(text_input.encode("utf-8")).decode("utf-8")
                st.success("🔒 MESSAGE SECURED:")
                st.code(encoded, language="text")
            else:
                try:
                    decoded = base64.b64decode(text_input).decode("utf-8")
                    st.success(f"🔓 DECODED: {decoded}")
                except:
                    st.error("❌ INVALID KEY.")

# --- TAB 3: BIO-METRICS ---
with tab3:
    st.markdown("### 🧬 OPERATOR STATUS")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**PHYSICAL**")
        t1 = st.checkbox("Creatine (5g)")
        t2 = st.checkbox("Water (1 Gal)")
        t3 = st.checkbox("Workout")
    with c2:
        st.write("**CEREBRAL**")
        t4 = st.checkbox("Read 10 Pages")
        t5 = st.checkbox("Code Practice")
        t6 = st.checkbox("No Sugar")
        
    percent = sum([t1,t2,t3,t4,t5,t6]) / 6
    st.progress(percent)
    st.write(f"INTEGRITY: {int(percent*100)}%")
    if percent == 1.0: st.balloons()
