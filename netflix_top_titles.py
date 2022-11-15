import pandas as pd
import numpy as np


filename = 'data/all-weeks-countries.tsv'
df = pd.read_csv(filename, sep='\t')

us_df = df[(df['country_iso2'] == 'US') & (df['category'] == 'Films')]

groupby_cols = ['week', 'category', 'show_title']

us_weekly_df = df[df['country_iso2'] == 'US']\
    [['week', 'category', 'show_title', 'weekly_rank']]\
    .groupby(['week', 'category', 'show_title'])\
    .min('weekly_rank')\
    .reset_index()

#71 weeks of data from 7/4/2021 to 11/6/2022    

def top_shows_and_films(us_weekly_df, category, num_results):
    tmp = us_weekly_df[us_weekly_df['category'] == category]
    print(tmp[['category', 'show_title', 'weekly_rank']]\
        .groupby(['category', 'show_title'])\
        .agg(weeks=('weekly_rank', 'size'), top_rank=('weekly_rank', 'min'))\
        .sort_values(['weeks', 'top_rank'], ascending=[False, True])\
        .head(num_results))
    
    
top_shows_and_films(us_weekly_df, category='TV', num_results=15)
top_shows_and_films(us_weekly_df[us_weekly_df['weekly_rank']==1], category='TV', num_results=15)

top_shows_and_films(us_weekly_df, category='Films', num_results=15)
top_shows_and_films(us_weekly_df[us_weekly_df['weekly_rank']==1], category='Films', num_results=15)