import streamlit as st
import streamlit.components.v1 as components # <--- YOU NEED THIS LINE AT THE TOP

st.title("⚖️ Dad Ops: Citation Generator")

# 1. The Input Form
col1, col2 = st.columns(2)
offender = col1.text_input("Offender Name:", "Brother")
violation = col2.selectbox("Violation Type:", [
    "Leaving Lights On", 
    "Messy Room", 
    "Touching the Thermostat", 
    "Eating the Last Slice", 
    "Bad Attitude",
    "Custom..."
])

if violation == "Custom...":
    violation = st.text_input("Enter Custom Violation:")

fine = st.text_input("Penalty / Fine:", "10 Pushups")
date = "DEC 23, 2025" # You can use datetime.now() if you want dynamic dates

# 2. The Visual Ticket (HTML/CSS)
# We draw a box that looks like a ticket so it prints nicely
st.markdown(f"""
<div style="
    border: 3px solid black; 
    padding: 20px; 
    font-family: 'Courier New'; 
    background-color: #fffbe6; 
    color: black; 
    text-align: center;
    margin-bottom: 20px;
">
    <h2>⚠️ OFFICIAL VIOLATION NOTICE ⚠️</h2>
    <p><b>DATE:</b> {date}</p>
    <p><b>OFFENDER:</b> {offender.upper()}</p>
    <hr style="border-top: 2px dashed black;">
    <h3>VIOLATION: {violation.upper()}</h3>
    <p>You have been cited for violation of House Rules.</p>
    <p><b>PENALTY ASSESSED:</b></p>
    <h2 style="color: red; border: 2px solid red; display: inline-block; padding: 5px;">{fine.upper()}</h2>
    <br><br>
    <p><i>SIGNED: __________________________</i></p>
    <p><i>(Dad / Warden)</i></p>
</div>
""", unsafe_allow_html=True)

# 3. The Print Button Logic
if st.button("🖨️ PRINT TICKET"):
    # This line sends a javascript command to the browser to open the print dialog
    components.html("<script>window.print()</script>", height=0, width=0)
