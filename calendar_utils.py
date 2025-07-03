from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Calendar Setup
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "680ae2f631bcf5095d1a6c1b4785e413b1a8c20befe7271230cefba87bf57a6a@group.calendar.google.com"  # Replace this

# Authenticate once
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)
calendar_service = build("calendar", "v3", credentials=credentials)


def check_availability(start_dt, end_dt):
    """
    Check if there are any events in the given time range.
    Returns True if the time is free, False if busy.
    """
    events_result = calendar_service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat() + 'Z',
        timeMax=end_dt.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return len(events) == 0  # True = available


def get_free_slots(start_day, end_day, slot_duration_minutes=30):
    """
    Find available time slots between start_day and end_day.
    """
    print(f"🟢 get_free_slots() called with: {start_day} to {end_day}")

    free_slots = []
    current = start_day

    while current + timedelta(minutes=slot_duration_minutes) <= end_day:
        slot_end = current + timedelta(minutes=slot_duration_minutes)
        if check_availability(current, slot_end):
            free_slots.append((current, slot_end))
        current += timedelta(minutes=slot_duration_minutes)

    return free_slots



def book_appointment(summary, description, start_dt, end_dt):
    """
    Book an event on the calendar.
    """
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": "Asia/Kolkata"},
    }

    created_event = calendar_service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event
