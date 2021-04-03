#connects python code to the database
import sqlite3
from datetime import datetime
import os.path

#create absolute path file for connecting database without error
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'TweetStockScoresdb.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()


def dbConnect(scoreList): 
    runOnce = 0 
    date = datetime.today().strftime('%Y-%m-%d')

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
        
        #insert average tweet sentiment score into db table 'Scores'
        cur.execute('''INSERT OR REPLACE INTO Scores (score, stock_id, date_id)
        VALUES( ?, ?, ?)''',(score['score'], stock_id, date_id  ) )
    
        conn.commit()
       
        #selects the score of the stock and prints stock name and score
        cur.execute('SELECT stock_id FROM Stocks WHERE ticker = ? ', (score['stock'], ))
        stock_id = cur.fetchone()[0]

        #select current date_id
        cur.execute('SELECT date_id FROM Dates WHERE score_date = ? ', (date, ))
        date_id = cur.fetchone()[0]

        #select current dbscore
        cur.execute('SELECT score FROM Scores WHERE date_id = ? AND stock_id = ?', (date_id, stock_id))
        dbscore = cur.fetchone()[0]
        
        print(score['stock'], dbscore)
        
        try:
            #queries list of date IDs then selects second to last date ID for comparison to previous score at the last run-date
            allDates = [date_id[0] for date_id in cur.execute('SELECT date_id FROM Dates')]
            prevDate = allDates[-2]
            
            cur.execute('SELECT score FROM Scores WHERE date_id = ? AND stock_id = ?', (prevDate, stock_id))
            prevdbScore = cur.fetchone()[0]
        
            #calculate percentage change from previous score date
            if prevdbScore == 0:
                pchange = abs((dbscore - prevdbScore)/1)
            else:
                pchange = abs((dbscore - prevdbScore)/prevdbScore)
            
            #accounts for negative number to grater negative number
            if prevdbScore > dbscore:
                pchange = pchange*-1
            pchange = "{:.2%}".format(pchange)
            print (pchange)
        except: 
            continue
        
        print('\n')
       