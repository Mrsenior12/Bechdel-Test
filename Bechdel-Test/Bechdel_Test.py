import pandas as pd
import matplotlib.pyplot as plt
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