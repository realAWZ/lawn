import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import datetime

st.set_page_config(page_title="NJ Family Court", page_icon="⚖️", layout="centered")

def create_ticket_image(defendant, location, violation, penalty):
    # 1. Setup the Blank Paper (Yellowish)
    width, height = 600, 800
    color_paper = (255, 251, 230) # Off-white/yellow
    color_black = (0, 0, 0)
    color_red = (178, 34, 34)
    
    img = Image.new('RGB', (width, height), color_paper)
    draw = ImageDraw.Draw(img)
    
    # 2. Draw Borders
    draw.rectangle([(20, 20), (width-20, height-20)], outline=color_black, width=5)
    draw.rectangle([(30, 30), (width-30, height-30)], outline=color_black, width=2)
    
    # 3. Load Fonts (Try to load a good one, fallback to default)
    try:
        # Trying common fonts
        font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
        font_label = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
        font_text = ImageFont.truetype("DejaVuSans.ttf", 20)
        font_stamp = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
    except:
        # Fallback if specific fonts aren't on the server
        font_header = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_stamp = ImageFont.load_default()

    # 4. Write Content
    # Helper to center text
    def draw_centered(text, y, font, color=color_black):
        # Calculate width using textbbox (newer PIL versions) or textlength
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
        except:
             text_width = draw.textlength(text, font=font)
        
        x = (width - text_width) / 2
        draw.text((x, y), text, fill=color, font=font)

    # Header
    draw_centered("STATE OF NEW JERSEY", 60, font_header)
    draw_centered("FAMILY COURT DIVISION", 100, font_label)
    
    # Details
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
    
    # Draw Penalty Box
    draw.rectangle([(50, 590), (width-50, 660)], outline=color_red, width=3)
    draw_centered(penalty.upper(), 615, font_stamp, color=color_red)
    
    # Signature
    draw.line([(50, 720), (300, 720)], fill=color_black, width=2)
    draw.text((50, 730), "ISSUING OFFICER (DAD)", fill=color_black, font=font_text)

    return img

# --- APP UI ---
st.title("🚓 Citation Generator")
st.caption("Generate an Official Image Ticket")

# Inputs
col1, col2 = st.columns(2)
defendant = col1.text_input("Defendant Name")
location = col2.text_input("Location")

violation = st.selectbox("Violation", ["Messy Room", "Lights On", "Bad Attitude", "Custom"])
if violation == "Custom":
    violation = st.text_input("Enter Custom Violation")
    
penalty = st.text_input("Penalty", "10 Pushups")

if st.button("🖼️ GENERATE TICKET IMAGE"):
    if not defendant:
        st.error("Need a Name!")
    else:
        # Create the image
        img = create_ticket_image(defendant, location, violation, penalty)
        
        # Show it on screen
        st.image(img, caption="Official Citation Preview", use_container_width=True)
        
        # Convert to bytes for download
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        # Download Button
        st.download_button(
            label="⬇️ DOWNLOAD TICKET (PNG)",
            data=byte_im,
            file_name=f"citation_{defendant}.png",
            mime="image/png"
        )
