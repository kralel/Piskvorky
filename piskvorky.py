from tkinter import *
from tkinter import messagebox
import math
from enum import IntEnum
import random

strana = 25

class Pole(IntEnum):
	volne_pole = 0
	hrac = -1
	pocitac = 1

class Piskvorky:
	platno = None
	sirka = 0
	vyska = 0
	pocet_vyhra = 0
	obtiznost = 0
	plan = []
	tahy = 0													# Počet umístěných znaků

	def __init__(self, okno, vyska, sirka, pocet_vyhra, obtiznost):		
		try:
			if vyska < 0:
				raise ValueError("Výška je záporná!")
			elif sirka < 0:
				raise ValueError("Šířka je záporná!")
			elif pocet_vyhra < 0:
				raise ValueError("Počet potřebných kamenů na výhru je záporný!")
			elif obtiznost < 0:
				raise ValueError("Obtížnost je záporná!")
		except TypeError:
			print("Vstupní parametry nejsou číselné!")
			exit()
		
		self.platno = Canvas(okno, width = sirka * strana, height = vyska * strana)
		self.platno.grid()
		self.platno.bind("<Button-1>", self.tah)				# Po kliknutí zavolá funkci tah
		self.sirka = sirka
		self.vyska = vyska
		self.pocet_vyhra = pocet_vyhra
		self.obtiznost = obtiznost
		for x in range(sirka):
			# Sloupec
			self.plan.append([])
			for y in range(vyska):
				# Řádek
				self.plan[x].append(Pole.volne_pole)
				self.platno.create_rectangle(x * strana, y * strana,
					(x + 1) * strana, (y + 1) * strana)

	def tah(self, udalost):
		# Zisk souřadnic pole
		pole_x = int(udalost.x / strana)
		pole_y = int(udalost.y / strana)
		if self.plan[pole_x][pole_y] != Pole.volne_pole:
			print("Pole je obsazené!")
		else:
			self.umisteni(pole_x, pole_y)
			# Další tah
			ohodnoceni = self.minimax(self.obtiznost, self.plan, Pole.pocitac, -math.inf, math.inf)
			self.umisteni(ohodnoceni[0], ohodnoceni[1])

	def umisteni(self, pole_x, pole_y):
		'''
		Umístění kamene na hrací plán na dané souřadnice
		pole_x: x-souřadnice pole
		pole_y: y-souřadnice pole
		'''
		if self.tahy % 2 == 0:									# Hráč
			self.kolecko(pole_x, pole_y)
			self.plan[pole_x][pole_y] = Pole.hrac
		else:													# Počítač
			self.krizek(pole_x, pole_y)
			self.plan[pole_x][pole_y] = Pole.pocitac
		self.tahy += 1

		if self.pocet_v_rade(pole_x, pole_y, self.plan) == self.pocet_vyhra:
			if self.plan[pole_x][pole_y] == Pole.hrac:
				if messagebox.showinfo(title="Konec hry", message="Vyhráli jste!"):
					exit()
			else:
				if messagebox.showinfo(title="Konec hry", message="Prohráli jste!"):
					exit()
				
		elif self.tahy == self.vyska * self.sirka:				# Zaplněný plán - remíza
			if messagebox.showinfo(title="Konec hry", message="Remíza!"):
				exit()

	def krizek(self, x, y):
		'''
		Nakreslení křížku do daného pole
		x: x-souřadnice pole
		y: y-souřadnice pole
		'''
		self.platno.create_line((x * strana) + 5, (y * strana) + 5, ((x + 1) * strana) - 5, ((y + 1) * strana) - 5, fill="blue", width=2)
		self.platno.create_line((x * strana) + 5, ((y + 1) * strana) - 5, ((x + 1) * strana) - 5, (y * strana) + 5, fill="blue", width=2)

	def kolecko(self, x, y):
		'''
		Nakreslení kolečka do daného pole
		x: x-souřadnice pole
		y: y-souřadnice pole
		'''
		self.platno.create_oval((x * strana) + 5, (y * strana) + 5, ((x + 1) * strana) - 5, ((y + 1) * strana) - 5, outline = "red", width = 2)

	def minimax(self, hloubka, plan, hrac_na_tahu, alfa, beta):
		'''
		Vybere nejvýhodnější pole pro umístění kamene
		hloubka: hloubka propočtu, obtížnost
		plan: hrací plán
		hrac_na_tahu: hráč na tahu, pro kterého byla funkce volána
		alfa: minimální možné skóre maximalizujícího hráče
		beta: maximální možné skóre minimalizujícího hráče
		return: trojice [x-souřadnice, y-souřadnice, ohodnocení plánu] nejvýhodnějšího pole
		'''
		# Počáteční hodnoty
		if hrac_na_tahu == Pole.hrac:							# Hráč
			nejlepsi = [-1, -1, math.inf]
		else:													# Počítač
			nejlepsi = [-1, -1, -math.inf]
		
		if self.tahy == self.vyska * self.sirka:				# Remíza
			return [-1, -1, 0]

		# Náhodný výběr pořadí polí
		posloupnost_x = list(range(self.sirka))
		random.shuffle(posloupnost_x)
		posloupnost_y = list(range(self.vyska))
		random.shuffle(posloupnost_y)
		for x in posloupnost_x:
			for y in posloupnost_y:
				if plan[x][y] == Pole.volne_pole:
					# Dočasné umístění
					plan[x][y] = hrac_na_tahu
					self.tahy += 1
					if hloubka == 0:
						ohodnoceni = [x, y, self.ohodnoceni_planu(plan)]
					else:
						ohodnoceni = [x, y, self.minimax(hloubka - 1, plan, -hrac_na_tahu, alfa, beta)[2]]
					# Odebrání
					plan[x][y] = Pole.volne_pole
					self.tahy -= 1

					if hrac_na_tahu == Pole.hrac:
						# Přepsání starší hodnoty - jinak může zůstat počáteční hodnota [-1, -1, math.inf]
						if ohodnoceni[2] <= nejlepsi[2]:
							nejlepsi = ohodnoceni

						if nejlepsi[2] < alfa:
							return nejlepsi
						beta = min(beta, nejlepsi[2])
					else:
						# Přepsání starší hodnoty - jinak může zůstat počáteční hodnota [-1, -1, -math.inf]
						if ohodnoceni[2] >= nejlepsi[2]:
							nejlepsi = ohodnoceni

						if nejlepsi[2] > beta:
							return nejlepsi
						alfa = max(alfa, nejlepsi[2])

				elif self.pocet_v_rade(x, y, plan) == self.pocet_vyhra:
					if plan[x][y] == Pole.hrac:
						return [-1, -1, -math.inf]
					else:
						return [-1, -1, math.inf]

		return nejlepsi

	def pocet_v_rade(self, pole_x, pole_y, plan):
		'''
		Vypočítání počtu kamenů v řadě na hracím plánu pro umisťovaný kámen
		pole_x: x-souřadnice pole
		pole_y: y-souřadnice pole
		plan: hrací plán
		return: maximální počet kamenů v řadě
		'''
		maximum = -math.inf

		# Kontrolování všech možných směrů {dolu, doleva, doleva dolu, doprava dolu}
		for i in [ [0, 1], [-1, 0], [-1, 1], [1, 1] ]:
			v_rade = 1

			j = 1
			while self.je_na_planu(pole_x + (i[0] * j), pole_y + (i[1] * j)) and \
					plan[pole_x][pole_y] == plan[pole_x + (i[0] * j)][pole_y + (i[1] * j)]:
				v_rade += 1
				j += 1

			j = 1
			while self.je_na_planu(pole_x - (i[0] * j), pole_y - (i[1] * j)) and \
					plan[pole_x][pole_y] == plan[pole_x - (i[0] * j)][pole_y - (i[1] * j)]:
				v_rade += 1
				j += 1

			if v_rade > maximum:
				maximum = v_rade

		return maximum

	def ohodnoceni_planu(self, plan):
		'''
		Ohodnocení každého pole na hracím plánu dle počtu kamenů v řadě pro jednotlivé hráče
		plan: hrací plán
		return: rozdíl počtu kamenů v řadě mezi hráči
		'''
		# Nejmenší počáteční hodnota
		pocitac_max = -math.inf
		hrac_max = -math.inf

		for x in range(self.sirka):
			for y in range(self.vyska):
				if plan[x][y] == Pole.hrac:
					hodnota = self.pocet_v_rade(x, y, plan)
					if hodnota > hrac_max:
						hrac_max = hodnota
					
				elif plan[x][y] == Pole.pocitac:
					hodnota = self.pocet_v_rade(x, y, plan)
					if hodnota > pocitac_max:
						pocitac_max = hodnota

		return pocitac_max - hrac_max

	def je_na_planu(self, pole_x, pole_y):
		'''
		Je pole na hracím plánu?
		pole_x: x-souřadnice pole
		pole_y: y-souřadnice pole
		return: "True" pokud je pole na hracím plánu, jinak "False"
		'''
		if pole_x < 0 or pole_x >= self.sirka:
			return False
		if pole_y < 0 or pole_y >= self.vyska:
			return False
		else:
			return True


okno = Tk()


hra = Piskvorky(okno, 3, 3, 3, 2)

okno.mainloop()