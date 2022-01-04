import json

with open('historical_data_10mil', "r") as outfile:
# with open('files/7.30',  "r") as outfile:
    r=outfile.read()
check=json.loads(r)[:]
n=len(check)

def gameWin(arr, MAX_LOSSES=5):
	loss=0
	profit=0
	betPoint = 1
	n=1
	a=[]

# WAITING- PROFIT 63 8.76

	loss_count = 0
	one_profit = 0 

	INTIAL_BALANCE = 0
	PLAYING_BALANCE = 1000
	PROFIT_BALANCE = 2000 # always much greater than PLAYING_BALANCE
	num_profits = 0
	num_losses = 0

	balance = PLAYING_BALANCE


	for x in arr:

		if (balance > PROFIT_BALANCE):
			num_profits += 1
			balance -= PLAYING_BALANCE
			INTIAL_BALANCE += PLAYING_BALANCE
			n=1
			betPoint =1
			loss_count = 0
			one_profit = 0

		if (balance - betPoint < 0):
			num_losses += 1
			balance = PLAYING_BALANCE
			INTIAL_BALANCE -= PLAYING_BALANCE
			n=1
			betPoint =1
			loss_count = 0
			one_profit = 0


		if x >= 2:
			if (loss_count == MAX_LOSSES):
				loss_count = 0
				one_profit = 1
				# print("WAITING- PROFIT", betPoint, x)
				continue

			profit += betPoint
			balance += betPoint
			
			# print("PROFIT", betPoint, x)

			a.append(betPoint)
			n=1
			betPoint =1
			loss_count = 0
			one_profit = 0

		else:
			if (loss_count == MAX_LOSSES):
				# print("WAITING - LOSS", loss_count, betPoint, x)
				continue

			
			balance -= betPoint
			loss -= betPoint
			
			# print("LOSS", betPoint, x)

			a.append(-betPoint)
			n += 1
			betPoint = (2**n)-1
			loss_count += 1
			
			if (one_profit):
				loss_count = MAX_LOSSES


	print(num_losses, num_profits, MAX_LOSSES, loss, profit, profit+loss, min(a))





gameWin(check, 5)
