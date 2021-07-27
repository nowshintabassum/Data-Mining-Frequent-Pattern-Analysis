from collections import defaultdict, OrderedDict
from csv import reader
import time
from itertools import chain, combinations
from optparse import OptionParser
from fpgrowth_py.utils import *

start_time = time.time()
def fpgrowth(itemSetList, minSupRatio, minConf):
    frequency = getFrequencyFromList(itemSetList)
    minSup = len(itemSetList) * minSupRatio
    fpTree, headerTable = constructTree(itemSetList, frequency, minSup)
    if(fpTree == None):
        print('No frequent item set')
    else:
        freqItems = []
        mineTree(headerTable, minSup, set(), freqItems)
        rules = associationRule(freqItems, itemSetList, minConf)
        return freqItems, rules

def fpgrowthFromFile(fname, minSupRatio, minConf):
    itemSetList, frequency = getFromFile(fname)
    minSup = len(itemSetList) * minSupRatio
    fpTree, headerTable = constructTree(itemSetList, frequency, minSup)
    if(fpTree == None):
        print('No frequent item set')
    else:
        freqItems = []
        mineTree(headerTable, minSup, set(), freqItems)
        rules = associationRule(freqItems, itemSetList, minConf)
        return freqItems, rules

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='inputFile',
                         help='CSV filename',
                         default='sleep-analysis_output.csv')
    optparser.add_option('-s', '--minSupport',
                         dest='minSup',
                         help='Min support (float)',
                         default=0.4,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minConf',
                         help='Min confidence (float)',
                         default=0.7,
                         type='float')

    (options, args) = optparser.parse_args()

    freqItemSet, rules = fpgrowthFromFile(
        options.inputFile, options.minSup, options.minConf)
    for item in freqItemSet:
        print("item : ",item)
    print("======================================================")
    print("RULES : ")
    for rule in rules:
        print(str(rule[0])+'-->' + str(rule[1]) + ' Confidence : ',rule[2])

    print("================================")
    print("TIME REQUIRED : ")
    print(time.time() - start_time, "seconds")