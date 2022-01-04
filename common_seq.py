import json


f = open('12.30', 'r')
check = json.load(f)
f.close()

f = open('1.30', 'r')
main = json.load(f)
f.close()

check.reverse()
main.reverse()



def longest_seq_from(main, check):
    for n1_check_index in range(0, len(main)):
        starting_index = n1_check_index
        check_index = 0
        while True:
            main_num = main[starting_index+check_index]
            check_num = check[check_index]
            check_index += 1

            if (main_num != check_num):
                break

            if (starting_index+check_index) == len(main):
                return n1_check_index
    

n1 = longest_seq_from(main, check)
print('n1 =', n1)


# checking...
n = 1000000-n1
assert(main[n1:n1+n] == check[0:n])
