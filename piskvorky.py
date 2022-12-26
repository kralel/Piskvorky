from turtle import exitonclick, forward, left, right, circle, speed, setpos, hideturtle, pendown, penup, home, color, width
from math import sqrt

try:
	sit = int(input("Zadej počet sloupců a řádků ve čtvercové síti:"))
except ValueError:
	print("Nebylo zadáno číslo!")
	exit()
sloupec = sit
radek = sit
strana = 50
uhlopricka = sqrt(strana**2+strana**2)

def krizek(x, y):
	penup()
	home()							# Umístění do poč. bodu a nulové rotace
	setpos(x*strana, y*strana)
	right(45)
	forward(10)
	width(5)
	color("blue")
	pendown()
	forward(uhlopricka-20)
	penup()
	forward(10)
	right(135)
	forward(strana)
	right(135)
	forward(10)
	pendown()
	forward(uhlopricka-20)
	penup()

def kolecko (x, y):
	penup()
	home()
	setpos(x*strana, y*strana)
	right(90)
	forward(strana)
	left(90)
	forward(strana/2)
	left(90)
	forward(5)
	right(90)
	width(5)
	color("red")
	pendown()
	circle(strana/2-5)
	penup()


speed(0)
hideturtle()

plan=[]
for y in range(radek):
	plan.append([])
	for x in range(sloupec):
		plan[y].append(0)
		for i in range(4):
			forward(strana)
			right(90)
		forward(strana)
	left(180)
	forward(sloupec*strana)
	left(90)
	forward(strana)
	left(90)



speed("normal")
tahy = 0										# Počet umístěných znaků


while tahy != sloupec*radek:								# Existuje volné pole?
	# Počítání od 0 => "zadané pole" - 1
	# Turtle - poč. souřadnic vlevo dole X Hráč - poč. souřadnic vlevo nahoře => -y
	try:
		x = int(input("Hráč " + str(tahy%2 + 1) + ": zadej číslo sloupce:"))-1	
		y = -(int(input("Hráč " + str(tahy%2 + 1) + ": zadej číslo řádku:"))-1)
	except ValueError:
		print("Nebylo zadáno číslo!")

	if x < sloupec and x >= 0 and y > -radek and y <= -0:
		if plan[y][x] != 0:						# Je dané pole volné?
			print("Pole je obsazené!")
			continue
		elif tahy%2 == 0:						# Hráč 1
			krizek(x, y)
			plan[y][x] = 1
			tahy += 1
			
		else:									# Hráč 2
			kolecko(x, y)
			plan[y][x] = 2
			tahy += 1
			
	else:
		print("Neplatné pole!")

if tahy == sloupec*radek:
	print("Hrací pole je plné! Konec hry.")
	exitonclick()