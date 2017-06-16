from random import randint

'''
A different take on Powerball:

We'll allow for multiple players,
each player must pick 5 unique numbers (1-69) and a Powerball number (1-26)
The winning number will consist of the most frequently picked duplicated numbers, ties will be broken randomly
If there are not enough duplicates, the remaining picks will be picked at random
'''

if __name__ == "__main__":
	debug = False
	# First: Set up vars
	numberCounts = [0] * 70
	powerballCounts = [0] * 27
	entries = []
	# Second: Take in favorite numbers
	print("Welcome to Powerball\n\nPlease fill in entries below")
	while True:
		# Get name of entrant, if blank we finish taking entries
		firstName = input("\nEnter first name (leave blank if finished): ")
		if firstName == '':
			break
		lastName = input("Enter last name: ")
		# Get first 5 favorite numbers, ensuring they are unique and in range
		favoriteNums = []
		while len(favoriteNums) < 5:
			th = {
				0 : "st",
				1 : "nd",
				2 : "rd"
			}.get(len(favoriteNums), "th")
			while True:
				try:
					num = int(input("Select %d%s number (1-69): " % (len(favoriteNums)+1, th)))
					if num < 1 or num > 69:
						print("Must be between 1-69!")
					elif num in favoriteNums:
						print("That number has already been picked!")
					else:
						favoriteNums.append(num)
						numberCounts[num] += 1
						if debug:
							print(numberCounts)
						break
				except ValueError:
					print("Must be an integer!")
		# Get the Powerball
		powerball = 0
		while True:
			try:
				pb = int(input("Enter powerball number (1-26): "))
				if pb < 1 or pb > 26:
					print("Must be between 1-26")
				else:
					powerball = pb
					powerballCounts[powerball] += 1
					if debug:
						print(powerballCounts)
					break
			except ValueError:
				print("Must be an integer!")
		# record the entry
		entries.append((firstName, lastName, favoriteNums, powerball))
					
	# Third: Print all inputs
	print("\nThankyou for playing Powerball\nThese are the entries for today's drawing:\n")
	for e in entries: print("%s %s  %s  powerball: %d" % (e[0],e[1]," ".join(map(str,e[2])), e[3]))
	# Last: Generate winning number
	winningNumbers = []
	# to easily sort counts, use a dictionary to put numbers in groups based on how many times they occured
	reverseCounts = {}
	for n in range(len(numberCounts)):
		if numberCounts[n] in reverseCounts:
			reverseCounts[numberCounts[n]].append(n)
		else:
			reverseCounts[numberCounts[n]] = [n]
		if debug:
			print(reverseCounts)
	# select winning numbers, starting with most picked
	for count in reversed(sorted(reverseCounts.keys())):
		if count <= 1: # we only want numbers that have been duplicated
			break
		if len(reverseCounts[count]) + len(winningNumbers) > 5:
			# we have too many numbers to add, ties are broken randomly
			while len(winningNumbers) < 5:
				rand = randint(0,len(reverseCounts[count])-1)
				winningNumbers.append(reverseCounts[count][rand])
				del(reverseCounts[count][rand])
		else: # we can add all numbers of this count to the winning number pool
			for num in reverseCounts[count]:
				winningNumbers.append(num)
		if debug:
			print("Winning Numbers(%d): " % (count) + str(winningNumbers))
		if len(reverseCounts) >= 5: # we've picked all 5 non-powerball numbers
			break
	# fill the rest of the winning numbers with random numbers if less than 5 were selected
	if len(winningNumbers) < 5:
		numberPool = []
		for x in range(1,70):
			if x not in winningNumbers:
				numberPool.append(x)
		while len(winningNumbers) < 5:
			rand = randint(0,len(numberPool)-1)
			winningNumbers.append(numberPool[rand])
			del(numberPool[rand])
	# keep things in order
	winningNumbers = sorted(winningNumbers)
	# find most occured powerball number, if no duplicates pick at random
	reversePowerball = {}
	for n in range(len(powerballCounts)):
		if powerballCounts[n] in reversePowerball:
			reversePowerball[powerballCounts[n]].append(n)
		else:
			reversePowerball[powerballCounts[n]] = [n]
		if debug:
			print(reversePowerball)
	winningPowerball = randint(1,26)
	pbCount = sorted(reversePowerball.keys())[-1]
	if pbCount > 1:
		if len(reversePowerball[pbCount]) > 1:
			winningPowerball = reversePowerball[pbCount][randint(0,len(reversePowerball[pbCount])-1)]
		else:
			winningPowerball = reversePowerball[pbCount][0]
	# print the results
	print("\nAnd the winning numbers are %s  powerball: %d" % (" ".join(map(str,winningNumbers)), winningPowerball))
	winnerFound = False;
	for e in entries:
		if sorted(e[2]) == winningNumbers and e[3] == winningPowerball:
			if not winnerFound:
				winnerFound = True
				print("\nThe Grand Prize Winners are:")
			print("%s %s" % (e[0], e[1]))
	if not winnerFound:
		print("No Grand Prize Winners, better luck next time!")
