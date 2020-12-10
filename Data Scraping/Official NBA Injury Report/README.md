# NBA official Injury Report
The NBA Association requires the teams to publish 3 times a day the players' status for the next game.
While trying to collect this data, our first goal was to gather all the information in one big data frame, from which we can later train our model.
During this process, we run into a few problems.

1. The NBA official injury report has 5 differnt formats since it started publishing:

- 2018/12/17 - 2019/11/14 format:
[Game Date, Game Time, Matchup, Team, Player Name, Category, Reason, Current Status, Previous Status]
![1](https://user-images.githubusercontent.com/70581662/94700143-d5d30280-0343-11eb-94ea-cc2fc85a4545.png)
<br />

- 2019/12/17 format:
[Game Date, Game Time, Matchup, Team, Player Name, Current Status, Reason, Previous Status, Previous Reason]
![2](https://user-images.githubusercontent.com/70581662/94700177-dc617a00-0343-11eb-930f-441bf55b97ba.png)
<br />

- 2019/11/15 - 2019/11/19 format:
[Game Date, Game Time, Matchup, Team, Player Name, Reason, Current Status, Previous Status]
![3](https://user-images.githubusercontent.com/70581662/94700184-de2b3d80-0343-11eb-82d5-0648546caaf8.png)
<br />

- 2019/11/20 - 2019/12/16 format:
[Game Date, Game Time, Matchup, Team, Player Name, Current Status, Reason, Previous Status]
![4](https://user-images.githubusercontent.com/70581662/94700194-dff50100-0343-11eb-9675-e91a93e5a448.png)
<br />

- 2019/12/18 - Today format:
[Game Date, Game Time, Matchup, Team, Player Name, Current Status, Reason]
![5](https://user-images.githubusercontent.com/70581662/94700208-e1bec480-0343-11eb-9113-078d5725c992.png)
<br />

2. Due to the fact we were converting from a pdf file to a pandas dataframe, the conversion is not done properly and not everything is in the right place. We fixed the problem by shifting rows to the right according to the right pattern.
At this stage, the dataframe looks like this:
![full](https://user-images.githubusercontent.com/70581662/94701872-cfde2100-0345-11eb-890f-ef5bc2ce1c27.png)
<br />

As you can see, every cell is located in the right column. The next step is to fill the NAs, to clean the data (team name, date & time and more) and to decide about one identical pattern that will guide us in every data we will scrape.

After the cleaning process, our injury report is well organized:

![nba report](https://user-images.githubusercontent.com/75788772/101799752-32595780-3b15-11eb-9e6f-d10e59370090.PNG)


