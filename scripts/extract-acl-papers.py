#!/usr/bin/env python3

import pandas as pd

from jinja2 import Environment, FileSystemLoader

# define the time for each paper in each session and
# starting and end time for each session based on the spreadsheet
# it's just faster to to do it manually than to deal with the
# non-structured format
session_times = {'1': '10:30 AM &ndash; 12:00 PM',
                 '2': '1:40 PM &ndash; 3:15 PM',
                 '3': '3:45 PM &ndash; 5:15 PM',
                 '4': '10:30 AM &ndash; 12:05 PM',
                 '5': '1:30 PM &ndash; 3:00 PM',
                 '6': '3:25 PM &ndash; 5:00 PM',
                 '7': '10:40 AM &ndash; 12:15 PM',
                 '8': '3:00 PM &ndash; 4:40 PM',
                 'p1': '6:00 PM &ndash; 9:30 PM',
                 'p2': '5:40 PM &ndash; 7:40 PM'}

session_paper_times = {'1a': ['10:30-10:48', '10:49-11:07', '11:08-11:26', '11:27-11:45', '11:46-11:58'],
                       '1b':['10:30-10:48', '10:49-11:07', '11:08-11:26', '11:27-11:45', '11:46-11:58'],
                       '1c': ['10:30-10:48', '10:49-11:07', '11:08-11:26', '11:27-11:45', '11:46-11:58'],
                       '1d': ['10:30-10:48', '10:49-11:07', '11:08-11:26', '11:27-11:45', '11:46-11:58'],
                       '1e': ['10:30-10:48', '10:49-11:07', '11:08-11:26', '11:27-11:45', '11:46-11:58'],
                       '2a': ['1:40-1:58', '1:59-2:17', '2:18-2:36', '2:37-2:55', '2:56-3:14'],
                       '2b': ['1:40-1:58', '1:59-2:17', '2:18-2:36', '2:37-2:55', '2:56-3:14'],
                       '2c': ['1:40-1:58', '1:59-2:17', '2:18-2:36', '2:37-2:55', '2:56-3:14'],
                       '2d': ['1:40-1:58', '1:59-2:17', '2:18-2:36', '2:37-2:55', '2:56-3:14'],
                       '2e': ['1:40-1:58', '1:59-2:17', '2:18-2:36', '2:37-2:55', '2:56-3:14'],
                       '3a': ['3:45-4:03', '4:04-4:22', '4:23-4:41', '4:42-5:00', '5:00-5:12'],
                       '3b': ['3:45-4:03', '4:04-4:22', '4:23-4:41', '4:42-5:00', '5:00-5:12'],
                       '3c': ['3:45-4:03', '4:04-4:22', '4:23-4:41', '4:42-5:00', '5:00-5:12'],
                       '3d': ['3:45-4:03', '4:04-4:22', '4:23-4:41', '4:42-5:00', '5:00-5:12'],
                       '3e': ['3:45-4:03', '4:04-4:22', '4:23-4:41', '4:42-5:00', '5:00-5:12'],
                       '4a': ['10:30-10:48', '10:49-11:07', '11:08-11:26', '11:27-11:45', '11:46-12:04'],
                       '4b': ['10:30-10:48', '10:49-11:07', '11:08-11:26', '11:27-11:45', '11:46-11:58'],
                       '4c': ['10:30-10:48', '10:49-11:07', '11:08-11:26', '11:27-11:45', '11:46-12:04'],
                       '4d': ['10:30-10:48', '10:49-11:07', '11:08-11:26', '11:27-11:45', '11:46-11:58'],
                       '4e': ['10:30-10:48', '10:49-11:07', '11:08-11:26', '11:27-11:45', '11:46-11:58'],
                       '5a': ['1:30-1:42', '1:43-2:01', '2:02-2:20', '2:21-2:39', '2:40-2:52'],
                       '5b': ['1:30-1:48', '1:49-2:07', '2:08-2:26', '2:27-2:39', '2:40-2:52'],
                       '5c': ['1:30-1:48', '1:49-2:07', '2:08-2:26', '2:27-2:39', '2:40-2:52'],
                       '5d': ['1:30-1:48', '1:49-2:07', '2:08-2:26', '2:27-2:39', '2:42-2:52'],
                       '5e': ['1:30-1:48', '1:49-2:07', '2:08-2:20', '2:21-2:33', '2:34-2:46'],
                       '6a': ['3:25-3:43', '3:44-4:02', '4:03-4:21', '4:22-4:40', '4:41-4:53'],
                       '6b': ['3:25-3:43', '3:44-4:02', '4:03-4:21', '4:22-4:40', '4:41-4:59'],
                       '6c': ['3:25-3:43', '3:44-4:02', '4:03-4:21', '4:22-4:40', '4:41-4:59'],
                       '6d': ['3:25-3:43', '3:44-4:02', '4:03-4:21', '4:22-4:34', '4:35-4:47'],
                       '6e': ['3:25-3:43', '3:44-4:02', '4:03-4:21', '4:22-4:40', '4:41-4:59'],
                       '7a': ['10:40-10:58', '10:59-11:17', '11:18-11:36', '11:37-11:49', '11:50-12:02', '12:03-12:15'],
                       '7b': ['10:40-10:58', '10:59-11:17', '11:18-11:30', '11:31-11:43', '11:44-11:56', '11:57-12:09'],
                       '8a': ['3:00-3:18', '3:19-3:37', '3:38-3:56', '3:57-4:15', '4:16-4:34'],
                       '8b': ['3:00-3:18', '3:19-3:37', '3:38-3:56', '3:57-4:15', '4:16-4:34']}

