import webbrowser
from tkinter import *
from tkinter import ttk, font, messagebox
import LinjaBoardGame

class GUI:

    def __init__(self):
        self.root = Tk()
        self.confTk()
        self.loadDates()
        self.root.mainloop()

    def confTk(self):
        self.root.title('Linja - Computational Intelligence')
        self.root.option_add("*tearOff", False)
        self.root.geometry("400x200")
        self.root.resizable(width=False, height=False)

    def loadDates(self):

        self.navBar = Menu(self.root)
        self.root['menu'] = self.navBar
        self.menuOne = Menu(self.navBar)
        self.navBar.add_cascade(menu=self.menuOne, label='Information')
        self.menuOne.add_command(
            label="WebPage", compound=LEFT, command=self.information)
        self.menuOne.add_separator()
        self.menuOne.add_command(label="Salir", command=self.root.quit)

        fontStyle = font.Font(family="Lucida Grande", size=14)
        self.etkWel = ttk.Label(
            self.root, text="Welcome to Linja", font=fontStyle)
        self.sep = ttk.Separator()
        self.etkSel = ttk.Label(self.root, text="Select Game Mode")

        values = ['1-Human', '2-Machine']
        self.cmbOne = ttk.Combobox(self.root, state="readonlye", values=values)
        self.cmbTwo = ttk.Combobox(self.root, state="readonlye", values=values)

        self.cmbOne.current(0)
        self.cmbTwo.current(0)

        self.btnPlay = ttk.Button(
            self.root, text="PLAY", command=self.playGame)

        self.frameOne = Frame(self.root)

        self.imag = PhotoImage(file="images/menu.png")
        self.etkImg = ttk.Label(self.frameOne, image=self.imag)

        self.locationElements()

    def playGame(self):
        playerOne = True if self.cmbOne.get().split('-')[0] == '1' else False
        playerTwo = True if self.cmbTwo.get().split('-')[0] == '1' else False
        LinjaBoardGame.mainGame(playerOne, playerTwo)

    def information(self):
        webbrowser.open("www.google.com")

    def locationElements(self):
        self.frameOne.place(x=198, y=0, width=200, height=198)
        self.etkWel.place(x=20, y=5)
        self.sep.place(x=20, y=40, width=160)
        self.etkSel.place(x=46, y=50)
        self.cmbOne.place(x=20, y=80, width=160)
        self.cmbTwo.place(x=20, y=120, width=160)
        self.etkImg.pack(side=TOP, fill=BOTH, expand=True)
        self.btnPlay.place(x=50, y=150, width=100, height=30)
