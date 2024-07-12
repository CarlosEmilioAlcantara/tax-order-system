from tkinter import *

class TaxOrderSystem(Tk):
    def __init__(self):
        super().__init__()
        self.state = self.winfo_viewable()

        # Initialize the window
        self.geometry("900x600")
        self.configure(background="#D5E0ED")
        # Remove titlebar
        self.overrideredirect(True)

        # Titlebar
        self.titleBar = Frame(self, bg="#3B6ED6")
        self.titleBar.grid(row=0, column=0, sticky="nsew") # Stick to all directions
        self.grid_columnconfigure(0, weight=1) # Fill all columns at top

        # Window movement
        self.titleBar.bind("<ButtonPress-1>", self.startMove)
        self.titleBar.bind("<ButtonRelease-1>", self.stopMove)
        self.titleBar.bind("<B1-Motion>", self.doMove)

        # Window icon
        self.titleIcon = PhotoImage(file='./icons/header-icon.png')        
        self.resizeTitleIcon = self.titleIcon.subsample(2, 2)

        self.titleIcon = Label(
            self.titleBar,
            image=self.resizeTitleIcon, 
            bg="#3B6ED6", 
            fg="#FCFCFC", 
            font="Helvetica")
        self.titleIcon.pack(side=LEFT, padx=6, pady=6)

        # Window title
        self.titleLabel = Label(
            self.titleBar, 
            text="San Pablo City Government - Tax Order System", 
            bg="#3B6ED6", 
            fg="#FCFCFC", 
            font="Helvetica")
        self.titleLabel.pack(side=LEFT, padx=6, pady=6)

        # Window buttons
        # Exit button
        self.exitIcon = PhotoImage(file='./icons/exit.png')
        self.resizeExitIcon = self.exitIcon.subsample(2, 2)

        self.exitBtn = Button(
            self.titleBar, 
            image=self.resizeExitIcon, 
            relief=FLAT,
            bg="#9D4250",
            bd=4,
            cursor="hand2",
            activebackground="#7B2F3B")
        self.exitBtn.pack(side=RIGHT, padx=6, pady=(0, 18))
        self.exitBtn.bind("<Button-1>", self.exitApp)        

        # Minimize button
        self.minimizeIcon = PhotoImage(file='./icons/minimize.png')
        self.resizeMinimizeIcon = self.minimizeIcon.subsample(2, 2)

        self.minimizeBtn = Button(
            self.titleBar, 
            image=self.resizeMinimizeIcon, 
            relief=FLAT,
            bg="#9D4250",
            bd=4,
            cursor="hand2",
            activebackground="#7B2F3B")
        self.minimizeBtn.pack(side=RIGHT, padx=6, pady=(0, 18))
        self.minimizeBtn.bind("<Button-1>", self.minimize)

        # self.exitLabel = Label(
        #     self.titleBar, 
        #     text="X",
        #     bg="#3B6ED6",
        #     fg="#FCFCFC",            
        #     font="Helvetica 12 bold",
        #     cursor="hand2")
        # self.exitLabel.pack(side=RIGHT, padx=6, pady=(0, 6))
        # self.exitLabel.bind("<Button-1>", self.exitApp)

        self.removeTitle(self.state)

    # Window movement functions
    def startMove(self, event):
        self.x = event.x
        self.y = event.y

    def stopMove(self, event):
        self.x = None
        self.y = None

    def doMove(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    # def keepFlat(self, event):       # on click,
    #     if event.widget is self.exitBtn: # if the click came from the button
    #         event.widget.config(relief=FLAT) # enforce an option  

    def minimize(self, event):
        self.update_idletasks()
        self.overrideredirect(False)
        #self.state('withdrawn')
        self.state('iconic')

    def exitApp(self, event):
        self.quit()
        self.destroy()

    def removeTitle(self, state):
        if state == "viewable":
            state.overrideredirect(True)


# Create app object
app = TaxOrderSystem()

if __name__ == "__main__":
    # Loop to listen for events
    app.mainloop()