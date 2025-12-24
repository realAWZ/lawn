import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import datetime

st.set_page_config(page_title="NJ Family Court", page_icon="⚖️", layout="centered")

# --- 1. IMAGE GENERATOR ENGINE (The Backend) ---
def create_ticket_image(defendant, location, violation, penalty):
    width, height = 600, 800
    color_paper = (255, 251, 230) # Off-white/yellow
    color_black = (0, 0, 0)
    color_red = (178, 34, 34)
    
    img = Image.new('RGB', (width, height), color_paper)
    draw = ImageDraw.Draw(img)
    
    # Draw Borders
    draw.rectangle([(20, 20), (width-20, height-20)], outline=color_black, width=5)
    draw.rectangle([(30, 30), (width-30, height-30)], outline=color_black, width=2)
    
    # Load Fonts (Safe Fallback)
    try:
        font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
        font_label = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
        font_text = ImageFont.truetype("DejaVuSans.ttf", 20)
        font_stamp = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
    except:
        font_header = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_stamp = ImageFont.load_default()

    # Helper to center text
    def draw_centered(text, y, font, color=color_black):
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
        except:
             text_width = draw.textlength(text, font=font)
        x = (width - text_width) / 2
        draw.text((x, y), text, fill=color, font=font)

    # Content Drawing
    draw_centered("STATE OF NEW JERSEY", 60, font_header)
    draw_centered("FAMILY COURT DIVISION", 100, font_label)
    
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    case_id = datetime.datetime.now().strftime('%m%d-%H%M')
    
    draw.text((50, 180), f"CASE #: {case_id}", fill=color_black, font=font_label)
    draw.text((50, 210), f"DATE:   {current_time}", fill=color_black, font=font_text)
    
    draw.line([(50, 250), (width-50, 250)], fill=color_black, width=3)
    
    draw.text((50, 280), "DEFENDANT:", fill=color_black, font=font_label)
    draw.text((50, 310), defendant.upper(), fill=color_black, font=font_text)
    
    draw.text((50, 360), "LOCATION:", fill=color_black, font=font_label)
    draw.text((50, 390), location.upper(), fill=color_black, font=font_text)
    
    draw.line([(50, 440), (width-50, 440)], fill=color_black, width=3)
    
    draw.text((50, 470), "VIOLATION CITED:", fill=color_red, font=font_label)
    draw.text((50, 500), violation, fill=color_black, font=font_text)
    
    draw.text((50, 560), "PENALTY ASSESSED:", fill=color_red, font=font_label)
    
    draw.rectangle([(50, 590), (width-50, 660)], outline=color_red, width=3)
    draw_centered(penalty.upper(), 615, font_stamp, color=color_red)
    
    draw.line([(50, 720), (300, 720)], fill=color_black, width=2)
    draw.text((50, 730), "ISSUING OFFICER (DAD)", fill=color_black, font=font_text)

    return img

# --- 2. THE UI (Restored to Original Specification) ---
st.title("🚓 Family Citation Writer")
st.caption("Official Title 39-H Issuance System")

# Inputs
defendant = st.text_input("Defendant Name:", placeholder="Enter name...")
location = st.text_input("Location:", placeholder="Living Room...")

st.divider()

# Violation Logic (Restored Radio Buttons)
v_mode = st.radio("Violation Type:", ["Select List", "Write Custom"], horizontal=True)
if v_mode == "Select List":
    violation = st.selectbox("Violation:", ["39:H-10 :: Empty Water Pitcher", "39:H-22 :: Lights Left On", "39:H-99 :: Gaming Past Curfew"])
else:
    violation = st.text_input("Enter Custom Violation:", placeholder="e.g. Ate the last cookie")

st.divider()

# Penalty Logic (Restored Radio Buttons)
p_mode = st.radio("Penalty Type:", ["Select List", "Write Custom"], horizontal=True)
if p_mode == "Select List":
    penalty = st.selectbox("Penalty:", ["Verbal Warning", "Trash Duty", "Mow Lawn", "Loss of WiFi"])
else:
    penalty = st.text_input("Enter Custom Penalty:", placeholder="e.g. Buy Dad Coffee")

st.divider()

# --- 3. THE BUTTON & OUTPUT ---
# (Restored "Issue Citation" button text)
if st.button("🚨 ISSUE CITATION"):
    if not defendant:
        st.error("Enter a Defendant Name!")
    else:
        # Create the image
        img = create_ticket_image(defendant, location, violation, penalty)
        
        # Show the image (looks like the HTML version but is actually a picture)
        st.write("### 📄 Official Citation Generated")
        st.image(img, caption="Official Summons", use_container_width=True)
        
        # Prepare for download
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        # Download Button (This is the only way to get a clean image on phones)
        st.download_button(
            label="⬇️ DOWNLOAD IMAGE TO SHARE",
            data=byte_im,
            file_name=f"citation_{defendant}.png",
            mime="image/png"
        )
