import turtle
import random


class HeatSource(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__(self, visible = False)
        self.shape('circle')
        self.penup()
        self.color(255, 190, 60)
        self.goto(0, 0)
        self.showturtle()


class Vehicle1(turtle.Turtle):

    def __init__(self, heatsource1, wn):
        turtle.Turtle.__init__(self, visible = False)
        self.heatsource = heatsource1
        self.onclick(self.move)
        self.create_turtle()
        self.wn = wn

    def create_turtle(self):
        self.shape('classic')
        self.turtlesize(2)
        self.penup()
        self.color(0, 0, 255)
        self.goto(random.randint(-390, 390), random.randint(-390, 390))
        # set original location
        self.right(random.randint(0, 360))
        # where the arrow is pointing towards
        self.showturtle()

    def move(self, x, y):
        speed = 1
        while speed > 0:
            distance = self.distance(self.heatsource.position())
            right_distance = distance + 3
            left_distance = distance - 3
            right_speed = (80 / (right_distance ** 0.2)) - 16
            # numerator: controlling speed / affect radius of the feeling center;
            left_speed = (80 / (left_distance ** 0.2)) - 16
            if left_speed - right_speed > 0:
                self.right(60 * (left_speed - right_speed))
                self.forward(100 * (left_speed - right_speed))
            print(100 * (left_speed - right_speed), right_distance, left_distance)
            self.wn.update()
            # show the location after moving


def create_screen():
    wn = turtle.Screen()
    wn.colormode(255)
    wn.setup(1200, 800)
    wn.title("Vehicle 1")
    return wn


def main():
    wn = create_screen()
    wn.tracer(0, 0)
    # don't update unless told to.
    heatsource1 = HeatSource()
    vehicle_list = []
    for i in range(10):
        vehicle_list.append(Vehicle1(heatsource1, wn))
    wn.update()
    wn.mainloop()


main()

            