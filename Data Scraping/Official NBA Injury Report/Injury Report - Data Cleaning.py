import pandas as pd
import os
import numpy as np


team_dic = {"ATL":"Atlanta Hawks",
"BOS":"Boston Celtics",
"BKN":"Brooklyn Nets",
"CHA":"Charlotte Hornets",
"CHI":"Chicago Bulls",
"CLE":"Cleveland Cavaliers",
"DAL":"Dallas Mavericks",
"DEN":"Denver Nuggets",
"DET":"Detroit Pistons",
"GSW":"Golden State Warriors",
"HOU":"Houston Rockets",
"IND":"Indiana Pacers",
"LAC":"LA Clippers",
"LAL":"Los Angeles Lakers",
"MEM":"Memphis Grizzlies",
"MIA":"Miami Heat",
"MIL":"Milwaukee Bucks",
"MIN":"Minnesota Timberwolves",
"NOP":"New Orleans Pelicans",
"NYK":"New York Knicks",
"OKC":"Oklahoma City Thunder",
"ORL":"Orlando Magic",
"PHY":"Philadelphia 76ers",
"PHX":"Phoenix Suns",
"POR":"Portland Trail Blazers",
"SAC":"Sacramento Kings",
"SAS":"San Antonio Spurs",
"MIN":"Timberwolves",
"TOR":"Toronto Raptors",
"UTA":"Utah Jazz",
"WAS":"Washington Wizards"
}



def split_matchup_to_teams(df):
    #report.insert(3,'Home Team',np.nan)
    #report.insert(4,'Away Team',np.nan)
    df['Home_Team'] = df['Matchup'].str.slice(0,3)
    df['Away_Team'] = df['Matchup'].str.slice(4,7)
    df.drop(columns=['Matchup'])
    df = df[['Game Date', 'Game Time', 'Home_Team', 'Away_Team', 'Team','Player Name',"Current Status", "Reason", "Category", "Previous Status", "Date injury Report", "Time injury Report" ]]
    return df

def remove_ET(df,column):
    df[column] = df[column].str.slice(0,5)
    return df

def team_full_names(df):
    for row in range(len(df)):
        df.iloc[row]["Home_Team"] = team_dic.get(df.iloc[row]["Home_Team"])
        df.iloc[row]["Away_Team"] = team_dic.get(df.iloc[row]["Away_Team"])
    return df

def reorder_player_name(df):
    for row in range(len(df)):
        if (type(df.iloc[row]['Player Name'])==str):
                    comma = df.iloc[row]['Player Name'].find(",")
                    first_name = str(df.iloc[row]['Player Name'][comma+2:])
                    df.iloc[row]['Player Name'] = df.iloc[row]['Player Name'].replace(", " +first_name,"")
                    df.iloc[row]['Player Name'] = first_name + " " + df.iloc[row]['Player Name']
    return df

def convert_to_right_type(df):
    df['Date injury Report'] = pd.to_datetime(df['Date injury Report'],format = '%Y/%m/%d')
    df['Date injury Report'] = df['Date injury Report'].dt.date
    df['Game Date'] = pd.to_datetime(df['Game Date'],format = '%m/%d/%Y')
    df['Game Date'] = df['Game Date'].dt.date
    
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "01","13" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "02","14" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "03","15" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "04","16" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "05","17" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "06","18" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "07","19" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "08","20" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "09","21" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "10","22" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "11","23" + df['Game Time'].str.slice(2,),df["Game Time"])
    df['Game Time'] = np.where(df['Game Time'].str.slice(0,2) == "12","00" + df['Game Time'].str.slice(2,),df["Game Time"])
       
    df['Game Time'] = pd.to_datetime(df['Game Time'],format = "%H:%M").dt.time
    df['Time injury Report'] = np.where(df['Time injury Report'].str.slice(0,2) == "05","17",df["Time injury Report"])
    df['Time injury Report'] = np.where(df['Time injury Report'].str.slice(0,2) == "02","14",df["Time injury Report"])
    df['Time injury Report'] = np.where(df['Time injury Report'].str.slice(0,2) == "11","11",df["Time injury Report"])
       
    df['Time injury Report'] = df['Time injury Report'] + ":00"
    df['Time injury Report'] = pd.to_datetime(df['Time injury Report'],format = "%H:%M").dt.time
    return df


def combine_dt(df):
    df.insert(0,"Game DT",np.nan)
    df.insert(11,"Report DT",np.nan)
    
    df["Game DT"] = df.apply(lambda r : pd.datetime.combine(r['Game Date'],r['Game Time']),1)
    df["Report DT"] = df.apply(lambda r : pd.datetime.combine(r['Date injury Report'],r['Time injury Report']),1)    
    return df


def organize_all(df):
    df = split_matchup_to_teams(df)
    df = remove_ET(df, "Game Time")
    df = team_full_names(df)
    df = reorder_player_name(df)
    df = convert_to_right_type(df)
    return df


# main 
full_report =  pd.read_csv("../NBA full injury report.csv")
full_report = organize_all(full_report)
full_report = combine_dt(full_report)
