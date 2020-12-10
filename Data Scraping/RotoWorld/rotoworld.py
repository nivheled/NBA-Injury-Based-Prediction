import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def report_to_df(report):
    """
    a function that extracts the data from a article of a report 
    :param div: bs4.element.Tag - the article of a report
    :return: data frame - the data frame with the variables 
    """    
    
    date_time = report.find('div',class_ = 'player-news-article__timestamp').text
    player_name_position_team = report.find('div',class_ = 'player-news-article__profile')
    player_name = player_name_position_team.find('span',class_ = 'player-news-article__profile__name').text
    position_and_team = player_name_position_team.find('span','player-news-article__profile__position').text
    title = report.find('div',class_ = 'player-news-article__title').text
    social_headline = report.find('div', class_ = 'social-share__headline').text
    
    summary = report.find('div',class_ = 'player-news-article__summary')
    if(summary is not None):
        summary = summary.text
    else:
        summary = np.NaN
        
    source = report.find('a',class_ = 'source-title')
    if(source is not None):
        source = source.text
    else:
        players_related = np.NaN
        
    players_related = report.find('div',class_ = 'player-news-article__related')
    if(players_related is not None):
        players_related = players_related.text
    else:
        players_related = np.NaN
        

    df = pd.DataFrame()
    df['date_time'] = [date_time]
    df['player'] = [player_name]
    df['position_and_team'] = [position_and_team]
    df['title'] = [title]
    df['summary'] = [summary]
    df['social_headline'] = [social_headline]
    df['players_related'] = [players_related]
    df['source'] = [source]

    return df


def source_code_to_df(content):
    """
    a function that gets a page source HTML code and returns a data frame of reports 
    in this page
    :param content: str - string of the HTML code
    :return: data frame - the data frame with all the reports 
    """

    soup = BeautifulSoup(content,'lxml')
    reports = soup.find_all('article',class_ = 'player-news-article repeated-rw_player_news--player-news-page')

    full_df = pd.DataFrame()
    full_df['date_time'] = np.NaN
    full_df['player'] = np.NaN
    full_df['position_and_team'] = np.NaN
    full_df['title'] = np.NaN
    full_df['summary'] = np.NaN
    full_df['social_headline'] = np.NaN
    full_df['players_related'] = np.NaN
    full_df['source'] = np.NaN


    for report in reports:
        df = report_to_df(report)
        full_df = full_df.append(df)

    return full_df


def full_data_frame_extract(webdriver_path,base_url,numbers,folder_path):
    """
    a function that returns the full dataframe with all NBA injuries reports
    :param webdriver_path: str - the path of the webdriver location
    :param numbers: int - the numbers of pages we want to extract
    :param folder_path: str - the folder path that the CSV for every 10000 reports will save
    :return: data frame - the data frame with all NBA injuries reports
    """

    driver = webdriver.Chrome(webdriver_path)
    wait = WebDriverWait(driver,15)
    driver.get(base_url)
    

    Df = pd.DataFrame()
    Df['date_time'] = np.NaN
    Df['player'] = np.NaN
    Df['position_and_team'] = np.NaN
    Df['title'] = np.NaN
    Df['summary'] = np.NaN
    Df['social_headline'] = np.NaN
    Df['players_related'] = np.NaN
    Df['source'] = np.NaN
    
    
    
    for num in range(1,numbers+1):
        wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='player-news-page-wrapper']/div/div/div[3]/ul/li[1]/article/div[1]")))
        content = driver.page_source
        full_df = source_code_to_df(content)
        Df = Df.append(full_df)
        
        click_next = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='player-news-page-wrapper']/div/div/div[2]/a[2]")))
        click_next.click()
        
        if(num%1000 == 0):
            path = folder_path + 'injuries' + str(num/1000) +'.csv'
            Df.to_csv(path, index = False)
            print("number of reports is:", num)
            
    driver.quit()
    return Df


#main



