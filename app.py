from http import client
from pydoc import locate
import streamlit as st
import requests
from sympy import true

# Set up the title and page layout of our dashboard interface
st.set_page_config(page_title="Trucking Logistics", layout="centered")

# Define the URL where our FastAPI backend is running
BACKEND_URL = "http://127.0.0.1:8000"

#Backend 
try:
    # Send a quick request with a short 2-second timeout.
    response = requests.get(f"{BACKEND_URL}/", timeout=2)
    
    if response.status_code == 200:
        st.sidebar.success("🟢 Connected to Backend API")
    else:
        st.sidebar.warning(f"⚠️ API Status Code: {response.status_code}")

except requests.exceptions.ConnectionError:
    # If the server isn't running on port 8000, stop right here and give directions
    st.sidebar.error("🔴 Backend API Offline")
    st.error("❌ CONNECTION FAILED: The backend server is offline.")
    st.info(
        "💡 **Troubleshooting Steps:**\n"
        "1. Open your VS Code terminal.\n"
        "2. Run your FastAPI backend in one tab: `uvicorn main:app --reload`\n"
        "3. Make sure it says it's running on `http://127.0.0.1:8000`.\n"
        "4. Refresh this web page."
    )
    st.stop()  # Keeps the user from interacting with broken forms below
except requests.exceptions.ReadTimeout:
    st.sidebar.error("⏱️ Backend is too slow (timeout)")
    st.stop()

st.title("🚚 Bamburi Batching System Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fill the following information.")
    DNo = st.text_input("Delivery Number")
    client = st.text_input("Client Name")
    location = st.text_input("Delivery Location")
    mix_label = st.selectbox("Select Mix Type", ["Mix A", "Mix B", "Mix C"])
    Desc = st.selectbox("Select Description", ["Description 1", "Description 2", "Description 3"])
with col2:
    st.write("Right Sidebar")

if st.button("Submit Delivery"):
        if DNo and client and location and mix_label:
            st.success("✅ Delivery information submitted successfully!")
            # Here you would typically send this data to your backend API
            try:
                payload = {"DNo": DNo, "client": client, "location": location, "mix_label": mix_label}
                response = requests.post(f"{BACKEND_URL}/deliveries", json=payload)
                if response.status_code == 200:
                    st.info("📤 Data sent to backend successfully!")
                else:
                    st.warning(f"⚠️ Failed to send data: Status Code {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error sending data to backend: {e}")
        else:
            st.error("❌ Please fill in all fields before submitting.")    
