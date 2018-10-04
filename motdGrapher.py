#!/usr/bin/python3

###############################################################
###############################################################
####  Created by Sal Mancuso
####  Free to use under the MIT Lic.
####  Copyright (c) 2018-2024 Scott Sal Mancuso
###############################################################
###############################################################
import sqlite3
import datetime
import re
import psutil
import calendar
import time


###############################################################
#### CAPTURE CUSTOM MESSAGE OF THE DAY
#### EDIT motdMessages.txt TO SEND OUT CUSTOM MESSAGES TO USERS
###############################################################
def additionalMOTDmessage():
    try:
        motdFileRaw = open('./motdMessages.txt', 'r')
        motdFile = motdFileRaw.read()
        print (motdFile)
        return motdFile
    except:
        None


###############################################################
#### FUNCTION TO BUILD ROWS WITH BARS FOR GRAPHS
#### CHANGE THE █ ICON TO CHANGE THE BAR LOOK
###############################################################
def makeChart(timeStamp, cpuUse, memUse, cpuPercent, memPercent):
    print ("""{0:8}{1:<26}{2:15}{3:<26}{4}""".format(timeStamp, int(cpuUse/4)*'█', cpuPercent, int(memUse/4)*'█', memPercent))
    appendMotdFile(str("""{0:8}{1:<26}{2:15}{3:<26}{4}""".format(timeStamp, int(cpuUse/4)*'█', cpuPercent, int(memUse/4)*'█', memPercent)))

###############################################################
#### CREATE A DATBASE CONNECTION AND/OR CREATE A
#### NEW DATABASE FILE
###############################################################
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        # print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

###############################################################
#### CREATE A NEW TABLE IN THE SQLITE DATABASE IF ONE
#### DOES NOT EXIST
###############################################################
def createTable(databaseName):
    try:
        sql_create_systemStats_table = """CREATE TABLE IF NOT EXISTS systemStats (UID integer PRIMARY KEY, systemTimeStamp VARCHAR(100), cpuPercentage DECIMAL(3,2) NOT NULL, memPercentage DECIMAL(3,2) NOT NULL); """
        # print (sql_create_systemStats_table)
        conn = create_connection(databaseName)
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        c.execute(sql_create_systemStats_table)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()

###############################################################
#### INSERT DATA INTO DATABASE FUNCTION
###############################################################
def insertIntoTable(databaseName, UID, systemTimeStamp, cpuPercentage, memPercentage):
    try:
        sql_insert_into_systemStats_table = """INSERT INTO systemStats (UID, systemTimeStamp, cpuPercentage, memPercentage) VALUES ({},'{}',{},{}); """.format(UID, systemTimeStamp, cpuPercentage, memPercentage )
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        c.execute(sql_insert_into_systemStats_table)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()

###############################################################
#### COLLECTS LAST 10 RECORDS THAT WILL BE USED TO CREATE
#### THE BAR CHART
#### WORTH NOTING, CHANGE THE SQL LIMIT TO INCREASE OR 
#### DECREASE THE SIZE OF THE CHARTS. 
###############################################################
def getLastTenMeasures():
    try:
        sql_get_last_ten_ssytemStats = """SELECT * FROM (SELECT * FROM systemStats ORDER BY UID DESC LIMIT 10) a ORDER BY UID ASC;"""
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        c.execute(sql_get_last_ten_ssytemStats)
        resultsList = c.fetchall()
        return resultsList
    except Error as e:
        print(e)
    finally:
        conn.close()

###############################################################
#### BEGIN THE MOTD FILE BUILD. THIS HAS SOME AESTHETICS
#### FOR THE CHARTS
###############################################################
def createMotdFile():
    motdFile = open('/etc/motd', 'w')
    motdFile.write(additionalMOTDmessage())
    motdFile.write("\n\n")
    motdFile.write("----------------------------- Current {} Usage -----------------------------".format("Test Server"))
    motdFile.write("\n")
    motdFile.write("""{0:8}{1:<35}{2:6}{3:15}""".format("TIME", "********** CPU Usage **********", "", "********** MEM Usage **********"))
    motdFile.write("\n")
    print("\n\n")
    print("----------------------------- Current {} Usage -----------------------------".format("Test Server"))
    print("""{0:8}{1:<35}{2:6}{3:15}""".format("TIME", "********** CPU Usage **********", "", "********** MEM Usage **********"))

###############################################################
#### WRITE THE GRAPH BARS TO THE FOR THE CHARTS
#### MUST HAVE ROOT ACCESS TO DO THIS FUNCTION ROOT!!!!!!
###############################################################    
def appendMotdFile(writeThisLine):
    motdFile = open('/etc/motd', 'a')
    motdFile.write(writeThisLine)
    motdFile.write("\n")

##############################################################################################################################
##############################################################################################################################
#### MAIN LOOP
##############################################################################################################################
##############################################################################################################################
if __name__ == "__main__":
    additionalMOTDmessage()

    #### DECLARE DATABASE FILEPATH AND NAME
    databaseName = "./motdSystemData.dat"
    createTable(databaseName)

    #### GET CPU PERCENTAGE
    cpuPercentage = float(psutil.cpu_percent(interval=1))/100

    #### GET MEM PERCENTAGE
    memData = re.findall(r'(percent\=)(.*?)(\,)', str(psutil.virtual_memory()), re.DOTALL)
    memPercentage = float(memData[0][1])/100

    #### UID IS USED TO SORT IN SQL. IT IS SIMPLY UNIX EPOCH TIME 
    UID = int(calendar.timegm(time.gmtime()))

    #### GET CURRENT CURRENT HOURS AND MINUTES FOR CHART TIMESTAMP
    now = datetime.datetime.now()
    currentHour = str(now.hour)
    if len(currentHour) <2:
        currentHour = str("0")+str(currentHour)  #### ADD 0 SO THAT 3:15 LOOKS LIKE 03:15
    currentMinute = str(now.minute)
    if len(currentMinute) <2:
        currentMinute = str("0")+str(currentMinute)  #### ADD 0 SO THAT 12:5 LOOKS LIKE 12:05
    systemTimeStamp = """{}:{}""".format(currentHour,currentMinute)

    #### PUSH THE LATEST MEASURES TO THE SQLITE DATABASE
    insertIntoTable(databaseName, UID, systemTimeStamp, cpuPercentage, memPercentage)

    #### GET LAST MEASURES OUT OF SQLITE DATABASE AND PUT RESULTS INTO A DICTIONARY 
    systemUsage = {}
    for rawData in getLastTenMeasures():
        UID = rawData[0]
        timeStamp = rawData[1]
        cpuPercent = rawData[2]
        memPercent = rawData[3]
        systemUsage[UID] = [timeStamp, cpuPercent, memPercent]

    ####  FORMAT STRINGS AND FLOATS TO BE INCLUDED IN CHART THEN PASS TO makeChart FUNCTION
    createMotdFile()
    for UID in systemUsage:
        cpuPercent = """{}{}""".format(int(systemUsage[UID][1] * 100), "%")
        memPercent = """{}{}""".format(int(systemUsage[UID][2] * 100), "%")
        cpuUse = int(systemUsage[UID][1] * 100)
        memUse = int(systemUsage[UID][2] * 100)
        timeStamp = str(systemUsage[UID][0])
        makeChart(timeStamp, cpuUse, memUse, cpuPercent, memPercent)


