from tkinter import *
import saves

bkgd = '#dde7f2'
bkgd1 = '#878ecd'
btn_font = "Helvetica 14 bold"
title_font = "Helvetica 36 bold"


class Menu():

    def __init__(self, win, name, parent):
        self.parent = parent
        self.check = False
        self.f_main = Frame(win, bg = bkgd)

        self.f_header = Frame(self.f_main, bg = bkgd1, height = 40)
        self.f_base = Frame(self.f_main, bg = bkgd)
        self.l_head = self.l_head = Label(self.f_header, bg = '#878ecd', text = name, font = btn_font)        
        self.b_back = Button(self.f_header, text = 'Back', font = btn_font, bg = bkgd1, width = 8, activebackground = bkgd1, relief = 'flat', command = lambda: self.parent.newScreen(self, 'b'))

        self.f_header.pack(fill = 'x')
        self.createSep(self.f_main).pack(fill = 'x', side = 'top')
        self.f_base.pack(fill = 'both', expand = True)
        self.l_head.place(anchor = 'c', y = 20, relx = 0.5)
        self.b_back.pack(side = 'left')
        self.createSep(self.f_header).pack(side = 'left', fill = 'y')
        self.f_main.pack(fill = 'both', expand = True)

    def createSep(self, frame):
        return Frame(frame, bg = 'black', height = 2, width = 2)

    def createInpt(self, frame, lst, option):
        temp = Label(frame, bg = bkgd, text = 'ERROR OOPS', font = btn_font)
        if option[1] == 'e':
            var = StringVar()
            temp = Entry(frame, textvariable = var)
            lst.append(var)

        if option[1] == 'c':
            var = IntVar()
            temp = Checkbutton(frame, bg = bkgd, variable = var)
            lst.append(var)

        if option[1] == 'l':
            temp = Label(self.f_baseOps, bg = bkgd, text = option[2], font = btn_font)

        return temp

    def createTop(self):
        raise NotImplementedError

    def createBottom(self):
        raise NotImplementedError

    def gridConfig(self, frame, rows, columns):
        for i in range(rows):
            frame.rowconfigure(i, weight = 1)

        for j in range(columns):
            frame.columnconfigure(j, weight = 1)

    def display(self, top, bottom, sim_type):
        if self.check:
            self.__init__()

        self.createTop(top, sim_type)
        try:
            self.createBottom(bottom)
        except:
            pass

    def discard(self):
        self.check = True
        self.f_main.destroy()


class MainMenu():

    def __init__(self, win, parent):
        self.parent = parent
        self.f_main = Frame(win, bg = bkgd)
        self.f_main.pack(fill = 'both', expand = True)

        self.f_buttons = Frame(self.f_main, bg = 'black')
        self.f_buttons.place(anchor = 'c', rely = 0.7, relx = 0.5, relwidth = 0.3)

    def create(self):
        self.l_head = Label(self.f_main, bg = bkgd, text = 'Mechanics Simulations', font = title_font)
        self.l_head.place(anchor = 'c', rely = 0.3, relx = 0.5)

        self.b_load = Button(self.f_buttons, text = 'Load', font = btn_font, bg = 'white', activebackground = 'white', relief = 'flat', command = lambda: self.parent.newScreen(self, 'l'))
        self.b_collisions = Button(self.f_buttons, text = 'Collisions', font = btn_font, bg = 'white', activebackground = 'white', relief = 'flat', command = lambda: self.parent.newScreen(self, 'c'))
        self.b_projectiles = Button(self.f_buttons, text = 'Projectiles', font = btn_font, bg = 'white', activebackground = 'white', relief = 'flat', command = lambda: self.parent.newScreen(self, 'p'))
        self.b_acceleration = Button(self.f_buttons, text = 'Variable Acceleration', font = btn_font, bg = 'white', activebackground = 'white', relief = 'flat', command = lambda: self.parent.newScreen(self, 'a'))
        self.b_exit = Button(self.f_buttons, text = 'Exit', font = btn_font, bg = 'white', activebackground = 'white', relief = 'flat', command = lambda: self.parent.newScreen(self, 'e'))

        self.b_load.pack(fill = X, padx = 3, pady  = 3)
        self.b_collisions.pack(fill = X, padx = 3)
        self.b_projectiles.pack(fill = X, padx = 3, pady = 3)
        self.b_acceleration.pack(fill = X, padx = 3)
        self.b_exit.pack(fill = X, padx = 3, pady = 3)

    def discard(self):
        self.check = True
        self.f_main.destroy()

        
