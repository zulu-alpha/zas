import httplib2
from datetime import datetime, timedelta

from .. import CONFIG

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery


SECRET = CONFIG['GOOGLE_SECRET']
SCOPES = CONFIG['GOOGLE_SCOPES']


def _authorize():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRET,
                                                                   scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    return discovery.build('calendar', 'v3', http=http)


def _now():
    return datetime.utcnow().isoformat() + 'Z'


def calendars():
    service = _authorize()
    result = service.calendarList().list().execute()
    return result.get('items', [])


def upcoming_events(calendar_id):
    service = _authorize()
    result = service.events().list(
        calendarId=calendar_id,
        timeMin=_now()
    ).execute()
    return result.get('items', [])


def event(calendar_id, event_id):
    """Gets the given event and returns the event response body

    :param calendar_id: Calendar ID event is in to update
    :param event_id: Event ID of event to update
    :return: Event response body
    """
    service = _authorize()
    result = service.events().get(
        calendarId=calendar_id,
        eventId=event_id
    ).execute()
    return result


def create_event(calendar_id, year, month, day, hour, minute, duration, summary, description,
                 location=''):
    """Creates an event in the given calendar. Accepts UTC

    :param calendar_id: Calendar ID to create event in
    :param year: Int on which year the event starts in
    :param month: Int on which month the event starts in
    :param day: Int on which day the event starts in
    :param hour: Int on which hour the event starts in. Note that this assumes UTC+2
    :param minute: Int on which minute the event starts in
    :param duration: Int on how long in minutes the event should last
    :param summary: Title of the event
    :param description: Description of the event
    :param location: Optional string specifying where the event will happen
    :return: eventId
    """
    # Convert to UTC
    start = datetime(year, month, day, hour, minute)
    end = (datetime(year, month, day, hour, minute) + timedelta(minutes=duration))
    start = start.isoformat()
    end = end.isoformat()
    body = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': 'UTC'
        },
        'end': {
            'dateTime': end,
            'timeZone': 'UTC'
        },
        'location': location
    }

    service = _authorize()
    result = service.events().insert(
        calendarId=calendar_id,
        body=body
    ).execute()
    return result['id']


def update_event(calendar_id, event_id, year=None, month=None, day=None, hour=None, minute=None,
                 duration=None, summary=None, description=None, location=None):
    """Updates an event with the given ID in the given Calendar. Accepts UTC

    :param calendar_id: Calendar ID event is in to update
    :param event_id: Event ID of event to update
    :param year: Int on which year the event starts in
    :param month: Int on which month the event starts in
    :param day: Int on which day the event starts in
    :param hour: Int on which hour the event starts in. Note that this assumes UTC+2
    :param minute: Int on which minute the event starts in
    :param duration: Optional Int on how long in minutes the event should last
    :param summary: Title of the event
    :param description: Description of the event
    :param location: Optional string specifying where the event will happen
    :return: eventId
    """
    # If any date time variable is given, make sure that they are all given
    start = None
    end = None
    if year or month or day or hour is not None or minute is not None or duration:
        assert year and month and day and hour is not None and minute is not None and duration
        start = datetime(year, month, day, hour, minute)
        end = (datetime(year, month, day, hour, minute) + timedelta(minutes=duration))
        start = start.isoformat()
        end = end.isoformat()

    body = {}
    change = False
    if summary:
        body['summary'] = summary
        change = True
    if description:
        body['description'] = description
        change = True
    if location:
        body['location'] = location
        change = True
    if start and end:
        body['start'] = {
            'dateTime': start,
            'timeZone': 'UTC'
        }
        body['end'] = {
            'dateTime': end,
            'timeZone': 'UTC'
        }
        change = True

    if change:
        service = _authorize()
        result = service.events().patch(
            calendarId=calendar_id,
            eventId=event_id,
            body=body
        ).execute()
        return result['id']


def delete_event(calendar_id, event_id):
    """Deletes the event with the given ID in the given Calendar.

    :param calendar_id: Calendar ID event is in to update
    :param event_id: Event ID of event to update
    :return: Empty response body
    """
    service = _authorize()
    result = service.events().delete(
        calendarId=calendar_id,
        eventId=event_id
    ).execute()
    return result

def url(calendar_id, event_id):
    """Gets the public URL to the event

    :param calendar_id: Calendar ID event is in to update
    :param event_id: Event ID of event to update
    :return: Event response body
    """
    return event(calendar_id, event_id)['htmlLink']
