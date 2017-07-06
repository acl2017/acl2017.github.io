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

# read in the guidebook-exported papers file
df_papers = pd.read_csv('guidebook-exports/papers.csv')

# read in the guidebook-exported posters file
df_posters = pd.read_csv('guidebook-exports/posters.csv')

# read in the guidebook-exported authors file
df_authors = pd.read_csv('guidebook-exports/authors.csv')

# read in the session link template
df_author_links = pd.read_csv('CustomListItem_Link_template.csv')
rows = []

# get the HTML from the program page we want to parse
with open('../_pages/testing/program.md', 'r') as htmlf:
    schedule_html = re.search(r'<div class="schedule">.*</div>', htmlf.read(), re.DOTALL).group()

# parse this HTML using BeautifulSoup
soup = BeautifulSoup(schedule_html, 'html.parser')

# go over each paper session, find each paper, find each of its authors
# and create the link rows from each author -> the paper
for session_id in paper_session_ids:
    session_html = soup.find(id="session-{}".format(session_id))
    for paper_html in session_html.find_all("tr", id="paper"):
        paper_title_str, author_str = list(paper_html.find_all("td")[1].stripped_strings)
        paper_title_str = paper_title_str.strip().rstrip('.')
        author_list = re.split(r',| and ', author_str)
        author_list = [name.strip() for name in author_list if name]

        # get the guidebook ID for this paper title
        guidebook_paper_id = df_papers[df_papers['Name'] == paper_title_str]['Item ID (Optional)'].values[0]
        assert isinstance(guidebook_paper_id, np.int64)

        # for each author in the list, get the guidebook ID and create the link
        for author_name in author_list:
            guidebook_author_id = df_authors[df_authors['Name'] == author_name]['Item ID (Optional)'].values[0]
            assert isinstance(guidebook_author_id, np.int64)

            d = {'Item ID (Optional)': guidebook_author_id,
                 'Item Name (Optional)': '',
                 'Link To Session ID (Optional)': '',
                 'Link To Session Name (Optional)': '',
                 'Link To Custom List Item ID (Optional)': guidebook_paper_id,
                 'Link To Custom List Item Name (Optional)': '',
                 'Link To Form Name (Optional)': '',
                 'Link To URLs (Optional)': '',
                 'URL Names (Optional)': ''}

            rows.append(d)

# now do the same for each poster as well
for session_id in ['poster-1', 'poster-2']:
    session_html = soup.find(id="session-{}".format(session_id))
    for poster_html in session_html.find_all("tr", id="poster"):
        poster_title_str, author_str = list(poster_html.find_all("td")[0].stripped_strings)
        poster_title_str = poster_title_str.strip().rstrip('.')
        author_list = re.split(r',| and ', author_str)
        author_list = [name.strip() for name in author_list if name]

        # get the guidebook custom list ID for this poster title
        guidebook_poster_id = df_posters[df_posters['Name'] == poster_title_str]['Item ID (Optional)'].values[0]
        assert isinstance(guidebook_poster_id, np.int64)

        # for each author in the list, get the guidebook ID and create the link
        for author_name in author_list:
            guidebook_author_id = df_authors[df_authors['Name'] == author_name]['Item ID (Optional)'].values[0]
            assert isinstance(guidebook_author_id, np.int64)

            d = {'Item ID (Optional)': guidebook_author_id,
                 'Item Name (Optional)': '',
                 'Link To Session ID (Optional)': '',
                 'Link To Session Name (Optional)': '',
                 'Link To Custom List Item ID (Optional)': guidebook_poster_id,
                 'Link To Custom List Item Name (Optional)': '',
                 'Link To Form Name (Optional)': '',
                 'Link To URLs (Optional)': '',
                 'URL Names (Optional)': ''}

            rows.append(d)

df_author_links = df_author_links.append(rows)
df_author_links['Item ID (Optional)'] = df_author_links['Item ID (Optional)'].astype(int)
df_author_links['Link To Custom List Item ID (Optional)'] = df_author_links['Link To Custom List Item ID (Optional)'].astype(int)
df_author_links.to_csv('acl2017-author-to-poster-and-paper-links.csv', index=False)
