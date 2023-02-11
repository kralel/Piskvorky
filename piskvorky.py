from tkinter import *
from tkinter import messagebox
import math
from enum import IntEnum
import random

side = 25

class Field(IntEnum):
	empty_field = 0
	human = -1
	computer = 1

class Tic_tac_toe:
	canvas = None
	width = 0
	height = 0
	no_win = 0
	difficulty = 0
	board = []
	moves = 0													# Number of placed stones

	def __init__(self, window, height, width, no_win, difficulty):		
		try:
			if height < 0:
				raise ValueError("Výška je záporná!")
			elif width < 0:
				raise ValueError("Šířka je záporná!")
			elif no_win < 0:
				raise ValueError("Počet potřebných kamenů na výhru je záporný!")
			elif difficulty < 0:
				raise ValueError("Obtížnost je záporná!")
		except TypeError:
			print("Vstupní parametry nejsou číselné!")
			exit()
		
		self.canvas = Canvas(window, width = width * side, height = height * side)
		self.canvas.grid()
		self.canvas.bind("<Button-1>", self.move)				# Call function move on left mouse button click
		self.width = width
		self.height = height
		self.no_win = no_win
		self.difficulty = difficulty
		for x in range(width):
			# Column
			self.board.append([])
			for y in range(height):
				# Row
				self.board[x].append(Field.empty_field)
				self.canvas.create_rectangle(x * side, y * side,
					(x + 1) * side, (y + 1) * side)

	def move(self, action):
		# Get game coordinates from click coordinates
		field_x = int(action.x / side)
		field_y = int(action.y / side)
		if self.board[field_x][field_y] != Field.empty_field:
			print("Pole je obsazené!")
		else:
			self.placement(field_x, field_y)
			# Next move
			evaluation = self.minimax(self.difficulty, self.board, Field.computer, -math.inf, math.inf)
			self.placement(evaluation[0], evaluation[1])

	def placement(self, field_x, field_y):
		'''
		Places stone on the game board at given coordinates
		field_x: x-coordinate of the field
		field_y: y-scoordinate of the field
		'''
		if self.moves % 2 == 0:									# Human
			self.draw_circle(field_x, field_y)
			self.board[field_x][field_y] = Field.human
		else:													# Computer
			self.draw_cross(field_x, field_y)
			self.board[field_x][field_y] = Field.computer
		self.moves += 1

		if self.no_in_row(field_x, field_y, self.board) == self.no_win:
			if self.board[field_x][field_y] == Field.human:
				if messagebox.showinfo(title="Konec hry", message="Vyhráli jste!"):
					exit()
			else:
				if messagebox.showinfo(title="Konec hry", message="Prohráli jste!"):
					exit()
				
		elif self.moves == self.height * self.width:				# Full board - draw
			if messagebox.showinfo(title="Konec hry", message="Remíza!"):
				exit()

	def draw_cross(self, x, y):
		'''
		Draws cross at given field
		x: x-coordinate of the field
		y: y-coordinate of the field
		'''
		self.canvas.create_line((x * side) + 5, (y * side) + 5, ((x + 1) * side) - 5, ((y + 1) * side) - 5, fill="blue", width=2)
		self.canvas.create_line((x * side) + 5, ((y + 1) * side) - 5, ((x + 1) * side) - 5, (y * side) + 5, fill="blue", width=2)

	def draw_circle(self, x, y):
		'''
		Draws circle at given field
		x: x-coordinate of the field
		y: y-coordinate of the field
		'''
		self.canvas.create_oval((x * side) + 5, (y * side) + 5, ((x + 1) * side) - 5, ((y + 1) * side) - 5, outline = "red", width = 2)

	def minimax(self, depth, board, player_on_move, alpha, beta):
		'''
		Selects the best field to place stone
		depth: difficulty
		board: game board
		player_on_move: player on turn for which the function was called
		alpha: minimum score of maximizing player
		beta: maximum score of minimizing player
		return: trinity [x-coordinate, y-coordinate, evaluate of board] of the best field
		'''
		# Starting values
		if player_on_move == Field.human:						# Human
			best = [-1, -1, math.inf]
		else:													# Computer
			best = [-1, -1, -math.inf]
		
		if self.moves == self.height * self.width:				# Draw
			return [-1, -1, 0]

		# Random selection of field order
		seq_x = list(range(self.width))
		random.shuffle(seq_x)
		seq_y = list(range(self.height))
		random.shuffle(seq_y)
		for x in seq_x:
			for y in seq_y:
				if board[x][y] == Field.empty_field:
					# Temporary placement
					board[x][y] = player_on_move
					self.moves += 1
					if depth == 0:
						evaluation = [x, y, self.evaluate_board(board)]
					else:
						evaluation = [x, y, self.minimax(depth - 1, board, -player_on_move, alpha, beta)[2]]
					# Remove
					board[x][y] = Field.empty_field
					self.moves -= 1

					if player_on_move == Field.human:
						# Overwrite older value - else starting value may remain [-1, -1, math.inf]
						if evaluation[2] <= best[2]:
							best = evaluation

						if best[2] < alpha:
							return best
						beta = min(beta, best[2])
					else:
						# Overwrite older value - else starting value may remain [-1, -1, -math.inf]
						if evaluation[2] >= best[2]:
							best = evaluation

						if best[2] > beta:
							return best
						alpha = max(alpha, best[2])

				elif self.no_in_row(x, y, board) == self.no_win:
					if board[x][y] == Field.human:
						return [-1, -1, -math.inf]
					else:
						return [-1, -1, math.inf]

		return best

	def no_in_row(self, field_x, field_y, board):
		'''
		Calculates number of stones in a row on the game board for placed stone
		field_x: x-coordinate of the field
		field_y: y-coordinate of the field
		board: game board
		return: maximum number of stones in a row
		'''
		maximum = -math.inf

		# Check all possible directions {down, left, left down, right down}
		for i in [ [0, 1], [-1, 0], [-1, 1], [1, 1] ]:
			in_row = 1

			j = 1
			while self.on_board(field_x + (i[0] * j), field_y + (i[1] * j)) and \
					board[field_x][field_y] == board[field_x + (i[0] * j)][field_y + (i[1] * j)]:
				in_row += 1
				j += 1

			j = 1
			while self.on_board(field_x - (i[0] * j), field_y - (i[1] * j)) and \
					board[field_x][field_y] == board[field_x - (i[0] * j)][field_y - (i[1] * j)]:
				in_row += 1
				j += 1

			if in_row > maximum:
				maximum = in_row

		return maximum

	def evaluate_board(self, board):
		'''
		Evaluates each field on the game board according to the number of stones in a row for each player
		board: game board
		return: difference in the number of stones in a row between players
		'''
		# Smallest starting value
		comp_max = -math.inf
		human_max = -math.inf

		for x in range(self.width):
			for y in range(self.height):
				if board[x][y] == Field.human:
					value = self.no_in_row(x, y, board)
					if value > human_max:
						human_max = value
					
				elif board[x][y] == Field.computer:
					value = self.no_in_row(x, y, board)
					if value > comp_max:
						comp_max = value

		return comp_max - human_max

	def on_board(self, field_x, field_y):
		'''
		Is this field on the game board?
		field_x: x-coordinate of the field
		field_y: y-coordinate of the field
		return: "True" if field is on the game board else "False"
		'''
		if field_x < 0 or field_x >= self.width:
			return False
		if field_y < 0 or field_y >= self.height:
			return False
		else:
			return True


window = Tk()


game = Tic_tac_toe(window, 3, 3, 3, 2)

window.mainloop()