import streamlit as st
import streamlit.components.v1 as components # Needed for the Print Button
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="ARGUS", page_icon="👁️", layout="wide")

# --- 2. STYLE ---
st.markdown("""
<style>
    .big-font { font-size:40px !important; font-family: 'Courier New'; font-weight: bold; color: #00ff00; }
    .stApp { background-color: #000000; color: #00ff00; }
    .citation-box { border: 2px solid #00ff00; padding: 20px; text-align: center; font-family: 'Courier New'; }
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
    st.markdown('<p class="big-font">ARGUS ONLINE</p>', unsafe_allow_html=True)

st.caption("SAFE MODE PROTOCOL // AUTH: ZOSCHE")
st.divider()

# --- 3. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📡 RADAR", "🔐 COMMS", "💪 BIO", "⚖️ ENFORCEMENT"])

# --- TAB 1: RADAR ---
with tab1:
    st.write("### 🛰️ SECTOR SCAN")
    city_input = st.text_input("COORDINATES:", "Newton")
    if st.button("SCAN"):
        import urllib.request
        import json
        import urllib.parse
        try:
            with st.spinner("ACQUIRING LOCK..."):
                safe_city = urllib.parse.quote(city_input)
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={safe_city}&count=1&language=en&format=json"
                with urllib.request.urlopen(geo_url) as response:
                    geo_data = json.loads(response.read().decode())
                if "results" in geo_data:
                    lat = geo_data["results"][0]["latitude"]
                    lon = geo_data["results"][0]["longitude"]
                    w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,rain&temperature_unit=fahrenheit&wind_speed_unit=mph"
                    with urllib.request.urlopen(w_url) as w_res:
                        w_data = json.loads(w_res.read().decode())
                    curr = w_data['current']
                    c1, c2, c3 = st.columns(3)
                    c1.metric("TEMP", f"{curr['temperature_2m']}°F")
                    c2.metric("WIND", f"{curr['wind_speed_10m']} MPH")
                    c3.metric("RAIN", f"{curr['rain']} MM")
                else:
                    st.error("TARGET NOT FOUND")
        except Exception as e:
            st.error(f"SCAN FAILURE: {e}")

# --- TAB 2: COMMS ---
with tab2:
    st.write("### 🔐 ENCRYPTION")
    txt = st.text_input("MESSAGE:")
    if st.button("ENCRYPT"):
        import base64
        encoded = base64.b64encode(txt.encode()).decode()
        st.code(encoded)

# --- TAB 3: BIO ---
with tab3:
    st.write("### 🧬 STATUS")
    c1, c2 = st.columns(2)
    with c1:
        st.checkbox("Hydration")
        st.checkbox("Training")
        st.checkbox("Creatine")
    with c2:
        st.checkbox("Read 10 Pages")
        st.checkbox("Code Practice")
    st.progress(0.5)

# --- TAB 4: ENFORCEMENT (NEW) ---
with tab4:
    st.write("### ⚖️ VIOLATION GENERATOR")
    
    # Input Form
    c1, c2 = st.columns(2)
    offender = c1.text_input("OFFENDER NAME:", "Brother")
    violation = c2.selectbox("VIOLATION TYPE:", ["MESSY ROOM", "LEAVING LIGHTS ON", "BAD MUSIC", "FORGOT CHORES", "CUSTOM"])
    
    if violation == "CUSTOM":
        violation = st.text_input("ENTER CUSTOM VIOLATION:")
        
    fine = st.text_input("PENALTY / FINE:", "10 Pushups")
    
    # The Visual Ticket
    st.divider()
    st.markdown(f"""
    <div class="citation-box">
        <h2>⚠️ OFFICIAL ARGUS CITATION ⚠️</h2>
        <p><b>DATE:</b> {time.strftime("%Y-%m-%d")}</p>
        <p><b>OFFENDER:</b> {offender.upper()}</p>
        <hr style="border-color: #00ff00;">
        <h3>VIOLATION: {violation.upper()}</h3>
        <p>You have been found in violation of House Statutes.</p>
        <p><b>PENALTY ASSESSED:</b> {fine.upper()}</p>
        <br>
        <p><i>SIGNED: OFFICER ZOSCHE</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Spacer
    
    # THE PRINT BUTTON
    if st.button("🖨️ PRINT OFFICIAL CITATION"):
        # This injects a tiny Javascript command to open the Print Dialog
        components.html("<script>window.print()</script>", height=0, width=0)
