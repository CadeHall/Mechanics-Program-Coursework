from tkinter import *
import math
import saves
import menus
import calculus
import random

bkgd = '#dde7f2'
bkgd1 = '#878ecd'
btn_font = "Helvetica 14 bold"
title_font = "Helvetica 36 bold"
projectiles_input = [[['Target Position', 'e'], ['Target Height', 'e']],
                     [['Height', 'e'], ['Speed', 'e'], ['Angle', 'e'], ['Length', 'e'], ['Mass', 'e'], ['Gravity', 'e']]]

px_m = 50
step = 0.008

class Ball:

    def __init__(self, parent, canvas, sim_type, count, mass = 1, colour = 'light blue', position = [0, 0], xvel = 0, yvel = 0):
        self.time = step
        self.pause = False
        self.recent = 11
        
        self.count = count
        self.parent = parent
        self.canvas = canvas
        self.sim_type = sim_type
        self.mass = float(mass)
        self.colour = colour
        self.position = [position[0] * px_m, 0]
        self.radius = 7 * self.mass
        if self.mass > 30:
            self.radius = 210
            
        self.xvel = float(xvel)
        self.yvel = float(yvel)
        self.speed = abs(self.xvel)
        self.height = self.parent.window.winfo_height()
        self.width = self.parent.window.winfo_width()
        self.Ball = self.canvas.create_oval(self.position[0] + (self.width/2) - self.radius, 
                                           (self.height - 143)/2 - self.position[1] - self.radius,
                                           self.position[0] + (self.width/2) + self.radius, 
                                           (self.height - 143)/2 - self.position[1] + self.radius,
                                           fill = self.colour)

    def play(self):
        if not self.pause:
            self.timeLabel.config(text = 'Time:  ' + str(self.time)[:5])
            
            if not self.parent.collision(self.parent.sim_data[1], self.parent.sim_data[2], self.parent.sim_data[3]):
                self.height = self.parent.window.winfo_height()
                self.width = self.parent.window.winfo_width()
                
                if self.sim_type == 'a':
                    self.xvel = self.parent.functions[0].calculate(self.time)
                    self.yvel = self.parent.functions[1].calculate(self.time)
                
                self.position[0] = self.position[0] + self.xvel * px_m * step             
                self.position[1] = self.position[1] + self.yvel * px_m * step
                
                self.canvas.coords(self.Ball, self.position[0] + (self.width/2) - self.radius, 
                               (self.height - 143)/2 - self.position[1] - self.radius,
                               self.position[0] + (self.width/2) + self.radius, 
                               (self.height - 143)/2 - self.position[1] + self.radius)
        
            self.text_box()
            self.time += step
            self.canvas.after(int(1000 * step), self.play)

    def text_box(self):
        start = 0
        self.text = [self.xvel, (0.5 * self.mass * self.xvel ** 2), self.xvel, self.position[0]/px_m, self.yvel, self.position[1]/px_m]
        self.box_labels = [['Velocity:  ', ' m/s'], ['Kinetic Energy:  ', ' J'], ['Velocity:  ', ' m/s'], ['Displacement:  ', ' m'], ['Velocity:  ', ' m/s'], ['Displacement:  ', ' m']]

        if self.sim_type == 'a':
            start = 2

        for i in range(len(self.text)):
            temp = self.text[i]
            self.intpart = math.floor(abs(temp))
            self.decimalpart = abs(temp) - self.intpart

            if i < 0:
                self.text[i] = '-' + str(self.intpart)

            else:
                self.text[i] = str(self.intpart)

            self.text[i] += str(self.decimalpart)[1:5]

            if abs(temp) < 0.0001:
                self.text[i] = '0.000'
                
        for i in range(2):
            self.infobox[self.count][i+1].config(text = self.box_labels[start + i][0] + self.text[start + i] + self.box_labels[start + i][1])

            if self.sim_type == 'a':
                self.infobox[1][i+1].config(text = self.box_labels[start + 2 + i][0] + self.text[start + 2 + i]  + self.box_labels[start + 2 + i][1])


