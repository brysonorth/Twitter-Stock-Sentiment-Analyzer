#connects python code to the database
import sqlite3
from datetime import datetime
date = datetime.today().strftime('%Y-%m-%d')
runOnce = 0

conn = sqlite3.connect('c:/Users/fitcr/MyPythonScripts/TwitterStockAn/TweetScoredb.db')
cur = conn.cursor()

stockList = ['$MA', 'TCEHY', 'GME', 'ICLN']
scoreList = [{'stock':'$MA', 'score': '0.754', 'date': date}, {'stock':'TCEHY', 'score':'-0.279', 'date':date}, 
{'stock':'GME', 'score':'0.896', 'date':date}, {'stock':'ICLN', 'score':'-4.05', 'date':date}]

#funct to insert a single date into table for each run of the program. allows table to increment date _id by 1 
def dateIn(date):
        cur.execute('''INSERT OR IGNORE INTO Dates (score_date)
            VALUES( ? )''',(date, ) )

#block connects to sqlite and inserts new stocks, scores and dates into into the tables, ignores if already in db
for score in scoreList:
    cur.execute('''INSERT OR IGNORE INTO Stocks (ticker)
        VALUES( ? )''',(score['stock'], ) )
    cur.execute('SELECT stock_id FROM Stocks WHERE ticker = ? ', (score['stock'], ))
    stock_id = cur.fetchone()[0]
    
    if runOnce == 0:  
        dateIn(date)
        runOnce = 1 
    cur.execute('SELECT date_id FROM Dates WHERE score_date = ? ', (score['date'], ))
    date_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Scores (score, stock_id, date_id)
    VALUES( ?, ?, ?)''',(score['score'], stock_id, date_id  ) )

   # print(cur.fetchone())
    conn.commit()

    #selects the score of the stock and prints stock name and score
    cur.execute('SELECT stock_id FROM Stocks WHERE ticker = ? ', (score['stock'], ))
    stock_id = cur.fetchone()[0]
    
    cur.execute('SELECT date_id FROM Dates WHERE score_date = ? ', (score['date'], ))
    date_id = cur.fetchone()[0]
    
    cur.execute('SELECT score FROM Scores WHERE date_id = ? AND stock_id = ?', (date_id, stock_id))
    dbscore = cur.fetchone()[0]

    prevDate = date_id - 1
    cur.execute('SELECT score FROM Scores WHERE date_id = ? AND stock_id = ?', (prevDate, stock_id))
    prevdbScore = cur.fetchone()[0]

    #calculate percetnage change from previous score date
    pchange = (dbscore - prevdbScore)/prevdbScore
    pchange = "{:.2%}".format(pchange)
    #results = cur.fetchall()
    #print(results)

    print(score['stock'], dbscore, '% Change:' + pchange, 'Last:')


