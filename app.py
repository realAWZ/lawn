import streamlit as st
import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="NJ Family Court", page_icon="⚖️", layout="centered")

# --- MEMORY ---
if 'issued' not in st.session_state:
    st.session_state['issued'] = False
if 'ticket_html' not in st.session_state:
    st.session_state['ticket_html'] = ""

# --- CSS STYLING ---
st.markdown("""
<style>
    /* Force background colors to print correctly */
    * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    
    .ticket-container {
        /* Makes it look like a card on screen for easy screenshots */
        box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
        margin-bottom: 20px;
    }

    .ticket { 
        border: 4px solid #000; 
        padding: 30px; 
        background-color: #fffbe6 !important; /* Yellowish Paper */
        background-image: url("https://www.transparenttextures.com/patterns/cream-paper.png");
        font-family: 'Courier New', monospace; 
        color: black !important;
    }
    .header { text-align: center; border-bottom: 3px solid #000; margin-bottom: 20px; font-weight: bold; font-size: 1.2em;}
    .statute { color: #b30000 !important; font-weight: bold; font-size: 1.1em;}
    .stButton>button { width: 100%; background-color: #b30000; color: white; font-weight: bold;}
    
    /* CRITICAL: HIDE EVERYTHING ELSE WHEN PRINTING */
    @media print {
        .stButton, header, footer, .stDeployButton, .stAppHeader, .stTextInput, .stSelectbox, .stRadio, .stDivider, h1, div[data-testid="stCaption"] { display: none !important; }
        .block-container { padding: 0px !important; margin: 0px !important; }
        .ticket-container { box-shadow: none !important; } /* No shadow on paper */
    }
</style>
""", unsafe_allow_html=True)

st.title("🚓 Family Citation Writer")
st.caption("Official Title 39-H Issuance System")

# --- INPUTS ---
defendant = st.text_input("Defendant Name:", placeholder="Enter name...")
location = st.text_input("Location:", placeholder="Living Room...")

st.divider()

# Violation
v_mode = st.radio("Violation Type:", ["Select List", "Write Custom"], horizontal=True)
if v_mode == "Select List":
    violation = st.selectbox("Violation:", ["39:H-10 :: Empty Water Pitcher", "39:H-22 :: Lights Left On", "39:H-99 :: Gaming Past Curfew", "39:H-04 :: Leaving Shoes by Door"])
else:
    violation = st.text_input("Enter Custom Violation:", placeholder="e.g. Ate the last cookie")

st.divider()

# Penalty
p_mode = st.radio("Penalty Type:", ["Select List", "Write Custom"], horizontal=True)
if p_mode == "Select List":
    penalty = st.selectbox("Penalty:", ["Verbal Warning", "Trash Duty", "Mow Lawn", "Loss of WiFi (24h)", "10 Pushups"])
else:
    penalty = st.text_input("Enter Custom Penalty:", placeholder="e.g. Buy Dad Coffee")

st.divider()

# --- ISSUE BUTTON ---
if st.button("🚨 ISSUE OFFICIAL CITATION"):
    if not defendant:
        st.error("Enter a Defendant Name!")
    else:
        date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        case_num = datetime.datetime.now().strftime('%m%d-%H%M')
        
        st.session_state['ticket_html'] = f"""
        <div class="ticket-container">
        <div class="ticket">
            <div class="header">STATE OF NEW JERSEY<br>FAMILY COURT DIVISION<br>CASE # {case_num}</div>
            <p><b>DATE/TIME:</b> {date_str}</p>
            <p><b>DEFENDANT:</b> {defendant.upper()}</p>
            <p><b>LOCATION:</b> {location.upper()}</p>
            <hr style="border-top: 2px dashed black;">
            <p><b>VIOLATION CITED:</b></p>
            <p class="statute">{violation.upper()}</p>
            <hr style="border-top: 2px dashed black;">
            <p><b>PENALTY ASSESSED:</b></p>
            <h3 style="text-align:center; color: red; border: 3px solid red; padding: 10px; transform: rotate(-2deg);">{penalty.upper()}</h3>
            <br>
            <p style="text-align:center; margin-top:20px;"><i>ISSUING OFFICER: _________________ (DAD)</i></p>
            <p style="font-size: 0.8em; text-align: center;">Failure to comply will result in further sanctions.</p>
        </div>
        </div>
        """
        st.session_state['issued'] = True

# --- OUTPUT AREA ---
if st.session_state['issued']:
    st.markdown("### 📄 Generated Citation")
    # Display the ticket
    st.markdown(st.session_state['ticket_html'], unsafe_allow_html=True)
    
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        # THE FIXED PRINT BUTTON
        if st.button("🖨️ PRINT TO PAPER"):
            components.html("<script>window.parent.print();</script>", height=0, width=0)
            
    with col2:
        # INSTRUCTIONS FOR SHARING
        st.info("📱 **TO SHARE VIA TEXT:** Take a screenshot of the ticket above on your phone, then send the photo.")

    if st.button("🔄 ISSUE NEW TICKET"):
        st.session_state['issued'] = False
        st.rerun()
