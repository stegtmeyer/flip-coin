import random, os, time, datetime, argparse

def askHowManyTimesToFlipCoin():
    timesToFlipCoin = int(input("Enter the number of times you would like the coin to be flipped (n): "))
    return timesToFlipCoin

def askHowManyTimesToRunFlipCoin():
    timesToRunFlipCoin= int(input("Enter the number of times you would like to run n flips: "))
    return timesToRunFlipCoin

def setBetParameters():
	doubleAfterFirstNConsecutiveLosses = (False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
	halveAfterBreakEven = 1
	betParameters = {'minBetSize': 10, 'doubleAfterFirstNConsecutiveLosses': doubleAfterFirstNConsecutiveLosses, 'halveAfterBreakEven': 1}
	return betParameters

def flip(timesToFlipCoin, betParameters):
	i = 0
	numHeads = 0
	numTails = 0
	numHeadsConsecutive = 0
	numTailsConsecutive = 0
	mostHeadsConsecutive = 0
	mostTailsConsecutive = 0
	moneyWon = 0
	numFlipsToBreakeven = 0
	numFlipsToHalving = 0
	amountToBreakeven = 0
	amountForNextHalving = 0
	tryingToBreakeven = False
	currentBetSize = betParameters['minBetSize']
	
	for i in range(timesToFlipCoin):
		flip = random.randrange(2)
		if flip == 0:
			numHeads += 1
			numHeadsConsecutive += 1
			# Assume heads is a win, tails is a loss
			moneyWon += currentBetSize
			if (tryingToBreakeven):
				numFlipsToBreakeven += 1
				numFlipsToHalving += 1
				amountToBreakeven -= currentBetSize
				if (amountToBreakeven <= 0):
					tryingToBreakeven = False
					print("Broke even after [", numFlipsToBreakeven, "] flips")
					numFlipsToBreakeven = 0
					amountToBreakeven = 0
					amountForNextHalving = 0
					numFlipsToHalving = 0
					currentBetSize = betParameters['minBetSize']
				elif (amountToBreakeven <= amountForNextHalving):
						currentBetSize /= 2
						if (currentBetSize == betParameters['minBetSize']):
							amountForNextHalving = 0
						else:
							# hack constant for numConsecutiveLosses before doubling bet size. Will remove as part of major refactor splitting flipping from betting strategy
							amountForNextHalving = amountToBreakeven - 7 * currentBetSize
						print("Halved bet after [", numFlipsToHalving, "] flips", "amountToBreakeven [", amountToBreakeven, "] amountForNextHalving [", amountForNextHalving, "]")
						numFlipsToHalving = 0
			if mostTailsConsecutive < numTailsConsecutive:
				mostTailsConsecutive = numTailsConsecutive
				numTailsConsecutive = 0
			else:
				numTailsConsecutive = 0
		else:
			numTails += 1
			numTailsConsecutive += 1
			# Assume heads is a win, tails is a loss
			moneyWon -= currentBetSize
			if (tryingToBreakeven):
				numFlipsToBreakeven += 1
				amountToBreakeven += currentBetSize

			if len(betParameters["doubleAfterFirstNConsecutiveLosses"]) > numTailsConsecutive:
				if betParameters["doubleAfterFirstNConsecutiveLosses"][numTailsConsecutive] == True:
					tryingToBreakeven = True
					amountToBreakeven = amountToBreakeven + numTailsConsecutive * currentBetSize
					amountForNextHalving = amountToBreakeven - numTailsConsecutive * currentBetSize
					currentBetSize *= 2
					print("Due to [", numTailsConsecutive, "] consecutive losses, doubling bet size to [", currentBetSize, "] in attempt to break even amountToBreakeven [$", amountToBreakeven, "] ", "amountForNextHalving [", amountForNextHalving, "]")
			else:
				print("No instructions for whether to double bet, as doubleAfterFirstNConsecutiveLosses tupple length is shorter than numTailsConsecutive [", numTailsConsecutive, "]")
			if mostHeadsConsecutive < numHeadsConsecutive:
				mostHeadsConsecutive = numHeadsConsecutive
				numHeadsConsecutive = 0
			else:
				numHeadsConsecutive = 0

	# Check for consecutive to account for not going through flip loop again
	if mostTailsConsecutive < numTailsConsecutive:
		mostTailsConsecutive = numTailsConsecutive
	if mostHeadsConsecutive < numHeadsConsecutive:
		mostHeadsConsecutive = numHeadsConsecutive
	
	return numHeads, numTails, mostHeadsConsecutive, mostTailsConsecutive, moneyWon

def calculatePercentagesAndDifference():
	tailsPercent = (100/timesToFlipCoin)*numTails
	headsPercent = (100/timesToFlipCoin)*numHeads
	if numTails > numHeads:
		difference = numTails - numHeads
	elif numHeads > numTails:
		difference = numHeads - numTails
	else:
	    difference = 0
	
	return tailsPercent, headsPercent, difference

def outputAnalysis(statsList):
	mostHeadsConsecutiveAllRuns = 0
	mostTailsConsecutiveAllRuns = 0
	maxDifference = 0
	maxDiffNumHeads = 0
	maxDiffNumTails = 0

	for x in statsList:
		if x["mostHeadsConsecutive"] > mostHeadsConsecutiveAllRuns:
			mostHeadsConsecutiveAllRuns = x["mostHeadsConsecutive"]
		if x["mostTailsConsecutive"] > mostTailsConsecutiveAllRuns:
			mostTailsConsecutiveAllRuns = x["mostTailsConsecutive"]
		if x["difference"] > maxDifference:
			maxDifference = x["difference"]
			maxDiffNumHeads = x["numHeads"]
			maxDiffNumTails = x["numTails"]

	print("\n\n")
	print("---------** ALL Runs Stats **---------")
	print("The max difference between the heads and tails was:", maxDifference, "heads[", maxDiffNumHeads, "]", "tails[", maxDiffNumTails, "]")
	print("The longest string of tails in a row was:", mostTailsConsecutiveAllRuns)
	print("The longest string of heads in a row was:", mostHeadsConsecutiveAllRuns)

# Begin program
parser = argparse.ArgumentParser(description="Simulate n coin flips nr times and display the results.")
parser.add_argument('-n', help='Number of times to flip coin (n)', nargs=1)
parser.add_argument('-nr', help='Number of times to run n flips', nargs=1)
args = parser.parse_args()

print("The following is a program that simulates n coin flips nr times and display the results.")

if args.n == None:
    timesToFlipCoin = askHowManyTimesToFlipCoin()
else:
    timesToFlipCoin = int(args.n[0])

if args.nr == None:
    timesToRunFlipCoin = askHowManyTimesToRunFlipCoin()
else:
    timesToRunFlipCoin = int(args.nr[0])

statsList = []
starttime = time.time()
for j in range(timesToRunFlipCoin):
	betParameters = setBetParameters()
	numHeads, numTails, mostHeadsConsecutive, mostTailsConsecutive, moneyWon = flip(timesToFlipCoin, betParameters)
	tailsPercent, headsPercent, difference = calculatePercentagesAndDifference()
	statsList.append({'numHeads': numHeads, 'numTails': numTails, 'mostHeadsConsecutive': mostHeadsConsecutive, 'mostTailsConsecutive': mostTailsConsecutive, 'tailsPercent': tailsPercent, 'headsPercent': headsPercent, 'difference': difference, 'moneyWon': moneyWon})
	
	print("\n\n")
	print("Tails was flipped", statsList[j]['numTails'], "times, or", statsList[j]['tailsPercent'], "% of the time.")
	print("Heads was flipped", statsList[j]['numHeads'], "times, or", statsList[j]['headsPercent'], "% of the time.")
	print("The difference between the two was", statsList[j]['difference'], ".")
	print("The longest string of tails in a row was:", statsList[j]['mostTailsConsecutive'])
	print("The longest string of heads in a row was:", statsList[j]['mostHeadsConsecutive'])
	print("The amount of money won was: $", statsList[j]['moneyWon'])

outputAnalysis(statsList)