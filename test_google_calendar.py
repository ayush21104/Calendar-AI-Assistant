from google.oauth2 import service_account
from googleapiclient.discovery import build

def test_calendar_access():
    creds = service_account.Credentials.from_service_account_file(
        "service_account.json",
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    service = build("calendar", "v3", credentials=creds)

    calendar_id = "primary"  # or use your custom calendar ID
    events = service.events().list(calendarId=calendar_id).execute()
    print("Upcoming Events:")
    for event in events.get("items", []):
        print(f"{event['summary']} at {event['start'].get('dateTime')}")

if __name__ == "__main__":
    test_calendar_access()
