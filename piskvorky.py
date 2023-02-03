from tkinter import *
import math, copy
from collections import namedtuple

strana = 25

class Piskvorky:
	platno = None
	sirka = 0
	vyska = 0
	plan=[]
	tahy = 0										# Počet umístěných znaků

	def __init__(self, vyska, sirka):
		self.platno = Canvas(okno, width = sirka * strana, height = vyska * strana)
		self.platno.grid()
		self.platno.bind("<Button-1>", self.hrac)
		self.sirka = sirka
		self.vyska = vyska
		for i in range(vyska):
			# Řádek
			self.plan.append([])
			for j in range(sirka):
				# Sloupec
				self.plan[i].append(0)
				self.platno.create_rectangle(j * strana, i * strana,
				(j + 1) * strana, (i + 1) * strana)

	def hrac(self, udalost):
		# Zisk souřadnic pole
		pole_x = int(udalost.x / strana)
		pole_y = int(udalost.y / strana)
		self.tah(pole_x, pole_y)
		# Další tah
		nejlepsi = 0
		x = 0
		y = 0
		for i in range(self.vyska):
			for j in range(self.sirka):
				if self.plan[i][j] == 0:
					# Dočasné umístění
					self.plan[i][j] = 2
					ohodnoceni = self.minimax(1, self.plan, 2)
					# Odebrání
					self.plan[i][j] = 0
					if ohodnoceni < nejlepsi:
						nejlepsi = ohodnoceni
						y = i
						x = j
		self.tah(x, y)

	def tah(self, pole_x, pole_y):
		if self.plan[pole_y][pole_x] != 0:						# Je dané pole volné?
			print("Pole je obsazené!")
			return

		if self.tahy % 2 == 0:									# Hráč
			self.kolecko(pole_x, pole_y)
			self.plan[pole_y][pole_x] = 1
		else:													# Počítač
			self.krizek(pole_x, pole_y)
			self.plan[pole_y][pole_x] = 2
		self.tahy += 1

		if self.pocet_v_rade(pole_x, pole_y, self.plan) == 3:
			if self.plan[pole_y][pole_x] == 1:
				print("Vyhrál hráč!")
			else:
				print("Vyhrál počítač!")
				
		if self.tahy == self.vyska * self.sirka:
			print("Hrací pole je plné! Konec hry.")

	def krizek(self, x, y):
		self.platno.create_line((x * strana) + 5, (y * strana) + 5, ((x + 1) * strana) - 5, ((y + 1) * strana) - 5, fill="blue", width=2)
		self.platno.create_line((x * strana) + 5, ((y + 1) * strana) - 5, ((x + 1) * strana) - 5, (y * strana) + 5, fill="blue", width=2)

	def kolecko(self, x, y):
		self.platno.create_oval((x * strana) + 5, (y * strana) + 5, ((x + 1) * strana) - 5, ((y + 1) * strana) - 5, outline = "red", width = 2)

	def minimax(self, hloubka, plan, hrac):		
		if hrac == 1:
			hodnota = math.inf									# Hráč
			for i in range(self.vyska):
				for j in range(self.sirka):
					if plan[i][j] == 0:
						plan[i][j] = hrac
						if hloubka == 0:
							hodnota = min(hodnota, -self.pocet_v_rade(i, j, plan))
						else:
							hodnota = min(hodnota, self.minimax(hloubka - 1, plan, 2))
						plan[i][j] = 0
			print(hodnota)
			return hodnota
		else:
			hodnota = -math.inf									# Počítač
			for i in range(self.vyska):
				for j in range(self.sirka):
					if plan[i][j] == 0:
						plan[i][j] = hrac
						if hloubka == 0:
							hodnota = max(hodnota, self.pocet_v_rade(i, j, plan))
						else:
							hodnota = max(hodnota, self.minimax(hloubka - 1, plan, 1))
						plan[i][j] = 0
			print(hodnota)
			return hodnota

	def pocet_v_rade(self, pole_x, pole_y, plan):
		maximum = - math.inf

		# Kontrolování všech možných směrů {nahoru, doleva, doleva nahoru, doprava nahoru}
		for i in [ [0, 1], [-1, 0], [-1, 1], [1, 1] ]:
			v_rade = 1
			j = 1
			while self.je_na_planu(pole_x + (i[0] * j), pole_y + (i[1] * j)) and \
					plan[pole_y][pole_x] == plan[pole_y + (i[1] * j)][pole_x + (i[0] * j)]:
				v_rade += 1
				j += 1
			j = 1
			while self.je_na_planu(pole_x - (i[0] * j), pole_y - (i[1] * j)) and \
					plan[pole_y][pole_x] == plan[pole_y - (i[1] * j)][pole_x - (i[0] * j)]:
				v_rade += 1
				j += 1
			if v_rade > maximum:
				maximum = v_rade
		print(maximum)
		return maximum
	
	def je_na_planu(self, pole_x, pole_y):
		if pole_x < 0 or pole_x >= len(self.plan[0]):
			return False
		if pole_y < 0 or pole_y >= len(self.plan):
			return False
		else:
			return True


okno = Tk()


try:
	hra = Piskvorky(3,3)
except ValueError as v:
	print(v)
	exit()

okno.mainloop()