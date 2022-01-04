import json
import matplotlib.pyplot as plt
import collections

import random

# name = 'historical_data_10mil'

f = open('freqOf1.txt', 'r')
ALL_ROUNDS = json.load(f)
f.close()

# print(ALL_ROUNDS.keys())

print("Got data", len((ALL_ROUNDS)))

print("Got data", ALL_ROUNDS)


plt.plot(ALL_ROUNDS)
plt.show()
exit(1)

ALL_ROUNDS = ALL_ROUNDS[0:300]


def find_avg(arr):
    total = 0
    for x in arr:
        total += x

    return total / float(len(arr))


def getting_num_rounds_for_1_percent_house_edge():
    num_validations = 100

    indexes = []

    def find_num_rounds(starting_index):
        one_count = 0
        total_count = 0
        index = starting_index
        
        while index < len(ALL_ROUNDS):
            if (ALL_ROUNDS[index] == 1):
                one_count += 1

            total_count += 1
            

            avg = one_count/total_count
            # indexes.append([index, ALL_ROUNDS[index], avg])
            if (total_count > 10 and avg == 0.01):
                # print(indexes)
                return index - starting_index

            index += 1

        return -1


    while num_validations != 0:
        starting_index = random.randint(0,len(ALL_ROUNDS))
        num = find_num_rounds(starting_index)
        if (num != -1):
            print(num+1)
            indexes.append(num+1)
            num_validations -= 1

    print('avg =', find_avg(indexes))

# getting_num_rounds_for_1_percent_house_edge()

# exit(1)

def distribution():
    dist = {}
    for num in ALL_ROUNDS:
        dist[num] = dist.get(num, 0) + 1

    print("length = ",len(dist.keys()))
    SORTED_DICT = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
    x_axis = list(SORTED_DICT.keys())
    y_axis = list(SORTED_DICT.values())

    axes = plt.gca()
    axes.set_xlim([0.9,3])
    plt.plot(x_axis,y_axis)
    plt.show()




def pattern(upper):
    dist = []
    for num in ALL_ROUNDS:
        if num > upper:
            num = upper
        dist.append(num)

    plt.plot(dist)
    plt.show()

# distribution()
# exit(1)
# ALL_ROUNDS = ALL_ROUNDS[0:1000]

# plt.plot(ALL_ROUNDS)
# plt.show()

def avg_distance_between(num):
    total = 0
    num_win = 0
    current_distance = 1
    max_distance = 0

    d = {}

    for bust in ALL_ROUNDS:
        if (num == 1):
            if (bust == 1):
                total += current_distance
                d[current_distance] = d.get(current_distance, 0) + 1
                current_distance = 1
                num_win += 1
            else:
                current_distance += 1
                max_distance = max(max_distance, current_distance)
        else:
            if (bust < num):
                current_distance += 1
                max_distance = max(max_distance, current_distance)
            else:
                total += current_distance
                d[current_distance] = d.get(current_distance, 0) + 1
                current_distance = 1
                num_win += 1

        # print(bust, current_distance, total, num_win)

    print("FOR BUST", num)
    print("max_distance", max_distance)
    print("avg_distance", total/float(num_win))
    return d
    


# for bust_bet in xrange(10,11,1):
#     d = avg_distance_between(bust_bet)
#     print(d)
#     plt.bar(d.keys(), d.values())
#     plt.show()

# exit(1)


def bust_count():
    busts_count = {}

    for bust in ALL_ROUNDS:
        if (bust <= 5 and bust >= 2):
            busts_count[bust] = busts_count.get(bust, 0) + 1

    # print(busts_count)
    x_axis = list(busts_count.keys())
    y_axis = list(busts_count.values())

    plt.scatter(x_axis,y_axis)
    plt.show()








def running_avg_bust(BUST_BET, NUM_PREV_ROUNDS):
    avg_bust = 0
    num = 0
    overall_total_busts = 0
    total_busts = 0


    overall_avg_busts = []
    avg_busts = []

    # def calc_avg(avg_list):
    #     total = 0
    #     num = len(avg_list)
    #     for avg in avg_list:
    #         total += avg
    #     return total / float(num)

    prev_busts = collections.deque(maxlen=NUM_PREV_ROUNDS)

    # for bust in ALL_ROUNDS[0:NUM_PREV_ROUNDS]:
    #     if (bust > BUST_BET):
    #         bust = BUST_BET
    #     prev_busts.append(bust)

    # avg_bust = calc_avg(prev_busts)

    for bust in ALL_ROUNDS[NUM_PREV_ROUNDS:]:
        # if (bust == 1):
        #     bust = 0
        if (BUST_BET != -1 and bust > BUST_BET):
            bust = BUST_BET
        # prev_busts.append(bust)
        total_busts += bust
        overall_total_busts += bust

        num += 1
        if (num > NUM_PREV_ROUNDS):
            total_busts -= prev_busts[0]

        prev_busts.append(bust)
        overall_avg_bust = float(overall_total_busts) / float(num)
        avg_bust = float(total_busts) / float(NUM_PREV_ROUNDS)

        avg_busts.append(avg_bust)
        overall_avg_busts.append(overall_avg_bust)

        # print(bust, total_busts, num, avg_bust)

    
    
    return overall_avg_busts, avg_busts


overall_avg_busts, avg_busts = running_avg_bust(2, 100)
print("avg", avg_busts)
axes = plt.gca()
axes.set_ylim([avg_busts[-1]-0.2,avg_busts[-1]+0.2])
plt.plot(avg_busts)
plt.show()
exit(1)

# def reduce_noise(num):
#     global ALL_ROUNDS
#     for i in range(len(ALL_ROUNDS)):
#         if ALL_ROUNDS[i] > num:
#             ALL_ROUNDS[i] = num

d = {}
for bust_bet in range(2,51):
    # reduce_noise(bust_bet)
    overall_avg_busts, avg_busts = running_avg_bust(bust_bet, 100)
    d[bust_bet] = avg_busts[-1]
    print(d)
    axes = plt.gca()
    axes.set_ylim([avg_busts[-1]-0.4,avg_busts[-1]+0.4])
    plt.plot(avg_busts)
    plt.show()

print(d)











'''


1 2 4 7 11 16 22 
1 2 3 4 5 
1 1 1 1 


'''
