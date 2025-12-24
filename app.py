import streamlit as st
import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="NJ Family Court", page_icon="⚖️", layout="centered")

# CSS for the Ticket
st.markdown("""
<style>
    .ticket { border: 2px solid #333; padding: 20px; background-color: #fcfbf9; font-family: monospace; }
    .header { text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; font-weight: bold; }
    .statute { color: #b30000; font-weight: bold; }
    .stButton>button { width: 100%; background-color: #b30000; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🚓 Family Citation Writer")
st.caption("Official Title 39-H Issuance System")

# --- INPUTS (No Form Wrapper) ---
defendant = st.text_input("Defendant Name:", placeholder="Enter name...")
location = st.text_input("Location:", placeholder="Living Room...")

st.divider()

# Violation Logic
v_mode = st.radio("Violation Type:", ["Select List", "Write Custom"], horizontal=True)
if v_mode == "Select List":
    violation = st.selectbox("Violation:", ["39:H-10 :: Empty Water Pitcher", "39:H-22 :: Lights Left On", "39:H-99 :: Gaming Past Curfew"])
else:
    violation = st.text_input("Enter Custom Violation:", placeholder="e.g. Ate the last cookie")

st.divider()

# Penalty Logic
p_mode = st.radio("Penalty Type:", ["Select List", "Write Custom"], horizontal=True)
if p_mode == "Select List":
    penalty = st.selectbox("Penalty:", ["Verbal Warning", "Trash Duty", "Mow Lawn", "Loss of WiFi"])
else:
    penalty = st.text_input("Enter Custom Penalty:", placeholder="e.g. Buy Dad Coffee")

st.divider()

if st.button("🚨 ISSUE CITATION"):
    if not defendant:
        st.error("Enter a Defendant Name!")
    else:
        html_ticket = f"""
        <div class="ticket">
            <div class="header">STATE OF NEW JERSEY<br>SUMMONS # {datetime.datetime.now().strftime('%m%d-%H%M')}</div>
            <p><b>DEFENDANT:</b> {defendant.upper()}</p>
            <p><b>LOCATION:</b> {location.upper()}</p>
            <hr>
            <p><b>VIOLATION:</b> <span class="statute">{violation}</span></p>
            <hr>
            <p><b>PENALTY:</b> {penalty.upper()}</p>
            <p style="text-align:center; margin-top:20px;"><i>ISSUING OFFICER: DAD</i></p>
        </div>
        """
        st.markdown(html_ticket, unsafe_allow_html=True)
        
      # --- 5. DISPLAY & PRINT (READS MEMORY) ---
if st.session_state['issued']:
    # Show the ticket
    st.markdown(st.session_state['ticket_html'], unsafe_allow_html=True)
    
    st.write("") # Spacer
    
   # --- PASTE THIS RIGHT AFTER THE TICKET DISPLAY ---
    st.write("") # Spacer
    if st.button("🖨️ PRINT CITATION"):
        components.html(f"""
             <script>
                window.print();
            </script>
        """, height=0, width=0)