class BaseMenu(Menu):

    def __init__(self, name, win, height, width, parent):
        Menu.__init__(self, win, name, parent)

        self.f_baseOps = Frame(self.f_base, bg = bkgd)
        self.f_secondOps = Frame(self.f_base, bg = bkgd)

        self.width = width
        self.height = height
        self.count = 0

        self.gridConfig(self.f_baseOps, height, width)

        self.f_baseOps.place(relwidth = 1, relheight = 0.4)
        self.createSep(self.f_base).place(relwidth = 1, rely = 0.4)
        self.f_secondOps.place(relwidth = 1, relheight = 0.6, rely = 0.4)

        self.base_inpt = []
        self.second_inpt = []
        self.boxes = []

    def createTop(self, inpt, sim_type):
        self.b_begin = Button(self.f_secondOps, text = 'Begin!', font = btn_font, bg = bkgd1, activebackground = bkgd1, relief = 'flat', command = lambda: self.parent.begin(self, sim_type, self.base_inpt, self.second_inpt))        
        self.b_begin.pack(side = 'bottom', fill = 'x')
        self.createSep(self.f_secondOps).pack(fill = 'x', side = 'bottom')

        for c in range(int(self.width / 2)):
            for r in range(self.height):
                
                current = inpt[self.count]
                Label(self.f_baseOps, bg = bkgd, text = current[0], font = btn_font).grid(row = r, column = 2 * c, sticky = 'we')
                self.createInpt(self.f_baseOps, self.base_inpt, current).grid(row = r, column = 2 * c + 1, sticky = 'w')
                self.count += 1

        self.count = 0

    def createBottom(self, inpt):
        for box in inpt:
            if self.count != 0:
                self.createSep(self.f_secondOps).pack(fill = 'y', side = 'left')
                
            self.count += 1
            
            tempframe = Frame(self.f_secondOps, bg = bkgd)
            self.l_title = Label(tempframe, bg = bkgd1, text = box[0], font = btn_font)
            self.boxes.append(tempframe)

            tempframe.pack(side = 'left', fill = 'both', expand = True)
            self.l_title.grid(row = 0, column = 0, columnspan = 2, sticky = 'we')
            
            for i in range(len(box[1])):
                tempframe.rowconfigure(i + 1, weight = 1)
                tempframe.columnconfigure(0, weight = 1)
                tempframe.columnconfigure(1, weight = 1)
                
                row = box[1][i]
                Label(tempframe, bg = bkgd, text = row[0], font = btn_font).grid(row = i + 1, column = 0, sticky = 'we')
                self.createInpt(tempframe, self.second_inpt, row).grid(row = i + 1, column = 1, sticky = 'w')
        

