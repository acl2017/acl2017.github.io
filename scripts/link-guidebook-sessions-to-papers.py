#!/usr/bin/env python3

import re

import numpy as np
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

# read in the guidebook-exported sessions file
df_schedule = pd.read_csv('guidebook-exports/schedule.csv')

# read in the guidebook-exported papers file
df_papers = pd.read_csv('guidebook-exports/papers.csv')

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
for session_id in paper_session_ids:
    session_html = soup.find(id="session-{}".format(session_id))
    for paper_html in session_html.find_all("tr", id="paper"):
        paper_title_str, author_str = list(paper_html.find_all("td")[1].stripped_strings)
        paper_title_str = paper_title_str.strip().rstrip('.')

        # get the guidebook custom list ID for this paper title
        guidebook_paper_id = df_papers[df_papers['Name'] == paper_title_str]['Item ID (Optional)'].values[0]
        assert isinstance(guidebook_paper_id, np.int64)

        # now get the guidebook ID for this session
        guidebook_session_id = df_schedule[df_schedule['Session Title'].str.startswith('[{}]'.format(session_id.upper()))]['Session ID'].values[0]
        assert isinstance(guidebook_session_id, np.int64)

        d = {'Session ID (Optional)': guidebook_session_id,
             'Session Name (Optional)': '',
             'Link To Session ID (Optional)': '',
             'Link To Session Name (Optional)':'',
             'Link To Custom List Item ID (Optional)': guidebook_paper_id,
             'Link To Custom List Item Name (Optional)':'',
             'Link To Form Name (Optional)':'',
             'Link To URLs (Optional)':'',
             'URL Names (Optional)':''}
        rows.append(d)

df_session_links = df_session_links.append(rows)
df_session_links['Session ID (Optional)'] = df_session_links['Session ID (Optional)'].astype(int)
df_session_links['Link To Custom List Item ID (Optional)'] = df_session_links['Link To Custom List Item ID (Optional)'].astype(int)
df_session_links.to_csv('acl2017-session-to-paper-links.csv', index=False)
