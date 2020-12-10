import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import datetime


def days_between(d1, d2):
    """
    function that calculate the difference between two dates
    :param d1: string - string the. format: ("%Y-%m-%d")
    :param d2: string - string the. format: ("%Y-%m-%d")
    :return: int - difference between two dates
    """       
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()
    return abs((d2 - d1).days)

def find_divs_display(driver,length,div_num,wait):
    """
    function that find the right div number for the games display in the page. also call
    to click_games
    :param driver: selenium.webdriver.chrome.webdriver.WebDriver - the driver object
    :param length: int - the number od div nubmer we are checking 
    :param wait: selenium.webdriver.support.wait.WebDriverWait - the wait driver object
    :return: int - the right div number 
    """
    if(div_num == -1):
        for num in range(length):
            xpath = "//*[@id='winnerLinePage']/div[1]/div[1]/div[1]/section[2]/div[" + str(num)+"]/div/div/div"
            # just for find exluded time.sleep()
            games = wait.until(EC.invisibility_of_element_located((By.XPATH,"xpath")))
            games = driver.find_elements_by_xpath(xpath)
            x = click_games(driver,games)
            if(x == True):
                div_num = num
                break
    else:
        xpath = "//*[@id='winnerLinePage']/div[1]/div[1]/div[1]/section[2]/div[" + str(div_num)+"]/div/div/div"
        # just for find exluded time.sleep()
        games = wait.until(EC.invisibility_of_element_located((By.XPATH,"xpath")))
        games = driver.find_elements_by_xpath(xpath)
        click_games(driver,games)
    return div_num
    
def click_games(driver,games):
    """
    function that chcek which game display on the page in click it
    :param driver: selenium.webdriver.chrome.webdriver.WebDriver - the driver object
    :param games: list - the list of games wh check 
    :return: bool - if find at least one game that display on the page 
    """
    boolean = False
    for game in games:
        if(game.is_displayed()):
            boolean = True
            time.sleep(1)
            game.click()
            time.sleep(2)
    return boolean

def extacrct_lines_change_table_to_df(game_info):
    """
    function extract the important data from a div of a game 
    :param game_info: bs4.element.Tag - the div game_info of a game included table of lines change 
    :return team_name0: str - the name of the home team
    :return team_nameq: str - the name of the home team
    :return: data frame - table with the lines change
    """    
    missing_change_line = False # this mean the no team has plus and the line in this game didn't change

    team_name = game_info.find('span', class_ = 'teamText').text
    team_name = team_name.partition(" לדף")[0][1:]

    table = game_info.find('table',{ 'class' : 'kode-table kode-table-v3 smaller','data-has-x' : "1"})
    
    if(table is None):
        table = game_info.find('table',{ 'class' : 'kode-table kode-table-v3','data-has-x' : "1"})
        missing_change_line = True
        
    tables_rows = table.find_all('tr')
    lst = []
    
    for tr in tables_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        lst.append(row)

    if(missing_change_line == True):
        lst = lst.append(np.NaN)
        
    df = pd.DataFrame(lst, columns=["date", "hour", '1','X','2','advantage'])
    df = df.iloc[1:]

    return team_name,df


def extacrct_game_to_df(div):
    """
    function extract the important data from a div of a game 
    :param div: bs4.element.Tag - the div of a game 
    :return: data frame - the data frame with the important varileble 
    """    
    spans = div.find_all('span')
    df = pd.DataFrame()
    
    df['time and date'] = [str(spans[3])[40:56]]
    df['teams'] = [spans[4].text]
    df['bet_home'] = [spans[6].text]
    df['bet_x'] = [spans[9].text]
    df['bet_guest'] = [spans[12].text]
    df['final_score'] = [spans[15].text]
    return df  

def is_contain_game(df,game_check):
    """
    function that check if game is already in the data frame
    :param df: data frame - the data frame with all the games 
    :param game_check: str - the teams play in the game
    :return: data frame - table with the lines change
    :return: boolean - if the data frame contain the game
    """       
    is_conain = False
    games = df['teams'].tolist()
    for game in games:
        if(type(game) is str):
            if(game_check in game):
                is_conain = True
    return is_conain

def fill_NaN_cells(df):
    """
    function that fill in the NaN values
    :param df: data frame - the data all records of a game 
    :return: data frame - data frame witout NaN values
    """       
    for index in range(6):
        df.iloc[1:,index] = df.iloc[0,index]
    df = df.iloc[1:]
    return df 

