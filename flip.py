import random, os, time, datetime, argparse

def analyzeOneRun(flipResults):
	numHeads = 0
	numTails = 0
	mostHeadsConsecutive = 0
	mostTailsConsecutive = 0
	numTailsConsecutive = 0
	numHeadsConsecutive = 0
	flipsAnalysis = {}
	
	for i in range(len(flipResults)):
		if flipResults[i] == 0:
			numHeads += 1
			numHeadsConsecutive += 1
			if mostTailsConsecutive < numTailsConsecutive:
				mostTailsConsecutive = numTailsConsecutive
				numTailsConsecutive = 0
			else:
				numTailsConsecutive = 0
		else:
			numTails += 1
			numTailsConsecutive += 1
			if mostHeadsConsecutive < numHeadsConsecutive:
				mostHeadsConsecutive = numHeadsConsecutive
				numHeadsConsecutive = 0
			else:
				numHeadsConsecutive = 0

	if mostTailsConsecutive < numTailsConsecutive:
		mostTailsConsecutive = numTailsConsecutive
	if mostHeadsConsecutive < numHeadsConsecutive:
		mostHeadsConsecutive = numHeadsConsecutive

	tailsPercent, headsPercent, difference = calculatePercentagesAndDifference(numHeads, numTails)
	flipsAnalysis = {
			'numHeads': numHeads, 
			'numTails': numTails, 
			'mostHeadsConsecutive': mostHeadsConsecutive, 
			'mostTailsConsecutive': mostTailsConsecutive, 
			'tailsPercent': tailsPercent, 
			'headsPercent': headsPercent, 
			'difference': difference
			}

	return flipsAnalysis

def flip(timesToFlipCoin):
	i = 0
	flipResults = []
	
	for i in range(timesToFlipCoin):
		flip = random.randrange(2)
		flipResults.append(flip)
	
	return flipResults

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
	j = 0
	for j in range(len(flipsAnalysis)):
		print("\n")
		print("Tails was flipped", flipsAnalysis[j]['numTails'], "times, or", flipsAnalysis[j]['tailsPercent'], "% of the time.")
		print("Heads was flipped", flipsAnalysis[j]['numHeads'], "times, or", flipsAnalysis[j]['headsPercent'], "% of the time.")
		print("The difference between the two was", flipsAnalysis[j]['difference'], ".")
		print("The longest string of tails in a row was:", flipsAnalysis[j]['mostTailsConsecutive'])
		print("The longest string of heads in a row was:", flipsAnalysis[j]['mostHeadsConsecutive'])

def userOutputMultipleRunAnalysis(flipsAnalysis):
	multipleRunsAnalysis = []
	multipleRunsAnalysis = analyzeMultipleRuns(flipsAnalysis)
	print("\n")
	print("---------** ALL Runs Stats **---------")
	print("The max difference between the heads and tails was:", multipleRunsAnalysis["maxDifference"], "heads[", multipleRunsAnalysis["maxDiffNumHeads"], "]", "tails[", multipleRunsAnalysis["maxDiffNumTails"], "]")
	print("The longest string of tails in a row was:", multipleRunsAnalysis["mostTailsConsecutiveAllRuns"])
	print("The longest string of heads in a row was:", multipleRunsAnalysis["mostHeadsConsecutiveAllRuns"])

def getBetStrategyOne():
	doubleAfterFirstNConsecutiveLosses = (False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
	halveAfterBreakEven = True
	betStrategy = {'minBetSize': 10, 'doubleAfterFirstNConsecutiveLosses': doubleAfterFirstNConsecutiveLosses, 'halveAfterBreakEven': True}
	return betStrategy

def applyBetStrategyToOneFlipRun(flipsRun, betStrategy):
	i = 0
	betStrategyResult = {}
	moneyWon = 0
	for i in range(len(flipsRun)):
		if flipsRun[i] == 0:
			moneyWon += betStrategy['minBetSize']
		else:
			moneyWon -= betStrategy['minBetSize']

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
userOutputEachRunAnalysis(flipsAnalysis)
userOutputMultipleRunAnalysis(flipsAnalysis)

betStrategy = getBetStrategyOne()
betStrategyResults = applyBetStrategyToMultipleFlipRuns(flipsRuns, betStrategy)
userOutputBetStrategyResults(betStrategyResults)