class Arrow:

    def __init__(self, parent, canvas, length = 10, mass = 1, position = [0, 0], speed = 10, angle = 0, gravity = 9.8):
        self.time = 0
        self.pause = True
        self.parent = parent
        self.window = self.parent.window
        self.height = self.window.winfo_height() - 40
        self.colour = 'black'
        
        self.canvas = canvas
        self.mass = mass
        self.position = [position[0], position[1]*px_m]
        self.speed = speed
        self.angle = math.radians(angle)
        self.xvel = speed * math.cos(self.angle)
        self.yvel = speed * math.sin(self.angle)
        self.acceleration = -1 * gravity
        self.length = length * px_m
        if self.length > 200:
            self.length = 200
        self.Arrow = self.canvas.create_line(self.position[0], self.height - self.position[1],
                                             self.position[0] - self.length * math.cos(self.angle),
                                             self.height - (self.position[1] - self.length * math.sin(self.angle)),
                                             fill = self.colour, 
                                             arrow = 'first')
        
    def refresh(self, parent, canvas, length, mass, position, speed, angle, gravity):
        self.parent = parent
        self.pause = False
        self.window = self.parent.window
        self.height = self.window.winfo_height() - 40
        self.colour = 'black'    
        self.canvas = canvas
        self.mass = mass
        self.position = [position[0], position[1]*px_m]
        self.speed = speed
        self.angle = math.radians(angle)
        self.xvel = speed * math.cos(self.angle)
        self.yvel = speed * math.sin(self.angle)
        self.acceleration = -1 * gravity
        self.length = length * px_m

    def play(self):
        self.timeLabel.config(text = 'Time:  ' + str(self.time)[:5] + 's')
        if not self.pause:
            self.height = self.window.winfo_height() - 40
            self.position[0] += self.xvel * px_m * step
            self.position[1] += self.yvel * px_m * step
                
            self.canvas.coords(self.Arrow, self.position[0], self.height - self.position[1],
                               self.position[0] - self.length * math.cos(self.angle),
                               self.height - (self.position[1] - self.length * math.sin(self.angle)))

            if not self.parent.collision([self, self.parent.parent.currentSim.target], 1, 1):
                self.yvel = round(self.yvel + self.acceleration * step, 8)
                self.angle = math.atan(self.yvel / self.xvel)
                self.text_box()

            else:
                self.yvel = 0
                self.xvel = 0

            self.time += step
            self.canvas.after(int(1000 * step), self.play)

    def text_box(self):
        self.text = [(0.5 * self.mass * (self.xvel ** 2 + self.yvel ** 2)), -1 * self.mass * self.acceleration * self.position[1]/px_m]

        for i in range(len(self.text)):
            temp = self.text[i]
            self.intpart = math.floor(abs(temp))
            self.decimalpart = abs(temp) - self.intpart

            if i < 0:
                self.text[i] = '-' + str(self.intpart)

            else:
                self.text[i] = str(self.intpart)

            self.text[i] += str(self.decimalpart)[1:5]

            if abs(temp) < 0.0001:
                self.text[i] = '0.000'

        self.infobox[0].config(text = 'Kinetic Energy:  ' + self.text[0] + ' J')
        self.infobox[1].config(text = 'Potential Energy:  ' + self.text[1] + ' J')
                

class Target:

    def __init__(self, canvas, window, colour = "red", height = 200, width = 50, position = [0, 0]):
        self.pause = False
        self.window = window
        self.canvas = canvas
        self.colour = colour
        self.height = height
        self.width = width
        self.position = position
        self.Target = self.canvas.create_rectangle(self.position[0], 700 - self.height,
                                                   self.position[0] + self.width, 700,
                                                   fill = self.colour)


    def play(self):
        if not self.pause:
            self.w_height = self.window.winfo_height() - 40
            self.canvas.coords(self.Target, self.position[0], self.w_height,
                               self.position[0] + self.width, self.w_height - self.height)

            self.canvas.after(8, self.play)


