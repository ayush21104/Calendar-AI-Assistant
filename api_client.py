# utils/api_client.py

import requests

API_BASE_URL = "http://localhost:8000"

def check_available_slots(start_iso: str, end_iso: str):
    """
    Calls the FastAPI /check endpoint to get available time slots.
    """
    payload = {
        "start_date": start_iso,
        "end_date": end_iso
    }
    try:
        res = requests.post(f"{API_BASE_URL}/check", json=payload)
        res.raise_for_status()
        return res.json().get("available_slots", [])
    except requests.exceptions.RequestException as e:
        return f"❌ Error checking availability: {e}"

def book_slot(summary, description, start_iso, end_iso):
    """
    Calls the FastAPI /book endpoint to book a time slot.
    """
    payload = {
        "summary": summary,
        "description": description,
        "start_time": start_iso,
        "end_time": end_iso
    }
    try:
        res = requests.post(f"{API_BASE_URL}/book", json=payload)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
