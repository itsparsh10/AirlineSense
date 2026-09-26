import os

import requests
import streamlit as st


API_URL = os.getenv("AIRLINESENSE_API_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="AirlineSense", page_icon="✈️", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background: #f4f8fa; }
    .block-container { max-width: 1180px; padding-top: 2rem; }
    h1, h2, h3 { color: #123044; }
    .hero { padding: 1.5rem 1.7rem; border-radius: 18px; background: linear-gradient(115deg, #083b4c, #0c7c86); color: white; margin-bottom: 1.4rem; }
    .hero h1 { color: white; margin: 0; font-size: 2.6rem; }
    .hero p { color: #d8f4f2; font-size: 1.08rem; margin: .45rem 0 0; }
    .result { padding: 1.4rem; border-radius: 16px; background: white; border-left: 7px solid #0c7c86; box-shadow: 0 8px 30px rgba(18,48,68,.08); }
    .muted { color: #617784; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>AirlineSense</h1>
      <p>Predict passenger satisfaction before the complaint.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("System status")
    try:
        health = requests.get(f"{API_URL}/health", timeout=3)
        health.raise_for_status()
        status = health.json()
        st.success("Prediction API connected")
        st.caption(f"{status.get('model_name', 'Model')} · v{status.get('model_version', '1.0.0')}")
    except requests.RequestException:
        st.error("Prediction API unavailable")
        st.caption(f"Expected at {API_URL}")
    st.divider()
    st.caption("Ratings use 0 = not applicable or very poor, 5 = excellent.")

st.subheader("Passenger and journey")
top = st.columns(5)
gender = top[0].selectbox("Gender", ["Female", "Male"])
age = top[1].number_input("Age", min_value=7, max_value=85, value=35)
customer_type = top[2].selectbox("Customer type", ["Returning", "First-time"])
type_of_travel = top[3].selectbox("Travel purpose", ["Business", "Personal"])
travel_class = top[4].selectbox("Cabin", ["Business", "Economy", "Economy Plus"])

journey = st.columns(4)
flight_distance = journey[0].number_input("Flight distance (miles)", 31, 5000, 821)
departure_delay = journey[1].number_input("Departure delay (min)", 0.0, 1600.0, 26.0)
arrival_delay = journey[2].number_input("Arrival delay (min)", 0.0, 1600.0, 39.0)
departure_arrival_convenience = journey[3].slider("Schedule convenience", 0, 5, 2)

st.subheader("Digital and airport experience")
digital = st.columns(4)
ease_of_online_booking = digital[0].slider("Online booking", 0, 5, 2)
online_boarding = digital[1].slider("Online boarding", 0, 5, 5)
inflight_wifi_service = digital[2].slider("In-flight Wi-Fi", 0, 5, 2)
gate_location = digital[3].slider("Gate location", 0, 5, 2)

airport = st.columns(3)
checkin_service = airport[0].slider("Check-in service", 0, 5, 3)
baggage_handling = airport[1].slider("Baggage handling", 1, 5, 5)
inflight_service = airport[2].slider("In-flight service", 0, 5, 5)

st.subheader("On-board experience")
onboard = st.columns(6)
onboard_service = onboard[0].slider("Cabin service", 0, 5, 5)
seat_comfort = onboard[1].slider("Seat comfort", 0, 5, 4)
leg_room_service = onboard[2].slider("Leg room", 0, 5, 5)
cleanliness = onboard[3].slider("Cleanliness", 0, 5, 5)
food_and_drink = onboard[4].slider("Food and drink", 0, 5, 3)
inflight_entertainment = onboard[5].slider("Entertainment", 0, 5, 5)

payload = {
    "gender": gender,
    "age": age,
    "customer_type": customer_type,
    "type_of_travel": type_of_travel,
    "travel_class": travel_class,
    "flight_distance": flight_distance,
    "departure_delay": departure_delay,
    "arrival_delay": arrival_delay,
    "departure_arrival_convenience": departure_arrival_convenience,
    "ease_of_online_booking": ease_of_online_booking,
    "checkin_service": checkin_service,
    "online_boarding": online_boarding,
    "gate_location": gate_location,
    "onboard_service": onboard_service,
    "seat_comfort": seat_comfort,
    "leg_room_service": leg_room_service,
    "cleanliness": cleanliness,
    "food_and_drink": food_and_drink,
    "inflight_service": inflight_service,
    "inflight_wifi_service": inflight_wifi_service,
    "inflight_entertainment": inflight_entertainment,
    "baggage_handling": baggage_handling,
}

if st.button("PREDICT SATISFACTION", type="primary", use_container_width=True):
    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        probability = float(result["probability"])
        st.markdown(
            f"""
            <div class="result">
              <h2>{result['prediction']}</h2>
              <h3>{probability:.1%} probability of satisfaction</h3>
              <p>{result['interpretation']}</p>
              <p class="muted">{result['model_name']} · model {result['model_version']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(probability)
    except requests.HTTPError as exc:
        detail = exc.response.json().get("detail", str(exc))
        st.error(f"Prediction rejected: {detail}")
    except requests.RequestException:
        st.error("The prediction service is unavailable. Start FastAPI and try again.")

