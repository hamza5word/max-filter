from tkinter import *
from PIL import ImageTk, Image
from csv import *
import tkinter.messagebox as gui
MAX_ADD_THEMES = 3
THEME = {}
THEME['BLACKMAROON'] = {'TITLE':'BM',
                     'Foregrounds':['white', 'maroon1'],
                     'Backgrounds':['gray25', 'gray24','gray11', 'gray8', 'gray20', 'gray18'],
                     'Active':['orchid1']
                    }
THEME['WHITEMAROON'] = {'TITLE':'WM',
                     'Foregrounds':['black', 'maroon1'],
                     'Backgrounds':['gray91', 'gray90', 'gray76', 'gray50', 'gray84', 'gray77'],
                     'Active':['orchid1']
                    }
THEME['DARKMATERIAL'] = {'TITLE':'DM',
                     'Foregrounds':['white', 'white'],
                     'Backgrounds':['gray19', 'gray18', 'gray10', 'black', 'gray8', 'gray6'],
                     'Active':['gray25']
                    }
THEME['WHITEMATE'] = {'TITLE':'WMT',
                     'Foregrounds':['cornflower blue', 'black'],
                     'Backgrounds':['white', 'gray98', 'gray90', 'gray85', 'snow', 'white'],
                     'Active':['cyan']
                    }
THEME['BLUEWATER'] = {'TITLE':'DKO',
                      'Foregrounds' : ['light cyan','cyan'],
                      'Backgrounds' : ['steel blue', 'medium blue', 'blue4','navy','blue', 'blue3'],
                      'Active':['white']
                        }
THEME['FAIRYTAIL'] = {'TITLE':'FTL',
                        'Foregrounds' : ['brown4','coral4'],
                        'Backgrounds' : ['sienna4', 'tan2', 'LightPink','gray69','salmon', 'DarkSeaGreen'],
                       'Active':['dim gray']
                        }

## Configuration
try:
    with open('data/theme.hmz', 'r') as f:
        val = f.readline()
        chosed = ''
        for c in val:
            if c != '\n':
                chosed += c
        CT = THEME[chosed]
except:
    CT = THEME['BLACKMAROON']

F = CT['Foregrounds']
B = CT['Backgrounds']
A = CT['Active']

