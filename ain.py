import json

# with open('historical_data_10mil', "r") as outfile:
with open('files/7.30',  "r") as outfile:
    r=outfile.read()
check=json.loads(r)[:] #2089+580+3359+18+543+115+512+185+241+51



def run(check):

	# check=[1,1,1,1,1,7,1,1,1,2,1,2,1,1,2,1,2,1,1,1,1]
	def nextBet(tempLosses, numberOfLosses, earnEveryRound):
		return tempLosses + earnEveryRound*(numberOfLosses +1)


	earnEveryRound=1
	betingPoint=1
	tempLosses=0
	totalProfit=0
	totalLoss=0
	numberOfLosses=0
	listOfBetResult=[]
	terminal=0
	lossWinTracker =[]
	resetCounter = 0
	resultDict={}
	depositeBalance=1000

	resetCounters = [1,2,3,5,8]

	for x in check:
		if ("".join(map(str, lossWinTracker[-3:])) == '010'):
			# print('tempLosses',tempLosses,numberOfLosses,listOfBetResult[-3:])
			resetCounter = 0

		if(x>=2):
			lossWinTracker.append(0)
			totalProfit += betingPoint
			listOfBetResult.append(betingPoint)
			if(terminal):
				betingPoint=nextBet(tempLosses, numberOfLosses, earnEveryRound)
				terminal=0
				# resetCounter=0
				continue
			betingPoint = 1
			numberOfLosses=0
			tempLosses=0
			resetCounter=0
		else:
			lossWinTracker.append(1)
			numberOfLosses += 1
			resetCounter +=1
			tempLosses += betingPoint
			totalLoss += betingPoint
			listOfBetResult.append(-betingPoint)
			requiredBalance = tempLosses + nextBet(tempLosses, numberOfLosses, earnEveryRound)
			if (requiredBalance > depositeBalance):
				break
			if(resetCounter >= 3):
				betingPoint = 1
				terminal=1
				continue

			
			betingPoint = nextBet(tempLosses, numberOfLosses, earnEveryRound)



	resultDict['listOfBetResult']=listOfBetResult
	resultDict['Total Earn']= totalProfit - totalLoss
	# resultDict['Max Loss'] = min(listOfBetResult)
	# resultDict['Max beting Point'] = max(listOfBetResult)
	resultDict['Last Total Temp Losses'] = -tempLosses
	resultDict['Last Number Of Continue Losses'] = numberOfLosses
	# resultDict['Minmum Balance Need'] = 2*(max(listOfBetResult)) -1  # need correction
	resultDict['Total Round Played'] = len(listOfBetResult)
	# resultDict['Loss Win Tracker'] = lossWinTracker

	for k,v in resultDict.items():
		print(k,'-->',v)
	print("".join(map(str, lossWinTracker[-3:])), resetCounter)

	return [resultDict['Total Earn'], resultDict['Total Round Played']]
	



total = 0
while len(check) > 1:
	[earn, limit] = run(check)
	check = check[limit:]
	total += earn
	print("TOTAL", total)










