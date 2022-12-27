from turtle import exitonclick, forward, left, right, circle, speed, setpos, hideturtle, pendown, penup, home, color, width
from math import sqrt

class Piskvorky:
	sit = 3
	strana = 50
	uhlopricka = sqrt(strana**2+strana**2)
	plan=[]
	tahy = 0										# Počet umístěných znaků

	def __init__(self, sit, strana):
		for y in range(sit):
			self.plan.append([])
			for x in range(sit):
				self.plan[y].append(0)
				for i in range(4):
					forward(strana)
					right(90)
				forward(strana)
			left(180)
			forward(sit*strana)
			left(90)
			forward(strana)
			left(90)

	def krizek(self, x, y):
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

	def kolecko (self,x, y):
		penup()
		home()
		setpos(x*self.strana, y*self.strana)
		right(90)
		forward(self.strana)
		left(90)
		forward(self.strana/2)
		left(90)
		forward(5)
		right(90)
		width(5)
		color("red")
		pendown()
		circle(self.strana/2-5)
		penup()

	def pocet_v_rade(self,x,y):
		v_rade = 1
		while self.plan[y][x] == self.plan[y-1][x]:
			v_rade += 1
		return v_rade

	def tah(self):
		while self.tahy != self.sit*self.sit:								# Existuje volné pole?
		# Počítání od 0 => "zadané pole" - 1
		# Turtle - poč. souřadnic vlevo dole X Hráč - poč. souřadnic vlevo nahoře => -y
			try:
				x = int(input("Hráč " + str(self.tahy%2 + 1) + ": zadej číslo sloupce:"))-1	
				y = -(int(input("Hráč " + str(self.tahy%2 + 1) + ": zadej číslo řádku:"))-1)
			except ValueError:
				print("Nebylo zadáno číslo!")

			if x < self.sit and x >= 0 and y > -self.sit and y <= -0:
				pole = self.plan[y][x]
				if pole != 0:						# Je dané pole volné?
					print("Pole je obsazené!")
					continue
				elif self.tahy%2 == 0:						# Hráč 1
					self.krizek(x, y)
					pole = 1
					self.tahy += 1
				
				else:									# Hráč 2
					self.kolecko(x, y)
					pole = 2
					self.tahy += 1
				
			else:
				print("Neplatné pole!")

speed(0)
hideturtle()


speed("normal")




#if tahy == sit*sit:
#	print("Hrací pole je plné! Konec hry.")
#	exitonclick()

hra = Piskvorky(3,50)
