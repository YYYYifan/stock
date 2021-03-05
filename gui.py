             # -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 15:39:48 2021

@author: duyif
"""
import tkinter as tk
from selector import selector
import datetime
import os 



def getIndexLogBox():
    global indexLogBox 
    indexLogBox = indexLogBox + 1
    return indexLogBox


def getindexMatchBox():
    global indexMatchBox 
    indexMatchBox = indexMatchBox + 1
    return indexMatchBox


def getMatchCode():
    myLogBox.insert(getIndexLogBox(), "检查网络连接")
    isConnect = False if os.system('ping -n 2 -w 1 192.168.1.15') else True
    if not isConnect:
        myLogBox.insert(getIndexLogBox(), "未连接到数据库，检查电脑VPN是否连通")
    else:
        myLogBox.insert(getIndexLogBox(), "已连接到数据库")
        myLogBox.insert(getIndexLogBox(), "正在计算匹配的股票")
        root.update()
        
        matchData, date = selector()
        myLogBox.insert(getIndexLogBox(), "计算完成, 共{}个匹配股票".format(len(matchData)))
        myLogBox.insert(getIndexLogBox(), "日线: {} - {}".format(date[1], date[0]))
        myLogBox.insert(getIndexLogBox(), "30分钟: {} {} - {} {}".format(date[2][0].strftime("%Y-%m-%d"), 
                                                                            (date[2][1]+datetime.datetime(2000, 1, 1)).strftime("%H:%M"),
                                                                            date[3][0].strftime("%Y-%m-%d"), 
                                                                            (date[3][1]+datetime.datetime(2000, 1, 1)).strftime("%H:%M")))
        
        for data in matchData:
            market = "深圳" if data[0] == "SZ" else "上海"
            code = data[1]
            MA60_Day = data[2]
            MA60_30 = data[3]
            index = getindexMatchBox()
            insertData = "{}. {}-{}   60线-天-涨幅: {:11s}60线-30分钟-涨幅:{:11s}".format(index, market, code, str(MA60_Day), str(MA60_30))
            
            myCodeBox.insert(index, insertData)
    

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("860x800")
    root.title("股票筛选")
    
    indexLogBox = 0
    indexMatchBox = 0

    
    myLogBox = tk.Listbox(root, font=("Helvetica",20))
    myCodeBox = tk.Listbox(root, font=("Helvetica",20))
    myLogBox.pack(fill="both")
    myCodeBox.pack(fill="both", expand=1)

    root.after(100, getMatchCode)
    root.mainloop()