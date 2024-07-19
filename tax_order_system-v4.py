import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime
from tkcalendar import Calendar
import tkinter.ttk as ttk
from database_funcs import initialize_database, get_license_numbers, \
                            search_license_numbers, add_record, open_record, \
                            edit_record, delete_record, get_receipts, \
                            add_receipt, detect_newness

GREY = "#DDDDDD"
BLUE = "#80B1D3"
WHITE = "#ECEFF4"
BLACK = "#0C0D0E"

def only_numbers(char):
    return char.isdigit() or char == '.'

class Sidebar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(width=190, bg=GREY, relief="ridge", 
                    highlightcolor=BLUE, border=1)
        self.pack_propagate(False)

        self.create_header()
        self.create_add()
        self.create_treeview()
        self.load_license_numbers()
        self.create_search()
        self.create_open()

    def create_header(self):
        self.frm_header = tk.Frame(self, bg=GREY)

        self.icn_sidebar = tk.PhotoImage(file='icons/header-icon.png')
        lbl_icon = tk.Label(self.frm_header, image=self.icn_sidebar, bg=GREY)

        lbl_sidebar = tk.Label(self.frm_header, 
                               text="Professional\nTax Order System", bg=GREY,
                               font=("bold"))

        lbl_icon.pack(pady=(20, 0))
        lbl_sidebar.pack(pady=(0, 10))
        self.frm_header.pack()

    def create_add(self):
        self.btn_add = tk.Button(self, text="Add Record", bg=BLUE,
                                      activebackground=BLUE, fg=WHITE,
                                      activeforeground=WHITE, font=("24"),
                                      command=self.open_add_record_window)

        self.btn_add.pack(padx=10, pady=10)

    def open_add_record_window(self):
        AddRecordWindow(self.master)

    def create_treeview(self):
        self.sty_treeview = ttk.Style()
        self.sty_treeview.theme_use('default')

        self.sty_treeview.configure("Treeview", background=WHITE,
                                    foreground=BLACK, rowheight=25,
                                    fieldbackground=WHITE)
        
        self.sty_treeview.map("Treeview", background=[('selected', BLUE)])

        self.frm_treeview = tk.Frame(self)
        self.frm_treeview.pack(padx=5)

        self.scrl_treeview_x = tk.Scrollbar(self.frm_treeview,
                                            orient="horizontal")
        self.scrl_treeview_x.pack(side="bottom", fill="x")
        
        self.scrl_treeview_y = tk.Scrollbar(self.frm_treeview)
        self.scrl_treeview_y.pack(side="right", fill="y")

        self.trv_license = ttk.Treeview(self.frm_treeview,
                                       columns="license_numbers",
                                       xscrollcommand=self.scrl_treeview_x,
                                       yscrollcommand=self.scrl_treeview_y,
                                       selectmode="extended")

        self.trv_license.heading("#0")
        self.trv_license.column("#0", width=0, stretch=tk.NO)

        self.trv_license.heading("license_numbers", text="License Numbers")
        self.trv_license.column("license_numbers", width=150,
                               anchor="center", stretch=tk.YES)
            
        self.trv_license.tag_configure("oddrow", background=BLUE, 
                                       foreground=WHITE)
        self.trv_license.tag_configure("oddrow", background=WHITE, 
                                       foreground=BLUE)

        self.trv_license.pack()

    def create_search(self):
        lbl_search = tk.Label(self, text="Search License Numbers:", bg=GREY)
        lbl_search.pack(pady=(6, 0))

        self.validation = self.register(only_numbers)
        self.search_number = tk.StringVar()

        self.ent_search = tk.Entry(self, textvariable=self.search_number,
                                    validate="key",
                                    validatecommand=(self.validation, '%S')
                                    )
        self.ent_search.pack()

        self.ent_search.bind("<KeyRelease>", self.handle_search)

    def load_license_numbers(self):
        self.trv_license.delete(*self.trv_license.get_children())
        license_numbers = get_license_numbers()
        for i, number in enumerate(license_numbers):
            if i % 2 == 0:
                self.trv_license.insert("", "end", text="", values=number,
                                        iid=i, tags=("evenrow",))
            else:
                self.trv_license.insert("", "end", text="", values=number,
                                        iid=i, tags=("oddrow",))

    def display_search_results(self, results):
        self.trv_license.delete(*self.trv_license.get_children())
        for i, result in enumerate(results):
            if i % 2 == 0:
                self.trv_license.insert("", "end", text="", values=result,
                                        iid=i, tags=("evenrow",))
            else:
                self.trv_license.insert("", "end", text="", values=result,
                                        iid=i, tags=("oddrow",))

    def handle_search(self, e):
        search_number = self.ent_search.get()
        results = search_license_numbers(search_number)
        self.display_search_results(results)

    def create_open(self):
        self.btn_open = tk.Button(self, text="Open Record", bg=BLUE,
                                      activebackground=BLUE, fg=WHITE,
                                      activeforeground=WHITE, font=("24"),
                                      command=self.handle_open_record)

        self.btn_open.pack(padx=10, pady=10)
    
    def handle_open_record(self):
        selected = self.trv_license.focus()
        license_no = self.trv_license.item(selected, "values")[0]

        record = open_record(license_no)

        self.master.mainwindow.ent_last_name.delete(0, "end")
        self.master.mainwindow.ent_first_name.delete(0, "end")
        self.master.mainwindow.ent_middle_name.delete(0, "end")
        self.master.mainwindow.ent_address.delete(0, "end")
        self.master.mainwindow.ent_profession.delete(0, "end")

        self.master.mainwindow.ent_last_name.insert(0, record[0][2])
        self.master.mainwindow.ent_first_name.insert(0, record[0][3])
        self.master.mainwindow.ent_middle_name.insert(0, record[0][4])
        self.master.mainwindow.ent_address.insert(0, record[0][5])
        self.master.mainwindow.ent_profession.insert(0, record[0][6])
        self.master.mainwindow.lbl_license_no.config(text=record[0][1])

        self.master.mainwindow.load_receipts(license_no)
        self.master.mainwindow.handle_detect_newness(license_no)

