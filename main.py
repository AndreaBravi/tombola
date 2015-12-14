from collections import defaultdict
import numpy as np

class CardGenerator(object):	
	def __init__(self):
		self.generateNumbers()	
		self.nIterations = 10	

	def getNumber(self):
		"""
		Continuously draw numbers from 0 to 89, repeating every 90 drawings
		"""
		if len(self.numbers) == 0:
			self.generateNumbers()
		return self.numbers.pop()

	def setNumber(self, n):
		"""
		Reinsert number in the list
		"""		
		self.numbers.insert(0, n)

	def getNumbers(self):
		"""
		Creates a dictionary containing 15 numbers divided among 9 keys (0 to 8),
		where key K holds numbers K * 10 + 1: (K+1) * 10
		"""				
		count = 0
		flag = True
		numbers = defaultdict(list)
		if len(self.numbers) == 15:
			for col in range(15):
				number = self.getNumber()
				col = number / 10
				numbers[col] += [number + 1]
		else:
			while count < 15:
				number = self.getNumber()
				col = number / 10
				if flag or len(numbers[col]) < 2:
					numbers[col] += [number + 1] # Correcting numbering
					count += 1
					if len(numbers[col]) == 3:
						flag = False
				else:
					self.setNumber(number)
		return numbers

	def fillCard(self, numbers):
		"""
		Returns a 3 x 9 zero-padded matrix holding the numbers between 1 and 90
		"""
		# Filling columns with three numbers		
		values = np.zeros([3, 9], dtype=int)
		for col, colValues in numbers.items():			
			if len(colValues) == 3:
				for row, colValue in enumerate(sorted(colValues)):
					values[row, col] = colValue
				numbers[col] = []
			else:
				# Preparing data for following step
				numbers[col] = sorted(colValues, reverse=True)

		# Filling all other columns, row by row, enforcing 5 numbers per row
		nFilledCols = sum(np.sum(values, 0) > 0)
		for row in range(3):
			counter = 0
			for col in np.random.permutation(9).tolist():
				if len(numbers[col]) > 0:
					number = numbers[col].pop()
					values[row, col] = number
					counter += 1
				if counter == 5 - nFilledCols:
					break
		return values		

	def getCard(self):
		"""
		Generate the numbers for a card and try nIteration times to sort them
		in rows of 5 numbers. If no solution is found, throws an AssertionError.
		"""
		numbers = self.getNumbers()		
		values = np.array([0])
		
		iteration = 0
		while np.sum(values > 0) != 15 and iteration < self.nIterations:
			values = self.fillCard(numbers.copy())
			iteration += 1
		assert iteration < self.nIterations, "RE-RUN ANALYSIS! SOLUTION WAS STUCK"
		assert np.sum(values > 0) == 15, "NOT POSSIBLE"		
		return values

	def generateNumbers(self):
		"""
		Generates 90 numbers (0 to 89) randomly sorted
		"""
		self.numbers = list(np.random.permutation(90))

	def cardSet(self):
		"""
		Generate 6 cards from a new set of 90 numbers
		"""
		self.generateNumbers()
		return [self.getCard() for n in range(6)]


class HTMLGenerator(object):
	def __init__(self, offset):
		self.tableWidth = 81
		self.boardWidth = 84
		self.offset = offset

	def addNumber(self, name):
		return '<h1><center>&nbsp;&nbsp;&nbsp;%d&nbsp;&nbsp;&nbsp;</center></h1>' % (name)

	def addFigure(self, name, width):
		return '<img src="images/%d.jpg" alt="" style="width:%dpx; height:auto;"></img>' % (name, width)

	def addCard(self, n, offset, tot, card):
		html = 'Tombola St. Peter - %d/%d<br><table border="2">\n' % (n + 1 + self.offset, tot + self.offset)
		for n in range(27):
			if n % 9 == 0:
				if n == 0:
	  				html += '<tr>\n'
	  			elif n == 26:
	  				html += '</tr>\n'
	  			else:
	  				html += '</tr>\n<tr>\n'
	  		html += '<td>%s</td>\n' % (self.addFigure(card.item(n), self.tableWidth))
		html += '</table>\n<br>\n'
		return html

	def printCards(self, cards):
		body = ""
		for n, card in enumerate(cards):
			body += self.addCard(n, offset, nCards, card)
			if (n + 1) % 4 == 0 and n > 0:
				body += '\n<p style="page-break-after:always;"></p>\n'
		self.write(body, 'cards')

	def addBoard(self, card):
		html = '<table border="2">\n'
		for n in range(33):
			if n % 11 == 0:
				if n == 0:
	  				html += '<tr>\n'
	  			elif n == 32:
	  				html += '</tr>\n'
	  			else:
	  				html += '</tr>\n<tr>\n'
	  		html += '<td>%s</td>\n' % (self.addFigure(card.item(n), self.boardWidth))	  		
		html += '</table>\n<br>\n'
		return html	

	def addNumbers(self, card):
		html = '<table border="2">\n'
		for n in range(33):
			if n % 11 == 0:
				if n == 0:
	  				html += '<tr>\n'
	  			elif n == 32:
	  				html += '</tr>\n'
	  			else:
	  				html += '</tr>\n<tr>\n'
	  		html += '<td>%s</td>\n' % (self.addNumber(card.item(n)))	  		
		html += '</table>\n<br>\n'
		return html			

	def printBoard(self, cards):
		body = '<center><h3 style="padding-left:200px;">Tombola St. Peter </h3></center>'
		for n, card in enumerate(cards):
			body += self.addBoard(card)
			if (n + 1) % 2 == 0 and n > 0:
				body += '\n<p style="page-break-after:always;"></p>\n'
		self.write(body, 'board')

	def printNumbers(self, cards):
			body = '<center><h3 style="padding-left:200px;">Tombola St. Peter </h3></center>'
			for n, card in enumerate(cards):
				body += self.addNumbers(card)
			self.write(body, 'numbers')

	def readTemplate(self):
		with open('template.html', 'r') as htmlFile:
			return htmlFile.read()

	def write(self, body, filename):
		html = self.readTemplate()
		with open(filename + '.html', 'w') as htmlFile:
			htmlFile.write(html.replace("htmlBODY", body))		

# ----------- Setup

# Parameters
nCards = 96
offset = 96

cg = CardGenerator()
hg = HTMLGenerator(offset)

# ----------- Generating cards

# Execution
cards = []
while len(cards) < nCards:
	try:
		cards += cg.cardSet()
		print 'Built #%d cards' % len(cards)
	except AssertionError:
		pass
cards = cards[:nCards]

hg.printCards(cards)

# ----------- Generating board
cards = []
for n in range(3):
	card = np.arange(30) + 1 + 30 * n
	card = card.tolist()
	card = np.array(card[:5] + [0] + card[5:15] + [0] + card[15:25] + [0] + card[25:])
	cards += [card]

hg.printBoard(cards)

# ----------- Generating drawing numbers
hg.printNumbers(cards)