class Root(Tk):
    """
        CLASS FOR SETING UP A PERSONAL WINDOW
    """
    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title(screenName)
        self.configure(bg=B[0])
        self.center()
        #self.bind('<Escape>', lambda event : event.widget.quit())

    def center(self, width=300, height=200):
        x = (self.winfo_screenwidth() / 2) - (width / 2)
        y = (self.winfo_screenheight() / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

class BLbutton(Button):
    def __init__(self, master=None, text=""):
        super().__init__(master)
        self.configure(text=text, font='calibri', padx=20, bd=0, bg=B[1], fg=F[0], activebackground=A[0]
                       , cursor='hand2')
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        self.configure(bg=B[4], fg=F[1])

    def on_leave(self, event):
        self.configure(bg=B[1], fg=F[0])

class BLbuttons(Frame):
    def __init__(self, master=None, *buttons):
        super().__init__(master)
        self.buttons = []
        self.configure(bg=B[3])
        for button in buttons:
            b = BLbutton(self, button)
            self.buttons.append(b)
            b.pack(side=LEFT, padx=10, pady=20)
        self.exbutton = BLbutton(self, 'Exit')
        self.exbutton.configure(command=master.destroy)
        self.exbutton.pack(side=RIGHT, padx=10, pady=20)

class BLFormula(Frame):
    def __init__(self, master=None,*inputs):
        super().__init__(master)
        self['bg'] = master['bg']
        self.labels = []
        self.entries = []
        self.title = Label(self, text='TRAINING INFO', font=('calibri',22), justify=CENTER, fg=F[1], bg=master['bg'],
                            padx=10, pady=40, width=22)
        self.butframe = Frame(self, bg=self['bg'])
        self.submit = BLbutton(self.butframe, 'Submit')
        self.exitBut = BLbutton(self.butframe, 'Exit')
        self.exitBut.configure(command=master.destroy)
        self.title.pack()
        self.submit.pack(side=LEFT, padx=1)
        self.exitBut.pack(side=LEFT, padx=1)
        self.butframe.pack(side=BOTTOM, pady=30)
        if len(inputs) <= 6 :
            for i in inputs :
                f = Frame(self, bg=master['bg'])
                l = Label(f, text=i, font='calibri', justify=LEFT, fg=F[0], bg=master['bg'], padx=10, pady=10, width=15)
                self.labels.append(l)
                e = Entry(f, width= 30, justify=CENTER, font=('calibri', 15))
                self.entries.append(e)
                l.grid(row=0)
                e.grid(row=0, column=1)
                f.pack(padx=12, pady=10)
        else:
            gui.showinfo('Warning', 'This Panel Holds at most 6 inputs <!>')

class BLMenu(Menu):
    def __init__(self, master=None, inp=True, *submenus):
        super().__init__(master)
        self.submenus = []
        self.configure(background=B[3])
        for submenu in submenus:
            menu = Menu(self, tearoff=0, activebackground=A[0], bd=0)
            self.add_cascade(label=submenu, menu=menu)
            self.submenus.append(menu)
            while(inp):
                v = input('Command for '+ str(submenu)+ ' : ')
                if v == 'quit' : break
                else:
                    menu.add_command(label=v)

class Sheet(Frame):
    def __init__(self, master=None,list=None, width=10, prkey = "", save_file_name='list.csv'):
        super().__init__(master)
        ### ATTRIBUTES
        self.width = width
        self.prkey = prkey
        self.currentindex = None
        self.currentkey = None
        self.clicktype = ''
        self.svlist = list
        self.configure(bg=master['bg'])
        self.list = self.addTolistFrame(list, self.width)
        self.listkeys = self.liskeys()
        self.confButt()


    def set(self, index1, index2, key, value):
        self.list[0][key].delete('0', 'end')
        self.list[0][key].insert(index2, value)

    def addemptyrow(self):
        self.update_idletasks()
        j = 0
        gdict = {}
        for k, v in self.list[0].items():
            entry = Entry(self, bd=0, width=self.width, justify=CENTER, font=('calibri', 15))
            gdict[k] = entry
            entry.grid(row=len(self.list)+2, column=j, padx=1, pady=1)
            j += 1
        self.list.append(gdict)
        self.confButt()
        print(len(self.list))

    def addrow(self, **addons):
        self.update_idletasks()
        j = 0
        gdict = {}
        for k, v in addons.items():
            entry = Entry(self, bd=0, width=self.width, justify=CENTER, font=('calibri', 15))
            entry.insert(j, str(v))
            if k == self.prkey :
                entry.configure(state=DISABLED)
            gdict[k] = entry
            entry.grid(row=len(self.list) + 2, column=j, padx=1, pady=1)
            j += 1
        self.list.append(gdict)
        self.confButt()
        print(len(self.list))

    def save(self):
        global save_file_name
        nlist = []
        for i in range(1, len(self.list)) :
            d = dict()
            for k, v in self.list[i].items():
                d[k] = v.get()
            nlist.append(d)
        with open(save_file_name, 'w', newline='') as csvfile:
          w = DictWriter(csvfile, fieldnames=self.liskeys())
          w.writeheader()
          for row in nlist:
              w.writerow(row)
        self.svlist = nlist


    def liskeys(self):
        listkeys = []
        for el in self.list:
            for k in el.keys():
                listkeys.append(k)

            break
        return listkeys

    def removerow(self):
        for v in self.list[self.currentindex].values():
            v.destroy()

        self.svlist.remove(self.svlist[self.currentindex-1])
        self.list.remove(self.list[self.currentindex])
        self.confButt()
        print(len(self.list))


    def addTolistFrame(self, list, width=10):
        """FIRST KEY ROW"""
        if list == None :
            return
        j = 0
        glist = []
        if isinstance(list[0], dict):
            keys = {}
            for k in list[0].keys():
                entry = Entry(self, bd=0, width=width, justify=CENTER, font=('calibri', 15), bg=F[1], fg=F[0])
                entry.insert(j, str(k))
                keys[k] = entry
                entry.grid(row=0, column=j, padx=1, pady=1)
                j += 1
            glist.append(keys)
        for i in range(0, len(list)):
            j = 0
            gdict = {}
            for k, v in list[i].items():
                entry = Entry(self, bd=0, width=width, justify=CENTER, font=('calibri', 15))
                entry.insert(j, str(v))
                if k == self.prkey : entry.configure(state=DISABLED)
                gdict[k] = entry
                entry.grid(row=i + 1, column=j, padx=1, pady=1)
                j += 1
            glist.append(gdict)
        return glist

    def confButt(self):
        for i in range(1, len(self.list)):
            for k, v in self.list[i].items():
                v.unbind('<Button-1>')
                v.bind('<Button-1>', self.helper(i,k))
                v.bind('<Double-Button-1>', self.helper2(i,k))
                v.bind('<Button-3>', self.helper3(i,k))


    def helper(self, arg1, arg2):
        return lambda event : self.retclicked(event, arg1, arg2)
    def helper2(self, arg1, arg2):
        return lambda event: self.dbclicked(event, arg1, arg2)
    def helper3(self, arg1, arg2):
        return lambda event: self.lfclicked(event, arg1, arg2)
    def retclicked(self, event, index, key):
        self.currentindex = index
        self.currentkey = key
        self.clicktype = 'CLICK'
        print('clicked index = ', index)
        print('clicked key = ', key)

    def dbclicked(self, event, index, key):
        self.currentindex = index
        self.currentkey = key
        self.clicktype = 'DB_CLICK'
        window = Root()
        window.resizable(False, False)
        window.center(600, 400)

        BLInfoBox(window, **self.svlist[self.currentindex-1]).pack()
        print('double clicked index = ', index)
        print('doucle clicked key = ', key)

        window.mainloop()

    def lfclicked(self, event, index, key):
        self.currentindex = index
        self.currentkey = key
        self.clicktype = 'R_CLICK'
        self.removerow()
        print('double clicked index = ', index)
        print('doucle clicked key = ', key)
        self.update_idletasks()

class DLS(Frame):
    def __init__(self, master=None, list=None, primaryKey=None, column_width=10, maxRows=100, padding=100, save_file_name='list.csv'):
        """
                                    DLS ---> DICTIONARY LIST SHOW <---
            THIS CLASS IS CAPABLE TO SHOW A LIST OF INFORMATION STOCKED AS DICTIONARIES
        """
        super().__init__(master)
        ### SCROLLBAR INITIALISATION
        vsb = Scrollbar(master, orient=VERTICAL)
        vsb.pack(side=RIGHT, fill=Y)
        hsb = Scrollbar(master, orient=HORIZONTAL)
        hsb.pack(side=BOTTOM, fill=X)
        self.c = Canvas(master, yscrollcommand=vsb.set, xscrollcommand=hsb.set, height=500)
        self.c.pack(fill=BOTH, expand=True, padx=padding, pady=15)
        vsb.config(command=self.c.yview)
        hsb.config(command=self.c.xview)
        ### CREATING SHEET FOR THE CLASS LIST SHOW
        self.sheet = Sheet(self.c, list, column_width, primaryKey, save_file_name=save_file_name)
        for i in range(len(self.sheet.list), maxRows) : self.sheet.addemptyrow()
        self.c.create_window(0, 0, anchor=NW, window=self.sheet)
        self.sheet.update_idletasks()
        self.c.config(scrollregion=self.c.bbox("all"))
        ### TOOLBAR FOR EDITING LIST ITEM
        self.toolbar = Frame(master, bg='gray18')
        self.savButt = BLbutton(self.toolbar, 'SAVE SHEET')
        self.savButt.configure(command=self.sheet.save)
        self.extButt = BLbutton(self.toolbar, 'EXIT SHEET')
        def goexit(event):
           master.destroy()
        self.extButt.bind('<Button-1>', goexit)
        self.extButt.pack(side=RIGHT, padx=8)
        self.savButt.pack(side=RIGHT, padx=8)
        self.toolbar.pack(side=BOTTOM, padx=12, pady=12)

class BLSearch(Frame):
    def __init__(self, master=None, text='ENTER TEST : '):
        super().__init__(master)
        if ' : ' not in text : text += ' : '
        self.configure(bg=master['bg'])
        self.label = Label(self, text=text, bg=master['bg'], fg=F[0], font=('calibri', 38))
        self.entry = Entry(self, bd=0, justify=CENTER, font=('calibri', 18), width=10)
        self.submit = BLbutton(self, 'SUBMIT')
        self.label.pack(side=LEFT, pady=10, fill=X, padx=80)
        self.entry.pack(side=LEFT, pady=12)
        self.submit.pack(side=LEFT)

class BLInfoBox(Frame):
    def __init__(self, master=None, **infos):
        super().__init__(master)
        self.infos = infos
        self.labels = []
        self.configure(bg=B[5])
        self.title = Label(self, text='INFORAMTION PANEL', bg=self['bg'], fg=F[1], font=('Calibri', 30))
        self.title.pack(side=TOP, pady=14)
        for k, v in infos.items():
            l = Label(self, text=str(k)+' : '+str(v), bg=self['bg'], fg=F[0], font=('Calibri', 15))
            l.pack(pady=14)
            self.labels.append(l)

class BLToolbar(Frame):
    def __init__(self, master=None, *bars):
        super().__init__(master)
        self.configure(bg=B[5])
        self.bars = []
        for b in bars:
            button = BLbutton(self, b)
            button.configure(width=10)
            button.pack(pady=20, padx=8)
            self.bars.append(button)

class BLImagedTitle(Frame):
    def __init__(self, master=None, image=None, text='text', background=B[4], foreground=F[1], fontweight=20):
        super().__init__(master)
        self.configure(bg=background)
        self.imglabel = Label(self, image=image, bg=self['bg'])
        self.txtlabel = Label(self, bg=self['bg'], fg=foreground, font=('Calibri', fontweight), text=text)
        self.imglabel.pack(side=LEFT, padx=3)
        self.txtlabel.pack(side=LEFT, padx=3)

class BLProfile(Frame):
    def __init__(self, master, image, name, *infos):
        super().__init__(master)
        self.configure(bg=B[4])
        self.pic_label = Label(master, image=image, bg=B[4], fg=F[1])
        self.profile = Frame(master, bg=B[4])
        self.name = Label(self.profile, text=name, font=('Arial', 45), bg=B[4], fg=F[1])
        self.name.grid(row=0, column=1, sticky=W)
        v = 1
        for i in infos:
            li = Label(self.profile, text=i, bg=B[4], fg=F[0])
            li.grid(row=v, column=1, sticky=W)
            v += 1
        exit = BLbutton(self.profile, 'EXIT')
        exit.configure(command=master.destroy)
        exit.grid(row=v+1, column=1, sticky=W)
        self.profile.pack(side=LEFT, padx=30)
        self.pic_label.pack(side=RIGHT)

class BLTippGiver(Frame):
    def __init__(self, master=None, title='TIPPS GIVER', desc='TIPPS Always reserve better use', image=None):
        super().__init__(master)
        self.configure(bg=B[4])
        self.title = Label(self, bg=self['bg'], fg=F[1], font=('Calibri', 30), justify=LEFT, text=title)
        self.desc = Label(self, bg=self['bg'], fg=F[0], font=('Calibri', 11), justify=LEFT, text=desc)
        self.img = Label(self, bg=self['bg'], image=image)
        self.title.pack(pady=12)
        self.desc.pack(anchor=W, padx=5)
        self.img.pack(pady=10)

def center(window, width, height):
    x = (window.winfo_screenwidth()/2) - (width/2)
    y = (window.winfo_screenheight()/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

def makepages(*elements):
    for element in elements:
        element.grid(row=0, column=0, sticky='news')

def raise_frame(frame):
    frame.tkraise()

def enter_leave_effect(frame, enter_color, leave_color, background=True):
    if background:
        def on_enter(event):
            frame.configure(bg=enter_color)
        def on_leave(event):
            frame.configure(bg=leave_color)
        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)
    else:
        def on_enter(event):
            frame.configure(fg=enter_color)
        def on_leave(event):
            frame.configure(fg=leave_color)
        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)

