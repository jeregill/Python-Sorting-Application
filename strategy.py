# Python project for sorting algorithms, using the strategy design pattern

import random
import abc
import sys


# The abstract strategy class for our strategy design pattern
class Strategy(abc.ABC):
	# Given a list of numbers, run the selected algorithm
	@abc.abstractmethod
	def runAlgorithm(self, numbers):
		pass

	def swap(self, list, index1, index2):
		temp = list[index1]
		list[index1] = list[index2]
		list[index2] = temp


# The following are all implemenations of the abstract subclass for the various sorting algorithms

# Concrete BubbleSort algorithm
class BubbleSort(Strategy):
	def runAlgorithm(self, numbers):
		for outerIndex, outerValue in enumerate(numbers[:-1]):
			swapped = False
			for innerIndex, innerValue in enumerate(numbers[:-1]):
				if numbers[innerIndex] > numbers[innerIndex + 1]:
					# Swap them
					super().swap(numbers,innerIndex, innerIndex + 1)
					swapped = True
			if not swapped:
				break;
		return numbers


# Concrete MergeSort algorithm
class MergeSort(Strategy):
	def runAlgorithm(self, numbers):
		# base case
		if len(numbers) > 1:
			# Need integer division
			mid = len(numbers)//2
			# Divide the array into two halves
			left = numbers[:mid]
			right = numbers[mid:]

			# Recursive calls on left and right
			self.runAlgorithm(left)
			self.runAlgorithm(right)

			# The "Merge" part

			i = j = k = 0

			while i < len(left) and j < len(right):
				# if the left array number is less, place it before the right array number
				if left[i] < right[j]:
					numbers[k] = left[i]
					i += 1
				else:
					# the right array number is larger
					numbers[k] = right[j]
					j += 1
				# Move to the next position
				k += 1

			 # Add in any remaining numbers
			while i < len(left):
				numbers[k] = left[i]
				i += 1
				k += 1

			while j < len(right):
				numbers[k] = right[j]
				j += 1
				k += 1

		return numbers





# Concrete QuickSort algorithm
class QuickSort(Strategy):
	def runAlgorithm(self, numbers):
		return self.quickSortHelper(numbers, 0, len(numbers) - 1)

	## Helper functions for quicksort implementation
	def quickSortHelper(self, numbers, first, last):
		if first < last:

			split = self.partition(numbers, first, last)

			self.quickSortHelper(numbers, first, split -1)
			self.quickSortHelper(numbers, split + 1, last)

			return numbers

	def partition(self, numbers, first, last):
		# We have selected the pivot as the first value
		pivot = numbers[first]

		leftIndex = first + 1
		rightIndex = last

		crossed = False

		## While the two pivots have not crossed each other
		while not crossed:
			while leftIndex <= rightIndex and numbers[leftIndex] <= pivot:
				leftIndex += 1

			while rightIndex >= leftIndex and numbers[rightIndex] >= pivot:
				rightIndex -= 1

			if rightIndex < leftIndex:
				crossed = True
			else:
				super().swap(numbers, leftIndex, rightIndex)

		# Swap the pivot (firstIndex) with the rightIndex and we can recurse on these two halves
		super().swap(numbers, first, rightIndex)

		return rightIndex


# Concrete BubbleSort algorithm
class InsertionSort(Strategy):
	def runAlgorithm(self, numbers):
		for index, value in enumerate(numbers[1:]):
			key = numbers[index]
			inner = index
			# Move the first number from the unsorted array into the correct part in the sorted part of the array
			while inner > 0 and numbers[inner - 1] > key:
				numbers[inner] = numbers[inner - 1]
				inner -= 1

			numbers[inner] = key

		return numbers


# Concrete BubbleSort algorithm
class SelectionSort(Strategy):
	def runAlgorithm(self, numbers):
		for outerIndex, outerValue in enumerate(numbers[1:]):
			minIndex = outerIndex

			# Let us find the minimum element in the rest of the list
			for innerIndex, innerValue in enumerate(numbers[outerIndex:]):
				if numbers[innerIndex] < numbers[minIndex]:
					minIndex = innerIndex

			# Now, swap the min element and loop back up
			if minIndex != outerIndex:
				super().swap(numbers, minIndex, outerIndex)
		return numbers


# Concrete HeapSort algorithm
class HeapSort(Strategy):
	def runAlgorithm(self, numbers):
		return self.runHeapSort(numbers)

	def heapify(self, numbers, size, root):
		largest = root
		left = 2 * root + 1
		right = 2 * root + 2

		# If the left child is larger than the root
		if left < size and numbers[root] > numbers[left]:
			largest = left

		# If the right child is larger than the root (or the left child, if already swapped in above code)
		if right < size and numbers[largest] > numbers[right]:
			largest = right

		# Now, we check if largest has changed, then we will swap
		if largest != root:
			super().swap(numbers, largest, root)

			# Now, we recurse on the sub-tree
			self.heapify(numbers, size, largest) # largest is now the root of the subtree

	def runHeapSort(self, numbers):
		size = len(numbers)
		for index in range(size, -1, -1): # go in reverse order
			self.heapify(numbers, size, index)

		# Now, extract elements

		for index in range(size-1, 0, -1): # Again, to go reverse order
			# Extract the max (which is at index i, and swap with the first element)
			super().swap(numbers, index, 0)
			# Now call heapfiy on the sub array
			self.heapify(numbers, index, 0)

		return numbers

# Concrete QuickSelect algorithm. For simplicity, our algorithm only returns the median (not general k)
class QuickSelect(Strategy):
	def runAlgorithm(self, numbers):
		median = len(numbers) // 2
		return [self.runQuickSelect(numbers, median)]


	def runQuickSelect(self, numbers, median):
		pivot = numbers[0]
		twoHalves = self.getLesserAndGreater(numbers, pivot)
		lesser = twoHalves[0]
		greater = twoHalves[1]
		if len(greater) == median - 1:
			return pivot
		elif len(greater) > median - 1:
			return self.runQuickSelect(greater, median)
		else: # len(greater) < k - 1
			return self.runQuickSelect(lesser, median - len(greater) - 1)

	# Helper function to get all numbers lesser than the pivot
	def getLesserAndGreater(self, numbers, pivot):
		lesser = []
		greater = []
		for x in numbers:
			if x < pivot:
				lesser.append(x)
			elif x > pivot:
				greater.append(x)

		return (lesser, greater)



