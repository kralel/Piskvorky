# Napište hru piškvorky na 3x3 polích. Program nemusí umět vyhodnocovat, že nějaký
# hráč vyhrál, ani kolizi v políčkách. Hráči zadávají souřadnice do konzole,
# průběh hry je vykreslen želví grafikou

from turtle import forward, exitonclick, left, right, circle, speed

a = int(input("Zadej počet sloupců:"))
b = int(input("Zadej počet řádků:"))
strana = 50

speed(10)

for y in range(b):
	for x in range(a):
		for i in range(4):
			forward(strana)
			left(90)
		forward(strana)
	right(180)
	forward(a*strana)
	right(90)
	forward(strana)
	right(90)

speed("normal")

circle(15)

exitonclick()
