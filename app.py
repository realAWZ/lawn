import streamlit as st
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="NJ Family Court", page_icon="⚖️", layout="centered")

# --- CUSTOM CSS (To make the ticket look real) ---
st.markdown("""
<style>
    .ticket-box {
        border: 2px solid #000;
        padding: 20px;
        background-color: #fdfbf7; /* Paper color */
        font-family: 'Courier New', Courier, monospace;
    }
    .header { text-align: center; font-weight: bold; border-bottom: 2px solid black; margin-bottom: 10px; }
    .statute { font-weight: bold; color: #b30000; }
</style>
""", unsafe_allow_html=True)

st.title("🚓 Family Citation Writer")
st.caption("Official Issuance System for Household Violations")

# --- INPUT FORM ---
with st.form("ticket_form"):
    col1, col2 = st.columns(2)
    officer = col1.text_input("Issuing Officer:", value="Trooper Dad")
    defendant = col2.selectbox("Defendant:", ["Ayden", "Mom", "Brother", " The Dog", "Guest"])
    
    location = st.text_input("Location of Incident:", placeholder="Kitchen, Living Room, Driveway...")
    
    # The "Statutes"
    violation_type = st.selectbox("Violation (Title 39-H):", [
        "39:H-10 :: Failure to Refill Water Pitcher",
        "39:H-22 :: Leaving Lights On in Empty Room",
        "39:H-45 :: Thermostat Tampering (1st Degree Felony)",
        "39:H-50 :: Failure to Rinse Dish Before Loading",
        "39:H-88 :: Shoes Left in Hallway (Obstruction of Traffic)",
        "39:H-99 :: Excessive Noise / Gaming after 2300 Hours",
        "CUSTOM :: Write my own..."
    ])
    
    if "CUSTOM" in violation_type:
        custom_violation = st.text_input("Enter Custom Violation:")
    
    fine = st.selectbox("Assessed Penalty:", [
        "Verbal Warning",
        "Take Out Trash (Immediate)",
        "Empty Dishwasher",
        "Mow The Lawn",
        "Walk The Dog (2 Miles)",
        "Loss of Car Keys (24 Hours)"
    ])
    
    submitted = st.form_submit_button("🚨 ISSUE CITATION")

# --- TICKET GENERATOR ---
if submitted:
    # Handle custom text
    violation_text = custom_violation if "CUSTOM" in violation_type else violation_type
    
    st.divider()
    st.markdown("### 🖨️ CITATION GENERATED")
    
    # The Visual "Paper" Ticket
    st.markdown(f"""
    <div class="ticket-box">
        <div class="header">
            STATE OF NEW JERSEY<br>
            FAMILY MUNICIPAL COURT<br>
            SUMMONS # {datetime.datetime.now().strftime('%m%d-%H%M')}
        </div>
        <p><b>DATE:</b> {datetime.date.today()}</p>
        <p><b>DEFENDANT:</b> {defendant.upper()}</p>
        <p><b>LOCATION:</b> {location.upper()}</p>
        <hr>
        <p><b>VIOLATION OBSERVED:</b></p>
        <p class="statute">{violation_text}</p>
        <hr>
        <p><b>PENALTY ASSESSED:</b></p>
        <p><b>{fine.upper()}</b></p>
        <hr>
        <p><i>ISSUING OFFICER: {officer}</i></p>
        <p style="font-size: 10px; text-align: center;">FAILURE TO COMPLY MAY RESULT IN WIFI TERMINATION.</p>
    </div>
    """, unsafe_allow_html=True)