class LoadMenu(Menu):

    def __init__(self, name, win, saves, parent):
        Menu.__init__(self, win, name, parent)
        self.var = ()
        self.index = 0
        self.saves = saves

        self.f_mid = Frame(self.f_base, bg = bkgd)
        self.f_buttons = Frame(self.f_base, bg = 'black')
        self.b_begin = Button(self.f_buttons, width = 30, text = 'Begin!', font = btn_font, bg = bkgd1, activebackground = bkgd1, relief = 'flat', command = lambda: self.getData(self.index))
        self.b_delete = Button(self.f_buttons, width = 30, text = 'Delete selected', font = btn_font, bg = bkgd1, activebackground = bkgd1, relief = 'flat', command = lambda: self.deleteSave(self.index))

        self.f_buttons.pack(side = 'bottom', fill = 'x')
        self.b_begin.pack(side = 'left', expand = True, fill = 'x')
        self.createSep(self.f_buttons).pack(fill = 'y', side = 'left')
        self.b_delete.pack(side = 'left', expand = True, fill = 'x')
        self.createSep(self.f_base).pack(fill = 'x', side = 'bottom')
        self.f_mid.pack(side = 'bottom', fill = 'both', expand = True, padx = 10, pady = 10)        

    def create(self):
        self.f_reading = Frame(self.f_mid, bg = bkgd)
        self.t_info = Text(self.f_mid)
        self.sb_list = Scrollbar(self.f_reading, orient = 'vertical')
        self.lb_saves = Listbox(self.f_reading, yscrollcommand = self.sb_list.set, font = btn_font, selectmode = 'single')
        self.sb_list.config(command = self.lb_saves.yview)

        self.f_reading.place(anchor = 'nw', relwidth = 0.5, relheight = 1)
        self.t_info.place(anchor = 'nw', relwidth = 0.5, relheight = 1, relx = 0.5)
        self.lb_saves.pack(side = 'left', fill = 'both', expand = True)
        self.sb_list.pack(side = 'left', fill = 'both', padx = 10)

        if len(self.saves) > 0:
            self.msg = 'No simulation selected.'
            for item in self.saves:
                self.lb_saves.insert(END, item[1])

        else:
            self.msg = 'No simulations saved.'

    def updateDesc(self):
        try:
            self.var = self.lb_saves.curselection()[0]
            self.index = self.saves[self.var][0]
            self.desc = self.saves[self.var][2]

        except:
            self.desc = self.msg
            
        self.t_info.delete(1.0, 'end')
        self.t_info.insert('end', self.desc)
        self.t_info.after(8, self.updateDesc)

    def getData(self, index):
        self.sim_type = self.saves[self.var][3]
        self.savesDB = saves.Database()
        self.data = self.savesDB.load_specific(self.sim_type, str(index))       
        self.savesDB.finish()

        if self.sim_type == 'a':
            self.datatop = [self.data[0][0][2], self.data[1][0][5], self.data[1][0][4], self.data[1][0][6], self.data[0][0][3], 0, 0, 0]
            self.databottom = ['', '', self.data[0][0][4], '', '', '', self.data[0][0][5], '']

        elif self.sim_type == 'c':
            self.datatop = [self.data[0][0][2], self.data[0][0][3], self.data[0][0][4], self.data[0][0][5],
                            self.data[0][0][6], self.data[0][0][7], self.data[0][0][8], self.data[0][0][9],
                            self.data[0][0][10]]

            self.databottom = []
            for i in range(len(self.data[1])):
                self.databottom = self.databottom + [self.data[1][i][4], self.data[1][i][7],
                                                     self.data[1][i][9], self.data[1][i][6]]

            self.databottom = self.databottom + ['', '', '', ''] * (4 - len(self.data[1]))


        self.parent.begin(self, self.sim_type, self.datatop, self.databottom)

    def deleteSave(self, index):
        self.savesDB = saves.Database()
        self.savesDB.remove(str(index))

        
class SaveMenu(Menu):

    def __init__(self, name, win, parent):
        Menu.__init__(self, win, name, parent)
        self.title = StringVar()

    def create(self):
        self.f_outline = Frame(self.f_base, bg = 'black')
        self.f_centre = Frame(self.f_outline, bg = '#b9bbdf')
        self.l_title = Label(self.f_centre, bg = '#b9bbdf', relief = 'flat', text = 'Title', font = btn_font)
        self.l_description = Label(self.f_centre, bg = '#b9bbdf', relief = 'flat', text = 'Description', font = btn_font)
        self.e_title = Entry(self.f_centre, textvariable = self.title)
        self.f_text = Frame(self.f_centre, bg = '#b9bbdf')
        self.t_description = Text(self.f_text)
        self.b_save = Button(self.f_outline, text = 'Save', font = btn_font, bg = bkgd1, activebackground = bkgd1, relief = 'flat', command = lambda: self.parent.finalSave(self.title, self.t_description))

        self.gridConfig(self.f_centre, 5, 3)

        self.f_outline.place(anchor = 'c', relwidth = 0.5, relheight = 0.8, relx = 0.5, rely = 0.5)
        self.f_centre.pack(fill = 'both', expand = True, padx = 2, pady = 2)
        self.l_title.grid(row = 0, column = 0, sticky = 'we')
        self.e_title.grid(row = 0, column = 1, columnspan = 2, sticky = 'we', padx = 20, pady = 20)
        self.l_description.grid(row = 1, column = 0, sticky = 'we')
        self.f_text.grid(row = 1, column = 1, columnspan = 2, rowspan = 4, sticky = 'nswe', padx = 20)
        self.f_text.pack_propagate(0)
        self.t_description.pack(fill = 'both', expand = True, pady = 20)
        self.createSep(self.f_outline).pack(fill = 'x', side = 'bottom')
        self.b_save.pack(side = 'bottom', fill = 'x', padx = 2)


