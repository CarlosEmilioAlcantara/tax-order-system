import tkinter as tk

# Colors
BLACK = "#333333"
WHITE = "#FCFCFC"
GREEN = "#008F67"
DARKGREEN = "#007856"
GREY = "#585858"
RED = "#CC241D"
DARKRED = "#B8201A"
YELLOW = "#D79921"
DARKYELLOW = "#C28A1D"
BLUE = "#1C8BFF"

# Titlebar
## Symbols
## -------
# ⬤ – □ ×
## -------

frmTitleBar = tk.Frame(app, bg = BLACK)

# Window action functions
def maxWindow():
    if app.wm_state() == "zoomed":
        app.state("normal")
        app.geometry("900x600+50+50")
    else:
        app.state("zoomed")

def minWindow():
    app.overrideredirect(False)
    app.state("iconic")
    app.overrideredirect(True)

btnClose = tk.Button(
    frmTitleBar,
    text = "×",
    bd = 0,
    bg = BLACK,
    fg = RED,
    font = ("Helvetica Black", 16),
    command = lambda: app.destroy())
btnClose.pack(side = tk.RIGHT, pady = (3, 0))

btnMaximize = tk.Button(
    frmTitleBar,
    text = "□",
    bd = 0,
    bg = BLACK,
    fg = GREEN,
    font = ("Helvetica Black", 16),
    command = maxWindow)
btnMaximize.pack(side = tk.RIGHT)

btnMinimize = tk.Button(
    frmTitleBar,
    text = "–",
    bd = 0,
    bg = BLACK,
    fg = YELLOW,
    font = ("Helvetica Black", 16),
    command = minWindow)
btnMinimize.pack(side = tk.RIGHT)

# Window title
## Window title icon
frmWindowIcon = tk.Frame(frmTitleBar)
icnTitle = tk.PhotoImage(file = "./icons/header-icon.png").subsample(2, 2)
lblIcon = tk.Label(frmWindowIcon, image = icnTitle, bg = BLACK)
lblIcon.pack()
frmWindowIcon.pack(side = "left")

## Window title text
frmTitleContainer = tk.Frame(frmTitleBar, bg = BLACK)

frmTitleLabelTop = tk.Label(
    frmTitleContainer, 
    text = "San Pablo City Government", 
    bg = BLACK,
    fg = WHITE,
    font = ("Helvetica", 8, "italic"))

frmTitleLabelBottom = tk.Label(
    frmTitleContainer, 
    text = "Tax Order System", 
    bg = BLACK,
    fg = WHITE,
    font = ("Helvetica", 10))

frmTitleContainer.pack(anchor = tk.W)
frmTitleLabelTop.pack(pady = (3, 0))
frmTitleLabelBottom.pack(pady = (0, 3))

# Initialize the titlebar
frmTitleBar.pack(anchor=tk.N, fill=tk.X)

# Window drag functions
def getPos(e):
    xWin = app.winfo_x()
    yWin = app.winfo_y()
    startX = e.x_root
    startY = e.y_root

    xWin = xWin - startX
    yWin = yWin - startY

    def mvWindow(e):
        app.geometry(f"+{e.x_root + xWin}+{e.y_root + yWin}")

    frmTitleBar.bind("<B1-Motion>", mvWindow)

# Bindings
## Window drag
frmTitleBar.bind("<B1-Motion>", getPos)

## Window buttons
btnClose.bind("<Enter>", lambda e: btnClose.config(fg = DARKRED))
btnClose.bind("<Leave>", lambda e: btnClose.config(fg = RED))

btnMaximize.bind("<Enter>", lambda e: btnMaximize.config(fg = DARKGREEN))
btnMaximize.bind("<Leave>", lambda e: btnMaximize.config(fg = GREEN))

btnMinimize.bind("<Enter>", lambda e: btnMinimize.config(fg = DARKYELLOW))
btnMinimize.bind("<Leave>", lambda e: btnMinimize.config(fg = YELLOW))