class MainWindow(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.mainwindow_top()
        self.create_treeview()

    def mainwindow_top(self):
        self.frm_top = tk.Frame(self)

        self.create_professional(self.frm_top)
        self.create_receipt(self.frm_top)

        self.frm_top.pack()

    def create_professional(self, top):
        self.frm_professional = tk.Frame(top)
        self.frm_professional_left = tk.Frame(self.frm_professional)
        self.frm_professional_middle = tk.Frame(self.frm_professional)
        self.frm_professional_right = tk.Frame(self.frm_professional)

        lbl_professional = tk.Label(self.frm_professional, 
                                    text="Professional Records", font=("24"))
        lbl_professional.pack()

        lbl_last_name = tk.Label(self.frm_professional_left, text="Last Name:")
        lbl_last_name.pack(anchor="w")
        self.ent_last_name = tk.Entry(self.frm_professional_left, width=30)
        self.ent_last_name.pack(anchor="w", ipady=3, pady=(0, 5))

        lbl_first_name = tk.Label(self.frm_professional_left, 
                                  text="First Name:")
        lbl_first_name.pack(anchor="w")
        self.ent_first_name = tk.Entry(self.frm_professional_left, width=30)
        self.ent_first_name.pack(anchor="w", ipady=3, pady=(0, 5))

        lbl_middle_name = tk.Label(self.frm_professional_left, 
                                   text="Middle Name:")
        lbl_middle_name.pack(anchor="w")
        self.ent_middle_name = tk.Entry(self.frm_professional_left, width=30)
        self.ent_middle_name.pack(anchor="w", ipady=3)

        lbl_address = tk.Label(self.frm_professional_middle, text="Address:")
        lbl_address.pack(anchor="w")
        self.ent_address = tk.Entry(self.frm_professional_middle, width=30)
        self.ent_address.pack(anchor="w", ipady=3, pady=(0, 5))

        lbl_profession = tk.Label(self.frm_professional_middle, 
                                  text="Profession:")
        lbl_profession.pack(anchor="w")
        self.ent_profession = tk.Entry(self.frm_professional_middle, width=30)
        self.ent_profession.pack(anchor="w", ipady=3, pady=(0, 5))

        lbl_license = tk.Label(self.frm_professional_middle, 
                               text="License Number:")
        lbl_license.pack(anchor="w")
        self.lbl_license_no = tk.Label(self.frm_professional_middle, 
                                       text="LICENSE")
        self.lbl_license_no.pack(anchor="w")

        self.btn_edit_professional = tk.Button(self.frm_professional_right,
                                               text="Edit Professional",
                                               command=self.handle_edit_record)
        self.btn_edit_professional.pack()

        self.btn_delete_professional = tk.Button(self.frm_professional_right,
                                               text="Delete Professional",
                                               command=self.handle_delete_record)
        self.btn_delete_professional.pack()

        self.frm_professional_left.pack(side="left", padx=6)
        self.frm_professional_right.pack(side="right", padx=6)
        self.frm_professional_middle.pack(side="right", padx=6)
        self.frm_professional.pack(side="left")

    def handle_edit_record(self):
        license_no = self.lbl_license_no.cget("text")    

        last_name = self.ent_last_name.get()
        first_name = self.ent_first_name.get()
        middle_name = self.ent_middle_name.get()
        address = self.ent_address.get()
        profession = self.ent_profession.get()


        if (len(license_no) == 0 or len(last_name) == 0 or 
            len(first_name) == 0 or len(middle_name) == 0 or
            len(address) == 0 or len(profession) == 0):

            messagebox.showerror(
                "Record Editing Error", 
                "Error! Have you inputted all/the proper values?"
            )
        else:
            edit_record(license_no, last_name, first_name, middle_name, 
                        address, profession)

            messagebox.showinfo("Record Editing Successful", 
                                "Done! Records have been edited.")

    def handle_delete_record(self):
        license_no = self.lbl_license_no.cget("text")    

        if license_no == "LICENSE":
            messagebox.showerror("Record Deletion Error",
                                "Error! Please pick a record first.")
        else:
            answer = messagebox.askyesno("Deletion Confirmation",
                                        "Are you sure you want to delete this " +
                                        "professional's record?")

            if answer:
                delete_record(license_no)

                self.ent_last_name.delete(0, "end")
                self.ent_first_name.delete(0, "end")
                self.ent_middle_name.delete(0, "end")
                self.ent_address.delete(0, "end")
                self.ent_profession.delete(0, "end")
                self.lbl_license_no.config(text="LICENSE")

                messagebox.showinfo("Record Deletion Successful",
                                    "Done! Records have been deleted.")

                self.master.sidebar.load_license_numbers()

    def load_receipts(self, license_no):
        self.trv_receipt.delete(*self.trv_receipt.get_children())
        receipts = get_receipts(license_no)
        for i, number in enumerate(receipts):
            if i % 2 == 0:
                self.trv_receipt.insert("", "end", text="", values=number,
                                        iid=i, tags=("evenrow",))
            else:
                self.trv_receipt.insert("", "end", text="", values=number,
                                        iid=i, tags=("oddrow",))

    def create_receipt(self, top):
        self.frm_receipt = tk.Frame(top)
        self.frm_receipt_left = tk.Frame(self.frm_receipt)
        self.frm_receipt_middle = tk.Frame(self.frm_receipt)
        self.frm_receipt_right = tk.Frame(self.frm_receipt)

        lbl_order = tk.Label(self.frm_receipt, text="Order Receipts", 
                             font=("24"))
        lbl_order.pack(pady=(46, 8))

        lbl_date = tk.Label(self.frm_receipt_left, text="Date:")
        lbl_date.pack(anchor="w")

        today = datetime.now()
        self.cal_date = Calendar(self.frm_receipt_left, selectmode="day",
                                 year=int(today.strftime("%Y")),
                                 month=int(today.strftime("%m")),
                                 day=int(today.strftime("%d")))
        self.cal_date.pack()

        lbl_receipt_no = tk.Label(self.frm_receipt_middle, 
                                  text="Official Receipt Number:")
        lbl_receipt_no.pack(anchor="w")

        self.validation = self.register(only_numbers)
        self.input_receipt = tk.StringVar()

        self.ent_receipt_no = tk.Entry(self.frm_receipt_middle, 
                                       textvariable=self.input_receipt,
                                       validate="key",
                                       validatecommand=(self.validation, '%S'),
                                       width=30)
        self.ent_receipt_no.pack(anchor="w", ipady=3, pady=(0, 5))

        lbl_amount = tk.Label(self.frm_receipt_middle, text="Amount:")
        lbl_amount.pack(anchor="w")

        self.input_amount = tk.StringVar()
        self.ent_amount = tk.Entry(self.frm_receipt_middle, 
                                   textvariable=self.input_amount,
                                   validate="key",
                                   validatecommand=(self.validation, '%S'),
                                   width=30)
        self.ent_amount.pack(anchor="w", ipady=3, pady=(0, 5))

        lbl_type_of_payment = tk.Label(self.frm_receipt_middle, 
                                       text="Type of Payment")
        lbl_type_of_payment.pack(anchor="w")

        self.frm_radiobuttons = tk.Frame(self.frm_receipt_middle)

        self.payment = tk.StringVar()
        self.payment.set("None")
        self.rdb_new = tk.Radiobutton(self.frm_radiobuttons, text="New",
                                      variable=self.payment, value="New")
        self.rdb_new.pack(anchor="w", side="left")

        self.rdb_renew = tk.Radiobutton(self.frm_radiobuttons, text="Renew",
                                        variable=self.payment, value="Renew")
        self.rdb_renew.pack(anchor="w", side="right")

        self.frm_radiobuttons.pack(anchor="w")

        self.btn_add_receipt = tk.Button(self.frm_receipt_right,
                                         text="Add Receipt",
                                         command=self.handle_add_receipt)
        self.btn_add_receipt.pack()

        self.btn_edit_receipt = tk.Button(self.frm_receipt_right,
                                          text="Edit Receipt")
        self.btn_edit_receipt.pack()

        self.btn_delete_receipt = tk.Button(self.frm_receipt_right,
                                            text="Delete Receipt")
        self.btn_delete_receipt.pack()

        self.frm_receipt_left.pack(side="left", padx=6)
        self.frm_receipt_right.pack(side="right", padx=6)
        self.frm_receipt_middle.pack(side="right", padx=6)
        self.frm_receipt.pack(side="right")

    def handle_add_receipt(self):
        license_no = self.lbl_license_no.cget("text")    

        receipt_no = self.ent_receipt_no.get()
        type_of_payment = self.payment.get()
        receipt_date = self.cal_date.get_date()        
        amount = self.ent_amount.get()

        if (len(license_no) == 0 or len(receipt_no) == 0 or 
            type_of_payment == "None" or len(receipt_date) == 0 or
            len(amount) == 0):

            messagebox.showerror(
                "Receipt Addition Error", 
                "Error! Have you inputted all/the proper values?"
            )
        elif self.check_amount():
            messagebox.showerror(
                "Receipt Addition Error", 
                "Error! You have too many zeroes in the amount."
            )
        else: 
            add_receipt(license_no, receipt_no, type_of_payment, receipt_date, 
                        amount)

            messagebox.showinfo("Record Addition Successful", 
                                "Done! Receipt has been added.")

            self.load_receipts(license_no)

    def check_amount(self):
        characters = self.ent_amount.get()
        characters = list(characters)

        x = 0
        for y in characters:
            if y == ".":
                x += 1

        if x > 1:
            return True

    def create_treeview(self):
        self.sty_treeview = ttk.Style()
        self.sty_treeview.theme_use('default')

        self.sty_treeview.configure("Treeview", background=WHITE,
                                    foreground=BLACK, rowheight=25,
                                    fieldbackground=WHITE)
        
        self.sty_treeview.map("Treeview", background=[('selected', BLUE)])

        self.frm_treeview = tk.Frame(self)
        self.frm_treeview.pack(padx=5)

        self.scrl_treeview_x = tk.Scrollbar(self.frm_treeview,
                                            orient="horizontal")
        self.scrl_treeview_x.pack(side="bottom", fill="x")
        
        self.scrl_treeview_y = tk.Scrollbar(self.frm_treeview)
        self.scrl_treeview_y.pack(side="right", fill="y")

        self.trv_receipt = ttk.Treeview(self.frm_treeview,
                                       columns=("license_numbers", "receipt_no",
                                                "type_of_payment", "date",
                                                "amount", "penalty"),
                                       xscrollcommand=self.scrl_treeview_x,
                                       yscrollcommand=self.scrl_treeview_y,
                                       selectmode="extended")

        self.trv_receipt.heading("#0")
        self.trv_receipt.column("#0", width=0, stretch=tk.NO)

        self.trv_receipt.heading("license_numbers", text="License Numbers")
        self.trv_receipt.column("license_numbers", width=150,
                               anchor="center", stretch=tk.YES)

        self.trv_receipt.heading("receipt_no", text="Official Receipt Number")
        self.trv_receipt.column("receipt_no", width=150,
                               anchor="center", stretch=tk.YES)

        self.trv_receipt.heading("type_of_payment", 
                                 text="Type of Payment")
        self.trv_receipt.column("type_of_payment", width=150,
                               anchor="center", stretch=tk.YES)

        self.trv_receipt.heading("date", text="Date of Payment")
        self.trv_receipt.column("date", width=150,
                               anchor="center", stretch=tk.YES)

        self.trv_receipt.heading("amount", text="Amount")
        self.trv_receipt.column("amount", width=150,
                               anchor="center", stretch=tk.YES)

        self.trv_receipt.heading("penalty", text="Penalty")
        self.trv_receipt.column("penalty", width=150,
                               anchor="center", stretch=tk.YES)
            
        self.trv_receipt.tag_configure("oddrow", background=BLUE, 
                                       foreground=WHITE)
        self.trv_receipt.tag_configure("oddrow", background=WHITE, 
                                       foreground=BLUE)

        self.trv_receipt.pack()

    def handle_detect_newness(self, license_no):
        count = detect_newness(license_no)

        if (count == 0):
            self.payment.set("New")
            self.rdb_renew.config(state="disabled")
            self.lbl_new = tk.Label(self.frm_receipt_middle, text="NO RECORDS YET",
                               fg="#ff0000")
            self.lbl_new.pack()
        else:
            try:
                if self.lbl_new.winfo_exists():
                    self.payment.set("None")
                    self.rdb_renew.config(state="normal")
                    self.lbl_new.pack_forget()
            except AttributeError:
                pass

class AddRecordWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.geometry("500x300+60+60")
        self.resizable(0, 0)
        self.grab_set()

        self.create_header()
        self.create_add_form()
        self.create_btn_new()

    def create_header(self):
        lbl_header = tk.Label(self, text="Add Professional Record", bg=WHITE,
                              font=("bold"))

        lbl_header.pack(pady=10)

    def create_add_form(self):
        self.frm_add = tk.Frame(self)
        self.frm_add_left = tk.Frame(self.frm_add)
        self.frm_add_right = tk.Frame(self.frm_add)

        lbl_last_name = tk.Label(self.frm_add_left, text="Last Name:")
        lbl_last_name.pack(anchor="w")
        self.ent_last_name = tk.Entry(self.frm_add_left, width=30)
        self.ent_last_name.pack(anchor="w", ipady=3)

        lbl_first_name = tk.Label(self.frm_add_left, text="First Name:")
        lbl_first_name.pack(anchor="w")
        self.ent_first_name = tk.Entry(self.frm_add_left, width=30)
        self.ent_first_name.pack(anchor="w", ipady=3)

        lbl_middle_name = tk.Label(self.frm_add_left, text="Middle Name:")
        lbl_middle_name.pack(anchor="w")
        self.ent_middle_name = tk.Entry(self.frm_add_left, width=30)
        self.ent_middle_name.pack(anchor="w", ipady=3)

        lbl_address = tk.Label(self.frm_add_right, text="Address:")
        lbl_address.pack(anchor="w")
        self.ent_address = tk.Entry(self.frm_add_right, width=30)
        self.ent_address.pack(anchor="w", ipady=3)

        lbl_profession = tk.Label(self.frm_add_right, text="Profession:")
        lbl_profession.pack(anchor="w")
        self.ent_profession = tk.Entry(self.frm_add_right, width=30)
        self.ent_profession.pack(anchor="w", ipady=3)

        lbl_license = tk.Label(self.frm_add_right, text="License No:")
        lbl_license.pack(anchor="w")

        self.validation = self.register(only_numbers)
        self.input_number = tk.StringVar()

        self.ent_license = tk.Entry(self.frm_add_right, 
                                    textvariable=self.input_number,
                                    validate="key",
                                    validatecommand=(self.validation, '%S'),
                                    width=30)
        self.ent_license.pack(anchor="w", ipady=3)

        self.frm_add_left.pack(side="left", padx=6)
        self.frm_add_right.pack(side="right", padx=6)
        self.frm_add.pack(anchor="center")

    def create_btn_new(self):
        btn_add = tk.Button(self, text="Add New Record", 
                            command=self.handle_add_record)
        btn_add.pack(padx=10, pady=10)

    def handle_add_record(self):
        license_no = self.ent_license.get()
        last_name = self.ent_last_name.get()
        first_name = self.ent_first_name.get()
        middle_name = self.ent_middle_name.get()
        address = self.ent_address.get()
        profession = self.ent_profession.get()

        if (len(license_no) == 0 or len(last_name) == 0 or 
            len(first_name) == 0 or len(middle_name) == 0 or
            len(address) == 0 or len(profession) == 0):

            messagebox.showerror(
                "Record Addition Error", 
                "Error! Have you inputted all/the proper values?"
            )
        else:
            add_record(license_no, last_name, first_name, middle_name, address,
                       profession)
       
            self.master.sidebar.load_license_numbers()
            self.destroy()

class TaxOrderSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")

        initialize_database()

        self.geometry("900x600+50+50")
        self.title("San Pablo City Government - Professional Tax Order System")
        self.ph_title = tk.PhotoImage(file='icons/header-icon.png')
        self.iconphoto(self, self.ph_title)

        self.sidebar = Sidebar(self)
        self.sidebar.pack(side="left", fill="y")

        self.mainwindow = MainWindow(self)
        self.mainwindow.pack(side="right", fill="both")

def main():
    app = TaxOrderSystem()
    app.mainloop()

if __name__ == "__main__":
    main()