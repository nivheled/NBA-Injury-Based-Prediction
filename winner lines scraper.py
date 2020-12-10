import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import time

url = 'https://www.winner.co.il/mainbook/sport-%D7%9B%D7%93%D7%95%D7%A8%D7%A1%D7%9C/ep-%D7%90%D7%A8%D7%A6%D7%95%D7%AA-%D7%94%D7%91%D7%A8%D7%99%D7%AA/ep-%D7%A4%D7%9C%D7%99%D7%99%D7%90%D7%95%D7%A3---NBA'
try:
    page = urllib.request.urlopen(url)
except:
    print('An error occured.')
soup = BeautifulSoup(page,'lxml')


def extarct_games_to_df(soup):
    """
    function extract winner games and lines to data frame 
    :param soup: bs4.BeautifulSoup - soup of a page
    :return: data frame - data frame with NBA winner games and lines 
    """   
    
    teams = {"יוטה ג'אז" : "Utah Jazz","ניו אורלינס פליקאנס" : "New Orleans Pelicans", "דנבר נאגטס" : "Denver Nuggets",
                  "יוסטון רוקטס" : "Houston Rockets", "מילווקי באקס" : "Milwaukee Bucks", "בוסטון סלטיקס" : "Boston Celtics",
                  "גולדן סטייט ווריורס" : "Golden State Warriors", "פילדלפיה 76" : "Philadelphia 76ers", "דטרויט פיסטונס" : "Detroit Pistons",
                  "ברוקלין נטס" : "Brooklyn Nets", "טורונטו ראפטורס" : "Toronto Raptors", "אטלנטה הוקס" : "Atlanta Hawks",
                  "סקרמנטו קינגס" : "Sacramento Kings", "ממפיס גריזליס" : "Memphis Grizzlies", "לוס אנג'לס קליפרס" : "LA Clippers",
                  "לוס אנג'לס לייקרס" : "Los Angeles Lakers", "שארלוט הורנטס" : "Charlotte Hornets", "פורטלנד טרייל בלייזרס" : "Portland Trail Blazers",
                  "פיניקס סאנס" : "Phoenix Suns", "אורלנדו מג'יק" : "Orlando Magic", "מינסוטה טימברוולבס" : "Minnesota Timberwolves",
                  "דאלאס מאבריקס" : "Dallas Mavericks", "סאן אנטוניו ספרס" : "San Antonio Spurs", "אינדיאנה פייסרס" : "Indiana Pacers",
                  "שיקגו בולס" : "Chicago Bulls", "מיאמי היט" : "Miami Heat", "אוקלהומה סיטי ת'אנדר" : "Oklahoma City Thunder",
                  "וושינגטון וויזארדס" : "Washington Wizards", "קליבלנד קבלירס" : "Cleveland Cavaliers", "ניו יורק ניקס" : "New York Knicks"}
    
    games = soup.find_all('div', attrs = {'class': 'event-content sport_BASK'})
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    for game in games:
        home_team = game.find_all('span',{'class' :"name ellipsis outcomedescription"})[0].text.partition(" (")[0]
        if home_team not in teams:
            continue
        else:
            home_team = teams[home_team]
        guest_team = game.find_all('span',{'class' :"name ellipsis outcomedescription"})[2].text.partition(" (")[0]
        guest_team = teams[guest_team]
        game_time = game.find('td',{'class' :"time_date"}).text
        lines = game.find_all('span',{'class' :"formatted_price"})
        home_line = lines[0].text
        x_line = lines[1].text
        guest_line = lines[2].text
        sign = game.find_all('span',{'class' :"name ellipsis outcomedescription"})[0].text[-2]
        advantage = int(game.find_all('span',{'class' :"name ellipsis outcomedescription"})[0].text[-4] + sign)

        df1['game_time'] = [game_time]
        df1['chcek_time'] = time.strftime("%H:%M")
        df1['home'] = [home_team]
        df1['guest'] = [guest_team]
        df1['1'] = [home_line]
        df1['X'] = [x_line]
        df1['2'] = [guest_line]
        df1['advantage'] = [advantage]
        df = df.append(df1)
    return df
