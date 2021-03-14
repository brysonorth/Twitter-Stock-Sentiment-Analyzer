#connects python code to the database
import sqlite3
from datetime import datetime
import os.path

#create absolute path file for connecting database without error
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'TweetSentScoresdb.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

#stockList = ['$MA', 'TCEHY', 'GME', 'ICLN']
#scoreList = [{'stock':'$NVDA', 'score': '0.888'}, {'stock':'$AAPL', 'score':'-0.444'},
#{'stock':'$NFLX', 'score':'0.777'}]#, {'stock':'ICLN', 'score':'-4.05', 'date':date}]

def dbConnect(scoreList): 
    runOnce = 0 
    #date = datetime.today().strftime('%Y-%m-%d')
    date = '2021-03-25'
    
    #block connects to sqlite and inserts new stocks, scores and dates into into the tables, ignores if already in db
    for score in scoreList:
        cur.execute('''INSERT OR IGNORE INTO Stocks (ticker)
            VALUES( ? )''',(score['stock'], ) )
        cur.execute('SELECT stock_id FROM Stocks WHERE ticker = ? ', (score['stock'], ))
        stock_id = cur.fetchone()[0]

        # only inserts a single date into table for each run of the program. allows table to increment date _id by 1 
        if runOnce == 0:  
            cur.execute('''INSERT OR IGNORE INTO Dates (score_date)
                VALUES( ? )''',(date, ) )
            runOnce = 1 
        cur.execute('SELECT date_id FROM Dates WHERE score_date = ? ',( date, ))
        date_id = cur.fetchone()[0]
        cur.execute('''INSERT OR REPLACE INTO Scores (score, stock_id, date_id)
        VALUES( ?, ?, ?)''',(score['score'], stock_id, date_id  ) )
        # print(cur.fetchone())
        conn.commit()
        #selects the score of the stock and prints stock name and score
        cur.execute('SELECT stock_id FROM Stocks WHERE ticker = ? ', (score['stock'], ))
        stock_id = cur.fetchone()[0]

        cur.execute('SELECT date_id FROM Dates WHERE score_date = ? ', (date, ))
        date_id = cur.fetchone()[0]

        cur.execute('SELECT score FROM Scores WHERE date_id = ? AND stock_id = ?', (date_id, stock_id))
        dbscore = cur.fetchone()[0]
        #prevDate = date_id - 1
        prevDate = 5
        cur.execute('SELECT score FROM Scores WHERE date_id = ? AND stock_id = ?', (prevDate, stock_id))
        prevdbScore = cur.fetchone()[0]
        
        #calculate percentage change from previous score date
        pchange = (dbscore - prevdbScore)/prevdbScore
        pchange = "{:.2%}".format(pchange)
       
        print(score['stock'], dbscore, pchange)
       