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
		pole_x = int(udalost.x/25)
		pole_y = int(udalost.y/25)
		self.kolecko(pole_x, pole_y)
		self.plan[pole_x][pole_y]
		

	'''def krizek(self, x, y):
		penup()
		home()							# Umístění do poč. bodu a nulové rotace
		setpos(x*self.strana, y*self.strana)
		right(45)
		forward(10)
		width(5)
		color("blue")
		pendown()
		forward(self.uhlopricka-20)
		penup()
		forward(10)
		right(135)
		forward(self.strana)
		right(135)
		forward(10)
		pendown()
		forward(self.uhlopricka-20)
		penup()
		'''

	def kolecko (self, x, y):
		self.platno.create_oval((x * strana)+5, (y * strana)+5, ((x + 1) * strana)-5, ((y + 1) * strana)-5, outline="red")

	def pocet_v_rade(self,x,y):
		if x >= self.x or y <= -self.x:
			raise IndexError("Neplatné pole!")
		
		maximum = - math.inf

		# Kontrolování všech možných směrů {nahoru, doleva, doleva nahoru, doprava nahoru}
		for i in [ [0, 1], [-1, 0], [-1, 1], [1, 1] ]:
			v_rade = 1
			j = 1
			while self.plan[y][x] == self.plan[y + (i[1] * j)][x + (i[0] * j)]:
				v_rade += 1
				j += 1
			j = 1
			while self.plan[y][x] == self.plan[y - (i[1] * j)][x - (i[0] * j)]:
				v_rade += 1
				j += 1
			if v_rade > maximum:
				v_rade = maximum
		return v_rade

	def tah(self):
		self.platno_onclick()
		'''if self.plan[y][x] != 0:						# Je dané pole volné?
			print("Pole je obsazené!")
			return
		elif self.tahy%2 == 0:						# Hráč 1
			self.krizek
			self.plan[y][x] = 1
			self.tahy += 1
		else:									# Hráč 2
			self.kolecko(x, y)
			self.plan[y][x] = 2
			self.tahy += 1

		if self.pocet_v_rade(x,y) == 3:
			if self.plan[y][x] == 1:
				print("Vyhrál hráč!")
			else:
				print("Vyhrál počítač!")
'''

okno = Tk()


try:
	hra = Piskvorky(3,3)
except ValueError as v:
	print(v)
	exit()
#try:
#	while hra.tahy != hra.sit*hra.sit:								# Existuje volné pole?
#		hra.tah()
#except IndexError as i:
#	print(i)
#	exit()
	
#if hra.tahy == hra.sit*hra.sit:
#	print("Hrací pole je plné! Konec hry.")

okno.mainloop()