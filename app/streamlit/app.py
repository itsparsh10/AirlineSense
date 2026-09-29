import os

import requests
import streamlit as st


API_URL = os.getenv("AIRLINESENSE_API_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(
    page_title="AirlineSense · Passenger satisfaction",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {
      color-scheme: light;
      --ink: #112d3c;
      --muted: #5e7480;
      --teal: #0f8993;
      --teal-dark: #075363;
      --line: #dce8ec;
    }

    .stApp,
    [data-testid="stAppViewContainer"] {
      background:
        radial-gradient(circle at 88% 7%, rgba(35, 178, 176, .13), transparent 24rem),
        linear-gradient(180deg, #f7fbfc 0%, #eef5f7 100%);
      color: var(--ink);
    }

    [data-testid="stHeader"] {
      background: rgba(247, 251, 252, .88);
      backdrop-filter: blur(12px);
    }

    .block-container {
      max-width: 1240px;
      padding: 2rem 2rem 4rem;
    }

    h1, h2, h3, h4, p, label,
    [data-testid="stMarkdownContainer"],
    [data-testid="stWidgetLabel"] p {
      color: var(--ink);
    }

    [data-testid="stWidgetLabel"] p {
      font-weight: 650;
      font-size: .88rem;
    }

    .hero {
      position: relative;
      overflow: hidden;
      padding: 2.2rem 2.35rem;
      border-radius: 24px;
      background: linear-gradient(120deg, #073b4c 0%, #086c78 58%, #12a0a3 100%);
      box-shadow: 0 22px 55px rgba(7, 83, 99, .18);
      margin-bottom: 1.5rem;
    }

    .hero::after {
      content: "✈";
      position: absolute;
      right: 2rem;
      top: 50%;
      transform: translateY(-50%) rotate(-7deg);
      font-size: 6rem;
      color: rgba(255, 255, 255, .12);
    }

    .eyebrow {
      color: #8fe2dc;
      font-weight: 800;
      letter-spacing: .12em;
      font-size: .73rem;
      margin-bottom: .45rem;
    }

    .hero h1 {
      color: #fff;
      margin: 0;
      font-size: clamp(2.25rem, 5vw, 3.35rem);
      line-height: 1.05;
      letter-spacing: -.045em;
    }

    .hero p {
      color: #dcf7f5;
      font-size: 1.08rem;
      margin: .7rem 0 1.15rem;
      max-width: 680px;
    }

    .hero-badges {
      display: flex;
      flex-wrap: wrap;
      gap: .55rem;
    }

    .hero-badges span {
      color: #fff;
      background: rgba(255, 255, 255, .12);
      border: 1px solid rgba(255, 255, 255, .2);
      border-radius: 999px;
      padding: .35rem .72rem;
      font-size: .78rem;
      font-weight: 700;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
      background: rgba(255, 255, 255, .9);
      border: 1px solid var(--line);
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(18, 48, 68, .055);
    }

    .section-head { margin-bottom: .4rem; }
    .section-head strong {
      display: block;
      color: var(--ink);
      font-size: 1.18rem;
      letter-spacing: -.015em;
    }
    .section-head span {
      color: var(--muted);
      font-size: .86rem;
    }

    [data-baseweb="select"] > div,
    [data-baseweb="input"] {
      background: #fff;
      border-color: #cbdde2;
    }
    [data-baseweb="select"] *,
    [data-baseweb="input"] *,
    input {
      color: var(--ink) !important;
    }
    [data-testid="stSlider"] [role="slider"] {
      box-shadow: 0 0 0 4px rgba(15, 137, 147, .14);
    }

    button[kind="primary"] {
      min-height: 3.25rem;
      border: 0;
      border-radius: 14px;
      background: linear-gradient(90deg, #087b87, #10a0a0);
      box-shadow: 0 10px 22px rgba(15, 137, 147, .22);
      font-size: .96rem;
      font-weight: 800;
      letter-spacing: .025em;
    }
    button[kind="primary"]:hover {
      background: linear-gradient(90deg, #075f6b, #0c898f);
      border: 0;
    }
    button[kind="primary"] p {
      color: #fff !important;
    }

    .result {
      padding: 1.65rem 1.8rem;
      border-radius: 20px;
      background: linear-gradient(135deg, #fff 0%, #effbf8 100%);
      border: 1px solid #ccebe5;
      border-left: 8px solid #0b9b82;
      box-shadow: 0 15px 40px rgba(18, 48, 68, .1);
      margin-top: .3rem;
    }
    .result-label {
      color: #087a69;
      font-size: .76rem;
      font-weight: 850;
      letter-spacing: .1em;
    }
    .result h2 {
      color: var(--ink);
      margin: .25rem 0 0;
      font-size: 2rem;
    }
    .result h3 {
      color: #087a69;
      margin: .35rem 0 .7rem;
      font-size: 1.3rem;
    }
    .result p { color: #3f5965; margin: .25rem 0; }
    .result .model {
      color: #67808b;
      font-size: .82rem;
      margin-top: .8rem;
      font-weight: 650;
    }
    [data-testid="stProgress"] > div > div > div > div {
      background: linear-gradient(90deg, #0f8993, #29b7a5);
    }

    section[data-testid="stSidebar"] {
      background: linear-gradient(180deg, #102b39 0%, #0b202c 100%);
      border-right: 1px solid rgba(255, 255, 255, .08);
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
      color: #e8f4f5;
    }
    .sidebar-brand { margin: .5rem 0 1.6rem; }
    .sidebar-brand strong {
      display: block;
      color: #fff;
      font-size: 1.15rem;
    }
    .sidebar-brand span {
      color: #8fb1ba;
      font-size: .78rem;
    }

    @media (max-width: 760px) {
      .block-container { padding: 1rem .85rem 2.5rem; }
      .hero { padding: 1.6rem 1.3rem; border-radius: 18px; }
      .hero::after { display: none; }
      .hero p { font-size: .95rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <div class="eyebrow">PASSENGER EXPERIENCE INTELLIGENCE</div>
      <h1>AirlineSense</h1>
      <p>Turn journey and service signals into an instant passenger satisfaction forecast.</p>
      <div class="hero-badges">
        <span>96.0% test accuracy</span>
        <span>22 passenger signals</span>
        <span>Real-time prediction</span>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand"><strong>✈ AirlineSense</strong><span>ML prediction console</span></div>',
        unsafe_allow_html=True,
    )
    st.subheader("System status")
    try:
        health = requests.get(f"{API_URL}/health", timeout=3)
        health.raise_for_status()
        status = health.json()
        st.success("Prediction API connected")
        st.caption(
            f"{status.get('model_name', 'Model')} · v{status.get('model_version', '1.0.0')}"
        )
    except requests.RequestException:
        st.error("Prediction API unavailable")
        st.caption(f"Expected at {API_URL}")
    st.divider()
    st.markdown("**How to read the ratings**")
    st.caption("0 means not applicable or very poor. 5 means excellent.")
    st.caption("Use the passenger's actual journey experience for the most useful prediction.")

with st.container(border=True):
    st.markdown(
        '<div class="section-head"><strong>Passenger & journey</strong><span>Who is travelling and what does the trip look like?</span></div>',
        unsafe_allow_html=True,
    )
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

with st.container(border=True):
    st.markdown(
        '<div class="section-head"><strong>Digital & airport experience</strong><span>Rate the booking, boarding, and airport touchpoints.</span></div>',
        unsafe_allow_html=True,
    )
    digital = st.columns(4)
    ease_of_online_booking = digital[0].slider("Online booking", 0, 5, 2)
    online_boarding = digital[1].slider("Online boarding", 0, 5, 5)
    inflight_wifi_service = digital[2].slider("In-flight Wi-Fi", 0, 5, 2)
    gate_location = digital[3].slider("Gate location", 0, 5, 2)
    airport = st.columns(3)
    checkin_service = airport[0].slider("Check-in service", 0, 5, 3)
    baggage_handling = airport[1].slider("Baggage handling", 1, 5, 5)
    inflight_service = airport[2].slider("In-flight service", 0, 5, 5)

with st.container(border=True):
    st.markdown(
        '<div class="section-head"><strong>On-board experience</strong><span>Rate comfort, service quality, and cabin amenities.</span></div>',
        unsafe_allow_html=True,
    )
    onboard = st.columns(3)
    onboard_service = onboard[0].slider("Cabin service", 0, 5, 5)
    seat_comfort = onboard[1].slider("Seat comfort", 0, 5, 4)
    leg_room_service = onboard[2].slider("Leg room", 0, 5, 5)
    onboard_second = st.columns(3)
    cleanliness = onboard_second[0].slider("Cleanliness", 0, 5, 5)
    food_and_drink = onboard_second[1].slider("Food and drink", 0, 5, 3)
    inflight_entertainment = onboard_second[2].slider("Entertainment", 0, 5, 5)

payload = {
    "gender": gender, "age": age, "customer_type": customer_type,
    "type_of_travel": type_of_travel, "travel_class": travel_class,
    "flight_distance": flight_distance, "departure_delay": departure_delay,
    "arrival_delay": arrival_delay,
    "departure_arrival_convenience": departure_arrival_convenience,
    "ease_of_online_booking": ease_of_online_booking,
    "checkin_service": checkin_service, "online_boarding": online_boarding,
    "gate_location": gate_location, "onboard_service": onboard_service,
    "seat_comfort": seat_comfort, "leg_room_service": leg_room_service,
    "cleanliness": cleanliness, "food_and_drink": food_and_drink,
    "inflight_service": inflight_service,
    "inflight_wifi_service": inflight_wifi_service,
    "inflight_entertainment": inflight_entertainment,
    "baggage_handling": baggage_handling,
}

if st.button("PREDICT PASSENGER SATISFACTION", type="primary", use_container_width=True):
    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        probability = float(result["probability"])
        st.markdown(
            f"""
            <div class="result">
              <div class="result-label">PREDICTION COMPLETE</div>
              <h2>{result['prediction']}</h2>
              <h3>{probability:.2%} probability of satisfaction</h3>
              <p>{result['interpretation']}</p>
              <p class="model">{result['model_name']} · model {result['model_version']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(probability)
    except requests.HTTPError as exc:
        try:
            detail = exc.response.json().get("detail", str(exc))
        except ValueError:
            detail = str(exc)
        st.error(f"Prediction rejected: {detail}")
    except requests.RequestException:
        st.error("The prediction service is unavailable. Start FastAPI and try again.")
