import tkinter as tk
from ctypes import windll

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

app = tk.Tk()
app.geometry("900x600+50+50")
app.config(bg = WHITE)
app.overrideredirect(True)

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

def setAppWindow(mainWindow):
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
   
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())

def minWindow():
    app.attributes("-alpha", 0)

def unminWindow(e):
    app.focus
    app.attributes("-alpha", 1)

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

buttons = ["LN: 12345"]

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

# Body
frmBody = tk.Frame(app)

## Panes
### Create Records pane
# We need to preload images
icnCreate = tk.PhotoImage(file = "./icons/pen.png").subsample(2, 2)

def pnRecords():
    top = tk.Toplevel()
    top.overrideredirect(True)
    frmPopupTitleBar = tk.Frame(top, bg = BLACK)

    # Popup titlebar
    btnClose = tk.Button(
        frmPopupTitleBar,
        text = "×",
        bd = 0,
        bg = BLACK,
        fg = RED,
        font = ("Helvetica Black", 16),
        command = lambda: top.destroy())
    btnClose.pack(side = tk.RIGHT, pady = (3, 0))

    # Window title
    ## Window title icon
    frmWindowIcon = tk.Frame(frmPopupTitleBar)
    lblIcon = tk.Label(frmWindowIcon, image = icnTitle, bg = BLACK)
    lblIcon.pack()
    frmWindowIcon.pack(side = "left")

    ## Window title text
    frmTitleContainer = tk.Frame(frmPopupTitleBar, bg = BLACK)

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
    frmPopupTitleBar.pack(anchor=tk.N, fill=tk.X)

    # Window drag functions
    def getPos(e):
        xWin = top.winfo_x()
        yWin = top.winfo_y()
        startX = e.x_root
        startY = e.y_root

        xWin = xWin - startX
        yWin = yWin - startY

        def mvWindow(e):
            top.geometry(f"+{e.x_root + xWin}+{e.y_root + yWin}")

        frmPopupTitleBar.bind("<B1-Motion>", mvWindow)

    # Bindings
    ## Window drag
    frmPopupTitleBar.bind("<B1-Motion>", getPos)

    ## Window buttons
    btnClose.bind("<Enter>", lambda e: btnClose.config(fg = DARKRED))
    btnClose.bind("<Leave>", lambda e: btnClose.config(fg = RED))

    frmCreateRecord = tk.Frame(top, bg = WHITE)
    frmCreateRecordLeft = tk.Frame(frmCreateRecord, bg = WHITE)

    top.bind("<FocusIn>", unminWindow)
    top.after(1, lambda: setAppWindow(top))

    # Record entries left
    lblSurname = tk.Label(
        frmCreateRecordLeft,
        text = "Surname / Last name:",
        fg = GREY,
        bg = WHITE,
        font = ("Helvetica", 8)
    )
    lblSurname.pack(anchor = tk.W)

    entSurname = tk.Entry(
        frmCreateRecordLeft,
        bd = 0,
        bg = WHITE,
        fg = BLACK,
        font = ("Helvetica", 10),
        highlightthickness = 1,
        highlightbackground = GREY,
        width = 30)
    entSurname.pack(ipady = 5)

    lblFirstname = tk.Label(
        frmCreateRecordLeft,
        text = "Firstname / Given name:",
        fg = GREY,
        bg = WHITE,
        font = ("Helvetica", 8)
    )
    lblFirstname.pack(anchor = tk.W)

    entFirstname = tk.Entry(
        frmCreateRecordLeft,
        bd = 0,
        bg = WHITE,
        fg = BLACK,
        font = ("Helvetica", 10),
        highlightthickness = 1,
        highlightbackground = GREY,
        width = 30)
    entFirstname.pack(ipady = 5)

    lblMiddlename = tk.Label(
        frmCreateRecordLeft,
        text = "Middle name:",
        fg = GREY,
        bg = WHITE,
        font = ("Helvetica", 8)
    )
    lblMiddlename.pack(anchor = tk.W)

    entMiddlename = tk.Entry(
        frmCreateRecordLeft,
        bd = 0,
        bg = WHITE,
        fg = BLACK,
        font = ("Helvetica", 10),
        highlightthickness = 1,
        highlightbackground = GREY,
        width = 30)
    entMiddlename.pack(ipady = 5)

    def test():
        buttons.append(entSurname.get())

        # Kunin number ng pinakabago tapos display
        for button in buttons:
            name = "btn" + button
            name = tk.Button(
                frmSidebar, 
                bd = 0,
                text = name, 
                bg = WHITE,
                font = ("Helvetica", 10),
                )
            name.pack(side = tk.TOP, padx = 24, pady = 24)

    frmCreateRecordRight = tk.Frame(frmCreateRecord, bg = WHITE)

    # Record entries right
    lblAddress = tk.Label(
        frmCreateRecordRight,
        text = "Address:",
        fg = GREY,
        bg = WHITE,
        font = ("Helvetica", 8)
    )
    lblAddress.pack(anchor = tk.W)

    entAddress = tk.Entry(
        frmCreateRecordRight,
        bd = 0,
        bg = WHITE,
        fg = BLACK,
        font = ("Helvetica", 10),
        highlightthickness = 1,
        highlightbackground = GREY,
        width = 30)
    entAddress.pack(ipady = 5)

    lblProfession = tk.Label(
        frmCreateRecordRight,
        text = "Profession:",
        fg = GREY,
        bg = WHITE,
        font = ("Helvetica", 8)
    )
    lblProfession.pack(anchor = tk.W)

    entProfession = tk.Entry(
        frmCreateRecordRight,
        bd = 0,
        bg = WHITE,
        fg = BLACK,
        font = ("Helvetica", 10),
        highlightthickness = 1,
        highlightbackground = GREY,
        width = 30)
    entProfession.pack(ipady = 5)

    lblLicenseNo = tk.Label(
        frmCreateRecordRight,
        text = "License #:",
        fg = GREY,
        bg = WHITE,
        font = ("Helvetica", 8)
    )
    lblLicenseNo.pack(anchor = tk.W)

    entLicenseNo = tk.Entry(
        frmCreateRecordRight,
        bd = 0,
        bg = WHITE,
        fg = BLACK,
        font = ("Helvetica", 10),
        highlightthickness = 1,
        highlightbackground = GREY,
        width = 30)
    entLicenseNo.pack(ipady = 5)

    btnCreate = tk.Button(
        frmCreateRecordRight, 
        bd = 0,
        text = "Save", 
        image = icnCreate,
        compound = tk.LEFT,
        bg = GREEN,
        fg = WHITE,
        font = ("Helvetica", 12),
        width = 70,
        height = 22,
        command = test)
    btnCreate.pack(side = tk.RIGHT, pady = (10, 0))

    frmCreateRecordLeft.pack(anchor = tk.CENTER, side = tk.LEFT, padx = (30, 10), pady = (0, 36))
    frmCreateRecordRight.pack(anchor = tk.CENTER, side = tk.RIGHT, padx = (0, 30), pady = (20, 20))
    frmCreateRecord.pack(anchor = tk.W, fill = tk.BOTH, expand = True, side = tk.LEFT)
    # frmCreateRecord.pack_propagate(False)

## Sidebar
frmSidebar = tk.Frame(frmBody, bg = GREEN)
# frmSidebar.config(width = 150)

### Sidebar buttons
icnAdd = tk.PhotoImage(file = "./icons/user-plus.png").subsample(2, 2)
btnAdd = tk.Button(
    frmSidebar, 
    bd = 0,
    text = "Add Record", 
    image = icnAdd, 
    compound = tk.LEFT, 
    bg = WHITE,
    font = ("Helvetica", 10),
    width = 110,
    height = 30,
    command = pnRecords)
btnAdd.pack(side = tk.TOP, padx = 24, pady = 24)

for button in buttons:
    name = "btn" + button
    name = tk.Button(
        frmSidebar, 
        bd = 0,
        text = name, 
        bg = WHITE,
        font = ("Helvetica", 10),
        )
    name.pack(side = tk.TOP, padx = 24, pady = 24)

frmSidebar.pack(anchor = tk.W, fill = tk.Y, side = tk.LEFT)
# frmSidebar.pack_propagate(False)


frmBody.pack(fill = tk.BOTH, expand = True)

app.bind("<FocusIn>", unminWindow)
app.after(1, lambda: setAppWindow(app))
app.mainloop()