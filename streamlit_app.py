# streamlit_app.py

import streamlit as st
from datetime import datetime, timedelta

from api_client import check_available_slots, book_slot

st.set_page_config(page_title="Calendar AI Assistant", page_icon="📅")

st.title("📅 Calendar AI Assistant")
st.markdown("Talk to your assistant or use the forms below to check availability and book meetings.")

st.sidebar.title("🕐 Check Availability")

# --- Availability Form ---
with st.sidebar.form("availability_form"):
    start_date = st.date_input("Start Date", value=datetime.today())
    start_time = st.time_input("Start Time", value=datetime.strptime("09:00", "%H:%M").time())
    end_time = st.time_input("End Time", value=datetime.strptime("17:00", "%H:%M").time())

    submitted = st.form_submit_button("Check Slots")

    if submitted:
        start_dt = datetime.combine(start_date, start_time)
        end_dt = datetime.combine(start_date, end_time)

        st.sidebar.write("🔍 Checking availability...")
        slots = check_available_slots(start_dt.isoformat(), end_dt.isoformat())

        if isinstance(slots, list):
            if slots:
                st.sidebar.success("✅ Available Slots:")
                for slot in slots:
                    st.sidebar.write(f"- {slot}")
            else:
                st.sidebar.warning("No available slots in this range.")
        else:
            st.sidebar.error(slots)

# --- Booking Section ---
st.header("📌 Book an Appointment")

with st.form("booking_form"):
    summary = st.text_input("Meeting Title", "Consultation with Ayush")
    description = st.text_area("Description", "Talk about the AI calendar assistant project")
    start_input = st.text_input("Start Time (ISO Format)", "2025-07-03T14:30:00")
    end_input = st.text_input("End Time (ISO Format)", "2025-07-03T15:00:00")

    submit_booking = st.form_submit_button("Book Slot")

    if submit_booking:
        result = book_slot(summary, description, start_input, end_input)
        if "status" in result:
            st.success("✅ Booking Successful!")
            st.markdown(f"[🔗 View Event]({result['event_link']})")
        else:
            st.error(f"❌ Booking failed: {result.get('error')}")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + FastAPI + LangChain")
