############ Created by Sal Mancuso
############ Free to use under the MIT Lic. 

def makeChart(timeStamp, cpuUse, memUse, cpuPercent, memPercent):
    print ("""{0:8}{1:<26}{2:15}{3:<26}{4}""".format(timeStamp, int(cpuUse/4)*'█', cpuPercent, int(memUse/4)*'█', memPercent))


systemUsage = {"1500": [1,.22], "1501": [.9,1], "1502": [.50,.75], "1503": [.60,.34], "1504": [.65,.23], "1505": [.85,.47], "1506": [.45,.67], "1507": [.93,.80], "1508": [.79,.64], "1509": [.76,.93], "1510": [.92,.42], "1511": [.45,.84]}

print("\n\n")
print("-------------------------------- Current {} Usage --------------------------------".format("Yen3"))
print ("""{0:8}{1:<35}{2:6}{3:15}""".format("TIME", "*********** CPU Usage ************","", "*********** MEM Usage ************"))
for timeStamp in systemUsage:
    cpuPercent = """{}{}""".format(int(systemUsage[timeStamp][0]*100),"% CPU")
    memPercent = """{}{}""".format(int(systemUsage[timeStamp][1]*100),"% MEM")
    cpuUse = int(systemUsage[timeStamp][0]*100)
    memUse = int(systemUsage[timeStamp][1]*100)
    makeChart(timeStamp, cpuUse, memUse,cpuPercent, memPercent)
