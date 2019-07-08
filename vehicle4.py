import turtle
import random
import math

'''
    Modify this program in the following ways:
        - Add at least 1 more class representing another kind of input other than heat.
        - Have the input_list contain multiple kinds of input sources.
        - Use custom images for each input sources
        - Modify vehicle 3 so that it has an 'innate preference' or 'innate dislike' of each kind of input 
'''



class HeatSource(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__(self, visible = False)
        self.shape('sun.gif')
        self.penup()
        self.color(255, 190, 60)
        self.goto(random.randint(-200, 200), random.randint(-200, 200))
        self.showturtle()

class FoodSource(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self, visible = False)
        self.shape('food.gif')
        self.penup()
        self.color(200, 200, 60)
        self.goto(random.randint(-200, 200), random.randint(-200, 200))
        self.showturtle()

class Vehicle3(turtle.Turtle):

    def __init__(self, input_list1, input_list2, vehicle_id, vehicle_type):
        turtle.Turtle.__init__(self, visible = False)
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.input_list = [input_list1, input_list2]
        #self.input_list2 = input_list2
        self.create_vehicle()
        self.speed_parameters = [20, 0.2, 6]
        self.turn_parameters = [20]
        self.moves = 0

    def create_vehicle(self):
        self.shape('turtle')
        self.turtlesize(1)
        self.penup()
        if self.vehicle_type == 'crossed':
            self.color(random.randint(0, 150), random.randint(0, 150), 255)
        else:
            self.color(255, random.randint(0, 150), random.randint(0, 150))
        self.goto(random.randint(-290, 290), random.randint(-290, 290))
        self.right(random.randint(0, 360))
        self.pendown()
        self.showturtle()


    def get_input_information(self, position1, position2):
        input_heat_distance = self.distance(position1)
        input_heat_angle = self.heading() - self.towards(position1)
        input_food_distance = self.distance(position2)
        input_food_angle = self.heading() - self.towards(position2)
        return input_heat_distance, input_heat_angle, input_food_distance, input_food_angle


    def get_sensor_distances(self, distance1, angle1, distance2, angle2):
        sin_angle1 = math.sin(math.radians(angle1))
        left_distance1 = distance1 - sin_angle1
        right_distance1 = distance1 + sin_angle1
        combined_distance1 = math.sqrt(left_distance1 ** 2 + right_distance1 ** 2)
        sin_angle2 = math.sin(math.radians(angle2))
        left_distance2 = distance2 - sin_angle2
        right_distance2 = distance2 + sin_angle2
        combined_distance2 = math.sqrt(left_distance2 ** 2 + right_distance2 ** 2)
        return left_distance1, right_distance1, left_distance2, right_distance2, combined_distance1, combined_distance2

    def compute_speed(self, left_distance1, right_distance1, left_distance2, right_distance2, combined_distance1, combined_distance2):
        if combined_distance2 > combined_distance1:
            if self.vehicle_type == 'crossed':
                left_speed = (self.speed_parameters[0] / (right_distance1 ** self.speed_parameters[1])) - self.speed_parameters[2]
                right_speed = (self.speed_parameters[0] / (left_distance1 ** self.speed_parameters[1])) - self.speed_parameters[2]

            else:
                left_speed = (self.speed_parameters[0] / (left_distance1 ** self.speed_parameters[1])) - self.speed_parameters[2]
                right_speed = (self.speed_parameters[0] / (right_distance1 ** self.speed_parameters[1])) - self.speed_parameters[2]
            
            if combined_distance1 > 10:
                combined_speed = (left_speed + right_speed) / 10
            else:
                combined_speed = (left_speed + right_speed) / 2

        else:
            if self.vehicle_type == 'crossed':
                left_speed = (self.speed_parameters[0] / (right_distance2 ** self.speed_parameters[1])) - self.speed_parameters[2]
                right_speed = (self.speed_parameters[0] / (left_distance2 ** self.speed_parameters[1])) - self.speed_parameters[2]
            else:
                left_speed = (self.speed_parameters[0] / (left_distance2 ** self.speed_parameters[1])) - self.speed_parameters[2]
                right_speed = (self.speed_parameters[0] / (right_distance2 ** self.speed_parameters[1])) - self.speed_parameters[2]

            if combined_distance2 > 10:
                combined_speed = (left_speed + right_speed) / 10
            else:
                combined_speed = (left_speed + right_speed) / 2
                
        return left_speed, right_speed, combined_speed

    def compute_turn_amount(self, left_speed, right_speed):
        turn_amount = self.turn_parameters[0] * (right_speed - left_speed)
        return turn_amount

    def move(self):
            combined_speed = 0
            combined_turn_amount = 0

            
            for current_input in self.input_list:
                for i in range(0, 5):
                    input_heat_distance, input_heat_angle = self.get_input_information(current_input[0][i].position(), current_input[1][i].position())
                left_distance, right_distance = self.get_sensor_distances(input_heat_distance, input_heat_angle, input_food_distance, input_food_angle)
                left_speed, right_speed, average_speed = self.compute_speed(left_distance1, right_distance1, left_distance2, right_distance2, combined_distance1, combined_distance2)
                turn_amount = self.compute_turn_amount(left_speed, right_speed)
                combined_turn_amount += turn_amount
                combined_speed += average_speed

            
            try:
                self.right(combined_turn_amount)
            except:
                print(combined_turn_amount)
            self.forward(combined_speed)
            self.moves += 1


def create_screen():
    wn = turtle.Screen()
    wn.colormode(255)
    wn.setup(1200, 800)
    wn.title("Vehicle 3")
    wn.tracer(0, 0)
    return wn


def main():
    wn = create_screen()
    wn.register_shape('sun.gif')
    wn.register_shape('food.gif')

    num_vehicles = 5
    num_heat_sources = 4
    num_food_sources = 4

    vehicle_list = []
    
    input_list = []
    input_list1 = []
    input_list2 = []

    for i in range(num_heat_sources):
        input_list1.append(HeatSource())
    for i in range(num_food_sources):
        input_list2.append(FoodSource())

    input_list.append(input_list1)
    input_list.append(input_list2)

    for i in range(num_vehicles):
        vehicle_list.append(Vehicle3(input_list[0], input_list[1], i, random.choice(["crossed", "direct"])))

    wn.update()
    while True:
        for j in range(num_vehicles):
            vehicle_list[j].move()
        wn.update()

main()

