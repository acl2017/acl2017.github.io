#!/usr/bin/env python3

import re

from datetime import datetime

import pandas as pd

from bs4 import BeautifulSoup


paper_session_ids = ['1a', '1b' ,'1c', '1d', '1e',
                     '2a', '2b' ,'2c', '2d', '2e',
                     '3a', '3b' ,'3c', '3d', '3e',
                     '4a', '4b' ,'4c', '4d', '4e',
                     '5a', '5b' ,'5c', '5d', '5e',
                     '6a', '6b' ,'6c', '6d', '6e',
                     '7a', '7b',
                     '8a', '8b']
tutorial_session_ids = ['morning-tutorials', 'afternoon-tutorials']
plenary_session_ids = ['']

# get the HTML from the program page we want to parse
with open('../_pages/testing/program.md', 'r') as htmlf:
    schedule_html = re.search(r'<div class="schedule">.*</div>', htmlf.read(), re.DOTALL).group()

# parse this HTML using BeautifulSoup
soup = BeautifulSoup(schedule_html, 'html.parser')

# now for each session ID, get the information into the format that guidebook expects
df = pd.read_csv('Guidebook_Schedule_Template.csv')
rows = []

# parse the tutorial descriptions from _pages/tutorials.md
tutorial_description_dict = {}
with open('../_pages/tutorials.md', 'r') as tutorialf:
    tutorial_html = re.search(r'<span class="btn btn--small">.*</p>', tutorialf.read(), re.DOTALL).group()
    tutorial_soup = BeautifulSoup(tutorial_html, 'html.parser')
    for tutorial_id in ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']:
        tutorial_description_dict[tutorial_id] = str(tutorial_soup.find('span', text=tutorial_id).find_next_sibling('div'))

# 1. The Tutorials
for session_id in tutorial_session_ids:
    session_html = soup.find(id="session-{}".format(session_id))
    raw_day = session_html.find_previous_sibling(class_="day").text
    session_date = datetime.strptime(raw_day + ', 2017', '%A, %B %d, %Y').strftime('%m/%d/%y')
    session_time = session_html.find(class_="session-time").text
    session_start_time, session_end_time = session_time.split(' – ')
    for tutorial_html in session_html.find_all("tr", id="tutorial"):
        title_html, location_html = tutorial_html.find_all("span")
        session_title = title_html.text
        tutorial_id = re.search(r'T[0-9]', session_title).group()
        session_location = location_html.text
        d = {'Session Title': session_title,
             'Date': session_date,
             'Time Start': session_start_time,
             'Time End': session_end_time,
             'Room/Location': session_location,
             'Schedule Track (Optional)': '',
             'Description (Optional)': tutorial_description_dict[tutorial_id],
             'Allow Checkin (Optional)': 'True',
             'Checkin Begin (Optional)': '',
             'Limit Spaces? (Optional)': '',
             'Allow Waitlist (Optional)': 'False'}
        rows.append(d)

# 2. The paper sessions
for session_id in paper_session_ids:
    session_html = soup.find(id="session-{}".format(session_id))
    session_title = session_html.find(class_="session-title").text
    raw_day = session_html.find_previous_sibling(class_="day").text
    session_date = datetime.strptime(raw_day + ', 2017', '%A, %B %d, %Y').strftime('%m/%d/%y')
    session_location = session_html.find(class_="session-location").text
    session_time = session_html.find(class_="session-time").text
    session_start_time, session_end_time = session_time.split(' – ')
    d = {'Session Title': '[{}] {}'.format(session_id.upper(), session_title),
         'Date': session_date,
         'Time Start': session_start_time,
         'Time End': session_end_time,
         'Room/Location': session_location,
         'Schedule Track (Optional)': '',
         'Description (Optional)': 'Session Chair: XXX',
         'Allow Checkin (Optional)': 'True',
         'Checkin Begin (Optional)': '',
         'Limit Spaces? (Optional)': '',
         'Allow Waitlist (Optional)': 'False'}
    rows.append(d)

# 3. The poster sessions
for poster_session_id in ['poster-1', 'poster-2']:
    poster_html = soup.find(id="session-{}".format(poster_session_id))
    session_title = poster_html.find(class_="session-title").text
    raw_day = poster_html.find_previous_sibling(class_="day").text
    session_date = datetime.strptime(raw_day + ', 2017', '%A, %B %d, %Y').strftime('%m/%d/%y')
    session_location = poster_html.find(class_="session-location").text
    session_time = poster_html.find(class_="session-time").text
    session_start_time, session_end_time = session_time.split(' – ')

    if poster_session_id == "poster-1":
        session_description = "Long paper, short paper, and student research workshop posters."
    else:
        session_description = "Long paper posters, short paper posters, and system demonstrations."

    d = {'Session Title': session_title,
         'Date': session_date,
         'Time Start': session_start_time,
         'Time End': session_end_time,
         'Room/Location': session_location,
         'Schedule Track (Optional)': '',
         'Description (Optional)': session_description,
         'Allow Checkin (Optional)': 'True',
         'Checkin Begin (Optional)': '',
         'Limit Spaces? (Optional)': '',
         'Allow Waitlist (Optional)': 'False'}
    rows.append(d)


