# RotoWorld

To test the connection between betting lines and the players' injuries, we used selenium to extract injury status reports from RotoWorld that contained live-time data of the NBA players.

The problem with the data is the absence of a label, meaning we have descriptions of status but not a label for it, so we tagged the data using simple patterns, but since some patterns were not enough accurate in this case, we performed the tagging manually.


In the future, we are interested in building a model that will classify us for the injury status of the players given the description (we already have a nice tagged dataset that contains almost 30,00 records).
