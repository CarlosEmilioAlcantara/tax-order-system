import tkinter as tk
import sqlite3
from tkinter import StringVar, ttk
from ctypes import windll

# DATABASE
# -----------------------------------------------------------------------------

# dummyProfessionals = [
#     ['123456', 'Doe', 'John', 'Jones', '123 Brgy Lugar', 'Doctor'],
#     ['678901', 'Doe', 'Jane', 'Jones', '123 Brgy Lugar', 'Engineer'],
#     ['333333', 'Doe', 'Jack', 'Jones', '123 Brgy Lugar', 'Accountant'],
#     ['111111', 'Doe', 'Jill', 'Jones', '123 Brgy Lugar', 'Dentist']
# ]

# Create (if not already existing) or connect to database
try:
    conn = sqlite3.connect("tax-order-records.db")

    # Create a table if it still does not exist
    query = """
            CREATE TABLE 
               IF NOT EXISTS professionals(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   license_no TEXT,
                   last_name TEXT,
                   first_name TEXT,
                   middle_name TEXT,
                   address TEXT,
                   profession TEXT
               )
            """

    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()
except sqlite3.Error as e:
    print(f"Error occured: {e}")

# try:
#     # Adding dummy data
#     for record in dummyProfessionals:
#         query = f"""
#                 INSERT INTO professionals (
#                     license_no,
#                     last_name,
#                     first_name,
#                     middle_name,
#                     address,
#                     profession
#                 )
#                 VALUES (
#                     "{record[0]}",
#                     "{record[1]}",
#                     "{record[2]}",
#                     "{record[3]}",
#                     "{record[4]}",
#                     "{record[5]}"
#                 )
#                 """
#         cursor.execute(query)

#     conn.commit()
# except sqlite3.Error as e:
#     print(f"Error occured: {e}")

def getLicenseNumbers():
    conn = sqlite3.connect("tax-order-records.db")
    cursor = conn.cursor()

    query = "SELECT license_no FROM professionals"
    cursor.execute(query)
    licenseNumbers = cursor.fetchall()

    conn.close()

    return licenseNumbers