class SimulationScreen(Menu):

    def __init__(self, name, win, parent, sim_type):
        Menu.__init__(self, win, name, parent)
        
        self.cn_main = Canvas(self.f_base, bg = bkgd, borderwidth = 0)
        self.b_pause = Button(self.f_header, text = 'Pause', font = btn_font, bg = bkgd1, width = 8, activebackground = bkgd1, relief = 'flat', command = lambda: self.parent.pause())
        self.b_save = Button(self.f_header, text = 'Save', font  = btn_font, bg = bkgd1, width = 8, activebackground = bkgd1, relief = 'flat', command = lambda: self.parent.save())
        self.l_time = Label(self.f_header, text = 'Time:  0s', font = btn_font, bg = bkgd1, relief = 'flat', width = 10)

        self.b_pause.pack(side = 'left')
        self.createSep(self.f_header).pack(side = 'left', fill = 'y')
        if sim_type != 'p':
            self.b_save.pack(side = 'left')
            self.createSep(self.f_header).pack(side = 'left', fill = 'y')
        self.l_time.pack(side = 'right')
        self.createSep(self.f_header).pack(side = 'right', fill = 'y')

        self.ballNames = ['A', 'B', 'C', 'D']
        self.dimensions = ['X', 'Y']
        self.itemBoxes = []
        self.sim_type = sim_type
        self.count = 0

    def drawInputs(self, inpt):
        self.data = []
        self.f_objInfo = Frame(self.f_base, bg = bkgd, width = 100)
        self.f_values = Frame(self.f_objInfo, bg = bkgd)
        self.f_wallInput = Frame(self.f_objInfo, bg = bkgd)
        self.f_arrowInput = Frame(self.f_objInfo, bg = bkgd)
        self.b_update = Button(self.f_objInfo, text = 'Update', font = btn_font, bg = bkgd1, activebackground = bkgd1, relief = 'flat', command = lambda: self.parent.update_cn(self.data))
        self.b_create = Button(self.f_objInfo, text = 'Create', font = btn_font, bg = bkgd1, activebackground = bkgd1, relief = 'flat', command = lambda: self.parent.new_arrow(self.cn_main, self.data))

        self.gridConfig(self.f_wallInput, 2, 2)
        self.gridConfig(self.f_arrowInput, 6, 2)
        self.gridConfig(self.f_values, 2, 1)

        self.inpt = [[self.f_wallInput] + inpt[0], [self.f_arrowInput] + inpt[1]]

        self.f_objInfo.pack(side = 'left', fill = 'y')
        self.createSep(self.f_objInfo).pack(side = 'right', fill = 'y')
        self.cn_main.pack(side = 'right', fill = 'both', expand = True)
        self.f_values.pack(side = 'top', fill = 'both', expand = True)
        self.createSep(self.f_objInfo).pack(side = 'top', fill = 'x')
        self.f_wallInput.pack(side = 'top', fill = 'both', expand = True)
        self.b_update.pack(side = 'top', fill = 'x')
        self.createSep(self.f_objInfo).pack(side = 'top', fill = 'x')
        self.f_arrowInput.pack(side = 'top', fill = 'both', expand = True)
        self.b_create.pack(side = 'top', fill = 'x')

        for box in self.inpt:
            for i in range (len(box) - 1):
                Label(box[0], bg = bkgd, relief = 'flat', text = box[i + 1][0], font = btn_font).grid(row = i, column = 0, sticky = 'we')
                self.createInpt(box[0], self.data, box[i + 1]).grid(row = i, column = 1, sticky = 'we', padx = 3)

        
    def infoBox(self, sim_objects):

        if self.sim_type != 'p':
            self.f_objInfo = Frame(self.f_base, bg = bkgd, height = 100)
            self.f_objInfo.pack(side = 'bottom', fill = 'x')
            self.cn_main.pack(side = 'top', fill = 'both', expand = True)
            
            for i in range(len(sim_objects)):
                if self.count != 0:
                    self.createSep(self.f_objInfo).pack(side = 'left', fill = 'y')

                self.tempframe = Frame(self.f_objInfo, bg = bkgd)
                self.createSep(self.tempframe).pack(side = 'top', fill = 'x')

                if self.sim_type == 'c':
                    self.l_title = Label(self.tempframe, bg = sim_objects[i].colour, relief = 'flat', text = self.ballNames[i], font = btn_font)
                    self.l_kinetic = Label(self.tempframe, bg = bkgd, relief = 'flat', text = 'null', font  = btn_font, width = 10)

                if self.sim_type == 'a':
                    self.l_title = Label(self.tempframe, bg = bkgd1, relief = 'flat', text = self.dimensions[i], font = btn_font)
                    self.l_pos = Label(self.tempframe, bg = bkgd, relief = 'flat', text = 'null', font = btn_font, width = 10)

                self.l_vel = Label(self.tempframe, bg = bkgd, relief = 'flat', text = 'null', font = btn_font, width = 10)
                
                self.tempframe.pack(side = 'left', fill = 'both', expand = True)
                self.l_title.pack(side = 'top', fill = 'x')
                self.l_vel.pack(side = 'top', fill = 'x')
                
                try:
                    self.l_kinetic.pack(side = 'top', fill = 'x')
                    self.itemBoxes.append([self.tempframe, self.l_vel, self.l_kinetic]) 
                except:
                    self.l_pos.pack(side = 'top', fill = 'x')
                    self.itemBoxes.append([self.tempframe, self.l_vel, self.l_pos])
                        
                self.count += 1

        else:
            self.l_kinetic = Label(self.f_values, bg = bkgd, relief = 'flat', text = 'No arrow', font = btn_font)
            self.l_potential = Label(self.f_values, bg = bkgd, relief = 'flat', text = 'No arrow', font = btn_font)

            self.l_kinetic.grid(row = 0, column = 0, sticky = 'we')
            self.l_potential.grid(row = 1, column = 0, sticky = 'we')

            return [self.l_kinetic, self.l_potential]


