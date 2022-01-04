import json

with open('historical_data_10mil', "r") as outfile:
# with open('files/7.30',  "r") as outfile:
    r=outfile.read()
check=json.loads(r)[:]
n=len(check)

def gameWin(arr):
    loss=0
    profit=0
    betPoint = 1
    n=1
    a=[]

    MAX_BET = 256


    for x in arr:

        if betPoint > MAX_BET:
            betPoint = 1


        if x >= 2:
            
            profit += betPoint
            
            # print("PROFIT", betPoint, x)

            a.append(betPoint)
            n=1
            betPoint =1

        else:

            loss -= betPoint
            
            # print("LOSS", betPoint, x)

            a.append(-betPoint)
            n += 1
            betPoint = (2**n)-1            
          

    print(loss, profit, profit+loss, min(a))





gameWin(check)
