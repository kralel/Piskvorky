from tkinter import *
import math

strana = 25

class Piskvorky:
	platno = None
	sirka = 0
	vyska = 0
	plan=[]
	#: jsou tahy potřeba?
	tahy = 0													# Počet umístěných znaků
	#TODO: použít enum pro hráče, počítač a volné pole 
	hrac = -1
	pocitac = 1

	def __init__(self, okno, vyska, sirka):
		self.platno = Canvas(okno, width = sirka * strana, height = vyska * strana)
		self.platno.grid()
		self.platno.bind("<Button-1>", self.tah)
		self.sirka = sirka
		self.vyska = vyska
		for x in range(sirka):
			# Sloupec
			self.plan.append([])
			for y in range(vyska):
				# Řádek
				self.plan[x].append(0)
				self.platno.create_rectangle(x * strana, y * strana,
					(x + 1) * strana, (y + 1) * strana)

	def tah(self, udalost):
		# Zisk souřadnic pole
		pole_x = int(udalost.x / strana)
		pole_y = int(udalost.y / strana)
		self.umisteni(pole_x, pole_y)
		# Další tah
		ohodnoceni = self.minimax(3, self.plan, self.pocitac)
		self.umisteni(ohodnoceni[0], ohodnoceni[1])

	def umisteni(self, pole_x, pole_y):
		if self.plan[pole_x][pole_y] != 0:						# Je dané pole volné?
			print("Pole je obsazené!")
			return

		#TODO: použít proměnnou hráč_na_tahu místo tahy?
		if self.tahy % 2 == 0:									# Hráč
			self.kolecko(pole_x, pole_y)
			self.plan[pole_x][pole_y] = self.hrac
		else:													# Počítač
			self.krizek(pole_x, pole_y)
			self.plan[pole_x][pole_y] = self.pocitac
		self.tahy += 1

		#TODO: parametrizovat počet potřebný pro vítězství
		if self.pocet_v_rade(pole_x, pole_y, self.plan) == 3:
			if self.plan[pole_x][pole_y] == self.hrac:
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

	def minimax(self, hloubka, plan, hrac_na_tahu):		
		if hrac_na_tahu == self.hrac:							# Hráč
			nejlepsi = [-1, -1, math.inf]
		else:													# Počítač
			nejlepsi = [-1, -1, -math.inf]
		
		#TODO: přidat kontrolu i dalších konců hry (nejen remízy)
		if self.tahy == self.vyska * self.sirka:
			return [-1, -1, 0]

		for x in range(self.sirka):
			for y in range(self.vyska):
				if plan[x][y] == 0:
					# Dočasné umístění
					plan[x][y] = hrac_na_tahu
					self.tahy += 1
					if hloubka == 0:
						ohodnoceni = [x, y, self.ohodnoceni_planu(plan)]
					else:
						ohodnoceni = [x, y, self.minimax(hloubka - 1, plan, -hrac_na_tahu)[2]]
					# Odebrání
					plan[x][y] = 0
					self.tahy -= 1

					if hrac_na_tahu == self.hrac:
						if ohodnoceni[2] < nejlepsi[2]:
							nejlepsi = ohodnoceni
					else:
						if ohodnoceni[2] > nejlepsi[2]:
							nejlepsi = ohodnoceni

				# TODO: parametrizovat počet potřebný pro výhru
				elif self.pocet_v_rade(x, y, plan) == 3:
					if plan[x][y] == self.hrac:
						return [-1, -1, -math.inf]
					else:
						return [-1, -1, math.inf]						

		return nejlepsi

	def pocet_v_rade(self, pole_x, pole_y, plan):
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
		pocitac_max = -math.inf
		hrac_max = -math.inf

		for x in range(self.sirka):
			for y in range(self.vyska):
				if plan[x][y] == self.hrac:
					hodnota = self.pocet_v_rade(x, y, plan)
					if hodnota > hrac_max:
						hrac_max = hodnota
					
				elif plan[x][y] == self.pocitac:
					hodnota = self.pocet_v_rade(x, y, plan)
					if hodnota > pocitac_max:
						pocitac_max = hodnota

		return pocitac_max - hrac_max

	def je_na_planu(self, pole_x, pole_y):
		if pole_x < 0 or pole_x >= self.sirka:
			return False
		if pole_y < 0 or pole_y >= self.vyska:
			return False
		else:
			return True


okno = Tk()


#TODO: pocet kamenu potrebnych pro vitezstvi jako parametr
hra = Piskvorky(okno, 3, 3)

okno.mainloop()