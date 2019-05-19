# The script to be run for our Sorting Algorithms Using the Strategy Design Pattern

import strategy
import random
import pdb
import time

NUM_OPTIONS = 7


# The context class in our strategy design pattern
class Context:
	def __init__(self, strategy, numbers):
		self.strategy = strategy
		self.numbers = numbers;
	
	def changeStrategy(self, strategy):
		self.strategy = strategy



# Helper functions for our main function

# Used for validating user input
def getChoice(low, high):
	while True:
		try:
			choice = int(input("Type Number Here: "))
			if low <= choice <= high:
				break
			else:
				print("Sorry, that is not a valid number, try again")
				continue
		except:
			print("Sorry, that was not a number, try again")
	return choice


# Util function to utilize the dynamic switching using the Strategy Pattern
def getAlgorithm(dictionary, key):
	output = dictionary[key]
	return output

# Uses list comprehension to generate a random list for our application
def generateRandomNumberList(size, high):
	myList = [random.randint(0,high) for _ in range(size)]
	return myList

# Used if a user wants to input their own list
def generateOwnList():
	print("Enter each number followed by enter")
	print("When you are finished, type DONE")
	ownList = []
	while True:
		try:
			num = input("Type the number here: ")
			if num == "DONE":
				if len(ownList) == 0:
					print("Sorry, the size of the list cannot be zero")
					continue
				else:
					break;
			else:
				num = int(num)
				ownList.append(num)
		except:
			print("Sorry, that was not not a number, try again")
	return ownList

# Utility function to help the user set up their list to be run
def genNumListSetUp():
	returnList = None
	print("Would you like to input your own list [1] or use a randomly generated List [2]?")
	listChoice = getChoice(1, 2)
	if listChoice == 2:
		print("Enter the size of the list (max size is 1,000,000,000,000)")
		size = getChoice(1, 1000000000000)
		print("Enter the range of the numbers (will range from 0 to the number you enter) ")
		listRange = getChoice(1, 100000000000000000000)
		return generateRandomNumberList(size, listRange)
	else: 
		# entering their own list
		return generateOwnList()


# Display list (before sorting; input)
def displayList(theList):
	inputFile = open("inputFile.txt", "w+")
	if len(theList) <= 100:
		print("Here is the list of numbers")
		for x in theList:
			print("{}".format(x))
			inputFile.write("\n {}".format(x))
	else:
		print("Oops, the list was too big; check the input file for all the numbers.")
		for x in theList:
			inputFile.write("\n {}".format(x))


# Display the sorted list and write to file
def displayListAndWriteToFile(theList, time):
	outputFile = open("output.txt", "w+")
	if len(theList) <= 100:
		print("Here is the sorted list of numbers")
		for x in theList:
			print("{}".format(x))
			outputFile.write("\n {}".format(x))
	else:
		print("Oops, the list was too big; check the output file for the results.")
		for x in theList:
			outputFile.write("\n {}".format(x))
	
	outputFile.write("\n The time taken was {} seconds".format(time))
	print("\n The time taken was {} seconds".format(time))

def getRuntime(start, end):
	runtime = end - start
	runtimeSeconds = runtime / (10**9)
	return runtimeSeconds

# This method will run the "race". It will sort the numbers using all of the algorithms, and tell the user which one was the fastest. ++
def runRace(numbers, dict):
	keepStats = {}
	print("Who do you think will win? Type the number")
	print("Here are the choices, in case you forgot")
	print("\t 1: BubbleSort \n \t 2: InsertionSort \n \t 3: QuickSort \n \t 4: MergeSort \n \t 5: SelectionSort \n \t 6: HeapSort \n \t 7: QuickSelect (median)")
	winner = getChoice(1, NUM_OPTIONS)
	raceFile = open("RaceFile.txt", "w+")
	winnerSoFar = [1]
	timeSoFar = 10000000000000000000000000 # Placeholder, it will obviously be beat
	for key, value in dict.items():
		context = Context(value, numbers)
		# time the algorithm
		start = time.time_ns()
		sortedList = context.strategy().runAlgorithm(numbers)
		# Call helper function to get the runtime
		end = time.time_ns()
		runtime = getRuntime(start, end)
		if runtime < timeSoFar:
			timeSoFar = runtime
			winnerSoFar = [int(key)]
		elif runtime == timeSoFar:
			winnerSoFar.append(key)
		raceFile.write("The time for {} was {} seconds \n".format(dict[str(key)], timeSoFar))
		keepStats[key] = runtime

	if len(winnerSoFar) > 1:
		print("There was a tie")
		print("The winning time was {} second".format(runtime))
		for item in winnerSoFar:
			print("{} had this time".format(dict[item]))
	else:
		print("The winner was {}". format(dict[str(winnerSoFar[0])]))
		print("The winning time was {}".format(runtime))

	if winner in winnerSoFar:
		print("Congratulations, you guessed it!")
	else:
		print("Better luck next time")


def main():
	while True:
		# Programmatic entry point into the project
		# Welcome messages, asking user which algorithm they would like to run today
		print("Welcome to the Numerical Algorithm Application! Please select your algorithm of choice by selecting the correct number:")
		print("\t 1: BubbleSort \n \t 2: InsertionSort \n \t 3: QuickSort \n \t 4: MergeSort \n \t 5: SelectionSort \n \t 6: HeapSort \n \t 7: QuickSelect (median)")
		choice = getChoice(1, NUM_OPTIONS);
		dict = {"1": strategy.BubbleSort, "2": strategy.InsertionSort, "3": strategy.QuickSort, "4": strategy.MergeSort, "5": strategy.SelectionSort, "6": strategy.HeapSort, "7": strategy.QuickSelect}
		algorithm = getAlgorithm(dict, str(choice))
		# Determine if the user would like to create their own list or use a randomly generated list
		listOfNumbers = genNumListSetUp()
		# Display the list of numbers to the user
		displayList(listOfNumbers)
		# run the algorithm
		print("Now, we will run the algorithm you picked")
		context = Context(algorithm, listOfNumbers)
		# time the algorithm
		start = time.time_ns()
		sortedList = context.strategy().runAlgorithm(listOfNumbers)
		# Call helper function to get the runtime
		end = time.time_ns()
		runtime = getRuntime(start, end)
		# Display the sorted list and wrtie to file
		displayListAndWriteToFile(sortedList, runtime)

		# Added race functionality for all the algorithms
		print("Would you like to run a race with the algorithms? Please type 1[YES] or 2[NO]")
		raceChoice = getChoice(1,2)
		if raceChoice == 1:
			runRace(listOfNumbers, dict)
		# Ask them if they would like to play again
		print("Check the input/output/race files for full results. Would you like to play again? Type 1[YES] or 2[NO]?")
		print("Note, the files will be overwritten, so save them if you like to keep them")
		playAgain = getChoice(1,2)
		if playAgain == 1:
			continue
		else:
			break
	print("Thank you for playing!")



# Run the main script
if __name__ == "__main__":
	main()