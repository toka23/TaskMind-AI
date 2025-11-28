import streamlit as st
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


API_URL = "https://nigel-placid-anabelle.ngrok-free.dev/test"
 
API_KEY = "secret123"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ===============================
# STREAMLIT UI
# ===============================
st.set_page_config(page_title="Task AI Assistant", page_icon="🧠", layout="centered")

st.title("🧠 Task AI Assistant")
st.write("Enter all your tasks below. The system will classify them → plan your day → give advice.")

tasks_input = st.text_area(
    "✍️ Write your tasks (one per line):",
    height=200,
    placeholder="Example:\nFinish Python assignment\nClean the room\nBuy groceries\nPrepare meeting..."
)

if st.button("🚀 Generate Plan"):
    if not tasks_input.strip():
        st.error("Please enter your tasks first.")
    else:
        with st.spinner("Processing..."):
            payload = {
                "tasks": tasks_input.strip().split("\n")
            }

            try:
                res = requests.post(API_URL, headers=headers, json=payload, verify= False)
                data = res.json()

                # ===============================
                # PARSE OUTPUT
                # ===============================
                classify = data.get("classified", {})
                plan = data.get("plan", {})
                advice = data.get("advice", [])

                # ===============================
                # DISPLAY RESULTS
                # ===============================
                st.subheader("📌 Classification")
                st.json(classify)

                st.subheader("🗓️ Daily Plan")
                st.json(plan)

                st.subheader("💡 Advice")
                for i, tip in enumerate(advice, 1):
                    st.write(f"**Tip {i}:** {tip}")

            except Exception as e:
                st.error(f"Error: {e}")
