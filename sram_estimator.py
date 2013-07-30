import sys
from SRAMPowerEstimator import *

def parseSpecFile(fileName):
	fp = open(fileName, 'r')
	specs = {16:[], 32:[], 64:[], 96:[], 128:[]}
	for line in fp:
		t = line.split()
		sr = int(t[0])
		for i in range(1,len(t)):
			specs[sr].append(float(t[i]))
	fp.close()
	return specs

numViews = int(sys.argv[1])
simFile = open(sys.argv[2])
specs = parseSpecFile(sys.argv[3])

VIEWS = 3.0
viewRatio = numViews / VIEWS

for line in simFile:
	tokens = line.split()
	label = tokens[0]
	sr = int(tokens[1])
	timeRatio = float(tokens[2])
	leakReduction = float(tokens[3])
	unmergedRD = int(tokens[4]) * viewRatio 
	mergedRD = int(tokens[5]) * viewRatio
	wrMBDRLevelC = int(tokens[6]) * viewRatio
	wrMBDRLevelCPlus = int(tokens[7]) * viewRatio
	wrRCDR = int(tokens[8]) * viewRatio

	#LevelC
	leakPower = 4 * specs[sr][2]
	accEnergy = specs[sr][3]
	levelCParams = [timeRatio, 1.0, unmergedRD, wrMBDRLevelC]
	levelCPower = SRAMPowerEstimator(leakPower, accEnergy)
	resultLevelC = levelCPower.estimate(levelCParams)

	
	#LevelC+
	leakPower = 4 * specs[sr][0]
	accEnergy = specs[sr][1]
	levelCPlusParams = [timeRatio, 1.0, unmergedRD, wrMBDRLevelCPlus]
	levelCPlusPower = SRAMPowerEstimator(leakPower, accEnergy)
	resultLevelCPlus = levelCPlusPower.estimate(levelCPlusParams)


	#RCDR w/o Power Gating and Block Merging
	leakPower = specs[sr][2]
	accEnergy = specs[sr][3]
	rcdrParams = [timeRatio, 1.0, unmergedRD, wrRCDR]
	rcdrPower = SRAMPowerEstimator(leakPower, accEnergy)
	resultRCDR = rcdrPower.estimate(rcdrParams)

	
	#RCDR with Power Gating and Block Merging (PGBM)
	leakPower = specs[sr][2]
	accEnergy = specs[sr][3]
	rcdrPGBMParams = [timeRatio, leakReduction, mergedRD, wrRCDR]
	rcdrPGBMPower = SRAMPowerEstimator(leakPower, accEnergy)
	resultRCDR_PGBM = rcdrPGBMPower.estimate(rcdrPGBMParams)

	print label, numViews, sr, resultLevelC, resultLevelCPlus, resultRCDR, resultRCDR_PGBM
