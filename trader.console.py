#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.
import pdb
import sys
from timeit import default_timer as timer

import IPython

import random
import operator
import csv
import itertools

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import quantiacsToolbox


class Strat(object):

    strategy = None

    def myTradingSystem(self, DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
        ''' This system uses trend following techniques to allocate capital into the desired equities'''

        #print "context: ",pset.context

        code = self.strategy.__str__()
        #print "code: ",code
        func = toolbox.compile(expr=code)

        #print "OPEN: ",OPEN.shape
        #print OPEN[-1,0]

        vector = [OPEN[-1,0],HIGH[-1,0],LOW[-1,0],CLOSE[-1,0],VOL[-1,0],OPEN,HIGH,LOW,CLOSE,VOL]
        #vector = [OPEN[-1,0],HIGH[-1,0],LOW[-1,0],CLOSE[-1,0],VOL[-1,0],OPEN[-1,0],HIGH[-1,0],LOW[-1,0],CLOSE[-1,0],VOL[-1,0]]
        #vector = [OPEN[-1,0],HIGH[-1,0],LOW[-1,0],CLOSE[-1,0],VOL[-1,0]]
        #print "vector: ",vector[:5]

        result = func(*vector)

        #sys.stdout.write(str(result)+" ")
        
        #pdb.set_trace()

        nMarkets=CLOSE.shape[1]

        #periodLonger=100
        #periodShorter=20
        #
        ## Calculate Simple Moving Average (SMA)
        #smaLongerPeriod=numpy.nansum(CLOSE[-periodLonger:,:],axis=0)/periodLonger
        #smaShorterPeriod=numpy.nansum(CLOSE[-periodShorter:,:],axis=0)/periodShorter
        #
        #longEquity= smaShorterPeriod > smaLongerPeriod
        #shortEquity= ~longEquity
        ##
        #pos=numpy.zeros(nMarkets)
        #pos[longEquity]=1
        #pos[shortEquity]=-1
        ##
        #weights = pos/numpy.nansum(abs(pos))
        #
        #return weights, settings

        #print result
        EntCondL = result
        ExCondL = not(EntCondL)
        
        pos=numpy.zeros(nMarkets)
        MarketPositionLong = settings['MarketPositionLong']
        
        if MarketPositionLong == True:
            if ExCondL == True:
                pos[0] = 0
                pos[1] = 0
                #log.write("Exit %s %s\n" % (DATE[-1],CLOSE[-1]))
        
        if EntCondL:
            pos[0] = 1
            pos[1] = 1
            #log.write("Enter %s %s\n" % (DATE[-1],CLOSE[-1]))
        
        MarketPositionLong = reduce(lambda p1, p2: p1 > 0 and p2 > 0, pos)
        settings['MarketPositionLong'] = MarketPositionLong

        #print "pos:",pos

        # increase count
        settings['iteration'] += 1

        #return weights, settings
        return pos, settings


    def mySettings(self):
        ''' Define your trading system settings here '''
        
        settings= {}
        
        # Futures Contracts

        #settings['markets']  = ['CASH','F_AD', 'F_BO', 'F_BP', 'F_C', 'F_CC', 'F_CD',
        #                        'F_CL', 'F_CT', 'F_DX', 'F_EC', 'F_ED', 'F_ES', 'F_FC','F_FV', 'F_GC',
        #                        'F_HG', 'F_HO', 'F_JY', 'F_KC', 'F_LB', 'F_LC', 'F_LN', 'F_MD', 'F_MP',
        #                        'F_NG', 'F_NQ', 'F_NR', 'F_O', 'F_OJ', 'F_PA', 'F_PL', 'F_RB', 'F_RU',
        #                        'F_S','F_SB', 'F_SF', 'F_SI', 'F_SM', 'F_TU', 'F_TY', 'F_US','F_W', 'F_XX',
        #                        'F_YM']
        settings['markets'] = ['F_AD','F_AD']
        settings['beginInSample'] = '20120506'
        settings['endInSample'] = '20150506'
        settings['lookback']= 504
        #settings['lookback']= 100
        settings['budget']= 10**6
        settings['slippage']= 0.05

        settings['iteration']= 0

        nMarkets=len(settings['markets'])
        settings['MarketPositionLong']= False

        return settings


# Read the spam list features and put it in a list of lists.
# The dataset is from http://archive.ics.uci.edu/ml/datasets/Spambase
# This example is a copy of the OpenBEAGLE example :
# http://beagle.gel.ulaval.ca/refmanual/beagle/html/d2/dbe/group__Spambase.html
#with open("spambase/spambase.csv") as spambase:
#    spamReader = csv.reader(spambase)
#    spam = list(list(float(elem) for elem in row) for row in spamReader)

# defined a new primitive set for strongly typed GP
#pset = gp.PrimitiveSetTyped("MAIN", itertools.repeat(float, 10), bool)

class Vector(object): pass

pset = gp.PrimitiveSetTyped("MAIN", (float, float, float, float, float, Vector, Vector, Vector, Vector, Vector), bool)
#pset = gp.PrimitiveSetTyped("MAIN", itertools.repeat(float, 5), bool)

#pdb.set_trace()

# boolean operators
pset.addPrimitive(operator.and_, [bool, bool], bool)
pset.addPrimitive(operator.or_, [bool, bool], bool)
pset.addPrimitive(operator.not_, [bool], bool)

# floating point operators
# Define a protected division function
def protectedDiv(left, right):
    try: return left / right
    except ZeroDivisionError: return 1

pset.addPrimitive(operator.add, [float,float], float)
pset.addPrimitive(operator.sub, [float,float], float)
pset.addPrimitive(operator.mul, [float,float], float)
pset.addPrimitive(protectedDiv, [float,float], float)

# logic operators
# Define a new if-then-else function
def if_then_else(input, output1, output2):
    if input: return output1
    else: return output2

class Lookback(object): pass


#def converter(price,lb):
#    return price

def ident(scalar):
    return scalar

def identvec(vec):
    return vec

def average(PRICE, window):
    sma = numpy.nansum(PRICE[-window:,:],axis=0)/window
    return sma[0]

pset.addPrimitive(operator.lt, [float, float], bool)
pset.addPrimitive(operator.eq, [float, float], bool)
pset.addPrimitive(if_then_else, [bool, float, float], float)
#pset.addPrimitive(converter, [float,Lookback], float)
pset.addPrimitive(ident, [Lookback], Lookback)  ##cg add dummy w/ Lookback output or barf
# IndexError: The gp.generate function tried to add a primitive of type '<class '__main__.Vector'>', but there is none available.
pset.addPrimitive(identvec, [Vector], Vector)  ##cg add dummy w/ Vector output or barf
pset.addPrimitive(average, [Vector, Lookback], float)

pset.renameArguments(ARG0='OPENARG')
pset.renameArguments(ARG1='HIGHARG')
pset.renameArguments(ARG2='LOWARG')
pset.renameArguments(ARG3='CLOSEARG')
pset.renameArguments(ARG4='VOLARG')
pset.renameArguments(ARG5='OPENVEC')
pset.renameArguments(ARG6='HIGHVEC')
pset.renameArguments(ARG7='LOWVEC')
pset.renameArguments(ARG8='CLOSEVEC')
pset.renameArguments(ARG9='VOLVEC')

# terminals
pset.addEphemeralConstant("rand100", lambda: int(random.random() * 100), float)
pset.addEphemeralConstant("rand101", lambda: int(random.random() * 100), Lookback)
pset.addTerminal(False, bool)
pset.addTerminal(True, bool)

#print pset.ret
#print pset.primitives[pset.ret]

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalSecurities(individual):
    #print "strategy: ",individual.__str__()
    # Transform the tree expression in a callable function
    code = str(individual)
    print
    print "code: ",code
    func = toolbox.compile(expr=individual)
    #pdb.set_trace()
    # Randomly sample 400 mails in the spam database
    #spam_samp = random.sample(spam, 400)
    # Evaluate the sum of correctly identified mail as spam
    #result = sum(bool(func(*mail[:5])) is bool(mail[57]) for mail in spam_samp)

    strat = Strat()
    strat.strategy = individual
    #pdb.set_trace()
    result = quantiacsToolbox.runts(strat, plotEquity=False)

    sharpe = result['stats']['sharpe']

    if numpy.isnan(sharpe):
        sharpe = -10
        
    print "sharpe: ",sharpe

    #print result

    #pdb.set_trace()

    #try: 
    #    print individual[0].seq
    #except:
    #    #pdb.set_trace()
    #    pass

    return sharpe,
    
toolbox.register("evaluate", evalSecurities)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    #random.seed(10)
    random.seed(1234)
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    #stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    #_ , logbook = algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 40, stats, halloffame=hof)
    _ , logbook = algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 40, stats, halloffame=hof, verbose=True)

    return pop, stats, hof, logbook

if __name__ == "__main__":
    start = timer()
    #popu, stats, hof, logbook = main()
    IPython.embed()
    
    end = timer()
    delta = end - start
    print
    print logbook
    print "time ", delta
    print "BEST:"
    print "code: ",hof[0]
    print "stats: ",stats.compile(popu)

    #pdb.set_trace()

    gen = logbook.select("gen")
    fit_mins = logbook.chapters["fitness"].select("max")
    size_avgs = logbook.chapters["size"].select("avg")

    import matplotlib.pyplot as plt

    fig, ax1 = plt.subplots()
    line1 = ax1.plot(gen, fit_mins, "b-", label="Maximum Fitness")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness", color="b")
    for tl in ax1.get_yticklabels():
        tl.set_color("b")

    ax2 = ax1.twinx()
    line2 = ax2.plot(gen, size_avgs, "r-", label="Average Size")
    ax2.set_ylabel("Size", color="r")
    for tl in ax2.get_yticklabels():
        tl.set_color("r")

    lns = line1 + line2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="center right")

    plt.show()
