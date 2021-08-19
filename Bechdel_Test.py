import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import urllib,json
#What is a Bechdel Test?
#The Bechdel Test is a measure of the representation of women in fiction. 
#It asks whether a work features at least two women who talk to each other about something other than a man.

df = pd.read_json('http://bechdeltest.com/api/v1/getAllMovies')
print(df.head())
# there are five variables:
# IMDBID -> The Movie's IMDB number
# ID -> Unique movie ID
# YEAR -> Year the movie was released
# TITLE -> Movie title
# RATING ->Becheld Score of the movie from 0 to 3. Rating Lower than 3 means the movie failed the Bechdel Test

# When we look at the column 'YEAR' we'll see that there are movies from 19th century.
# And most of them has Bechdel score of 0. I'm going to split my Dataframe into to, one with Movies before 1956.
# And the second one will have Movies after 1956.
dfBefore = df[df["year"] < 1956]
dfAfter = df[df["year"] >= 1956]

# Now we can look if we create our new dataframes correctly
print("\n",dfBefore['year'].max(),dfAfter['year'].min())

# As we can see, dataframe with movies before 1956 contain movies which wasen't released after 1955,
# and dataframe with movies after 1956 starts at 1956. So we created dataframe correctly

# Now i want to show proportion in movies before and after 1956 which get 0,1,2 or 3 points in Bechdel Test
fig, axs = plt.subplots(ncols=2,nrows=1,sharey=True) 
sns.countplot(x='rating',data=dfBefore,ax=axs[0])
sns.countplot(x='rating',data=dfAfter,ax=axs[1])
axs[0].set_title('before 1956')
axs[1].set_title('after 1956')
plt.show(block=False)
plt.pause(15)
plt.close()

# As we can see movies after 1956 are more likely to pass Bechdel Test.
# that's whhy i'm going to focus on Dataframe with movies released after 1956
# Now i'm going to create list with 1/0, where '0' means movie didn't passed Bechdel Test and '1' means that the movie passed it

movie_list = []
for score in dfAfter['rating']:
    if score != 3:
        movie_list.append(0)
    else:
        movie_list.append(1)

dfAfter['passed test'] = movie_list
print(dfAfter.head())

# now it's time to count how many movies passed or didn't pass this test
sns.countplot(x='passed test',data=dfAfter)
plt.show(block=False)
plt.pause(15)
plt.close()