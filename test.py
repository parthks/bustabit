# -*- coding: utf-8 -*-
import hashlib
import hmac
 
consec_losses = 0
total_bets = 0

class bustabit():
   
    def __init__(self):
        #BTC hash of block 530523
        self.client_hash = "0000000000000000002dddc28874e5a9b2b8c285a09af36d094d91045bb054ae"
   
   
    def divisible(self, hashcode, modulo):
        #Checks if game crashes instantly
        hash_len = len(hashcode) % 4
        e = 0
        start = 0
        if (hash_len > 0):
            e = hash_len - 4
           
        while(e < len(hashcode)):
            substr = hashcode[start:e + 4]
            x = 0 + int(substr, 16) % modulo
            e += 4
            start = e
           
        if x == 0:
            return True
        else:
            return False
           
           
    def hmac(self, key, v):
        #Returns the hash with crashpoint information
        key = key.encode('utf-8')
        v = v.encode('utf-8')
        hmac_hash = hmac.new(key, v, "sha256").hexdigest()
        return hmac_hash
           
   
    def gen_gamehash(self, seed):
        #Generates the previous game hash based on current game hash
        seed = seed.encode('utf-8')
        sha256 = hashlib.sha256(seed).hexdigest()
        return sha256
   
   
    def crashpoint_from_hash(self, seed):
        #Get the crashpoint of the current hash/game
        crash_hash = self.hmac(seed, self.client_hash)
        #In 1 of 101 games the game crashes instantly
        if self.divisible(crash_hash, 101):
            return 1.00
        h = int(crash_hash[0:13], 16)
        e = int(2**52)
        crash_point = round((((100 * e - h) / (e - h))/100)-0.005,2)
        return crash_point
       
       
    def get_results(self, last_hash, amount):
        #Returns a list with the last crashpoints
        last_hash = last_hash
        history = []
        for i in range(0, amount):
            #Get crash of current hash
            crash = self.crashpoint_from_hash(last_hash)
            history.append(crash)
            #Generate new game hash
            last_hash = self.gen_gamehash(last_hash)
        return history
       
       
       
class simulator():
   
    def __init__(self):
        self.bab = bustabit()
   
    # bets - 1,2,3,4,5,6,7,8,9,11,13,15,17,19,21,23,25,28,31,34,37,40,43,47,51,55,59,64,69,74,79,85,91,97,104,111,119,127
            # 1,1,1,1,1,1,1,1,2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7,  7,  8,  8
    def strategy(self, lastwin, bet, budget, cashout):
        global consec_losses, total_bets
        #Enter your strategy here
        ##############################
        if lastwin:
            bet = 1
            consec_losses = 0
            total_bets = 1
        else:
            bet += 1
            while bet*18 < total_bets/2:
                bet += 1
            total_bets += bet
            consec_losses += 1
        if consec_losses > 20:
            bet = 10
            total_bets = 10
        ##############################
        return {"bet": bet, "cashout": cashout}
       
       
    def get_game_results(self, start_hash, amount):
        #Get the results of the past games. Returns an array with the crashpoints
        game_results = self.bab.get_results(start_hash, amount)
        return game_results
       
         
    def simulate_games(self, cashout, budget, bet, game_results):
        #Simulate games with your strategy
        budget_history = []
        games = 0
       
        for game in game_results:
            if budget < bet:
                print("Not enough money to bet left! This took {} games.".format(games))
                break
            elif game < cashout:
                budget -= bet
                lastwin = False
            else:
                budget += (bet * cashout) - bet
                lastwin = True
            budget_history.append(budget)
            strat = self.strategy(lastwin, bet, budget, cashout)
            bet = strat["bet"]
            cashout = strat["cashout"]
            games += 1
        return budget_history
 
   
    def plot_budget_history(self, budget_history):
        #Plot the budget history. You can delete this function if you don't need it and don't want to install matplotlib
        import matplotlib.pyplot as plt
        plt.plot(budget_history)
        plt.show()
       
       
       
def main():
    sim = simulator()
    results = sim.get_game_results("271579cf6d5d0af133a5dc5cd1f941aee55e8bbef95f440efcef7bb2c6ebcd72", 500000)
    budget_history = sim.simulate_games(19, 10000, 1, results)
    print(consec_losses)
    sim.plot_budget_history(budget_history)
    
   
   
if __name__ == "__main__":
    main()