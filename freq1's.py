import json
import matplotlib.pyplot as plt


f = open('freqOf1.txt', 'r')
freq = json.load(f)
f.close()

total = 0
distribution = {}
for x in freq:
    total += x
    distribution[x] = distribution.get(x, 0) + 1

avg_freq = total / len(freq)

print(avg_freq)

plt.hist(freq, 1000)
plt.show()


plt.plot(freq)
plt.show()



# freq.reverse()
# plt.plot(freq)
# plt.show()

exit(1)