class Sim:

    def __init__(self, sim_id, sim_type, title, win, parent):
        self.sim_id = sim_id
        self.sim_type = sim_type
        self.title = title
        self.parent = parent
        self.window = win
        self.simDisplay = menus.SimulationScreen(self.title, self.window, self, self.sim_type)
        self.canvas = self.simDisplay.cn_main

        self.width  = self.window.winfo_width()
        self.height = self.window.winfo_height()
        self.functions = []
        self.sim_objects = []

    def getData(self, sim_id, data_top, data_bottom):
        self.dataMerge = data_top + data_bottom
        self.data = []
        self.count = 0

        try:
            if self.sim_type == 'c':
                self.balls = []
                
                for i in range(4):
                    if data_bottom[4*i] != '':
                        temp = Ball(self, self.canvas, self.sim_type, self.count, data_bottom[4*i], data_bottom[4*i + 3], [int(data_bottom[4*i + 1]), 0], data_bottom[4*i + 2], 0)
                    
                        if data_top[2] == 1:
                            temp.pause = True

                        self.sim_objects.append(temp)
                        self.count += 1

                    else:
                        temp = []
                    
                    self.balls.append(temp)
                    self.emptyCheck = 0

                    for j in self.balls:
                        if j != []:
                            self.emptyCheck += 1
                    
                    if self.emptyCheck == 0:
                        return ['e', 'Make sure you enter some values.']

                for j in range(5):
                    try:
                        tempdata = float(data_top[3 + j])
                        if tempdata >= 1:
                            return ['e', 'A coefficient of restitution has to be between\n0 and 1']

                    except:
                        pass

                self.ball_pairs = [[self.balls[0], self.balls[1], data_top[3]], [self.balls[0], self.balls[2], data_top[4]],
                                    [self.balls[0], self.balls[3], data_top[5]], [self.balls[1], self.balls[2], data_top[6]],
                                    [self.balls[1], self.balls[3], data_top[7]], [self.balls[2], self.balls[3], data_top[8]]]

                self.data = [self.balls, self.ball_pairs, data_top[0], data_top[1]]

            elif self.sim_type == 'a':
                for i in range(2):
                    for j in range(4):
                        self.formula = data_bottom[4*(i+1) - 1 - j]
            
                        if self.formula != '':
                            self.function = calculus.Expression(data_top[4], self.formula)
                            if j == 0:
                                self.function.differentiate()

                            elif j != 1:
                                self.function.integrate()
                                self.function.solve(float(data_top[5]), float(data_top[6+i]))

                            if j == 3:
                                for term in self.function.final_terms:
                                    term.coefficient = term.coefficient / float(data_top[2])
                                    
                            self.functions.append(self.function)
                            break

                if int(data_top[1]) > 100:
                    data_top[1] = 100
                    
                self.particle = Ball(self, self.canvas, self.sim_type, 0, data_top[2], data_top[3], [0, 0], 0, 0)
                self.particle.radius = int(data_top[1])
                self.sim_objects.append(self.particle)
                self.data = [[self.particle], [], data_top[0], []]

            return self.data

        except Exception as err:

           return ['e', err]    

    def save(self):
        self.simDisplay.discard()
        self.saveScreen = menus.SaveMenu('Save Simulation', self.window, self)
        self.saveScreen.create()

    def finalSave(self, name, description):
        self.savesDB = saves.Database()

        if name.get() != '':
            try:
                if self.sim_type == 'a':
                    self.saveData = [name.get(), description.get(1.0, 'end'), self.sim_objects[0],
                                     [self.dataMerge[0], self.dataMerge[4], self.functions[0].convert_to_string(), self.functions[1].convert_to_string()]]

                elif self.sim_type == 'c':
                    for obj in self.sim_objects:
                        obj.position[0] = obj.position[0]/px_m
                        
                    self.saveData = [name.get(), description.get(1.0, 'end'), self.sim_objects, [self.dataMerge[0],
                                     self.dataMerge[1], self.dataMerge[2], self.dataMerge[3], self.dataMerge[4],
                                      self.dataMerge[5], self.dataMerge[6], self.dataMerge[7], self.dataMerge[8]]]

                self.savesDB.save(self.sim_type, self.saveData)
                self.savesDB.finish()

                self.parent.newScreen(self.saveScreen, 'b')

            except Exception as err:
                self.error = menus.ErrorScreen('Your input was not understood, please try again.\n\n' + str(err))
            
        else:
            self.error = menus.ErrorScreen('You have not given a name for the save.')

    def run(self, data_top, data_bottom):
        if self.sim_type != 'p':
            self.sim_data = self.getData(self.sim_id, data_top, data_bottom)

            if self.sim_data[0] != 'e':

                if self.sim_type == 'c':
                    self.simDisplay.infoBox(self.sim_objects)

                if self.sim_type == 'a':
                    self.simDisplay.infoBox(self.functions)

                for i in range(len(self.sim_objects)):
                    ball = self.sim_objects[i]
                    ball.infobox = self.simDisplay.itemBoxes
                    ball.timeLabel = self.simDisplay.l_time
                    ball.play()

                if self.sim_objects[0].pause:
                    self.simDisplay.b_pause.config(text = 'Resume')

            else:
                self.error = menus.ErrorScreen('Your input was not understood, please try again.\n\n' + str(self.sim_data[1]))
                self.parent.newScreen(self.simDisplay, 'b')
                
        else:
            self.simDisplay.drawInputs(projectiles_input)
            self.target = Target(self.canvas, self.window, 'red', 200, 50, [600, 0])
            self.target.play()

            self.arrow = Arrow(self, self.canvas, 0, 0, [200, -5000], 1, 0, 0)
            self.arrow.infobox = self.simDisplay.infoBox([])
            self.arrow.timeLabel = self.simDisplay.l_time
            self.arrow.play()

            self.sim_objects = [self.arrow, self.target]
            if self.arrow.pause:
                self.simDisplay.b_pause.config(text = 'Resume')

    def update_cn(self, data):
        try:
            self.target.position[0] = int(data[0].get()) * px_m
            self.target.height = int(data[1].get()) * px_m

        except Exception as err:
            self.error = menus.ErrorScreen('Your input was not understood, please try again.\n\n' + str(err))
              

    def new_arrow(self, canvas, data):
        try:
            self.arrow.refresh(self, self.canvas, float(data[5].get()), float(data[6].get()),
                            [200, int(data[2].get())], float(data[3].get()), float(data[4].get()), float(data[7].get()))

            self.arrow.canvas.coords(self.arrow.Arrow, self.arrow.position[0], self.arrow.height - self.arrow.position[1],
                               self.arrow.position[0] - self.arrow.length * math.cos(self.arrow.angle),
                               self.arrow.height - (self.arrow.position[1] - self.arrow.length * math.sin(self.arrow.angle)))

            self.arrow.time = 0
            if not self.arrow.pause:
                self.arrow.pause = True
                self.simDisplay.b_pause.config(text = 'Resume')
            
        except Exception as err:
            self.error = menus.ErrorScreen('Your input was not understood, please try again.\n\n' + str(err))

    def newScreen(self, old, inpt):
        self.parent.newScreen(old, inpt)

    def pause(self):
        if self.sim_type != 'p':
            self.objects = self.sim_objects

        else:
            self.objects = [self.sim_objects[0]]
            
        for obj in self.objects:
            if obj.pause == True:
                obj.pause = False
                self.simDisplay.b_pause.config(text = 'Pause')
                obj.play()

            elif obj.pause == False:
                obj.pause = True
                self.simDisplay.b_pause.config(text = 'Resume')
        
    def collision(self, pairs, wall, elastic):
        self.width  = self.window.winfo_width()
        self.height = self.window.winfo_height()
        self.coll = False

        if self.sim_type == 'p':
            self.arrow = pairs[0]
            self.target = pairs[1]

            if (self.target.position[0] < self.arrow.position[0] < self.target.position[0] + self.target.width) and (self.height - self.target.height < self.height - self.arrow.position[1] < self.height):
                return True

            else:
                return False
             
        if wall == 1:
            self.wall_detect()

        if self.sim_type == 'c':
            for pair in pairs:
                self.left = pair[0]
                self.right = pair[1]

                if not (self.left == [] or self.right == []):
                    if self.right.position[0] < self.left.position[0]:
                        self.left = pair[1]
                        self.right = pair[0]
                        
                    self.total_radius = self.right.radius + self.left.radius
                    self.closeness = self.right.position[0] - self.left.position[0] - self.total_radius
                    
                    if self.closeness <= 0 and self.left.recent > 10:
                        self.coll = True
                        self.total_mass = self.left.mass + self.right.mass
                        self.left.recent = 0
                        self.right.recent = 0
                        
                        if elastic == 1:
                            self.l_xvel = self.left.xvel
                            self.r_xvel = self.right.xvel
                            
                            self.left.xvel = ((((self.left.mass - self.right.mass)/self.total_mass) * self.l_xvel) + 
                                              (((2 * self.right.mass)/self.total_mass) * self.r_xvel))

                            self.right.xvel = ((((self.right.mass - self.left.mass)/self.total_mass) * self.r_xvel) + 
                                              (((2 * self.left.mass)/self.total_mass) * self.l_xvel))

                        else:
                            if pair[2] != '':
                                self.restitution = float(pair[2])
                            else:
                                self.restitution = 0.5
                                
                            self.momentum = (self.right.mass * self.right.xvel) + (self.left.mass * self.left.xvel)
                            self.rel_speed = self.left.speed + self.right.speed
                            
                            self.left.xvel = ((self.momentum - (self.right.mass * self.restitution * self.rel_speed)) / self.total_mass)
                            self.right.xvel = ((self.momentum + (self.left.mass * self.restitution * self.rel_speed)) / self.total_mass)

                        self.right.position[0] += self.right.xvel
                        self.left.position[0] += self.left.xvel                        
                        self.right.speed = abs(self.right.xvel)
                        self.left.speed = abs(self.left.xvel)

        return self.coll

    def wall_detect(self):
        for obj in self.sim_objects:
            obj.recent += 1
            if self.width - (obj.position[0] + (self.width/2)) <= obj.radius or obj.position[0] + (self.width/2) <= obj.radius and obj.recent > 10:
                self.coll = True
                if self.sim_type == 'a':
                    obj.xvel = 0
                    for term in obj.parent.functions[0].final_terms:
                        term.coefficient = term.coefficient * -1

                    obj.xvel = obj.parent.functions[0].calculate(obj.time)

                else:
                    obj.recent = 0
                    obj.xvel = obj.xvel * -1

                obj.position[0] += obj.xvel

            if (self.height/2) - obj.position[1] - 70 <= obj.radius or (self.height - 115)/2 + obj.position[1] <= obj.radius and obj.recent > 10:
                self.coll = True
                if self.sim_type == 'a':
                    obj.yvel = 0
                    for term in obj.parent.functions[1].final_terms:
                        term.coefficient = term.coefficient * -1

                    obj.yvel = obj.parent.functions[1].calculate(obj.time)

                else:
                    obj.yvel = obj.yvel * -1
                    obj.recent = 0

                obj.position[1] += obj.yvel

































            
