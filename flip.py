import random, os, time, datetime, argparse

numHeads = 0
numTails = 0
i = 0
j = 0
tempTailValue = 0
tempHeadValue = 0
mostTailsConsecutive = 0
mostHeadsConsecutive = 0
tailsPercent = 0
headsPercent = 0
difference = 0
statsList = []

parser = argparse.ArgumentParser(description="Simulate a coin flip a certain amount of times and display the results.")
parser.add_argument('-n', nargs=1)
parser.add_argument('-l', nargs=1)
parser.add_argument('-o', nargs=1)
parser.add_argument('-nr', nargs=1)
args = parser.parse_args()

print("The following is a program that simulates a coin flip a certain amount of times, and displays the results.")

def askHowManyTimesToFlipCoin():
    timesToFlipCoin = int(input("Enter the amount of times you would like the coin to be flipped: "))
    return timesToFlipCoin

def askHowManyTimesToRunFlipCoin():
    timesToRunFlipCoin= int(input("Enter the amount of times you would like to run flip coin: "))
    return timesToRunFlipCoin

def askToLogOrNot():
    logFileYesOrNo = input("Would you like to save a logfile? Y/N: ")
    if logFileYesOrNo.lower() == "y":
        logFileName = input("Log file filename: ")
    else:
        logFileName = "n"
    return logFileName

def askToShowVisualOutput():
    visualOutputYesOrNo = input("Would you like to visually output the result of each toss? Y/N: ").lower()
    return visualOutputYesOrNo

def flip(times):
	global numTails, numHeads, tempTailValue, tempHeadValue, mostTailsConsecutive, mostHeadsConsecutive

	for i in range(times):
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
		if visualOutputYesOrNo == "y":
			print(flip, end=" ")

	if mostTailsConsecutive < tempTailValue:
		mostTailsConsecutive = tempTailValue
	if mostHeadsConsecutive < tempHeadValue:
		mostHeadsConsecutive = tempHeadValue

def calculatePercentagesAndDifference():
	global tailsPercent, headsPercent, difference

	tailsPercent = (100/timesToFlipCoin)*numTails
	headsPercent = (100/timesToFlipCoin)*numHeads
	if numTails > numHeads:
		difference = numTails - numHeads
	elif numHeads > numTails:
	    difference = numHeads - numTails
	else:
	    difference = 0

"""
	elapsedtime = str(datetime.timedelta(seconds=round(time.time()-starttime, 2)))
	elapsedtime = elapsedtime[:-4]
"""
def outputAnalysis():
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


def outputLogFile():
	if logFileName.lower() != "n":
		logfile = open(os.getcwd()+'/'+logFileName, 'w')
		logfile.write("Flipped a coin " + str(timesToFlipCoin) + " times.\n")
		logfile.write("Total execution time: " + str(elapsedtime) + "\n")
		logfile.write("Tails was flipped " + str(numTails) + " times, or " + str(tailsPercent) + "% of the time.\n")
		logfile.write("Heads was flipped " + str(numHeads) + " times, or " + str(headsPercent) + "% of the time.\n")
		logfile.write("The difference between the two was " + str(difference) + ".\n")
		logfile.write("The longest string of tails in a row was " + str(mostTailsConsecutive) + ".\n")
		logfile.write("The longest string of heads in a row was " + str(mostHeadsConsecutive) + ".\n")
		logfile.write("The amount of time taken to flip each coin on average was " + str(estimate) + ".\n")
		logfile.close()
		print("A logfile was published to ", os.getcwd()+'/'+logFileName)
	else:
		print("No log created.")

if args.n == None:
    timesToFlipCoin = askHowManyTimesToFlipCoin()
else:
    timesToFlipCoin = int(args.n[0])

if args.nr == None:
    timesToRunFlipCoin = askHowManyTimesToRunFlipCoin()
else:
    timesToRunFlipCoin = int(args.nr[0])

if args.l == None:
    logFileName = askToLogOrNot()
elif args.l[0].lower() != "no" or args.l[0].lower() != "n":
    logFileName = args.l[0]
else:
    logFileName = "n"

if args.o == None:
    visualOutputYesOrNo = askToShowVisualOutput()
else:
    visualOutputYesOrNo = args.o[0].lower()

starttime = time.time()
for j in range(timesToRunFlipCoin):
	flip(timesToFlipCoin)
	calculatePercentagesAndDifference()
	statsList.append({'numHeads': numHeads, 'numTails': numTails, 'mostHeadsConsecutive': mostHeadsConsecutive, 'mostTailsConsecutive': mostTailsConsecutive, 'tailsPercent': tailsPercent, 'headsPercent': headsPercent, 'difference': difference})

	i = 0
	numHeads = 0
	numTails = 0
	tempTailValue = 0
	tempHeadValue = 0
	mostTailsConsecutive = 0
	mostHeadsConsecutive = 0
	tailsPercent = 0
	headsPercent = 0
	difference = 0

j = 0
for j in range(timesToRunFlipCoin):
	print("\n\n")
	print("Tails was flipped", statsList[j]['numTails'], "times, or", statsList[j]['tailsPercent'], "% of the time.")
	print("Heads was flipped", statsList[j]['numHeads'], "times, or", statsList[j]['headsPercent'], "% of the time.")
	print("The difference between the two was", statsList[j]['difference'], ".")
	print("The longest string of tails in a row was:", statsList[j]['mostTailsConsecutive'])
	print("The longest string of heads in a row was:", statsList[j]['mostHeadsConsecutive'])

outputAnalysis()
outputLogFile()