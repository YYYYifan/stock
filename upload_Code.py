import json
import pymysql


with open("code.json") as f:
    config = json.load(f)
""" 
db = pymysql.connect(
    host='192.168.1.15',
    user='root',
    password='980326',
    database='codeSelector'
)
cursor = db.cursor() 


for market, codes in config.items():
    print(market)
    
    for code in codes:
        insertSQL = "INSERT INTO market_code (market, code) VALUES('{}', '{}')".format(market, code)
        cursor.execute(insertSQL)
        db.commit() 
"""