#!/usr/bin/env python3

import re

import numpy as np
import pandas as pd

from bs4 import BeautifulSoup

# read in the guidebook-exported sessions file
df_schedule = pd.read_csv('guidebook-exports/schedule.csv')

# read in the guidebook-exported papers file
df_posters = pd.read_csv('guidebook-exports/posters.csv')

# read in the session link template
df_session_links = pd.read_csv('Sessions_Link_Template.csv')
rows = []

# get the HTML from the program page we want to parse
with open('../_pages/testing/program.md', 'r') as htmlf:
    schedule_html = re.search(r'<div class="schedule">.*</div>', htmlf.read(), re.DOTALL).group()

# parse this HTML using BeautifulSoup
soup = BeautifulSoup(schedule_html, 'html.parser')

# go over each paper session, find each paper and create the link from the session
# to its papers
for session_id in ['poster-1', 'poster-2']:
    session_html = soup.find(id="session-{}".format(session_id))
    for poster_html in session_html.find_all("tr", id="poster"):
        poster_title_str, author_str = list(poster_html.find_all("td")[0].stripped_strings)
        poster_title_str = poster_title_str.strip().rstrip('.')

        # get the guidebook custom list ID for this poster title
        guidebook_poster_id = df_posters[df_posters['Name'] == poster_title_str]['Item ID (Optional)'].values[0]
        assert isinstance(guidebook_poster_id, np.int64)

        # now get the guidebook ID for this session
        lookup_session_id = 'Posters & Dinner' if session_id == 'poster-1' else "Posters, Demos & Dinner"
        guidebook_session_id = df_schedule[df_schedule['Session Title'] == lookup_session_id]['Session ID'].values[0]
        assert isinstance(guidebook_session_id, np.int64)

        d = {'Session ID (Optional)': guidebook_session_id,
             'Session Name (Optional)': '',
             'Link To Session ID (Optional)': '',
             'Link To Session Name (Optional)':'',
             'Link To Custom List Item ID (Optional)': guidebook_poster_id,
             'Link To Custom List Item Name (Optional)':'',
             'Link To Form Name (Optional)':'',
             'Link To URLs (Optional)':'',
             'URL Names (Optional)':''}
        rows.append(d)

df_session_links = df_session_links.append(rows)
df_session_links['Session ID (Optional)'] = df_session_links['Session ID (Optional)'].astype(int)
df_session_links['Link To Custom List Item ID (Optional)'] = df_session_links['Link To Custom List Item ID (Optional)'].astype(int)
df_session_links.to_csv('acl2017-session-to-poster-links.csv', index=False)
