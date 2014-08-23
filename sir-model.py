# -*- coding: utf-8 -*-

##############################################################################
# S I M U L A T O R   O F   C O N T A G I O N
##############################################################################

import sys
#import matplotlib.pyplot as plt

class City(object):
    """
    Object for computing
    """
    def __init__(self, name, s, i, r, b, g, emigration, connections=[]):
        self.name = str(name)
        self.s = [float(s)] # susceptible
        self.i = [float(i)] # infected
        self.r = [float(r)] # removed
        self.b = float(b) # contacts per person
        self.g = float(g) # chance of recover per day
        self.emigration = float(emigration) # percent of emigration per step
        self.connections = connections
    def euler(self, start, stop, h):
        """
        Forward Euler method
        """
        for step in xrange(start, stop):
            s2i = self.b*self.s[step]*self.i[step]/(self.s[step]+self.r[step]+self.i[step])
            i2r = self.g*self.i[step]
            
            self.s.append(max(self.s[step] + h*(-s2i + (self.s[step]+self.r[step])*(BORNS-DEATHS)), 0.0))
            self.i.append(max(self.i[step] + h*(s2i - i2r + self.i[step]*(BORNS-DEATHS-LETHALITY)), 0.0))
            self.r.append(max(self.r[step] + h*(i2r + self.r[step]*(BORNS-DEATHS)), 0.0))
    
    def contagion(self):
        """
        Contagion of connected cities
        """
        for connection in self.connections:
            connection[0].s[-1] += self.emigration*self.s[-2]*connection[1]*S_RESTRICTION
            connection[0].i[-1] += self.emigration*self.i[-2]*connection[1]*I_RESTRICTION
            connection[0].r[-1] += self.emigration*self.r[-2]*connection[1]*R_RESTRICTION
            self.s[-1] = max(self.s[-1] - self.emigration*self.s[-2]*connection[1]*S_RESTRICTION, 0.0)
            self.i[-1] = max(self.i[-1] - self.emigration*self.i[-2]*connection[1]*I_RESTRICTION, 0.0)
            self.r[-1] = max(self.r[-1] - self.emigration*self.r[-2]*connection[1]*R_RESTRICTION, 0.0)

def export(f, l):
    """
    Export results in file
    """
    t = open(f, "w")
    t.write(str(END)+" "+str(STEP)+" "+str(H)+"\n")
    for c in l:
        t.write("|"+c.name+"\n") # | is start symbol
        t.write(" ".join([str(x) for x in c.s]) + "\n" + " ".join([str(x) for x in c.i]) + "\n" + " ".join([str(x) for x in c.r]) + "\n")
    t.close()
    
# Options
B = 0.05 # transmission percent for persone per contact
G = 0.01 # resurect percent for persone per day
BORNS = 0.005 # percent of total population
DEATHS = 0.005 # percent of total population
LETHALITY = 0.0015 # percent of infected

S_RESTRICTION = 1.0 # restriction of emigration
I_RESTRICTION = 0.05
R_RESTRICTION = 0.25

H = 0.1 # epsilon
END = 1250 # steps
STEP = 10 # size of step


#CITIES = (City("Odessa", 1014765.0, 173.0, 1000.0+sys.float_info.epsilon, B, G, 0.001), # 0
#          City("Bilhorod-Dnistrovskyi", 57210.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.0075), # 1
#          City("Izmail", 73336.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.001), # 2
#          City("Illichivsk", 63726.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.015), # 3
#          City("Kotovsk", 47668.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.001), # 4
#          City("Yuzhne", 29327.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.015), # 5
#          City("Teplodar", 10081.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.055) # 6
#         )

CITIES = (City("City #0", 1014765.0, 0.0, 1000.0+sys.float_info.epsilon, B, G, 0.001), # 0
          City("City #1", 57210.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.0075), # 1
          City("City #2", 73336.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.001), # 2
          City("City #3", 63726.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.015), # 3
          City("City #4", 47668.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.001), # 4
          City("City #5", 29327.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.015), # 5
          City("City #6", 10081.0, 0.0, 0.0+sys.float_info.epsilon, B, G, 0.055) # 6
         )


# Initialize connections
# Odessa
CITIES[0].connections.append([CITIES[1], 0.05])
CITIES[0].connections.append([CITIES[2], 0.001])
CITIES[0].connections.append([CITIES[3], 0.1])
CITIES[0].connections.append([CITIES[4], 0.001])
CITIES[0].connections.append([CITIES[5], 0.05])
CITIES[0].connections.append([CITIES[6], 0.05])
# Bilhorod-Dnistrovskyi
CITIES[1].connections.append([CITIES[0], 0.05])
CITIES[1].connections.append([CITIES[2], 0.005])
CITIES[1].connections.append([CITIES[3], 0.025])
# Izmail
CITIES[2].connections.append([CITIES[0], 0.001])
CITIES[2].connections.append([CITIES[1], 0.005])
# Illichivsk
CITIES[3].connections.append([CITIES[0], 0.1])
CITIES[3].connections.append([CITIES[1], 0.025])
CITIES[3].connections.append([CITIES[5], 0.025])
CITIES[3].connections.append([CITIES[6], 0.05])
# Kotovsk
CITIES[4].connections.append([CITIES[0], 0.001])
CITIES[4].connections.append([CITIES[5], 0.001])
CITIES[4].connections.append([CITIES[6], 0.005])
# Yuzhne
CITIES[5].connections.append([CITIES[0], 0.05])
CITIES[5].connections.append([CITIES[3], 0.025])
CITIES[5].connections.append([CITIES[6], 0.025])
# Teplodar
CITIES[6].connections.append([CITIES[0], 0.05])
CITIES[6].connections.append([CITIES[1], 0.025])
CITIES[6].connections.append([CITIES[3], 0.05])
CITIES[6].connections.append([CITIES[4], 0.005])
CITIES[6].connections.append([CITIES[5], 0.025])

# Driver
for step in xrange(END):
    for city in CITIES:
        city.euler(step*STEP, step*STEP+STEP, H)
    for city in CITIES:
        city.contagion()

export("./sir-res", CITIES)

# print results
#for step in xrange(END):
#    for city in CITIES:
#        print "%5.2f\t%5.2f\t%5.2f\t%5.2f\t\t"%(city.s[step*STEP], city.i[step*STEP], city.r[step*STEP], city.s[step*STEP] + city.i[step*STEP] + city.r[step*STEP]),
#    print
