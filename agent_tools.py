# agent_tools.py

import requests
from datetime import datetime

def get_free_slots():
    # Define today's 2PM–5PM range
    start_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)

    payload = {
        "start_date": start_time.isoformat(),
        "end_date": end_time.isoformat()
    }

    try:
        response = requests.post("http://127.0.0.1:8000/check", json=payload)
        response.raise_for_status()  # Raise exception for non-2xx codes
        data = response.json()
        slots = data.get("available_slots", [])

        if not slots:
            return "No available slots today between 2PM and 5PM."
        return "Today, available slots:\n" + "\n".join(slots)

    except Exception as e:
        return f"❌ Failed to fetch slots: {str(e)}"