class ErrorScreen():

    def __init__(self, message, poptype = 'norm', parent = 'null'):
        self.err_window = Tk()
        self.err_window.title('Error Message')
        self.err_window.geometry('480x270')
        self.poptype = poptype
        self.parent = parent
        
        self.text = Label(self.err_window, bg = bkgd, relief = 'flat', text = message, font = btn_font)
        self.exit = Button(self.err_window, bg = bkgd1, activebackground = bkgd1, relief = 'flat', text = 'Okay', font = btn_font, command = lambda: self.discard(False))

        if poptype == 'e':
            self.exit = Button(self.err_window, bg = bkgd1, activebackground = bkgd1, relief = 'flat', text = 'Yes', font = btn_font, command = lambda: self.discard(True))
            self.decline = Button(self.err_window, bg = bkgd1, activebackground = bkgd1, relief = 'flat', text = 'No', font = btn_font, command = lambda: self.discard(False))
            self.decline.pack(side = 'bottom', fill = 'x')
            Frame(self.err_window, bg = 'black', height = 2, width = 2).pack(side = 'bottom', fill = 'x')

        self.exit.pack(side = 'bottom', fill = 'x')
        Frame(self.err_window, bg = 'black', height = 2, width = 2).pack(side = 'bottom', fill = 'x')
        self.text.pack(fill = 'both', expand = True)

    def discard(self, ex):
        if ex == True:
            self.parent.window.destroy()
        self.err_window.destroy()











    
        