def extarct_df_for_day(page_source):
    """
    function that get a page source html code in return data frame of all games and 
    the useful details on the games
    :param page_source: str - string of the html code
    :return: data frame - the data frame with all the games 
    """
    
    # parser the html code using xlml parser
    soup = BeautifulSoup(page_source,'lxml')
    
    df = pd.DataFrame()
    df['time and date'] = np.NaN
    df['teams'] = np.NaN
    df['bet_home'] = np.NaN
    df['bet_x'] = np.NaN
    df['bet_guest'] = np.NaN
    df['final_score'] = np.NaN
    df['date'] = np.NaN
    df['hour'] = np.NaN
    df['1'] = np.NaN
    df['X'] = np.NaN
    df['2'] = np.NaN
    df['advantage'] = np.NaN
    
    # dict with the games in their lines change table 
    games_info = soup.find_all('div',class_ = 'game-info')
    dic = {}
    for game_info in games_info:
        teams_names_and_lines = extacrct_lines_change_table_to_df(game_info)
        dic[teams_names_and_lines[0]] = teams_names_and_lines[1]

    # find all games from the soup object
    game_a_filtered = soup.find_all('div',class_ = 'game is-father colorA disableBtns closedEvent hasExtraData open filtered-round')
    game_b_filtered = soup.find_all('div', class_ = 'game is-father colorB disableBtns closedEvent hasExtraData open filtered-round')
    game_a_open = soup.find_all('div',class_ = 'game is-father colorA disableBtns closedEvent hasExtraData open')
    game_b_open = soup.find_all('div', class_ = 'game is-father colorB disableBtns closedEvent hasExtraData open')
   
    # add games to the data frame
    for game in (game_a_filtered):
        df1 = extacrct_game_to_df(game)
        home_team = df1.iloc[0,1]
        if(is_contain_game(df,home_team)):
            continue
        home_team = min(home_team.partition("(")[0][:-1],home_team.partition("-")[0][:-2])
        df1 = df1.append(dic[home_team])
        df1 = fill_NaN_cells(df1)
        df = df.append(df1)
        
    for game in (game_b_filtered):
        df1 = extacrct_game_to_df(game)
        home_team = df1.iloc[0,1]
        if(is_contain_game(df,home_team)):
            continue
        home_team = min(home_team.partition("(")[0][:-1],home_team.partition("-")[0][:-2])
        df1 = df1.append(dic[home_team])
        df1 = fill_NaN_cells(df1)
        df = df.append(df1)
        
    for game in (game_a_open):
        df1 = extacrct_game_to_df(game)
        home_team = df1.iloc[0,1]
        if(is_contain_game(df,home_team)):
            continue
        home_team = min(home_team.partition("(")[0][:-1],home_team.partition("-")[0][:-2])
        df1 = df1.append(dic[home_team])
        df1 = fill_NaN_cells(df1)
        df = df.append(df1)
        
    for game in (game_b_open):
        df1 = extacrct_game_to_df(game)
        home_team = df1.iloc[0,1]
        if(is_contain_game(df,home_team)):
            continue
        home_team = min(home_team.partition("(")[0][:-1],home_team.partition("-")[0][:-2])
        df1 = df1.append(dic[home_team])
        df1 = fill_NaN_cells(df1)
        df = df.append(df1)
              
    return df         

