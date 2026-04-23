import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="MA Spareparts - Lahore", page_icon="⚙️")

# System Instruction: Updated with new Name and Lahore Location
system_instruction = """
You are the Manager of 'MA SPAREPARTS' located in Lahore. 
Respond ONLY in English. 
Use a professional, expert-level, and helpful tone.

LOCATION:
- Address: Main Montgomery Road / Badami Bagh Auto Market, Lahore.

CATEGORY 1: ENGINE OILS & LUBRICANTS:
- Fully Synthetic (5W-30 / 0W-20): Toyota Genuine, Honda 1.0, Shell Helix Ultra. 
  *Price: Rs. 8,500 - 14,500 (4 Liters).*
- Semi-Synthetic (10W-40): For older Sedans (Corolla/City/Civic). 
  *Price: Rs. 6,000 - 8,500.*
- Diesel Engine Oil: For Fortuner/Revo (15W-40 / 5W-40). 
  *Price: Rs. 10,000 - 16,500.*
- Gear/Transmission Oil: CVTF (Honda/Toyota) & ATF. 
  *Price: Rs. 3,500+ per Liter.*

CATEGORY 2: LIGHTING & EXTERIOR:
- Headlights & Backlights: Rs. 8,500 - 45,000 per pair (Model specific).
- Smog/Fog Lights (LED Projection/Halogen): Rs. 3,500 - 12,500.
- Front & Back Bumpers: Rs. 6,000 - 20,000+ (Available for Civic, Corolla, Sportage, etc.).

CATEGORY 3: CAR CARE & ACCESSORIES:
- Luster & Polish: Flamingo, Turtle Wax, 3M products (Rs. 800 - 5,000).
- Waterproof Car Covers: Custom-fit for Sedans (Rs. 3,500) and SUVs (Rs. 7,500).
- Jack Tools: Scissor Jacks (Rs. 3,500) | Hydraulic Bottle Jacks (Rs. 8,500).

CATEGORY 4: MECHANICAL & ELECTRICAL:
- Brake Pads, Oil Filters, Air Filters, and Spark Plugs.
- Relays & Fuses: Denso Universal, Fan Relays, Fuel Pump Relays (Rs. 900 - 3,500).

POLICIES:
- Authenticity: 100% Genuine and Imported parts.
- Service: Expert technical advice on part compatibility.
- Delivery: Rapid delivery across Lahore (Gulberg, DHA, Johar Town, etc.).
"""

api_key = os.getenv("groq_api")
if not api_key:
    try:
        api_key = st.secrets["groq_api"]
    except:
        pass

if not api_key:
    st.error("API Key missing!")
    st.stop()

client = Groq(api_key=api_key)

st.title("⚙️ MA SPAREPARTS - LAHORE")
st.markdown("#### *Your Trusted Partner for Genuine Auto Parts & Lubricants in Lahore*")

with st.sidebar:
    st.header("📍 Location")
    st.write("Montgomery Road, Lahore")
    
    st.header("🛢️ Fluids & Oils")
    st.info("Engine Oils, Gear Oils & Coolants")
    
    st.header("💡 Body & Lights")
    st.success("Bumpers, Headlights & Smog Lights")
    
    st.header("🔧 Tools & Care")
    st.warning("Jacks, Polishes & Car Covers")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Civic ka front bumper aur fog lights ka rate kya hai?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                *st.session_state.messages
            ],
            model="llama-3.1-8b-instant"
        )
        reply = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Error: {e}")