def enter_leave_data(frame, text_to_show, frame_in, orig=''):
    def on_enter(event):
        frame_in.configure(text=text_to_show)
    def on_leave(event):
        frame_in.configure(text=orig)
    frame.bind('<Enter>', on_enter)
    frame.bind('<Leave>', on_leave)

def escape_exit(frame):
    def exit(event):
        frame.destroy()
    frame.bind('<Escape>', exit)

def focus_set(frame):
    frame.lift()
    frame.focus_force()
    frame.grab_set()
    frame.grab_release()

### TEST CLASS
class Student:
    counter = 0
    def __init__(self, cne='', name='', departement='', grade=0.0):
        Student.counter +=1
        self._id = Student.counter
        self.cne = cne
        self.name = name
        self.departement = departement
        self.grade = grade

    @staticmethod
    def getcounter():
        return Student.counter

    def getid(self):
        return self._id

    id = property(getid)

    def getinfos(self):
        d = dict()
        d['ID'] = self.id
        d['CNE'] = self.cne
        d['Name'] = self.name
        d['Depart'] = self.departement
        d['Grade'] = self.grade
        return d

    def __str__(self):
        return str(self.getinfos())

    def __repr__(self):
        return self.__str__()
class StudentsManager():
    def __init__(self, students= []):
        self.students = students

    def addStudent(self, student):
        self.students.append(student.getinfos())

    def remStudent(self, student):
        self.students.remove(student.getinfos())

    def getbyid(self, id):
        for student in self.students:
            if str(student['ID']) == str(id) : return student
class Buttons(Frame):
    def __init__(self, master=None, *buttons):
        super().__init__(master)
        self.buttons = []
        self.configure(bg='gray8')
        for button in buttons:
            b = Button(self, text=button, font='calibri', padx=20, bd=0, bg='gray11', fg='white')
            b.bind('<Enter>', self.helper(b))
            b.bind('<Leave>', self.helper2(b))
            self.buttons.append(b)
            b.pack(side=LEFT, padx=10, pady=20)
        self.exbutton = Button(self, text='Exit', font='calibri', padx=40, bd=0, bg='gray11', fg='white',
                               command=self.quit)
        self.exbutton.pack(side=RIGHT, padx=10, pady=20)
        self.exbutton.bind('<Enter>', self.helper(self.exbutton))
        self.exbutton.bind('<Leave>', self.helper2(self.exbutton))

    def helper(self, button):
        return lambda event : self.on_enter(event, button)

    def helper2(self, button):
        return lambda event : self.on_leave(event, button)

    def on_enter(self, event, button):
        button.configure(fg='gold', bg='gray24')

    def on_leave(self, event, button):
        button.configure(fg='white', bg='gray11')

