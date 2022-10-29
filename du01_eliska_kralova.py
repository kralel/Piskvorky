# Napište hru piškvorky na 3x3 polích. Program nemusí umět vyhodnocovat, že nějaký
# hráč vyhrál, ani kolizi v políčkách. Hráči zadávají souřadnice do konzole,
# průběh hry je vykreslen želví grafikou

from turtle import forward, exitonclick, left, right, circle, speed, setpos, hideturtle, pendown, penup, home
from math import sqrt

a = int(input("Zadej počet sloupců:"))
b = int(input("Zadej počet řádků:"))
strana = 50
uhlopricka = sqrt(strana**2+strana**2)
def krizek(x, y):
	penup()
	setpos(x*strana, y*strana)
	right(45)
	penup()
	forward(10)
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
	home()
	

speed(10)
#hideturtle()

rows=[]
for y in range(b):
	rows.append([])
	for x in range(a):
		rows[y].append(0)
		for i in range(4):
			forward(strana)
			right(90)
		forward(strana)
	left(180)
	forward(a*strana)
	left(90)
	forward(strana)
	left(90)

speed("normal")

while rows != [1, 1, 1]:
	x = int(input("Zadej číslo sloupce:"))
	y = int(input("Zadej číslo řádku:"))
	krizek(x-1, -(y-1))	# Turtle - poč. souřadnic vlevo dole X hráč - poč. souřadnic vlevo nahoře => -y

if rows == [1, 1, 1]:
	print("Hrací pole je plné! Konec hry.")
	exit()

exitonclick()
