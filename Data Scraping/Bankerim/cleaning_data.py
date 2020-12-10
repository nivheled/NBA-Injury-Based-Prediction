import pandas as pd


def cleaning_and_processing(df):
    
    team_names_dict = {"יוטה ג'אז" : "Utah Jazz","ניו אורלינס פליקאנס" : "New Orleans Pelicans", "דנבר נאגטס" : "Denver Nuggets",
                  "יוסטון רוקטס" : "Houston Rockets", "מילווקי באקס" : "Milwaukee Bucks", "בוסטון סלטיקס" : "Boston Celtics",
                  "גולדן סטייט ווריורס" : "Golden State Warriors", "פילדלפיה 76" : "Philadelphia 76ers", "דטרויט פיסטונס" : "Detroit Pistons",
                  "ברוקלין נטס" : "Brooklyn Nets", "טורונטו ראפטורס" : "Toronto Raptors", "אטלנטה הוקס" : "Atlanta Hawks",
                  "סקרמנטו קינגס" : "Sacramento Kings", "ממפיס גריזליס" : "Memphis Grizzlies", "לוס אנג'לס קליפרס" : "LA Clippers",
                  "לוס אנג'לס לייקרס" : "Los Angeles Lakers", "שארלוט הורנטס" : "Charlotte Hornets", "פורטלנד טרייל בלייזרס" : "Portland Trail Blazers",
                  "פיניקס סאנס" : "Phoenix Suns", "אורלנדו מג'יק" : "Orlando Magic", "מינסוטה טימברוולבס" : "Minnesota Timberwolves",
                  "דאלאס מאבריקס" : "Dallas Mavericks", "סאן אנטוניו ספרס" : "San Antonio Spurs", "אינדיאנה פייסרס" : "Indiana Pacers",
                  "שיקגו בולס" : "Chicago Bulls", "מיאמי היט" : "Miami Heat", "אוקלהומה סיטי ת'אנדר" : "Oklahoma City Thunder",
                  "וושינגטון וויזארדס" : "Washington Wizards", "קליבלנד קבלירס" : "Cleveland Cavaliers", "ניו יורק ניקס" : "New York Knicks"}
    
    df = df.dropna()
    
    df['home'] = df['teams'].apply(lambda x: min(x.partition("(")[0][:-1],x.partition("-")[0][:-2]))
    df['home'] = df['home'].astype('category')
    df['home'] = df['home'].apply(lambda x:team_names_dict[x])
    
    df['guest'] = df['teams'].apply(lambda x:x.partition("-")[2][1:].partition("(")[0][:-1])
    df['guest'] = df['guest'].astype('category')
    df['guest'] = df['guest'].apply(lambda x:team_names_dict[x])
    
    df['date and time'] = df['time and date'].apply(lambda x:datetime.datetime.strptime(x, '%H:%M %d.%m.%Y'))
    
    ##
    df['line change date and hour'] = df['date'] + ' ' +  df['hour']
    df['line change date and hour'] = df['line change date and hour'].apply(lambda x:datetime.datetime.strptime(x,'%d/%m/%Y %H:%M'))
    ##
    df['home_score'] = df['final_score'].apply(lambda x:int(x.partition("-")[0][:-1]))
    df['guest_score'] = df['final_score'].apply(lambda x:int(x.partition("-")[2][:]))
    
    df['winner_temp'] = df['home_score'] - df['guest_score'] + df['advantage']
    df.loc[df['winner_temp'] > 0 , 'winner'] = 1 
    df.loc[df['winner_temp'] == 0, 'winner'] = 'X'
    df.loc[df['winner_temp'] < 0 , 'winner'] = 2


    del df['teams']
    del df['time and date']
    del df['final_score']
    del df['bet_home']
    del df['bet_x']
    del df['bet_guest']
    del df['winner_temp']
    
    df = df[['date and time','home','guest','home_score','guest_score','line change date and hour','1','X','2','advantage','winner']]
    
    return df


df1 = pd.read_csv("C:/Users/97254/Desktop/winner project/2018-19 season.csv")

full_df = cleaning_and_processing(df1)  

full_df.to_csv("C:/Users/97254/Desktop/winner project/2018-19 season_clean_data.csv",index = 0)  