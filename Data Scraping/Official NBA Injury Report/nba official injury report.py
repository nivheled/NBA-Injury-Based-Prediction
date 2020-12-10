import pandas as pd
import numpy as np
import tabula
import datetime
import requests
import re


#get the time out of string
def game_time_pattern(val):
    if "(ET)" in val:
        return True
    return False

#get teams from Matchup column
def matchup_pattern(val):
    if "@" in val:
        return True
    return False

#check if a cell belongs to the "player name" column
def player_name_pattern(val):
    if ", " in val:
        return True
    return False

#check if a cell belongs to the "Category" column
def category_pattern(val):
    categories = ["Injury/Illness", "Not With Team", "G League Team","G League - Two-Way","G League - On Assignment", "Personal Reasons",
                  "League Suspension","NOT YET SUBMITTED", "Coach's Decision", "Trade Pending", "Rest"]
    if val in categories:
        return True
    return False

#check if a cell belongs to the "Status" column
def reason_pattern(val):
    status = ["Out", "Doubtful", "Questionable", "Available", "Probable"]
    if val in status:
        return False
    return True

#check if a cell belongs to the "Team" column by building a list of all NBA teams
def teams_pattern(val):
    
    nba_teams = ["Atlanta Hawks",
    "Boston Celtics",
    "Brooklyn Nets",
    "Charlotte Hornets",
    "Chicago Bulls",
    "Cleveland Cavaliers",
    "Dallas Mavericks",
    "Denver Nuggets",
    "Detroit Pistons",
    "Golden State Warriors",
    "Houston Rockets",
    "Indiana Pacers",
    "LA Clippers",
    "Los Angeles Lakers",
    "Memphis Grizzlies",
    "Miami Heat",
    "Milwaukee Bucks",
    "New Orleans Pelicans",
    "New York Knicks",
    "Oklahoma City Thunder",
    "Orlando Magic",
    "Philadelphia 76ers",
    "Phoenix Suns",
    "Portland Trail Blazers",
    "Sacramento Kings",
    "San Antonio Spurs",
    "Toronto Raptors",
    "Utah Jazz",
    "Washington Wizards",
    "Minnesota "+
    "Timberwolves",
    "Minnesota\rTimberwolves"]

    if (val in nba_teams):
        return True
    return False


#check if a cell belongs to the "Current Status" column
def current_stat_pattern(val):
    status = ["Out", "Doubtful", "Questionable", "Available", "Probable"]
    if (val in status):
        return True
    return False

#a function that matches each column to it's pattern
def shift_by_pattern(cell, col): #function that check patterns
    
    pattern = None
    
    if col=="Game Date":
        date_pattern = "[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}"
        pattern = re.match(date_pattern,cell)
        
    if col=="Game Time":
        pattern = game_time_pattern(cell)
        
    if col=="Matchup":
        pattern = matchup_pattern(cell)
        
    if col=="Team":
        pattern = teams_pattern(cell)
        
    if col=="Player Name":
        pattern = player_name_pattern(cell)
        
    if col=="Category":
        pattern = category_pattern(cell)
        
    if col=="Reason":
        pattern = reason_pattern(cell)
        
    if col=="Current Status":
        pattern = current_stat_pattern(cell)
        
    return pattern



def move_cell_right(df):
    """
    a function that locating each variable in it's right cell using the patterns above
    :param df: data frame - Data frame fo NBA injury report
    :return: data frame - a fixed data frameof the NBA official injury report 
    """
    if (df.shape[1]==11|df.shape[1]==10):
        for row in range(df.shape[0]):
            for col in range(7):
                cell = df.iat[row,col]
                if (pd.isna(cell)==True or shift_by_pattern(cell, df.columns[col])):
                    continue
                else:
                    df.iloc[[row],col:]= df.iloc[[row],col:].shift(1, axis=1)
    else:
        for row in range(df.shape[0]):
            for col in range(6):
                cell = df.iat[row,col]
                if (pd.isna(cell)==True or shift_by_pattern(cell, df.columns[col])):
                    continue
                else:
                    df.iloc[[row],col:]= df.iloc[[row],col:].shift(1, axis=1)
    return df

