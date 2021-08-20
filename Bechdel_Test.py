import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import urllib,json
from plotnine import ggplot,geom_point,aes,geom_line

from seaborn.palettes import color_palette
#What is a Bechdel Test?
#The Bechdel Test is a measure of the representation of women in fiction. 
#It asks whether a work features at least two women who talk to each other about something other than a man.
#I want to answer the following questions
#  1. Have the Bechdel scores of movies improved over the years?
#  2. Do movies with higher IMDB ratings have higher Bechdel scores?
#  3. Do movies with female directors have higher Bechdel scores?
#  4. Does the budget of a movie have any impact on its Bechdel score?
#  5. Do movies with higher Bechdel scores generate a larger revenue?

df = pd.read_json('http://bechdeltest.com/api/v1/getAllMovies')
print(df.head())
# there are five variables:
# IMDBID -> The Movie's IMDB number
# ID -> Unique movie ID
# YEAR -> Year the movie was released
# TITLE -> Movie title
# RATING ->Becheld Score of the movie from 0 to 3. Rating Lower than 3 means the movie failed the Bechdel Test

# When we look at the column 'YEAR' we'll see that there are movies from 19th century.
# And most of them has Bechdel score of 0. I'm going to split my Data frame into to, one with Movies before 1962.
# And the second one will have Movies after 1962.
dfBefore = df[df["year"] < 1962]
dfAfter = df[df["year"] >= 1962]

# Now we can look if we create our new data frames correctly
print("\n",dfBefore['year'].max(),dfAfter['year'].min())

# As we can see, dataframe with movies before 1962 contain movies which wasen't released after 1961,
# and dataframe with movies after 1962 starts at 1962. So we created data frame correctly

# Now i want to show proportion in movies before and after 1956 which get 0,1,2 or 3 points in Bechdel Test
fig, axs = plt.subplots(ncols=2,nrows=1,sharey=True) 
sns.countplot(x='rating',data=dfBefore,ax=axs[0])
sns.countplot(x='rating',data=dfAfter,ax=axs[1])
axs[0].set_title('before 1962')
axs[1].set_title('after 1962')
plt.show(block=False)
plt.pause(15)
plt.close()

# As we can see movies after 1962 are more likely to pass Bechdel Test.
# that's whhy i'm going to focus on Data frame with movies released after 1962
# Now i'm going to create list with 1/0, where '0' means movie didn't passed Bechdel Test and '1' means that the movie passed it

movie_list = []
for score in dfAfter['rating']:
    if score != 3:
        movie_list.append(0)
    else:
        movie_list.append(1)

dfAfter['passed test'] = movie_list

# now it's time to count how many movies passed or didn't pass this test
sns.countplot(x='passed test',data=dfAfter)
plt.show(block=False)
plt.pause(15)
plt.close()

dfAfter.rename(columns={'rating':'bechdel score'},inplace=True)
dfAfter['year'] = pd.to_datetime(dfAfter['year'], format='%Y')
dfAfter['bechdel score'] = dfAfter['bechdel score'].astype('category',copy=False)

print(ggplot(dfAfter,aes('year',color=dfAfter['bechdel score']))
    +geom_point(stat='count',show_legend=True)
    +geom_line(stat='count',show_legend=True))
# As we can see on this plot, most movies before 1990 didn't pass the Bechdel test.
# During that time, there wasn't significant difference between movies that passed the Bechdel test and moviest that didn't.
# After 1990 we can see that amount of movies which passed Bechdel test was increasing. 
# And it is massive improvemnt comparing to movies relesed before 1990.


# Now i want to visualize relationship betwin IMBD rating and the Bachdel scores. 
# I want to knwo if movies with higher scores are more likly to have higher IMBF rating.
# If i want to do this i'll need to merge new dataset called "movies.csv" with existing data frame
# To do this I need to have only Titles and Ratings from "movies.csv"

# There might be some null values so i'm going to drop rows with null value
movies = pd.read_csv('movies.csv')
imbd = movies[['title','rating']]

dfAfter = pd.merge(dfAfter,imbd,how='left',left_on=['title'],right_on=['title'])
dfAfter = dfAfter.dropna()
print(dfAfter.head())
