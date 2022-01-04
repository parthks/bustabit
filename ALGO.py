import json
import random
import decimal
import collections

# 'historical_data_10mil'
f = open('historical_data_10mil', 'r')
ALL_ROUNDS = json.load(f)
f.close()

# ALL_ROUNDS = ALL_ROUNDS[0:1000]


INITIAL_BALANCE = 2000
BALANCE = INITIAL_BALANCE

LOWEST_BALANCE = BALANCE
HIGHEST_BALANCE = BALANCE

NUM_ROUNDS_PLAYED = 0
NUM_ROUNDS_LOST = 0
TOTAL_NUM_ROUNDS = len(ALL_ROUNDS)

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
Beat the house edge by trying to "miss" the 1(loss) multipliers
By waiting NUM_OF_WAITING_ROUNDS
Else just bet the BET_MULTIPLIER

** WILL NEVER CATCH UP TO RECOUP THAT LOSS **
'''
def strat_1(BET_MULTIPLIER, NUM_OF_WAITING_ROUNDS):
    global BALANCE
    bet_size = 1

    # BET_MULTIPLIER = 2.0
    # NUM_OF_WAITING_ROUNDS = 10

    num_rounds = 0

    wait_rounds = 0

    missed_the_loss = 0
    hit_the_loss = 0

    # lowest_balance = 0


    for bust in ALL_ROUNDS:
        # net_gain = (BET_MULTIPLIER*bet_size) - bet_size

        status = ''

        if (wait_rounds):
            status = "WAIT"

        if (bust < BET_MULTIPLIER):

            if (status == "WAIT"):
                missed_the_loss += 1
            else:
                hit_the_loss += 1

            wait_rounds = NUM_OF_WAITING_ROUNDS            

        # print(num_rounds, bust, net_gain, BALANCE, wait_rounds)

        if (status == "WAIT"):
            wait_rounds -= 1
        else:
            BET(bust, BET_MULTIPLIER, bet_size)
            # BALANCE += net_gain

        # lowest_balance = min(lowest_balance, BALANCE)
        num_rounds += 1
        # if (num_rounds > 10000):
        #     print(missed_the_loss, hit_the_loss)
        #     exit(1)


    return [missed_the_loss, hit_the_loss, lowest_balance]



def tune_strat1():
    global BALANCE
    '''
    Best tunes 
        Reallly high (~300's, 17000's, 57000's...) bet multiplers
        With very low (< 2) waiting rounds
    '''
    NUM_OF_WAITING_ROUNDS = 0

    for BET_MULTIPLIER in xrange(100,10000,100):
        for NUM_OF_WAITING_ROUNDS in xrange(0, 2):
            BALANCE = INITIAL_BALANCE
            [missed_the_loss, hit_the_loss, lowest_balance] = strat_1(BET_MULTIPLIER, NUM_OF_WAITING_ROUNDS)

            ratio = round((BALANCE/INITIAL_BALANCE if lowest_balance == 0 else BALANCE/(lowest_balance*-1.0)),2)

            if (ratio > 1):
                print(ratio, BALANCE, missed_the_loss, hit_the_loss, "FOR BET_MULTIPLIER", BET_MULTIPLIER, "NUM_OF_WAITING_ROUNDS", NUM_OF_WAITING_ROUNDS, lowest_balance)





'''
The chance you get a "green" after a "green" is higher than when after a "red"...
Since numbers bunch more likely than not in "random" sequences, 
"red's" will be grouped in large sequences more likely than not
"red" is a bust below 2. "green" is a bust 2 and above

'''
def strat_2():
    global BALANCE

    NUM_OF_WAITING_ROUNDS_MIN = 2
    NUM_OF_WAITING_ROUNDS_MAX = 5
     
    waiting_reds = 0
    bet_size = 100



    for bust in ALL_ROUNDS:

        
        if (waiting_reds):
            waiting_reds -= 1
            # print(bust, BALANCE, waiting_reds)
            continue
        else:
            BET_BUST = random.uniform(1.8, 2.1)
            BET(bust, BET_BUST, bet_size)
            # print(bust, BALANCE)

        if (bust < 2):
            waiting_reds = random.randint(5,10)






'''
Randomize bets to catch the high's 
Being more risky if ur doing well and more safe if ur doing badly "recently"
Be safe till you to "make-up" or "almost" make-up the money lost
high-risk; medium-risk (default); low-risk
'''
def strat_3():
    HIGH_RISK_BET = [10,20]
    MED_RISK_BET = [5,10]
    LOW_RISK_BET = [2,5]

    HIGH_RISK = [20,100]
    MED_RISK = [2,5]
    LOW_RISK = [1.01,2]

    HIGH_RISK_PROB = 1
    LOW_RISK_PROB = 0.3

    def get_bet_size(risk):
        if (risk == 'HIGH'): return random.randint(HIGH_RISK_BET[0], HIGH_RISK_BET[1])
        if (risk == 'MED'): return random.randint(MED_RISK_BET[0], MED_RISK_BET[1])
        if (risk == 'LOW'): return random.randint(LOW_RISK_BET[0], LOW_RISK_BET[1])

    def get_bet_bust(risk):
        if (risk == 'HIGH'): return random.uniform(HIGH_RISK[0], HIGH_RISK[1])
        if (risk == 'MED'): return random.uniform(MED_RISK[0], MED_RISK[1])
        if (risk == 'LOW'): return random.uniform(LOW_RISK[0], LOW_RISK[1])

    bet_size = BALANCE / 10.0

    for bust in ALL_ROUNDS:
        r = random.random()
        risk = "MED"
        if (r < HIGH_RISK_PROB):
            risk = "HIGH"
        elif (r > 1 - LOW_RISK_PROB):
            risk = "LOW"

        bet_size = get_bet_size(risk)
        bet_bust = get_bet_bust(risk)

        BET(bust,bet_bust, bet_size)




''' 
Sniper Strategy
If the running average is low, bet small with high multipliers
'''
def strat_4(THRESHOLD_AVG_BUST, BET_MULTIPLIER):
    bet_size = 1
    # THRESHOLD_AVG_BUST = 5.50
    # BET_MULTIPLIER = 100

    NUM_PREV_ROUNDS = 1000

    avg_bust = 0
    num = 0
    total_busts = 0

    prev_busts = collections.deque(maxlen=NUM_PREV_ROUNDS)

    wait_rounds_to_make_avg = NUM_PREV_ROUNDS

    for bust in ALL_ROUNDS:
        if (wait_rounds_to_make_avg):
            wait_rounds_to_make_avg -= 1
        elif (avg_bust < THRESHOLD_AVG_BUST):
            BET(bust, BET_MULTIPLIER, bet_size)


        if (bust > BET_MULTIPLIER):
            bust = BET_MULTIPLIER

        total_busts += bust
        if (wait_rounds_to_make_avg == 0):
            total_busts -= prev_busts[0]

        prev_busts.append(bust)

        avg_bust = float(total_busts) / float(NUM_PREV_ROUNDS)

        # if (BALANCE < 0):
        #     return


strat_4(4.2, 50)
end_game()
exit(1)

def tune_strat_4():
    
    def float_range(A, L=None, D=None):
        #Use float number in range() function
        # if L and D argument is null set A=0.0 and D = 1.0
        if L == None:
            L = A + 0.0
            A = 0.0
        if D == None:
            D = 1.0
        while True:
            if D > 0 and A >= L:
                break
            elif D < 0 and A <= L:
                break
            yield ("%g" % A) # return float number
            A = A + D
    #end of function float_range()

    AVG_THRESHOLDS = {2: 1.663895400000839, 3: 2.063718290001155, 4: 2.3472314900006883, 5: 2.5671506600003244, 6: 2.746658850000027, 7: 2.898595039999816, 8: 3.030404539999596, 9: 3.146559769999446, 10: 3.2504628399992863, 11: 3.3445064099991377, 12: 3.4304386699989964, 13: 3.509545629998898, 14: 3.5827876999988275, 15: 3.6508830199987536, 16: 3.7146759599986994, 17: 3.7746676499986567, 18: 3.8312848399986223, 19: 3.8848179199985746, 20: 3.9355647699985417, 21: 3.983821299998495, 22: 4.029802589998477, 23: 4.07368107999845, 24: 4.115719229998426, 25: 4.156065649998365, 26: 4.1948565499983275, 27: 4.232252959998217, 28: 4.268300059998186, 29: 4.303093049998148, 30: 4.336714769998064, 31: 4.369248189998084, 32: 4.400748229998025, 33: 4.431328359997978, 34: 4.460972279997952, 35: 4.48974794999794, 36: 4.517671939997892, 37: 4.54481682999787, 38: 4.571231589997872, 39: 4.596984369997858, 40: 4.62207330999787, 41: 4.646526099997854, 42: 4.670392199997832, 43: 4.6936769099978335, 44: 4.716417449997841, 45: 4.7386330099978, 46: 4.760387419997825, 47: 4.781697159997789, 48: 4.802547169997772, 49: 4.822988119997754, 50: 4.843000739997782, 51: 4.862629569997763, 52: 4.881875009997738, 53: 4.900711539997699, 54: 4.9191805399976865, 55: 4.9373216499977, 56: 4.955158109997677, 57: 4.9726848599976545, 58: 4.989861829997621, 59: 5.006725949997593, 60: 5.023292049997567, 61: 5.039586239997541, 62: 5.055606559997483, 63: 5.071382549997482, 64: 5.08689821999744, 65: 5.102172959997445, 66: 5.117217249997417, 67: 5.132043929997436, 68: 5.1466347699973864, 69: 5.161005409997377, 70: 5.175184499997344, 71: 5.189173229997335, 72: 5.20296921999732, 73: 5.216556709997302, 74: 5.229950859997316, 75: 5.243181269997322, 76: 5.256223459997295, 77: 5.2690950699973005, 78: 5.281806239997277, 79: 5.294368599997273, 80: 5.306759349997252, 81: 5.319012019997239, 82: 5.331110499997233, 83: 5.343057189997255, 84: 5.354846699997261, 85: 5.366489439997252, 86: 5.378000999997269, 87: 5.389385859997267, 88: 5.400626779997263, 89: 5.411732039997252, 90: 5.422716659997233, 91: 5.433580599997244, 92: 5.444323609997245, 93: 5.4549483799972345, 94: 5.46545159999724, 95: 5.475838309997252, 96: 5.486097689997253, 97: 5.496240069997239, 98: 5.506281499997243, 99: 5.516232649997244}


    for bust_bet in range(70,100,1):
        for avg_bust_error in float_range(-0.5,0,0.1):
            avg_bust = float(AVG_THRESHOLDS[bust_bet])
            avg_bust_error = float(avg_bust_error)
            avg_bust += float(avg_bust_error)

            reset()

            strat_4(avg_bust, bust_bet)
            # print(BALANCE, LOWEST_BALANCE)
            ratio = round((BALANCE/INITIAL_BALANCE if LOWEST_BALANCE > 0 else BALANCE/(INITIAL_BALANCE + (LOWEST_BALANCE*-1.0))),2)
            
            print(ratio, BALANCE, "FOR THRESHOLD_AVG_BUST", avg_bust, 'BET_BUST', bust_bet)

            if (ratio <= 1): continue

            print(ratio, BALANCE, "FOR THRESHOLD_AVG_BUST", avg_bust, 'BET_BUST', bust_bet)
            end_game()
            print("\n\n")


tune_strat_4()
# end_game()



