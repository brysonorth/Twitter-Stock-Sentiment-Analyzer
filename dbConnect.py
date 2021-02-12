#connects python code to the database
import sqlite3
from datetime import datetime
#import os.path
date = datetime.today().strftime('%Y-%m-%d')

conn = sqlite3.connect('c:/Users/fitcr/MyPythonScripts/TwitterStockAn/TweetScoredb.db')
cur = conn.cursor()

stockList = ['$MA', 'TCEHY', 'GME']
scoreList = [('$MA', 0.123), ('TCEHY', 0.267), ('GME', 0.982)]

for ticker in stockList:
    cur.execute('''INSERT OR IGNORE INTO Stocks (ticker)
        VALUES( ? )''',(ticker, ) )
     
    cur.execute('SELECT stock_id, ticker FROM Stocks WHERE ticker = ? ', (ticker, ))
    stock_id = cur.fetchone()[0]

    print(cur.fetchone())
    conn.commit()