def fill_na_with_above_value(df):
    """
    a function that fills Nan values with the appropriate value  
    :param df: data frame - Data frame fo the NBA injury report
    :return: data frame - Data frame of the NBA official injury report with values instead of Nan 
    """    
    for row in range (1,df.shape[0]):
        for col in range(4):
            cell = df.iat[row,col]
            if (pd.isna(cell)):
                df.iat[row,col] = df.iat[row-1,col]
    return df

def remove_if_not_submitted(df):
    """
    a function that remove rows with NOT YET SUBMITTED, which are not informative
    :param df: data frame - the data frame fo the NBA injury report
    :return: data frame - the data frame of the NBA official injury report without rows that contains NOT YET SUBMITTED values
    """     
    if (df.shape[1]==11):
        col_names = ['Game Date','Game Time','Matchup','Team','Player Name','Category','Reason',
                     'Current Status','Previous Status','Date injury Report','Time injury Report']
        if(list(df.columns) == col_names ):
            df = df[df['Category'] != 'NOT YET SUBMITTED']
        else:
            df = df[df['Reason'] != 'NOT YET SUBMITTED']
    else:
        df = df[df['Reason'] != 'NOT YET SUBMITTED']
    return df


def arrange_df(df):
    """
    a function that making all the relevant changes in the df to make it in the right format
    :param df: data frame - the data frame of the NBA injury report
    :return: data frame - The final and useful data frame of the NBA official injury report 
    """      
    df1 = df.iloc[:,:df.shape[1]-2]
    df2 = df.iloc[:,df.shape[1]-2:]    
    df1 = move_cell_right(df1)
    df1 = fill_na_with_above_value(df1)
    df = pd.concat([df1, df2], axis=1)
    df = remove_if_not_submitted(df)
    
    return df



def days_between(d1, d2):
    """
    a function that calculate the difference between two dates
    :param d1: string - string, format: ("%Y-%m-%d")
    :param d2: string - string, format: ("%Y-%m-%d")
    :return: int - the difference between the two dates
    """       
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()
    return abs((d2 - d1).days)