# Opening the record
def openRecord():
    # Assigning the selected row
    selected = treeBtns.focus()

    # Getting the license number from the row
    licenseNumber = treeBtns.item(selected, "values")[0]

    conn = sqlite3.connect("tax-order-records.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM professionals WHERE license_no = {licenseNumber}"
    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()

    return data

def searchLicenseNumbers(e):
    conn = sqlite3.connect("tax-order-records.db")
    cursor = conn.cursor()

    query = f"""
             SELECT license_no 
             FROM professionals 
             WHERE license_no
                LIKE '%{searchNumber.get()}%'
             """

    try:
        cursor.execute(query)
        likes = cursor.fetchall()

        if len(likes) > 0:
            for child in treeBtns.get_children():
                treeBtns.delete(child)

            for like in likes:
                treeBtns.insert(
                    parent = "",
                    index = "end",
                    text = "",
                    values = like
                )
        else:
            for child in treeBtns.get_children():
                treeBtns.delete(child)
    except sqlite3.Error as er:
        print(f"Error occured: {er}")

# -----------------------------------------------------------------------------
# END

# COLOR CONSTANTS
# -----------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------
# END

# THE APP WINDOW ITSELF
# -----------------------------------------------------------------------------

app = tk.Tk()
app.geometry("900x600+50+50")
app.config(bg = WHITE)
app.overrideredirect(True)

# -----------------------------------------------------------------------------
# END

# ALLOW INTS ONLY (TO BE USED ON ENTRY WIDGETS)
# -----------------------------------------------------------------------------

def onlyNumbers(char):
    return char.isdigit()

validation = app.register(onlyNumbers)

# -----------------------------------------------------------------------------
# END

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
frmMainTitleContainer = tk.Frame(frmTitleBar, bg = BLACK)

frmMainTitleLabelTop = tk.Label(
    frmMainTitleContainer, 
    text = "San Pablo City Government", 
    bg = BLACK,
    fg = WHITE,
    font = ("Helvetica", 8, "italic"))

frmMainTitleLabelBottom = tk.Label(
    frmMainTitleContainer, 
    text = "Tax Order System", 
    bg = BLACK,
    fg = WHITE,
    font = ("Helvetica", 10))

frmMainTitleContainer.pack(anchor = tk.W)
frmMainTitleLabelTop.pack(pady = (3, 0))
frmMainTitleLabelBottom.pack(pady = (0, 3))

# Initialize the titlebar
frmTitleBar.pack(anchor=tk.N, fill=tk.X)

buttons = ["12345"]

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
    frmMainTitleLabelTop.bind("<B1-Motion>", mvWindow)
    frmMainTitleLabelBottom.bind("<B1-Motion>", mvWindow)
    lblIcon.bind("<B1-Motion>", mvWindow)

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

# Records frame
def pnTaxRecord():
    frmTaxRecord = tk.Frame(frmBody)



    frmTaxRecord.pack(anchor = tk.W, fill = tk.BOTH, expand = True, side = tk.LEFT)

## Panes
### Create Records pane
# We need to preload images
icnCreate = tk.PhotoImage(file = "./icons/pen.png").subsample(2, 2)

def warnEmpty():
    warn = tk.Toplevel()
    warn.overrideredirect(True)
    frmWarnTitleBar = tk.Frame(warn, bg = BLACK)

    # Popup titlebar
    btnClose = tk.Button(
        frmWarnTitleBar,
        text = "×",
        bd = 0,
        bg = BLACK,
        fg = RED,
        font = ("Helvetica Black", 16),
        command = lambda: warn.destroy())
    btnClose.pack(side = tk.RIGHT, pady = (3, 0))

    # Window title
    ## Window title icon
    frmWindowIcon = tk.Frame(frmWarnTitleBar)
    lblIcon = tk.Label(frmWindowIcon, image = icnTitle, bg = BLACK)
    lblIcon.pack()
    frmWindowIcon.pack(side = "left")

    ## Window title text
    frmWarnTitleContainer = tk.Frame(frmWarnTitleBar, bg = BLACK)

    frmTitleLabelTop = tk.Label(
        frmWarnTitleContainer, 
        text = "San Pablo City Government", 
        bg = BLACK,
        fg = WHITE,
        font = ("Helvetica", 8, "italic"))

    frmTitleLabelBottom = tk.Label(
        frmWarnTitleContainer, 
        text = "Tax Order System", 
        bg = BLACK,
        fg = WHITE,
        font = ("Helvetica", 10))

    frmWarnTitleContainer.pack(anchor = tk.W)
    frmTitleLabelTop.pack(pady = (3, 0))
    frmTitleLabelBottom.pack(pady = (0, 3))

    # Initialize the titlebar
    frmWarnTitleBar.pack(anchor=tk.N, fill=tk.X)

    # Window drag functions
    def getPos(e):
        xWin = warn.winfo_x()
        yWin = warn.winfo_y()
        startX = e.x_root
        startY = e.y_root

        xWin = xWin - startX
        yWin = yWin - startY

        def mvWindow(e):
            warn.geometry(f"+{e.x_root + xWin}+{e.y_root + yWin}")

        frmWarnTitleContainer.bind("<B1-Motion>", mvWindow)
        frmWarnTitleBar.bind("<B1-Motion>", mvWindow)

    # Bindings
    ## Window drag
    frmWarnTitleBar.bind("<B1-Motion>", getPos)

    ## Window buttons
    btnClose.bind("<Enter>", lambda e: btnClose.config(fg = DARKRED))
    btnClose.bind("<Leave>", lambda e: btnClose.config(fg = RED))

    warn.bind("<FocusIn>", unminWindow)
    warn.after(1, lambda: setAppWindow(warn))

    frmWarningMessage = tk.Frame(
        warn,
        bg = WHITE
    )

    lblWarning = tk.Label(
        frmWarningMessage,
        text = "asfjlsafjlsafj"
    )
    lblWarning.pack()

    frmWarningMessage.pack(anchor = tk.S, fill = tk.BOTH, expand = 1)

def pnAddRecord():
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
    frmPopupTitleContainer = tk.Frame(frmPopupTitleBar, bg = BLACK)

    frmTitleLabelTop = tk.Label(
        frmPopupTitleContainer, 
        text = "San Pablo City Government", 
        bg = BLACK,
        fg = WHITE,
        font = ("Helvetica", 8, "italic"))

    frmTitleLabelBottom = tk.Label(
        frmPopupTitleContainer, 
        text = "Tax Order System", 
        bg = BLACK,
        fg = WHITE,
        font = ("Helvetica", 10))

    frmPopupTitleContainer.pack(anchor = tk.W)
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

        frmPopupTitleContainer.bind("<B1-Motion>", mvWindow)
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
        validate = "key",
        validatecommand = (validation, '%S'),
        bd = 0,
        bg = WHITE,
        fg = BLACK,
        font = ("Helvetica", 10),
        highlightthickness = 1,
        highlightbackground = GREY,
        width = 30)
    entLicenseNo.pack(ipady = 5)

    def createRecord():
        if len(entSurname.get()) == 0 or \
           len(entFirstname.get()) == 0 or \
           len(entMiddlename.get()) == 0 or \
           len(entAddress.get()) == 0 or \
           len(entProfession.get()) == 0 or \
           len(entLicenseNo.get()) == 0:
            
            warnEmpty()
        else:
            print("Oks")


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
        command = createRecord)
    btnCreate.pack(side = tk.RIGHT, pady = (10, 0))

    frmCreateRecordLeft.pack(anchor = tk.CENTER, side = tk.LEFT, padx = (30, 10), pady = (0, 36))
    frmCreateRecordRight.pack(anchor = tk.CENTER, side = tk.RIGHT, padx = (0, 30), pady = (20, 20))
    frmCreateRecord.pack()
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
    command = pnAddRecord
)
btnAdd.pack(side = tk.TOP, padx = 24, pady = 24)

