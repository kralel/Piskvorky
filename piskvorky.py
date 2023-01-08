from tkinter import *
import math

strana = 25

class Piskvorky:
	platno = None
	sirka = 0
	vyska = 0
	plan=[]
	tahy = 0										# Počet umístěných znaků

	def __init__(self,vyska,sirka):
		self.platno = Canvas(okno,width=sirka*strana,height=vyska*strana)
		self.platno.grid()
		self.platno.bind("<Button-1>", self.platno_onclick)
		self.sirka = sirka
		self.vyska = vyska
		for i in range(vyska):
			self.plan.append([])
			for j in range(sirka):
				self.plan[i].append(0)
				self.platno.create_rectangle(j * strana, i * strana,
				(j + 1) * strana, (i + 1) * strana)

	def platno_onclick(self,udalost):
		# Zisk souřadnic pole
		pole_x = int(udalost.x/strana)
		pole_y = int(udalost.y/strana)

		if self.plan[pole_x][pole_y] != 0:
			print("Pole je obsazené!")							# Je dané pole volné?
			return
		else:
			self.krizek(pole_x, pole_y)
			self.tahy += 1
			self.plan[pole_x][pole_y] = 1
			if self.pocet_v_rade(pole_x, pole_y) == 3:
				if self.plan[pole_x][pole_y] == 1:
					print("Vyhrál hráč!")
				else:
					print("Vyhrál počítač!")
		if self.tahy == self.vyska * self.sirka:
			print("Hrací pole je plné! Konec hry.")

	def krizek(self, x, y):
		self.platno.create_line((x * strana) + 5, (y * strana) + 5, ((x + 1) * strana) - 5, ((y + 1) * strana) - 5, fill="blue", width=2)
		self.platno.create_line((x * strana) + 5, ((y + 1) * strana) - 5, ((x + 1) * strana) - 5, (y * strana) + 5, fill="blue", width=2)


	def kolecko(self, x, y):
		self.platno.create_oval((x * strana)+5, (y * strana)+5, ((x + 1) * strana)-5, ((y + 1) * strana)-5, outline="red", width=2)

	def pocet_v_rade(self, pole_x, pole_y):
		maximum = - math.inf

		# Kontrolování všech možných směrů {nahoru, doleva, doleva nahoru, doprava nahoru}
		for i in [ [0, 1], [-1, 0], [-1, 1], [1, 1] ]:
			v_rade = 1
			j = 1
			while self.je_na_planu(pole_x + (i[0] * j), pole_y + (i[1] * j)) and self.plan[pole_x][pole_y] == self.plan[pole_x + (i[0] * j)][pole_y + (i[1] * j)]:
				v_rade += 1
				j += 1
			j = 1
			while self.je_na_planu(pole_x - (i[0] * j), pole_y - (i[1] * j)) and self.plan[pole_x][pole_y] == self.plan[pole_x - (i[0] * j)][pole_y - (i[1] * j)]:
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

	def tah(self):
		'''
		elif self.tahy%2 == 0:						# Hráč 1
			self.krizek
			self.plan[y][x] = 1
			self.tahy += 1
'''
		


okno = Tk()


try:
	hra = Piskvorky(3,3)
except ValueError as v:
	print(v)
	exit()

okno.mainloop()