session_titles = {'1a': 'Information Extraction 1 (NN)',
                  '1b': 'Semantics 1',
                  '1c': 'Discourse 1',
                  '1d': 'Machine Translation 1',
                  '1e': 'Generation',
                  '2a': 'Question Answering',
                  '2b': 'Vision 1',
                  '2c': 'Syntax 1',
                  '2d': 'Machine Learning 1 (NN)',
                  '2e': 'Sentiment 1 (NN)',
                  '3a': 'Information Extraction 2 / Biomedical',
                  '3b': 'Semantics 2 (NN)',
                  '3c': 'Speech / Dialogue 1',
                  '3d': 'Multilingual',
                  '3e': 'Phonology',
                  '4a': 'Information Extraction 3',
                  '4b': 'Cognitive Modeling / Vision 2',
                  '4c': 'Dialogue 2',
                  '4d': 'Machine Translation 2',
                  '4e': 'Social Media',
                  '5a': 'Multidisciplinary',
                  '5b': 'Languages &amp; Resources',
                  '5c': 'Syntax 2 (NN)',
                  '5d': 'Machine Translation 3 (NN)',
                  '5e': 'Sentiment 3',
                  '6a': 'Information Extraction 4',
                  '6b': 'Semantics 2 (NN)',
                  '6c': 'Discourse 2 / Dialogue 3',
                  '6d': 'Machine Learning 2',
                  '6e': 'Summarization',
                  '7a': 'Outstanding Papers 1',
                  '7b': 'Outstanding Papers 2',
                  '8a': 'Outstanding Papers 3',
                  '8b': 'Outstanding Papers 4',
                  'p1': 'Posters &amp; Dinner',
                  'p2': 'Posters, Demos &amp; Dinner'}

session_counts = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

poster_types = {'Long': 'Long Papers',
                'Short': 'Short Papers',
                'SRW': 'Student Research Workshop',
                'Software Demonstrations': 'System Demonstrations'}

# load the jinja2 paper session template
PAPER_SESSION_TEMPLATE = Environment(loader=FileSystemLoader('.')).get_template('paper_session.tmpl')
POSTER_SESSION_TEMPLATE = Environment(loader=FileSystemLoader('.')).get_template('poster_session.tmpl')

# given a data frame session 1d, session title, paper titles and author names
# create an HTML snippet that we can simply insert in the program page
def make_paper_session_html(session_id, df_session):

    session_start_end = session_times[session_id[0]]
    day_session_count = session_counts[session_id[-1]]
    session_title = session_titles[session_id]
    session_dict = {'id': session_id,
                    'count': day_session_count,
                    'title': session_title,
                    'start_end': session_start_end}
    papers = []
    paper_times = session_paper_times[session_id]
    assert len(df_session) == len(paper_times)
    for _, row in df_session.iterrows():
        try:
            paper_dict = {'title': row['Title'], 'authors': row['Author'], 'time': paper_times[int(row['Ordering']) - 1]}
        except:
            import ipdb
            ipdb.set_trace()
        papers.append(paper_dict)
    rendered_html = PAPER_SESSION_TEMPLATE.render(session=session_dict, papers=papers)
    return rendered_html


def make_poster_session_html(poster_type, df_type):

    posters = []
    for _, row in df_type.iterrows():
        poster_dict = {'title': row['Title'], 'authors': row['Author']}
        posters.append(poster_dict)
    rendered_html = POSTER_SESSION_TEMPLATE.render(type=poster_types[poster_type], posters=posters)
    return rendered_html


# first read the list of accepted papers by session into a data frame
df_full = pd.read_excel('acl-final-program.xlsx', sheetname='Accepted Papers')

# get rid of the posters for now
df_papers = df_full[~df_full['Session'].isin(['p1', 'p2'])].copy()

# now iterate over each of the individual sessions and convert to HTML
grouped = df_papers.groupby('Session')

for session_id, df_session in grouped:
    df_sorted_session = df_session[['Title', 'Author', 'Ordering']].sort_values(by='Ordering')
    with open('{}.html'.format(session_id), 'w') as outf:
        outf.write(make_paper_session_html(session_id, df_sorted_session))

# now let's do the posters
df_posters = df_full[df_full['Session'].isin(['p1', 'p2'])].copy()

# now iterate over each of the individual sessions and convert to HTML
grouped = df_posters.groupby('Session')

for session_id, df_session in grouped:
    grouped2 = df_session.groupby('Type')
    for poster_type, df_type in grouped2:
        with open('{}_{}.html'.format(session_id, poster_type), 'w') as outf:
            outf.write(make_poster_session_html(poster_type, df_type))
