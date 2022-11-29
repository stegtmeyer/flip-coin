import random, os, time, datetime, argparse

def flip(timesToFlipCoin):
	i = 0
	flipResults = []
	
	for i in range(timesToFlipCoin):
		flip = random.randrange(2)
		flipResults.append(flip)
	
	return flipResults

def analyzeOneRun(flipResults):
	numHeads = 0
	numTails = 0
	mostHeadsConsecutive = 0
	mostTailsConsecutive = 0
	numTailsConsecutive = 0
	numHeadsConsecutive = 0
	tailsConsecutiveList = []
	headsConsecutiveList = []
	flipsAnalysis = {}

	# Initializing assuming we will not have more consecutive flips in a row than listed
	for i in range(40):
		tailsConsecutiveList.append(0)
	for i in range(40):
		headsConsecutiveList.append(0)
	
	for i in range(len(flipResults)):
		if flipResults[i] == 0:
			numHeads += 1
			numHeadsConsecutive += 1
			if numTailsConsecutive > 0:
				tailsConsecutiveList[numTailsConsecutive] += 1
				numTailsConsecutive = 0
		else:
			numTails += 1
			numTailsConsecutive += 1
			if numHeadsConsecutive > 0:
				headsConsecutiveList[numHeadsConsecutive] += 1
				numHeadsConsecutive = 0

	if numTailsConsecutive > 0:
		tailsConsecutiveList[numTailsConsecutive] += 1
	else:
		headsConsecutiveList[numHeadsConsecutive] += 1

	for i in range(39, 0, -1):
		if tailsConsecutiveList[i] > 0:
			mostTailsConsecutive = i
			break

	for i in range(39, 0, -1):
		if headsConsecutiveList[i] > 0:
			mostHeadsConsecutive = i
			break

	tailsPercent, headsPercent, difference = calculatePercentagesAndDifference(numHeads, numTails)
	flipsAnalysis = {
			'numHeads': numHeads, 
			'numTails': numTails, 
			'mostHeadsConsecutive': mostHeadsConsecutive, 
			'mostTailsConsecutive': mostTailsConsecutive, 
			'headsConsecutiveList': headsConsecutiveList,
			'tailsConsecutiveList': tailsConsecutiveList,
			'tailsPercent': tailsPercent, 
			'headsPercent': headsPercent, 
			'difference': difference
			}

	return flipsAnalysis

def calculatePercentagesAndDifference(numHeads, numTails):
	tailsPercent = (100/timesToFlipCoin)*numTails
	headsPercent = (100/timesToFlipCoin)*numHeads
	if numTails > numHeads:
		difference = numTails - numHeads
	elif numHeads > numTails:
		difference = numHeads - numTails
	else:
		difference = 0

	return tailsPercent, headsPercent, difference

def analyzeMultipleRuns(flipsAnalysis):
	mostHeadsConsecutiveAllRuns = 0
	mostTailsConsecutiveAllRuns = 0
	maxDifference = 0
	maxDiffNumHeads = 0
	maxDiffNumTails = 0
	multipleRunsAnalysis = {}

	for x in flipsAnalysis:
		if x["mostHeadsConsecutive"] > mostHeadsConsecutiveAllRuns:
			mostHeadsConsecutiveAllRuns = x["mostHeadsConsecutive"]
		if x["mostTailsConsecutive"] > mostTailsConsecutiveAllRuns:
			mostTailsConsecutiveAllRuns = x["mostTailsConsecutive"]
		if x["difference"] > maxDifference:
			maxDifference = x["difference"]
			maxDiffNumHeads = x["numHeads"]
			maxDiffNumTails = x["numTails"]

	multipleRunsAnalysis = {'maxDifference': maxDifference, 'maxDiffNumHeads': maxDiffNumHeads, 'maxDiffNumTails': maxDiffNumTails, 'mostTailsConsecutiveAllRuns': mostTailsConsecutiveAllRuns, 'mostHeadsConsecutiveAllRuns': mostHeadsConsecutiveAllRuns}

	return multipleRunsAnalysis

def getUserInput():
	parser = argparse.ArgumentParser(description="Simulate n coin flips nr times and display the results.")
	parser.add_argument('-n', help='Number of times to flip coin (n)', nargs=1)
	parser.add_argument('-nr', help='Number of times to run n flips', nargs=1)
	args = parser.parse_args()

	if args.n == None:
		timesToFlipCoin = int(input("Enter the number of times you would like the coin to be flipped (n): "))
	else:
		timesToFlipCoin = int(args.n[0])

	if args.nr == None:
		timesToRunFlipCoin = int(input("Enter the number of times you would like to run n flips: "))
	else:
		timesToRunFlipCoin = int(args.nr[0])

	return timesToFlipCoin, timesToRunFlipCoin

def getFlipsRuns(timesToFlipCoin, timesToRunFlipCoin):
	flipsRuns = []
	j = 0
	for j in range(timesToRunFlipCoin):
		flipsRuns.append(flip(timesToFlipCoin))

	return flipsRuns

def getFlipAnalysis(flipsRuns):
	flipsAnalysis = []
	j = 0
	for j in range(len(flipsRuns)):
		flipsAnalysis.append(analyzeOneRun(flipsRuns[j]))

	return flipsAnalysis

