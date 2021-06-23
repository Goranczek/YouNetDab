import time
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import simpledialog
import os
from pathlib import Path
import json


class Window(object):

    def __init__(self, root):
        self.full_dict = {}
        self.root = root
        self.root.wm_title("CI Teradata")
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        self.root.iconbitmap(r'{}\icon.ico'.format(self.dir_path))

        # root label
        l1 = Label(root, text="files")
        l1.grid(row=0, column=0)

        login_holder = StringVar()
        self.login = Label(self.root, text="Username")
        self.login.grid(row=0, column=0)
        self.textfield_login = ttk.Entry(self.root, textvariable=login_holder)
        self.textfield_login.grid(row=0, column=1)

        pass_holder = StringVar()
        self.password = Label(self.root, text="Password")
        self.password.grid(row=1, column=0)
        self.textfield_pass = ttk.Entry(self.root, textvariable=pass_holder)
        self.textfield_pass.config(show="*")
        self.textfield_pass.grid(row=1, column=1)
        # root combobox
        loader_tmp = StringVar()
        self.cb1 = ttk.Combobox(root, textvariable=loader_tmp)
        self.cb1.grid(row=2, column=1)

        script_holder = StringVar()
        self.cmb2 = ttk.Combobox(self.root, textvariable=script_holder)

        self.l3 = Label(self.root, text="Prod tables")

        prod_tables = StringVar()
        self.textfield_prod_tables = ttk.Entry(self.root, textvariable=prod_tables)

        self.l4 = Label(self.root, text="Dev tables")

        dev_tables = StringVar()
        self.textfield_dev_tables = ttk.Entry(self.root, text=dev_tables)

        # root textbox
        self.text1 = Text(root, height=35, width=130)
        self.text1.grid(row=5, column=0, rowspan=2, columnspan=10)

        # menu definition
        main_menu = Menu(root)

        self.menuSoubor = Menu(main_menu, tearoff=0)
        self.menuSoubor.add_command(label="Open", command=self.open_dialog_window)
        # lambda allows send argument withnout executing the command in init phase
        self.menuSoubor.add_separator()
        self.menuSoubor.add_command(label="Exit", command=root.quit)
        self.menuSoubor.entryconfig(2, state=DISABLED)
        main_menu.add_cascade(label="File", menu=self.menuSoubor)

        root.config(menu=main_menu)

    def loader(self, list_files):
        self.cb1['values'] = list_files
        return

    # read filename, enable/disable buttons and other features
    def open_dialog_window(self):
        self.root.filename_open = filedialog.askdirectory()
        list_files = list()
        for file in Path(self.root.filename_open).iterdir():
            if file.suffix == ".txt":
                list_files.append(file.name)
        self.loader(list_files)
        btn = ttk.Button(self.root, text="Get scripts", command=self.get_scripts)
        btn.grid(row=2, column=2)

    def get_scripts(self):
        file = self.cb1.get()
        self.full_dict[file] = {}
        l2 = Label(self.root, text="Choose script")
        l2.grid(row=2, column=3)
        self.cmb2.grid(row=2, column=4)
        self.cmb2["values"] = self.scripts_parser(file)
        self.show_entry()
        btn2 = Button(self.root, text="Approve", command=self.set_dict)
        btn2.grid(row=2, column=5)

    def show_entry(self):
        self.l3.grid(row=3, column=3)
        self.textfield_prod_tables.grid(row=1, column=4)
        self.l4.grid(row=4, column=3)
        self.textfield_dev_tables.grid(row=2, column=4)

    def set_dict(self):
        file = self.cb1.get()
        script = self.cmb2.get()
        self.full_dict[file][script] = {}
        prod_tables = self.textfield_prod_tables.get()
        self.full_dict[file][script]["prod_tables"] = prod_tables
        dev_tables = self.textfield_dev_tables.get()
        self.full_dict[file][script]["dev_tables"] = dev_tables
        print(self.full_dict)

    def scripts_parser(self, file):
        with open(Path(self.root.filename_open, file), encoding="utf-8") as f:
            data = f.read()
            scripts = data.split(";")
            i = 1
            for script in scripts:
                self.text1.insert(END, str(i) + " " + script.strip() + "\n")
                i += 1
            self.text1.config(state=DISABLED)
        return scripts



window = Tk()
Window(window)
window.mainloop()
