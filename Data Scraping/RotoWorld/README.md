# RotoWorld

To test the connection between betting lines and the players' injuries, we used selenium to extract injury status reports from RotoWorld that contained live-time data of the NBA players.

The problem with the data is the absence of a label, meaning we have descriptions of status but not a label for it, so we tagged the data using simple patterns, but since some patterns were not enough accurate in this case, we performed the tagging manually.


In the future, we are interested in building a model that will classify us for the injury status of the players given the description (we already have a nice tagged dataset that contains almost 30,00 records).

- Raw Data
![roto1](https://user-images.githubusercontent.com/75788772/101787138-7180ac00-3b07-11eb-854b-0edcfd54c05f.png)

- Data after extraction and classification using rule-based patterns
![roto2](https://user-images.githubusercontent.com/75788772/101787203-7e9d9b00-3b07-11eb-9941-4a3144bfde84.png)

- Final Data atfer manual labeling
![roto3](https://user-images.githubusercontent.com/75788772/101787242-89583000-3b07-11eb-92fe-c16062f598b5.png)
