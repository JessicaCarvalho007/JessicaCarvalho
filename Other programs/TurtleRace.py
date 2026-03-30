import turtle
import random
import time


def get_number_racers():
    racers = 'Get Racers'
    while not racers.isdigit() or 3 < int(racers) > 15:
        racers = input("How many turtles would you like to race?\nMin-Max: 3-15\n")
    return int(racers)


def create_field(racers):
    y_field = 25 * racers
    field = turtle.Turtle()
    field.hideturtle()
    field.pu()
    field.speed(0)
    field.setpos(525, y_field)
    field.pd()
    field.setpos(-525, y_field)
    field.setpos(-525, -y_field)
    field.setpos(525, -y_field)
    field.begin_fill()
    field.setpos(525, y_field)
    field.setpos(500, y_field)
    field.setpos(500, -y_field)
    field.end_fill()
    field.setpos(-500, -y_field)
    field.begin_fill()
    field.setpos(-525, -y_field)
    field.setpos(-525, y_field)
    field.setpos(-500, y_field)
    field.end_fill()
    field.pu()
    field.setpos(0, y_field + 10)
    field.write("Racers get ready!!!", move=True, align="center", font=("Verdana", 35, "bold"))

    return racers, y_field, field


def tur_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def play(racers, y_cor, field):
    y_out = msg = y_cor
    y_cor -= 25
    turtles = [turtle.Turtle() for _ in range(racers)]
    turtle.colormode(255)
    colors = [tur_color() for _ in range(len(turtles))]
    for i, tur in enumerate(turtles):
        tur.color(colors[i])
        tur.speed(10)
        tur.penup()
        tur.pensize(20)
        tur.setpos(-500, y_cor)
        tur.pd()
        y_cor -= 50

    time.sleep(2)

    finals = []
    while len(finals) < 3:
        x = random.randint(0, len(turtles) - 1)
        if turtles[x] not in finals:
            turtles[x].forward(random.randint(2, 50))
        if turtles[x].xcor() >= 500:
            if turtles[x] not in finals:
                finals.append(turtles[x])

    time.sleep(1.5)
    race_finals(finals, turtles, y_out, field, msg)


def race_finals(finals, turtles, y_out, field, msg):
    y_final = 50
    for tur in turtles:
        tur.clear()
        if tur not in finals:
            tur.pu()
            tur.setpos(-550, y_out)
            tur.pd()
            tur.forward(10)
            y_out -= 20
        else:
            tur.pu()
            tur.setpos(-500, y_final)
            tur.pd()
            y_final -= 50

    field.setpos(0, -msg - 50)
    field.write("...Finals...", move=True, align="center", font=("Verdana", 35, "bold"))
    time.sleep(2)

    winner = False
    while not winner:
        x = random.randint(0, 2)
        finals[x].forward(random.randint(1, 40))
        if finals[x].xcor() >= 500:
            winner = True
            finals[x].hideturtle()
            finals[x].pu()
            finals[x].setpos(0, -msg - 100)
            finals[x].write("Winner", move=True, align="center", font=("Verdana", 35, "bold"))
    turtle.done()


def main():
    racers = get_number_racers()
    field = create_field(racers)
    play(*field)


if __name__ == "__main__":
    main()
