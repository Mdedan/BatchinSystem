import streamlit as st
import requests
from sympy import true

# Set up the title and page layout of our dashboard interface
st.set_page_config(page_title="Trucking Logistics", layout="centered")


# 1. Define your custom styled HTML div
st.container(border=True)
st.write("Figuring out how to plan a container") 
custom_div = """
<div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px;">
    <h4>Inside the Custom Div</h4>
    <p>This is styled with HTML.</p>
</div>
"""

# 1. Render the HTML div
st.html(custom_div)
st.button("I am a normal Streamlit button above the HTML!")

# 2. Anything you type below this is completely outside of the div
st.write("---") 
st.write("### Outside the Div")
st.button("I am a normal Streamlit button outside the HTML!")

st.title("👥 User Management Dashboard")

# Define the URL where our FastAPI backend is running
BACKEND_URL = "http://127.0.0.1:8000"

# ==========================================
# 🛡️ AUTOMATIC BACKEND CONNECTION CHECK
# ==========================================
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


# ==========================================
# --- SECTION 1: ADD NEW TRUCK ---
# ==========================================
st.header("➕ Create a New Truck")

# Create text input boxes for the form layout
item = st.text_input("Enter Item Name:", placeholder="e.g., Bananas")
truck = st.text_input("Enter Truck Type:", placeholder="e.g., Refrigerated Semi")
company = st.text_input("Enter Company Name:", placeholder="e.g., McOdsen Inc.")

if st.button("Submit Truck", use_container_width=True):
    if item and truck:
        # Prepare the payload to send to FastAPI (matching Pydantic schema)
        payload = {"item": item, "type": truck, "company": company}
        
        try:
            # Send a POST request to our FastAPI server
            response = requests.post(f"{BACKEND_URL}/trucks", json=payload, timeout=5)

            if response.status_code == 200 or response.status_code == 201:
                st.success(f"🎉 Success! Added item '{item}' to the database.")
            else:
                st.error(f"Backend rejected data. Status code: {response.status_code}")
                st.json(response.json())
        except Exception as e:
            st.error("Failed to communicate with the API endpoint.")
            st.exception(e)
    else:
        st.warning("Please fill out both fields before submitting.")

st.markdown("---")


# ==========================================
# --- SECTION 2: VIEW ALL TRUCKS ---
# ==========================================
st.header("📋 Current Trucks List")

if st.button("Refresh Trucks List", use_container_width=True):
    try:
        # Send a GET request to our FastAPI server to fetch database rows
        response = requests.get(f"{BACKEND_URL}/trucks", timeout=5)
            
        if response.status_code == 200:
            trucks_data = response.json()
            
            if not trucks_data:
                st.info("The database is currently empty. Add a truck above!")
            else:
                # Display the data cleanly as an interactive table
                st.dataframe(trucks_data, use_container_width=True)
        else:
            st.error(f"Could not fetch trucks. Status code: {response.status_code}")
    except Exception as e:
        st.error("Could not fetch data from the backend.")
        st.exception(e)
