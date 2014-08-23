# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

CITIES = []
city = []

# read data form file
t = open("./sir-res", "r")
END, STEP, H = [float(x) for x in t.readline()[:-1].split(" ")]

i = t.readline()[:-1]
while len(i) > 0:
    if i[0] == "|":
        CITIES.append(city)
        city = [i[1:]]
    else:
        city.append([float(x) for x in i.split(" ")])
    i = t.readline()[:-1]
CITIES.append(city)
CITIES = CITIES[1:]
t.close()

# plot data

#f, ayarr = plt.subplots(len(CITIES), sharex = True)
f = map(lambda x: x*H, range(int(END*STEP+1)))
for c in CITIES:
    plt.title(c[0])
    plt.plot(f, c[1], label='S')
    plt.plot(f, c[2], label='I')
    plt.plot(f, c[3], label='R')
    plt.legend(loc=0)
    plt.savefig("./sir-res-%s.png"%c[0])
    plt.clf()
#plt.show()
