import random, os, time, datetime, argparse

def askHowManyTimesToFlipCoin():
    timesToFlipCoin = int(input("Enter the number of times you would like the coin to be flipped (n): "))
    return timesToFlipCoin

def askHowManyTimesToRunFlipCoin():
    timesToRunFlipCoin= int(input("Enter the number of times you would like to run n flips: "))
    return timesToRunFlipCoin

def flip(timesToFlipCoin):
	i = 0
	numHeads = 0
	numTails = 0
	mostHeadsConsecutive = 0
	mostTailsConsecutive = 0
	tempTailValue = 0
	tempHeadValue = 0
	
	for i in range(timesToFlipCoin):
		flip = random.randrange(2)
		if flip == 0:
			numHeads = numHeads+1
			tempHeadValue = tempHeadValue+1
			if mostTailsConsecutive < tempTailValue:
				mostTailsConsecutive = tempTailValue
				tempTailValue = 0
			else:
				tempTailValue = 0
		else:
			numTails = numTails+1
			tempTailValue = tempTailValue+1
			if mostHeadsConsecutive < tempHeadValue:
				mostHeadsConsecutive = tempHeadValue
				tempHeadValue = 0
			else:
				tempHeadValue = 0

	if mostTailsConsecutive < tempTailValue:
		mostTailsConsecutive = tempTailValue
	if mostHeadsConsecutive < tempHeadValue:
		mostHeadsConsecutive = tempHeadValue
	
	return numHeads, numTails, mostHeadsConsecutive, mostTailsConsecutive

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
	numHeads, numTails, mostHeadsConsecutive, mostTailsConsecutive = flip(timesToFlipCoin)
	tailsPercent, headsPercent, difference = calculatePercentagesAndDifference()
	statsList.append({'numHeads': numHeads, 'numTails': numTails, 'mostHeadsConsecutive': mostHeadsConsecutive, 'mostTailsConsecutive': mostTailsConsecutive, 'tailsPercent': tailsPercent, 'headsPercent': headsPercent, 'difference': difference})
	
	print("\n\n")
	print("Tails was flipped", statsList[j]['numTails'], "times, or", statsList[j]['tailsPercent'], "% of the time.")
	print("Heads was flipped", statsList[j]['numHeads'], "times, or", statsList[j]['headsPercent'], "% of the time.")
	print("The difference between the two was", statsList[j]['difference'], ".")
	print("The longest string of tails in a row was:", statsList[j]['mostTailsConsecutive'])
	print("The longest string of heads in a row was:", statsList[j]['mostHeadsConsecutive'])

outputAnalysis(statsList)