from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from calendar_utils import get_free_slots, book_appointment

app = FastAPI()

# Request schemas
class AvailabilityRequest(BaseModel):
    start_date: str  # Format: "2025-07-03T09:00:00"
    end_date: str    # Format: "2025-07-03T17:00:00"

class BookingRequest(BaseModel):
    summary: str
    description: str
    start_time: str  # Format: "2025-07-03T14:30:00"
    end_time: str    # Format: "2025-07-03T15:00:00"

# Root
@app.get("/")
def read_root():
    return {"message": "Google Calendar Booking API is up and running 🚀"}

# Get available slots
@app.post("/check")
def check_availability(req: AvailabilityRequest):
    try:
        start_dt = datetime.fromisoformat(req.start_date)
        end_dt = datetime.fromisoformat(req.end_date)
        slots = get_free_slots(start_dt, end_dt)
        slot_strs = [f"{s[0].isoformat()} to {s[1].isoformat()}" for s in slots]
        return {"available_slots": slot_strs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Book appointment
@app.post("/book")
def book(req: BookingRequest):
    try:
        start_dt = datetime.fromisoformat(req.start_time)
        end_dt = datetime.fromisoformat(req.end_time)
        event = book_appointment(req.summary, req.description, start_dt, end_dt)
        return {"status": "success", "event_link": event.get("htmlLink")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
