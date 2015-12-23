# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import urllib2
import os
import sys
import re

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), os.getcwd()))
import ynucalender

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'ynu calendar'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'ynu-calendar-credential.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    parser = ynucalender.YNUCalendar()
    info = parser.get_info()
    for e in info:
        event = create_event(e['summary'], e['term'])
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))



def create_event(summary, term):
    event = {}
    event['summary'] = summary
    if not term['start'] == term['end']:
        dt = datetime.datetime.strptime(term['end'], '%Y-%m-%d') + datetime.timedelta(days=1)
        term['end'] = dt.date().isoformat()

    event['start'] = {
            'date': term['start'],
            'timeZone': 'Asia/Tokyo'
    }
    event['end'] = {
            'date': term['end'],
            'timeZone': 'Asia/Tokyo'
    }
    return event


if __name__ == '__main__':
    main()
