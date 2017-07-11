#!/usr/bin/env python3

import pandas as pd

# read in the exported paper and poster files
df_papers = pd.read_csv('guidebook-exports/papers.csv')
df_posters = pd.read_csv('guidebook-exports/posters.csv')

# read in the full acl program spreadsheet from Min-Yen so that
# we can get the anthology IDs
df_full_program = pd.read_excel('acl-final-program.xlsx', sheetname='Accepted Papers', parse_cols="F,H")

# iterate over the papers first, match in the two frames and add the link with the anthology ID
# to the end of the abstract
new_rows = []
for idx, paper_row in df_papers.iterrows():
    paper_title = paper_row['Name']
    anthology_id = df_full_program[df_full_program['Title'] == paper_title]['Anthology ID'].values[0]
    old_program_str = paper_row['Description (Optional)']
    if not isinstance(anthology_id, str):
        new_program_str = old_program_str
    else:
        new_program_str = old_program_str + '<br/><p>[<a href="http://www.aclweb.org/anthology/{}">PDF</a>]</p>'.format(anthology_id)
    paper_row['Description (Optional)'] = new_program_str
    new_rows.append(paper_row)

df_new_papers = pd.DataFrame(new_rows)

# and now do the posters
new_rows = []
for idx, poster_row in df_posters.iterrows():
    poster_title = poster_row['Name']
    anthology_id = df_full_program[df_full_program['Title'] == poster_title]['Anthology ID'].values[0]
    assert isinstance(anthology_id, str)
    old_program_str = poster_row['Description (Optional)']
    new_program_str = old_program_str + '<br/><p>[<a href="http://www.aclweb.org/anthology/{}">PDF</a>]</p>'.format(anthology_id)
    poster_row['Description (Optional)'] = new_program_str
    new_rows.append(poster_row)

df_new_posters = pd.DataFrame(new_rows)

# write out the new frames to new files
df_new_papers.to_csv('acl2017-papers-with-anthology-links.csv', index=False)
df_new_posters.to_csv('acl2017-posters-with-anthology-links.csv', index=False)