def extarct_official_injury_report(start_date,end_date):
    """
    a function that unifies all the different formats of the NBA official injuries reports between two dates
    and returns the full data frame.
    :param start_date: str - strat date, fromat: ("%Y-%m-%d")
    :param end_date: str -  end date, fromat: ("%Y-%m-%d")
    :return: data frame - the data frame with all the NBA official injuries reports 
    """
    
    # The NBA has 5 formars of reports over the years.
    """
    2018/12/17 - 2019/11/14 format is:
    [Game Date, Game Time, Matchup, Team, Player Name, Category, Reason, Current Status, Previous Status]
    """
    df_9col_1 = pd.DataFrame()

    """
    2019/12/17 format is:
    [Game Date, Game Time, Matchup, Team, Player Name, Current Status, Reason, Previous Status, Previous Reason]
    """
    df_9col_2 = pd.DataFrame()

    """
    2019/11/15 - 2019/11/19 format is:
    [Game Date, Game Time, Matchup, Team, Player Name, Reason, Current Status, Previous Status]
    """    
    df_8col_1 = pd.DataFrame()
    
    """
    2019/11/20 - 2019/12/16 format is:
    [Game Date, Game Time, Matchup, Team, Player Name, Current Status, Reason, Previous Status]
    """       
    df_8col_2 = pd.DataFrame()

    """
    2019/12/18 - Today format is:
    [Game Date, Game Time, Matchup, Team, Player Name, Current Status, Reason]
    """         
    df_7col = pd.DataFrame()

    
    df_9col_1_columns = ['Game Date','Game Time','Matchup','Team','Player Name','Category','Reason',
             'Current Status','Previous Status','Date injury Report','Time injury Report']
    df_8col_1_columns = ['Game Date','Game Time','Matchup','Team','Player Name','Reason','Current Status',
                   'Previous Status','Date injury Report','Time injury Report']
    
    base_url = "https://ak-static.cms.nba.com/referee/injury/Injury-Report_"
    days_num = days_between(start_date,end_date)+1

    for days in range(days_num):
        print("")
        print("Date: ",start_date)
        
        for hour in ("_11AM.pdf", "_02PM.pdf", "_05PM.pdf"):
            url = base_url + str(start_date) + hour 
            response = requests.get(url)
            
            if (str(response) != "<Response [200]>"):
                continue
                
            df_lst = tabula.read_pdf(url, pages="all")
            for df in df_lst:
                df['Date injury Report'] = start_date
                df['Time injury Report'] = hour[1:5]
                if(df.shape[1]==11):
                    if(list(df.columns) == df_9col_1_columns):
                        df_9col_1 = df_9col_1.append(df)
                    else:
                        df_9col_2 = df_9col_2.append(df)
                        
                elif(df.shape[1]==10):
                    if(list(df.columns) == df_8col_1_columns):
                        df_8col_1 = df_8col_1.append(df)
                    else:
                        df_8col_2 = df_8col_2.append(df)
                else:
                    df_7col = df_7col.append(df)
            print("The report is added")

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        start_date = str(start_date + datetime.timedelta(days=1))
        
    if(len(df_9col_1) != 0):
        df_9col_1 = arrange_df(df_9col_1)
        df_9col_1['Previous Reason'] = np.nan
        df_9col_1 = df_9col_1[["Game Date", "Game Time", "Matchup", "Team", "Player Name","Current Status",
                    "Reason", "Category", "Previous Status",'Previous Reason','Date injury Report','Time injury Report']]
        
    if(len(df_9col_2) != 0):  
        df_9col_2 = arrange_df(df_9col_2)
        df_9col_2['Category'] = np.nan
        df_9col_2 = df_9col_2[["Game Date", "Game Time", "Matchup", "Team", "Player Name","Current Status",
                    "Reason", "Category", "Previous Status",'Previous Reason','Date injury Report','Time injury Report']]
        
    if(len(df_8col_1) != 0):   
        df_8col_1 = arrange_df(df_8col_1)
        df_8col_1['Category'] = np.nan
        df_8col_1['Previous Reason'] = np.nan
        df_8col_1 = df_8col_1[["Game Date", "Game Time", "Matchup", "Team", "Player Name","Current Status",
                    "Reason", "Category", "Previous Status",'Previous Reason','Date injury Report','Time injury Report']]
        
    if(len(df_8col_2) != 0):    
        df_8col_2 = arrange_df(df_8col_2)
        df_8col_2['Category'] = np.nan
        df_8col_2['Previous Reason'] = np.nan
        df_8col_2 = df_8col_2[["Game Date", "Game Time", "Matchup", "Team", "Player Name","Current Status",
                    "Reason", "Category", "Previous Status",'Previous Reason','Date injury Report','Time injury Report']]
     
    if(len(df_7col) != 0):
        df_7col = arrange_df(df_7col)
        df_7col['Category'] = np.nan
        df_7col['Previous Status'] = np.nan
        df_7col['Previous Reason'] = np.nan
        df_7col = df_7col[["Game Date", "Game Time", "Matchup", "Team", "Player Name","Current Status",
                    "Reason", "Category", "Previous Status",'Previous Reason','Date injury Report','Time injury Report']]
    
    
    full_df = pd.DataFrame()
    full_df = full_df.append(df_9col_1)
    full_df = full_df.append(df_9col_2)
    full_df = full_df.append(df_8col_1)
    full_df = full_df.append(df_8col_2)
    full_df = full_df.append(df_7col)
                          
    return full_df

#main
start_date = '2018-12-17'
end_date = '2020-09-04'
df = extarct_official_injury_report(start_date,end_date)
