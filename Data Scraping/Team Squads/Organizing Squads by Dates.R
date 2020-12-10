library(data.table)
library(sqldf)

games <- fread(".../games.csv")
games_details <- fread(".../games_details.csv")


games <- games[,c('GAME_DATE_EST','GAME_ID')]
games_details <- games_details[,c('GAME_ID','TEAM_ABBREVIATION','PLAYER_NAME')]


games$GAME_DATE_EST <- as.Date(games$GAME_DATE_EST,format = "%Y- %m- %d")
games$GAME_DATE_EST <- as.numeric(games$GAME_DATE_EST)


#joining on games ID's

teams_players <- sqldf("select PLAYER_NAME as player,TEAM_ABBREVIATION as team,GAME_DATE_EST as date
      from games_details as gd join games as g on gd.GAME_ID = g.GAME_ID")


teams_players <- teams_players[order(teams_players$player, teams_players$date),]
teams_players$num <- NA

player <- teams_players[1,1]
team <- teams_players[1,2]
num<- 1


# Note that it is not recommended to use "for" loop in R dataframe due to poor runing time

for (row in 1:nrow(teams_players)){
  if(teams_players[row,1] == player){
    if(teams_players[row,2] == team){
      teams_players[row,4] <- num
    }
    else{
      num <- num + 1
      team <- teams_players[row,2]
      teams_players[row,4] <- num
    }
  }
  else{
    player <- teams_players[row,1]
    team <- teams_players[row,2]
    num <- 1
    teams_players[row,4] <- num
  }
}




teams_players <- sqldf("select player,team,min(date) as start_date,max(date) as end_date
                        from teams_players
                       group by player, num")


teams_players$start_date <- as.Date(teams_players$start_date ,origin ="1970-01-01")
teams_players$end_date <- as.Date(teams_players$end_date ,origin ="1970-01-01")


write.csv(teams_players,".../players_teams.csv", row.names = FALSE)
