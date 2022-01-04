import json
with open('7.30', "r") as outfile:
# with open('historical_data_10mil', "r") as outfile:
    r=outfile.read()
check=json.loads(r)
check.reverse()



# check=[8,8,8,8,1,7,8,1,1,9,8,7,1,7,9,8,9]
# check=check[738985:739489]
# after 2 ones, wait 3 rounds and the after the next one bet 10,00,000 to recover the 10k 
# assume after 3 ones come the next one will not be follwed by another one 





def method2():
    index =0
    t10000 = 0
    nextline=0
    betting=100
    amount =1000000 - betting 
    profit=0
    loss=0
    critical=0
    for x in check:
        index +=1
        if (critical < 0):
            critical +=1
            continue
        
        
        if (x == 1):
            if(t10000):
                loss -= betting
                # amount -= betting 
                critical +=1
                betting =1040000 + 700 
                nextline=1
                t10000 =0
                # print(betting, loss, profit , index, 'loss')
            else:
                loss -= betting
                # amount -= betting 
                # print(betting, loss, profit , index, 'loss')
                critical +=1
                betting = betting * 100 + 200

        elif(critical == 1):
            # print(3)
            profit += betting*0.01
            if(nextline):
                if((profit+loss)<0 ):
                    print(betting, loss, profit , index, 'profit' , profit+loss)
                    print()
                profit=0
                loss=0
                nextline=0
            else:
                pass
                # print(betting, loss, profit , index, 'profit')
            betting =100
            critical =0
        else:
            profit += betting*0.01
            # print(betting, loss, profit , index, 'profit')
                
        if((x == 1) and (critical == 2)):

            betting=100	
            critical=-3
            t10000 = 1	
            continue
    print(amount,profit,loss)
     

method2()