# for licenseNo in buttons:
#     btnLicenseNo = tk.Button(
#         frmSidebar, 
#         bd = 0,
#         text = "LN: " + licenseNo, 
#         bg = WHITE,
#         font = ("Helvetica", 10),
#         )
#     btnLicenseNo.pack(side = tk.TOP, padx = 24)

# SIDEBAR LICENSE NUMBER BUTTONS
# -----------------------------------------------------------------------------
# Using a treeview so we can search through the license numbers

# Initializing the treeview style
styleTreeBtns = ttk.Style()
styleTreeBtns.theme_use('default')

# Setting the colors and rows
styleTreeBtns.configure(
    "Treeview",
    background = WHITE,
    foreground = BLACK,
    rowheight = 25,
    fieldbackground = WHITE
)

# Change color of selected row
styleTreeBtns.map(
    'Treeview',
    background = [('selected', GREEN)]
)

# Initializing the frame where our treeview will go
frmTree = tk.Frame(
    frmSidebar,
    )
frmTree.pack(padx = 10)

# Initializing a scrollbar so we can scroll through the license numbers
scrlTreeY = tk.Scrollbar(frmTree)
scrlTreeY.pack(
    side = tk.RIGHT, 
    fill = tk.Y
)

scrlTreeX = tk.Scrollbar(frmTree, orient = "horizontal")
scrlTreeX.pack(
    side = tk.BOTTOM, 
    fill = tk.X,
)

# The actual treeview
treeBtns = ttk.Treeview(
    frmTree, 
    columns = ("license_numbers"),
    yscrollcommand = scrlTreeY.set, 
    xscrollcommand = scrlTreeX.set,
    selectmode = "extended"
)
treeBtns.pack()

# So we can actually scroll
scrlTreeY.config(
    command = treeBtns.yview
)

scrlTreeX.config(
    command = treeBtns.xview
)

# Defining treeview buttons
# For some reason tkinter has a default first column, so we get rid of it
treeBtns.heading("#0") 
treeBtns.column("#0", width = 0, stretch = tk.NO) 

treeBtns.heading("license_numbers", text="License Numbers")
treeBtns.column(
    "license_numbers", 
    width = 200, 
    minwidth = 200, 
    anchor = tk.CENTER, 
    stretch = tk.YES
) 

# Add to treeview
licenseNumbers = getLicenseNumbers()
for number in licenseNumbers:
    treeBtns.insert(
        parent = "",
        index = "end",
        text = "",
        values = (number[0])
    )

# Searching through license numbers
frmSidebarSearch = tk.Frame(
    frmSidebar,
    bg = GREEN
)

lblSidebarSearch = tk.Label(
    frmSidebarSearch,
    text = "Search:",
    fg = WHITE,
    bg = GREEN,
    font = ("Helvetica", 8)
)
lblSidebarSearch.pack(anchor = tk.W)

searchNumber = StringVar()
# def filterTreeView(*args):
#     searchList = treeBtns.item()["values"][0]
#     print(searchList)

#     itemsOnTreeView = treeBtns.get_children()
#     print(itemsOnTreeView)

#     search = str(searchNumber.get())
#     print(search)

#     for eachItem in itemsOnTreeView:
#         if search in treeBtns.item(eachItem)["values"][0]:
#             searchVar = treeBtns.item(eachItem)["values"]
#             treeBtns.delete(eachItem)

#             treeBtns.insert(
#                 parent = "",
#                 index = 0,
#                 text = 0,
#                 values = searchVar
#             )

entSidebarSearch = tk.Entry(
    frmSidebarSearch,
    textvariable = searchNumber,
    validate = "key",
    validatecommand = (validation, '%S'),
    bd = 0,
    bg = WHITE,
    fg = BLACK,
    font = ("Helvetica", 10),
    width = 30)
entSidebarSearch.pack(ipady = 5)

# searchNumber.trace('w', filterTreeView)

# def search(e):

entSidebarSearch.bind("<KeyRelease>", searchLicenseNumbers)

frmSidebarSearch.pack()




icnRecord = tk.PhotoImage(file = "./icons/user-record.png").subsample(2, 2)

btnOpenRecord = tk.Button(
    frmSidebar, 
    bd = 0,
    text = "  Open Record", 
    image = icnRecord, 
    compound = tk.LEFT, 
    bg = WHITE,
    font = ("Helvetica", 10),
    width = 110,
    height = 30,
    command = openRecord
)
btnOpenRecord.pack(pady = 3)

# -----------------------------------------------------------------------------
# END

frmSidebar.pack(anchor = tk.W, fill = tk.Y, side = tk.LEFT)
# frmSidebar.pack_propagate(False)


frmBody.pack(fill = tk.BOTH, expand = True)

app.bind("<FocusIn>", unminWindow)
app.after(1, lambda: setAppWindow(app))
app.mainloop()