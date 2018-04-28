from tkinter import *
import calculus
import menus
import simulations
import saves

window = Tk()
window.title('Mechanics Program')
window.geometry('960x540')
window.minsize(540, 400)

class CoreProgram:

    def __init__(self):
        self.window = window
        self.top1 = [['Solid Walls?', 'c'],['Elastic Collisions?', 'c'],                  
           ['Start Paused?', 'c'],['AB', 'e'], ['AC', 'e'], ['AD', 'e'], ['BC', 'e'], ['BD', 'e'], ['CD', 'e']]

        self.top2 = [['Solid Walls?', 'c'], ['Size', 'e'], ['Mass', 'e'], ['Colour', 'e'],['Variable', 'e'],
                     ['Known variables', 'l', 'Values'], ['Time', 'e'], ['X Velocity', 'e'], ['Y Velocity', 'e'],
                     ['', 'l', '']]

        self.bottom1 = [['Ball A', [['Mass', 'e'], ['Position', 'e'], ['Velocity', 'e'], ['Colour', 'e']]],
           ['Ball B', [['Mass', 'e'], ['Position', 'e'], ['Velocity', 'e'], ['Colour', 'e']]],
           ['Ball C', [['Mass', 'e'], ['Position', 'e'], ['Velocity', 'e'], ['Colour', 'e']]],
           ['Ball D', [['Mass', 'e'], ['Position', 'e'], ['Velocity', 'e'], ['Colour', 'e']]]]

        self.bottom2 = [['X Direction', [['Force', 'e'], ['Acceleration', 'e'], ['Velocity', 'e'], ['Displacement', 'e']]],
                        ['Y Direction', [['Force', 'e'], ['Acceleration', 'e'], ['Velocity', 'e'], ['Displacement', 'e']]]]

    def newScreen(self, old, option):

        if option == 'p':
            self.begin(old, option, [], [])

        elif option == 'e':
            self.exitCheck = menus.ErrorScreen('Are you sure you want to quit?', 'e', self)
            
        else:

            old.discard()
            if option == 'b':
                m = menus.MainMenu(window, self)
                m.create()

            if option == 'l':
                self.simulationDB = saves.Database()
                self.saveData = self.simulationDB.load_for_menu()
                
                load_menu = menus.LoadMenu('Saved Simulations', window, self.saveData, self)
                load_menu.create()
                load_menu.updateDesc()  

            if option == 'c':
                collisions_menu = menus.BaseMenu('Collisions Settings', window, 3, 6, self)
                collisions_menu.display(self.top1, self.bottom1, option)

            if option == 'a':
                acceleration_menu = menus.BaseMenu('Variable Acceleration Settings', window, 5, 4, self)
                acceleration_menu.display(self.top2, self.bottom2, option)

    def begin(self, old, sim_type, datatop, databottom):
        old.discard()
        
        if sim_type == 'c':
            self.currentSim = simulations.Sim(-1, sim_type, 'Collisions', window, self)

        if sim_type == 'a':
            self.currentSim = simulations.Sim(-1, sim_type, 'Variable Acceleration', window, self)

        if sim_type == 'p':
            self.currentSim = simulations.Sim(-1, sim_type, 'Projectiles', window, self)

        for i in range( len(datatop)):
            try:
                datatop[i] = datatop[i].get()
            except:
                pass

        for j in range(len(databottom)):
            try:
                databottom[j] = databottom[j].get()
            except:
                pass
            
        self.currentSim.run(datatop, databottom)
        
    def run(self):
        m = menus.MainMenu(window, self)
        m.create()

        window.mainloop()

            
program = CoreProgram()
program.run()