def full_data_frame_extract(webdriver_path,base_url,start_date,end_date,folder_path):
    """
    function that return the full data frame with the all nba games between two dates. also 
    save csc for each date
    :param webdriver_path: str - the path of the webdriver location
    :param base_url: str - the url adress
    :param start_date: str - the strat date, fromat: ("%Y-%m-%d")
    :param end_date: str -  the end date, fromat: ("%Y-%m-%d")
    :param folder_path: str - the folder path rhat the csv for each day will save
    :return: data frame - the data frame with all the games and the important variables 
    """

    driver = webdriver.Chrome(webdriver_path)
    wait = WebDriverWait(driver,15)
    
    # define full data frame
    full_df = pd.DataFrame()
    full_df['time and date'] = np.NaN
    full_df['teams'] = np.NaN
    full_df['bet_home'] = np.NaN
    full_df['bet_x'] = np.NaN
    full_df['bet_guest'] = np.NaN
    full_df['final_score'] = np.NaN
    full_df['date'] = np.NaN
    full_df['hour'] = np.NaN
    full_df['1'] = np.NaN
    full_df['X'] = np.NaN
    full_df['2'] = np.NaN
    full_df['advantage'] = np.NaN
    
    days_num = days_between(start_date,end_date) + 1

    for days in range(days_num):
        print("")
        print("Date: ",start_date)
       
        url = base_url + start_date
        driver.get(url)
        
        time.sleep(2)
        
        is_nba = False
        # just for find exluded time.sleep()
        tochnia_element = wait.until(EC.invisibility_of_element_located((By.XPATH,"//select[@class='leagueFilter selectpicker']")))    
        tochnia_element = driver.find_element_by_xpath("//select[@class='leagueFilter selectpicker']")
        time.sleep(0.5)
        # just for find exluded time.sleep()
        tochnia_all_options = wait.until(EC.visibility_of_element_located((By.TAG_NAME,"option")))
        tochnia_all_options = tochnia_element.find_elements_by_tag_name("option")

        for option in tochnia_all_options:
            if(option.get_attribute("value") == 'NBA'):
                option.click()
                is_nba = True
                print("There are NBA games in this day!!") 
                break
        if(is_nba == False):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            start_date = str(start_date + datetime.timedelta(days=1))
            print("There aren't NBA games in this day :(")
            continue
            
        tochnia_element = wait.until(EC.invisibility_of_element_located((By.XPATH,"//select[@class='roundFilter selectpicker']")))
        #tochnia_element = driver.find_element_by_xpath("//select[@class='roundFilter selectpicker']")

        # just for find exluded time.sleep()
        tochnia_all_options = wait.until(EC.visibility_of_element_located((By.TAG_NAME,"option")))    
        tochnia_all_options = tochnia_element.find_elements_by_tag_name("option")

        div_num = -1
        for option in tochnia_all_options:
            if(option.get_attribute("value") == ""):
                continue
            option.click()

            # just for find exluded time.sleep()
            length = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='winnerLinePage']/div[1]/div[1]/div[1]/section[2]/div")))
            length = len(driver.find_elements_by_xpath("//*[@id='winnerLinePage']/div[1]/div[1]/div[1]/section[2]/div"))
            div_num = find_divs_display(driver,length,div_num,wait)

        time.sleep(2)

        content = driver.page_source
        df = extarct_df_for_day(content)
        path = folder_path + 'NBA games on ' + start_date +'.csv'
        df.to_csv(path, index = False)
        print("NBA games on", start_date , "saved")
        full_df = full_df.append(df)
        
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        start_date = str(start_date + datetime.timedelta(days=1))

    driver.quit()
    return full_df

# main

webdriver_path = "C:/Users/97254/Downloads/chromedriver/chromedriver"
base_url = 'https://www.bankerim.co.il/%D7%9E%D7%A9%D7%97%D7%A7%D7%99%D7%9D/%D7%9E%D7%A9%D7%97%D7%A7%D7%99-%D7%95%D7%95%D7%99%D7%A0%D7%A8-%D7%9C%D7%99%D7%99%D7%9F.html?date='
start_date = '2018-10-16'
end_date = '2019-04-12'
folder_path = "C:/Users/97254/Desktop/winner project/2018-19 games/"

df = full_data_frame_extract(webdriver_path,base_url,start_date,end_date,folder_path)
df.to_csv("C:/Users/97254/Desktop/winner project/2018-19 season.csv", index = False)






# full data frame
start_date = '2018-10-18'
end_date = '2019-04-12'
days_num = days_between(start_date,end_date)

full_df = pd.read_csv("C:/Users/97254\Desktop/winner project/2018-19 games/NBA games on 2018-10-17.csv",index_col=0)
path = "C:/Users/97254\Desktop/winner project/2018-19 games/NBA games on "
for day in range(days_num):
    #print("Date: ",start_date)
    url = path + start_date + ".csv"
    try: 
        df = pd.read_csv(url,index_col=0)
        full_df = full_df.append(df)
    except:
        print(start_date)
        
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    start_date = str(start_date + datetime.timedelta(days=1))
    
full_df.to_csv("C:/Users/97254/Desktop/winner project/2018-19 season.csv", index = False)    


from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

print(pysqldf("select teams from full_df group by teams "))

