import pandas as pd
import matplotlib.pyplot as plt
from plotnine.geoms.geom import geom
from plotnine.scales.scale_xy import scale_y_continuous
import seaborn as sns
import numpy as np
import urllib,json
from plotnine import ggplot,geom_point,aes,geom_line,geom_smooth,labs
import gender_guesser.detector as gender

from seaborn.palettes import color_palette
#What is a Bechdel Test?
#The Bechdel Test is a measure of the representation of women in fiction. 
#It asks whether a work features at least two women who talk to each other about something other than a man.
#I want to answer the following questions
#  1. Have the Bechdel scores of movies improved over the years?
#  2. Do movies with higher IMDB ratings have higher Bechdel scores?
#  3. Do movies with female directors have higher Bechdel scores?
#  4. Do movies with female directors have higher IMBD ratings?
#  5. Does the budget of a movie have any impact on its Bechdel score?
#  6. Do movies with higher Bechdel scores generate a larger revenue?

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

print(ggplot(dfAfter,aes('year',color='bechdel score'))
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
#print(dfAfter.head())

# After me merge these two data sets i'm going to create new data frame with year, bechdel score and rating
dfNew = dfAfter.groupby(['year','bechdel score']).agg({'rating':'mean'}).reset_index()
#print(dfNew.head())

print(ggplot(dfNew,aes(x='year',y='rating',color='bechdel score'))
    +geom_point()
    +geom_smooth()
    +scale_y_continuous(name='imbd rating')
    +labs(color='bechdel score')
)
# It appears that movies which passed Bechdel test has lower IMBD ratings than movies that didn't pass this test and I was a bit surprised.
# Now I want to visualize the relationship between gender of the director and bechdel score and IMBD ratings
# To do this i'll have to merge another data set from "movielatest.csv"
# using gender prediction library i'll try to find gender of a director by his name.

latest = pd.read_csv("movielatest.csv",encoding='latin')
dfLatest = latest[['name','director']]
#print(dfLatest.head())
dfLatest.rename(columns={'name':'title'},inplace=True)
dfLatest = pd.merge(dfAfter,dfLatest,how='left',left_on=['title'],right_on=['title'])
dfLatest = dfLatest.dropna()
#print(dfLatest.head())

# Now I want to try to predict gender of the director using his first name
gen = gender.Detector()
genders = []
for i in dfLatest['director']:
    d = i.split()[0]
    if gen.get_gender(d) == 'male':
        genders.append('male')

    elif gen.get_gender(d) == 'female':
        genders.append('female')
    
    else:
        genders.append("unknown")
dfLatest['gender'] = genders

# now we have to pop "unknown" gender from our data frame
dfLatest = dfLatest[dfLatest['gender'] != 'unknown']

# the last part of this task is to add another column with 1/0 where 0 means 'male' and 1 means 'female'
gender_list = []
for i in dfLatest['gender']:
    if i == 'male':
        gender_list.append(0)
    else:
        gender_list.append(1)
dfLatest['female'] = gender_list
#print(dfLatest.head())

# Now I'll create count plot to show number of males and females in data frame
sns.countplot(x='gender',data=dfLatest)
plt.show()

# As I thought in our data frame there's huge difference in number of men and women directors.
# It shouldn't be surprise, because Hollywood is known to employ small amount of women directors
# Now i want to visualize the gender of the director and the Bechdel Score, to see if movies with male director have lower score.

sns.countplot(x='bechdel score',hue='gender',data=dfLatest)
plt.show()
# We can see that movies which were directed by a female director are more likely to pass bechdel test.

# Now I'd like to check if movies directed by female have higher IMBD
print(ggplot(dfLatest, aes(x='year',y='rating',color='gender'))
    +geom_smooth()
    +scale_y_continuous(name='IMBD rating')
    +labs(color='gender'))

# As we can see movies directed by male director used to have higher IMBD score than movies directed by female till late 1990s.
# In the years following 2000 movies with higher IMBD were directed by female.

# Now I want to see if budget of a movie is somehow correlated with Bechdel score.
dfLatest['budget'] = latest['budget']
print(ggplot(dfLatest,aes(x='year',y='budget',color='bechdel score'))
    +geom_point()
    +geom_smooth())

# One thing you'll see imemdiately is huge increase movie's budget over the years. 
# Looks like movies that passed Bechdel test are more likle to have higher budget than movies that score a zero.
# However there is no strong correlation between budget and bechdel score.
# I would like to know if gender has impact on movie's budget

print(ggplot(dfLatest,aes(x='year',y='budget',color='gender'))
    +geom_point()
    +geom_smooth())
# We can see that ther's no correlation between gender and movie's budget

# Now I would like to see which genre are most likely to pass Bechdel test
dfLatest['genre'] = latest['genre']
print(ggplot(dfLatest,aes(x='year',y='genre',color='bechdel score'))
    +geom_point())

dfLatest['gross'] = latest['gross']
print(ggplot(dfLatest,aes(x='year',y='gross',color='bechdel score'))
    +geom_point())

print(ggplot(dfLatest,aes(x='year',y='gross',color='gender'))
+geom_point()
+geom_smooth())

# And that's it! I managed to visualize relationship and answer all the data question.
# Few interesting facts:
# 1. Over the years, number of movies which pass Bechdel test has been increasing
# 2. Movies which didn't pass Bechdel test are more likely to have higher IMBD ratings
# 3. Movies directed by female are more likely to pass Bechdel test.
# 4. There's no clear correlation between the budget or revenue of a movie and its Bechdel score or gender of the director
# However this analysis might not represent entire population of movies. 
# If we want to make good conclusion than we should take data sets from different places. 
# Last but not least, Bechdel test isn't the best benchmark to measure female representation in movies. 
# It doesn't take into consideration how well character is written or its impact for story of a movie.

# data sets can be found here: https://github.com/Natassha/Bechdel-Test
