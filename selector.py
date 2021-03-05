# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:08:50 2021

@author: duyif
"""

# -*- coding: utf-8 -*-

import pymysql
import json
import datetime

resultIndex = 0


def getIndex():
    global resultIndex
    resultIndex = resultIndex + 1
    return resultIndex


def selector():
    global resultIndex
    
    db = pymysql.connect(
        host='192.168.1.15',
        user='root',
        password='980326',
        database='codeSelector'
    )     
    cursor = db.cursor()
    
    matchCode = []
    
    with open("code.json") as f:
        config = json.load(f)
    for market in ["SZ", "SH"]:
        codeList = config[market]
       
        codeAmount = len(codeList)
        for codeIndex in range(codeAmount):        
            
            
            selectSQL = "SELECT date, MA60 FROM {}_day WHERE code = '{}' ORDER BY date DESC LIMIT {}".format(market, codeList[codeIndex], '10')
            # print(selectSQL)
            cursor.execute(selectSQL)
            sqlResult = cursor.fetchall()          
            # print(codeList[codeIndex])
            if len(sqlResult) < 10:
                pass
            elif sqlResult[0][1] == None or sqlResult[9][1] == None:
                pass
            elif sqlResult[0][1] > sqlResult[9][1]:            
                matchCode.append([
                    market,
                    codeList[codeIndex],
                    sqlResult[9][0].strftime("%Y-%m-%d"),
                    sqlResult[0][0].strftime("%Y-%m-%d"),
                    str(round((sqlResult[0][1]-sqlResult[9][1])/sqlResult[9][1] * 100, 2)) + "%"
                    ])
    # return matchCode
    result = []
    for matchData in matchCode:
        selectSQL = "SELECT date, time, MA60 FROM {}_30min WHERE code = '{}' ORDER BY date DESC, time DESC LIMIT {}".format(matchData[0], matchData[1], '10')
        cursor.execute(selectSQL)
        sqlResult = cursor.fetchall()   
        # print(sqlResult)        
        if sqlResult[0][1] == None or sqlResult[9][1] == None:
            print(False)
            pass
        elif sqlResult[0][2] > sqlResult[9][2]:
            result.append([
                getIndex(),
                matchData[0],
                matchData[1],
                matchData[4],
                str(round((sqlResult[0][2]-sqlResult[9][2])/sqlResult[9][2] * 100, 2)) + "%"
                ])
    db.close()
    date = [
        matchData[2], 
        matchData[3], 
        sqlResult[9][0].strftime("%Y-%m-%d") + " " +(sqlResult[9][1] + datetime.datetime(2000, 1, 1)).strftime("%H:%M"),
        sqlResult[0][0].strftime("%Y-%m-%d") + " " +(sqlResult[0][1] + datetime.datetime(2000, 1, 1)).strftime("%H:%M"),        
    ]
    return result, date

if __name__ == "__main__":
    result, date = selector()
    result = {"LastUpdate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "Date": date, "Data": result}
    with open ("result.json", "w") as f:
        json_dicts=json.dumps(result, indent=4)
        f.write(json_dicts)