# 4. The lunches
for lunch_html in soup.find_all(id=re.compile("session-lunch")):
    session_title = lunch_html.find(class_="session-title").text
    raw_day = lunch_html.find_previous_sibling(class_="day").text
    session_date = datetime.strptime(raw_day + ', 2017', '%A, %B %d, %Y').strftime('%m/%d/%y')
    session_time = lunch_html.find(class_="session-time").text
    session_start_time, session_end_time = session_time.split(' – ')
    d = {'Session Title': session_title,
         'Date': session_date,
         'Time Start': session_start_time,
         'Time End': session_end_time,
         'Room/Location': 'Salons E/F' if re.search(r'arXiv', session_title) else '',
         'Schedule Track (Optional)': '',
         'Description (Optional)': '',
         'Allow Checkin (Optional)': 'False',
         'Checkin Begin (Optional)': '',
         'Limit Spaces? (Optional)': '',
         'Allow Waitlist (Optional)': 'False'}
    rows.append(d)

# 5. The breaks
for break_html in soup.find_all(id=re.compile("session-break")):
    session_title = break_html.find(class_="session-title").text
    raw_day = break_html.find_previous_sibling(class_="day").text
    session_date = datetime.strptime(raw_day + ', 2017', '%A, %B %d, %Y').strftime('%m/%d/%y')
    session_time = break_html.find(class_="session-time").text
    session_start_time, session_end_time = session_time.split(' – ')
    d = {'Session Title': session_title,
         'Date': session_date,
         'Time Start': session_start_time,
         'Time End': session_end_time,
         'Room/Location': '',
         'Schedule Track (Optional)': '',
         'Description (Optional)': '',
         'Allow Checkin (Optional)': 'False',
         'Checkin Begin (Optional)': '',
         'Limit Spaces? (Optional)': '',
         'Allow Waitlist (Optional)': 'False'}
    rows.append(d)

# 6. The invited talks
for invited_talk_html in soup.find_all(id=re.compile("session-invited")):
    session_title = invited_talk_html.find(class_="session-title").text
    raw_day = invited_talk_html.find_previous_sibling(class_="day").text
    session_date = datetime.strptime(raw_day + ', 2017', '%A, %B %d, %Y').strftime('%m/%d/%y')
    session_time = invited_talk_html.find(class_="session-time").text
    session_start_time, session_end_time = session_time.split(' – ')
    session_speaker = invited_talk_html.find(class_="session-people").text
    session_abstract = invited_talk_html.find(class_="session-abstract")
    session_description = '<p>{}</p><br/>{}'.format(session_speaker, session_abstract)
    session_location = invited_talk_html.find(class_="session-location").text
    d = {'Session Title': session_title,
         'Date': session_date,
         'Time Start': session_start_time,
         'Time End': session_end_time,
         'Room/Location': session_location,
         'Schedule Track (Optional)': '',
         'Description (Optional)': session_description,
         'Allow Checkin (Optional)': 'False',
         'Checkin Begin (Optional)': '',
         'Limit Spaces? (Optional)': '',
         'Allow Waitlist (Optional)': 'False'}
    rows.append(d)

# 7. The social event
social_event_html = soup.find(id="session-social")
session_title = social_event_html.find(class_="session-title").text
raw_day = social_event_html.find_previous_sibling(class_="day").text
session_date = datetime.strptime(raw_day + ', 2017', '%A, %B %d, %Y').strftime('%m/%d/%y')
session_time = social_event_html.find(class_="session-time").text
session_start_time, session_end_time = session_time.split(' – ')
session_description = social_event_html.find(class_="session-abstract")
session_location = social_event_html.find(class_="session-location").text
d = {'Session Title': session_title,
     'Date': session_date,
     'Time Start': session_start_time,
     'Time End': session_end_time,
     'Room/Location': session_location,
     'Schedule Track (Optional)': '',
     'Description (Optional)': session_description,
     'Allow Checkin (Optional)': 'False',
     'Checkin Begin (Optional)': '',
     'Limit Spaces? (Optional)': '',
     'Allow Waitlist (Optional)': 'False'}
rows.append(d)

# 8. Other plenary sessions: Welcome/LTA/Closing/Business Meeting
for plenary_session_id in ["reception", "welcome", "business-meeting",
                           "lifetime-achievement", "closing-awards"]:
    plenary_session_html = soup.find(id="session-{}".format(plenary_session_id))
    session_title = plenary_session_html.find(class_="session-title").text
    raw_day = plenary_session_html.find_previous_sibling(class_="day").text
    session_date = datetime.strptime(raw_day + ', 2017', '%A, %B %d, %Y').strftime('%m/%d/%y')
    session_time = plenary_session_html.find(class_="session-time").text
    session_start_time, session_end_time = session_time.split(' – ')
    session_location = plenary_session_html.find(class_="session-location").text

    if plenary_session_id == "business-meeting":
        session_description = "<strong>All attendees are encouraged to participate in the business meeting.</strong>"
    elif plenary_session_id == "reception":
        session_description= "<p>Catch up with your colleagues at the Welcome Reception!  It will be held immediately following the tutorials at the Westin Bayshore Hotel, Sunday, July 30th, in the Bayshore Grand Ballroom (the conference venue).  Refreshments and a light dinner will be provided and a cash bar will be available.</p>"
    else:
        session_description = ""

    d = {'Session Title': session_title,
         'Date': session_date,
         'Time Start': session_start_time,
         'Time End': session_end_time,
         'Room/Location': session_location,
         'Schedule Track (Optional)': '',
         'Description (Optional)': session_description,
         'Allow Checkin (Optional)': 'False',
         'Checkin Begin (Optional)': '',
         'Limit Spaces? (Optional)': '',
         'Allow Waitlist (Optional)': 'False'}
    rows.append(d)

df = df.append(rows)
df.to_csv('acl2017-sessions.csv', index=False)
