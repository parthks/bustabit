'''

learn quicksort


'''

import json

f = open('historical_data', 'r')
ALL_ROUNDS = json.load(f)
f.close()



INITIAL_BALANCE = 2000

TOTAL_NUM_ROUNDS = len(ALL_ROUNDS)
NUM_ROUNDS_PLAYED = 0
NUM_ROUNDS_LOST = 0

LOWEST_BALANCE = 0
HIGHEST_BALANCE = 0


BALANCE = INITIAL_BALANCE


def end_game():
    waited_rounds = TOTAL_NUM_ROUNDS - NUM_ROUNDS_PLAYED
    print('current total', BALANCE, 'in', NUM_ROUNDS_PLAYED,'rounds played', 'and', waited_rounds, 'skipped')
    print(float(NUM_ROUNDS_LOST)/TOTAL_NUM_ROUNDS, float(NUM_ROUNDS_PLAYED-NUM_ROUNDS_LOST)/TOTAL_NUM_ROUNDS)
    print("Lowest, Highest Balance", LOWEST_BALANCE, HIGHEST_BALANCE)

def reset():
    global NUM_ROUNDS_PLAYED, NUM_ROUNDS_LOST, LOWEST_BALANCE, HIGHEST_BALANCE, BALANCE
    BALANCE = INITIAL_BALANCE

    LOWEST_BALANCE = BALANCE
    HIGHEST_BALANCE = BALANCE

    NUM_ROUNDS_PLAYED = 0
    NUM_ROUNDS_LOST = 0


def BET(bust, bet_bust, bet_size):
    global NUM_ROUNDS_PLAYED, NUM_ROUNDS_LOST, LOWEST_BALANCE, HIGHEST_BALANCE, BALANCE

    bet_bust = round(bet_bust,2)
    bet_size = int(bet_size)

    net_gain = (bet_bust*bet_size) - bet_size
    if (bust < bet_bust):
            net_gain = -bet_size
            NUM_ROUNDS_LOST += 1

    BALANCE += net_gain

    # if (BALANCE < 0):
    #     end_game()
    #     exit(1)

    NUM_ROUNDS_PLAYED += 1

    LOWEST_BALANCE = min(LOWEST_BALANCE, BALANCE)
    HIGHEST_BALANCE = max(HIGHEST_BALANCE, BALANCE)



'''

1. to reach long straights of non 1
start = 100
bet 1.01
if lose double bet
when recover 2x - reset

'''
def algo_one():
    start = 100
    resetAtMultiplier = 2
    increaseMultiplerOnLoss = 2


    num_wins = 0
    bet_size = start
    BET_MULTIPLIER = 1.01
    current_round_profit = 0
    current_round_profit_freq = {}
    num_current_rounds = 0
    num_rounds_current_profit = []


    for bust in ALL_ROUNDS:
        # print(bust, bet_size)
        BET(bust, BET_MULTIPLIER, bet_size)
        if (bust == 1):
            bet_size *= increaseMultiplerOnLoss
            current_round_profit -= bet_size

        current_round_profit += (BET_MULTIPLIER*bet_size) - bet_size
        num_current_rounds += 1

        if (current_round_profit >= start*resetAtMultiplier):
            num_rounds_current_profit.append({"num_rounds_current_profit": num_current_rounds, "current_round_profit": current_round_profit, "bet_size": bet_size})
            
            num_current_rounds = 0
            bet_size = start
            num_wins += 1
            # current_round_profit_freq[current_round_profit] = current_round_profit_freq.get(current_round_profit, 0) + 1
            current_round_profit = 0

    print(num_rounds_current_profit)
    print(num_wins)

algo_one()
end_game()

















