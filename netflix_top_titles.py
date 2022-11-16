import pandas as pd

filename = 'data/all-weeks-global.tsv'
df = pd.read_csv(filename, sep='\t')

df['season_title'] = df['season_title'].fillna('n/a')

film_season = df.groupby(['category', 'show_title', 'season_title'])\
    .agg(weeks=('weekly_rank', 'size'), top_rank=('weekly_rank', 'min'))\
    .reset_index()

num_movies = len(film_season[film_season['category'] == 'Films (English)'])
num_seasons = len(film_season[film_season['category'] == 'TV (English)'])
num_series = len(film_season[film_season['category'] == 'TV (English)'][['show_title']].drop_duplicates())

print('{num_movies} movies and {num_seasons} seasons of {num_series} series appeared in the Netflix Weekly Top Ten in the US between July 4th 2021 & November 6th 2022'.format( num_movies=num_movies, num_seasons=num_seasons, num_series=num_series))

tv_season = film_season[film_season['category']=='TV (English)']

tv_season.groupby('show_title').agg(slots=('weeks', 'sum'), num_seasons=('season_title', 'size')).sort_values('num_seasons', ascending=False).head(10)

print('Only Cobra Kai had 5 seasons crack the Top 10. 6 other series have had 4 seasons in the top 10')

most_season_in_week = df[df['category'] == 'TV (English)'].groupby(['show_title', 'week']).size().sort_values(ascending=False)

print('Stranger Things (9x), Ozark (2x), & Cobra Kai (1x) had 4 seasons in the top 10 in the same week')

---
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


us_weekly_dups_df = df[df['country_iso2'] == 'US']
df[df['country_iso2'] == 'US'].groupby(['category', 'show_title', 'season_title']).size()