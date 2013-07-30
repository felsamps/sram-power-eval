class SRAMPowerEstimator:
	def __init__(self, leakPower, accEnergy):
		self.leakPower = leakPower * 0.001
		self.accEnergy = accEnergy * 0.000000001

	def estimate(self, params):
		timeRatio = params[0]
		leakReduction = params[1]
		accRD = params[2]
		accWR = params[3]

		totalLeakPower = self.leakPower * leakReduction
		totalDynPower = (accRD + accWR) * self.accEnergy * timeRatio
		totalPower = totalLeakPower + totalDynPower

		returnable = ''
		returnable += str(totalLeakPower) + ' '
		returnable += str(totalDynPower) + ' '
		returnable += str(totalPower)

		return returnable	

