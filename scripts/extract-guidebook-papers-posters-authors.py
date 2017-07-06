#!/usr/bin/env python3

import re

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


# get the HTML from the program page we want to parse
with open('../_pages/testing/program.md', 'r') as htmlf:
    schedule_html = re.search(r'<div class="schedule">.*</div>', htmlf.read(), re.DOTALL).group()

# parse this HTML using BeautifulSoup
soup = BeautifulSoup(schedule_html, 'html.parser')

# read in the custom list templates for both papers and authors
df_papers = pd.read_csv('Guidebook_CL_Template.csv')
df_posters = pd.read_csv('Guidebook_CL_Template.csv')
df_authors = pd.read_csv('Guidebook_CL_Template.csv')
paper_rows = []
poster_rows = []
author_rows = []
all_authors = set()

# read in the full acl program spreadsheet from Min-Yen so that
# we can get the abstracts
df_full_program = pd.read_excel('acl-final-program.xlsx', sheetname='Accepted Papers', parse_cols="A,B,C,D,H,K")

# 1. get all the paper titles, authors, and abstracts from all the paper sessions
# we also want to extract the authors in a separate CSV file
for session_id in paper_session_ids:
    session_html = soup.find(id="session-{}".format(session_id))
    for paper_html in session_html.find_all("tr", id="paper"):
        paper_title_str, author_str = list(paper_html.find_all("td")[1].stripped_strings)
        paper_title_str = paper_title_str.strip().rstrip('.')
        author_list = re.split(r',| and ', author_str)
        author_list = [name.strip() for name in author_list if name]
        abstract = df_full_program[(df_full_program['Session'] == session_id) &
                                   (df_full_program['Title'] == paper_title_str)]['Abstract'].values[0]
        try:
            abstract = re.sub(r'\\url{(.*?)}', r'<a href="\1">\1</a>', abstract)
            abstract = re.sub(r'\\emph{(.*?)}', r'<em>\1</em>', abstract)
            abstract = re.sub(r'\\textit{(.*?)}', r'<em>\1</em>', abstract)
            abstract = re.sub(r'\\end{abstract}', '', abstract)
        except TypeError:
            abstract = ''
        d = {'Name': paper_title_str,
             "Sub-Title (i.e. Location, Table/Booth, or Title/Sponsorship Level)": author_str,
             'Description (Optional)': abstract,
             'Location/Room': '',
             'Image (Optional)': '',
             'Thumbnail (Optional)': ''}
        paper_rows.append(d)

        # and now the authors, one by one
        for author_name in author_list:
            if not author_name or not re.match(r'^[A-Z]', author_name):
                import ipdb
                ipdb.set_trace()
            if author_name not in all_authors:
                d = {'Name': author_name,
                     "Sub-Title (i.e. Location, Table/Booth, or Title/Sponsorship Level)": '',
                     'Description (Optional)': '',
                     'Location/Room': '',
                     'Image (Optional)': '',
                     'Thumbnail (Optional)': ''}
                author_rows.append(d)
                all_authors.add(author_name)

# 2. get all the paper titles, authors, and abstracts from all the poster sessions
for poster_session_id in ['poster-1', 'poster-2']:
    session_html = soup.find(id="session-{}".format(poster_session_id))
    for poster_html in session_html.find_all("tr", id="poster"):
        poster_title_str, author_str = list(poster_html.find_all("td")[0].stripped_strings)
        poster_title_str = poster_title_str.strip().rstrip('.')
        author_list = re.split(r',| and ', author_str)
        author_list = [name.strip() for name in author_list if name]
        lookup_session_id = 'p1' if poster_session_id == 'poster-1' else 'p2'
        abstract = df_full_program[(df_full_program['Session'] == lookup_session_id) &
                                   (df_full_program['Title'] == poster_title_str)]['Abstract'].values[0]
        try:
            abstract = re.sub(r'\\url{(.*?)}', r'<a href="\1">\1</a>', abstract)
            abstract = re.sub(r'\\emph{(.*?)}', r'<em>\1</em>', abstract)
            abstract = re.sub(r'\\textit{(.*?)}', r'<em>\1</em>', abstract)
            abstract = re.sub(r'\\end{abstract}', '', abstract)
        except TypeError:
            print('skipping')
            abstract = ''
        d = {'Name': poster_title_str,
             "Sub-Title (i.e. Location, Table/Booth, or Title/Sponsorship Level)": author_str,
             'Description (Optional)': abstract,
             'Location/Room': '',
             'Image (Optional)': '',
             'Thumbnail (Optional)': ''}
        poster_rows.append(d)

        # and now the authors, one by one
        for author_name in author_list:
            if not author_name or not re.match(r'^[A-Z]', author_name):
                import ipdb
                ipdb.set_trace()
            if author_name not in all_authors:
                d = {'Name': author_name,
                     "Sub-Title (i.e. Location, Table/Booth, or Title/Sponsorship Level)": '',
                     'Description (Optional)': '',
                     'Location/Room': '',
                     'Image (Optional)': '',
                     'Thumbnail (Optional)': ''}
                author_rows.append(d)
                all_authors.add(author_name)


df_papers = df_papers.append(paper_rows)
df_papers.to_csv('acl2017-papers.csv', index=False)

df_posters = df_posters.append(poster_rows)
df_posters.to_csv('acl2017-posters.csv', index=False)

df_authors = df_authors.append(author_rows)
df_authors.sort_values(by='Name', inplace=True)
df_authors.to_csv('acl2017-authors.csv', index=False)