def userOutputEachRunAnalysis(flipsAnalysis):
	for i in range(len(flipsAnalysis)):
		print("\n")
		print("Tails was flipped", flipsAnalysis[i]['numTails'], "times, or", flipsAnalysis[i]['tailsPercent'], "% of the time.")
		print("Heads was flipped", flipsAnalysis[i]['numHeads'], "times, or", flipsAnalysis[i]['headsPercent'], "% of the time.")
		print("The difference between the two was", flipsAnalysis[i]['difference'], ".")
		print("The longest string of tails in a row was:", flipsAnalysis[i]['mostTailsConsecutive'])
		print("The longest string of heads in a row was:", flipsAnalysis[i]['mostHeadsConsecutive'])
		for j in range(39, 0, -1):
			if flipsAnalysis[i]['headsConsecutiveList'][j] > 0:
				print("Number of instances of [", j, "] consecutive heads is [", flipsAnalysis[i]['headsConsecutiveList'][j], "]")
			if flipsAnalysis[i]['tailsConsecutiveList'][j] > 0:
				print("Number of instances of [", j, "] consecutive tails is [", flipsAnalysis[i]['tailsConsecutiveList'][j], "]")

def userOutputMultipleRunAnalysis(flipsAnalysis):
	multipleRunsAnalysis = []
	multipleRunsAnalysis = analyzeMultipleRuns(flipsAnalysis)
	print("\n")
	print("---------** ALL Runs Stats **---------")
	print("The max difference between the heads and tails was:", multipleRunsAnalysis["maxDifference"], "heads[", multipleRunsAnalysis["maxDiffNumHeads"], "]", "tails[", multipleRunsAnalysis["maxDiffNumTails"], "]")
	print("The longest string of tails in a row was:", multipleRunsAnalysis["mostTailsConsecutiveAllRuns"])
	print("The longest string of heads in a row was:", multipleRunsAnalysis["mostHeadsConsecutiveAllRuns"])

def getBetStrategyOne():
	doubleAfterFirstNConsecutiveLosses = (False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
	halveAfterBreakEven = True
	betStrategy = {'minBetSize': 10, 'doubleAfterFirstNConsecutiveLosses': doubleAfterFirstNConsecutiveLosses, 'halveAfterBreakEven': True}
	return betStrategy

def applyBetStrategyToOneFlipRun(flipsRun, betStrategy):
	i = 0
	betStrategyResult = {}
	moneyWon = 0
	numTailsConsecutive = 0
	currentBetSize = betStrategy['minBetSize']
	amountToBreakEven = [0]

	for i in range(len(flipsRun)):
		if flipsRun[i] == 0:
			numTailsConsecutive = 0
			moneyWon += currentBetSize
			if betStrategy['halveAfterBreakEven'] and amountToBreakEven[-1] > 0:
				amountToBreakEven[-1] -= currentBetSize
				if amountToBreakEven[-1] <= 0:
					currentBetSize /= 2
					amountToBreakEven.pop()
					print("\nHalving bet size to [", currentBetSize, "] with new amountToBreakEven [", amountToBreakEven[-1], "] with moneywon [", moneyWon, "]")

		else:
			numTailsConsecutive += 1
			moneyWon -= currentBetSize
			if betStrategy['doubleAfterFirstNConsecutiveLosses'][numTailsConsecutive]:
				if betStrategy['halveAfterBreakEven']:
					amountToBreakEven.append(currentBetSize * numTailsConsecutive)
				currentBetSize *= 2	
				print("\nDoubling bet size to [", currentBetSize, "] with amountToBreakEven [", amountToBreakEven[-1], "] with moneywon [", moneyWon, "]")

	betStrategyResult = {'moneyWon': moneyWon}

	return betStrategyResult

def applyBetStrategyToMultipleFlipRuns(flipsRuns, betStrategy):
	i = 0
	betStrategyResults = []
	for i in range(len(flipsRuns)):
		betStrategyResults.append(applyBetStrategyToOneFlipRun(flipsRuns[i], betStrategy))

	return betStrategyResults

def userOutputBetStrategyResults(betStrategyResults):
	i = 0
	for i in range(len(betStrategyResults)):
		print("\nAmount of money won in run [", i, "] is: $", betStrategyResults[i]['moneyWon'])


# -----------------------------
# ------- Begin Program -------
# -----------------------------
timesToFlipCoin, timesToRunFlipCoin = getUserInput()

print("\nThe following simulates [", timesToFlipCoin, "] coin flips [", timesToRunFlipCoin, "] times and displays the results.")

flipsRuns = getFlipsRuns(timesToFlipCoin, timesToRunFlipCoin)
flipsAnalysis = getFlipAnalysis(flipsRuns)
betStrategy = getBetStrategyOne()
betStrategyResults = applyBetStrategyToMultipleFlipRuns(flipsRuns, betStrategy)

userOutputEachRunAnalysis(flipsAnalysis)
userOutputBetStrategyResults(betStrategyResults)
userOutputMultipleRunAnalysis(flipsAnalysis)