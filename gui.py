import time
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import simpledialog
import os
from pathlib import Path


class Window(object):

    def __init__(self, root):

        self.root = root
        self.root.wm_title("CI Teradata")
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        self.root.iconbitmap(r'{}\icon.ico'.format(self.dir_path))

        # root label
        l1 = Label(root, text="files")
        l1.grid(row=0, column=0)

        # root combobox
        loader_tmp = StringVar()
        self.cb1 = ttk.Combobox(root, textvariable=loader_tmp)
        self.cb1.grid(row=0, column=1)


        # root textbox
        self.text1 = Text(root, height=35, width=130)
        self.text1.grid(row=5, column=0, rowspan=2, columnspan=10)
        self.text1.config(state="disabled")

        self.text2 = Text(root, height=1, width=130)
        self.text2.grid(row=8, column=0, rowspan=1, columnspan=10)
        self.text2.config(state="normal")
        self.text2.insert(INSERT, "Ready")
        self.text2.config(state="disabled")

        # menu definition
        main_menu = Menu(root)

        self.menuSoubor = Menu(main_menu, tearoff=0)
        self.menuSoubor.add_command(label="Open", command=self.open_dialog_window)
        # lambda allows send argument withnout executing the command in init phase
        self.menuSoubor.add_separator()
        self.menuSoubor.add_command(label="Exit", command=root.quit)
        self.menuSoubor.entryconfig(2, state=DISABLED)
        main_menu.add_cascade(label="File", menu=self.menuSoubor)

        self.menuRun = Menu(main_menu, tearoff=0)
        self.menuRun.add_command(label="Analyze", command=self.popup_run_options)
        self.menuRun.entryconfig(0, state=DISABLED)
        self.menuRun.entryconfig(1, state=DISABLED)
        self.menuRun.entryconfig(2, state=DISABLED)
        main_menu.add_cascade(label="Run", menu=self.menuRun)

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
        btn.grid(row=0, column=2)

    def get_scripts(self):
        file = self.cb1.get()
        l2 = Label(self.root, text="Choose script")
        l2.grid(row=0, column=3)
        script_holder = StringVar()
        cmb2 = ttk.Combobox(self.root, textvariable=script_holder)
        cmb2.grid(row=0, column=4)
        cmb2["values"] = self.scripts_parser(file)

    def scripts_parser(self, file):
        with open(Path(self.root.filename_open, file)) as f:
            data = f.read()
            scripts = data.split(";")
        return scripts

    # method which run popup "setting" window
    def popup_run_options(self):
        self.popup = Toplevel()
        self.popup.wm_title("Run options")
        self.popup.iconbitmap(r'{}\icon.ico'.format(self.dir_path))

        # set of functions which allow user to define columns that should be analysed
        self.column_list = []
        def add_row():
            try:
                self.pop_list_orig.delete(self.index)
                self.pop_list_new.insert(END, self.selected_item_add)
                self.column_list.append(self.selected_item_add)
                self.index = None
                self.selected_item_add = None
                return self.pop_list_new
            except TclError:
                pass

        def remove_row():
            try:
                self.pop_list_new.delete(self.index_remove)
                self.pop_list_orig.insert(END, self.selected_item_remove)
                self.column_list.remove(self.selected_item_remove)
                self.index_remove = None
                self.selected_item_remove = None
                return self.pop_list_orig
            except TclError:
                pass

        def get_selected_row_add(event):
            try:
                self.index = self.pop_list_orig.curselection()[0]
                self.selected_item_add = self.pop_list_orig.get(self.index)
            except IndexError:
                pass

        def get_selected_row_remove(event):
            try:
                self.index_remove = self.pop_list_new.curselection()[0]
                self.selected_item_remove = self.pop_list_new.get(self.index_remove)
            except IndexError:
                pass

        # method for enable/disable listboxes and buttons for column analysis - depend on user input
        def check_column_analysis():
            if self.use_columns.get() == 0:
                pop_btn_add.config(state=DISABLED)
                pop_btn_del.config(state=DISABLED)
                self.pop_list_orig.config(state="disabled")
                self.pop_list_new.config(state="disabled")
            else:
                pop_btn_add.config(state=NORMAL)
                pop_btn_del.config(state=NORMAL)
                self.pop_list_orig.config(state="normal")
                self.pop_list_new.config(state="normal")

        # duplicates description group in popup window
        dupl_group = LabelFrame(self.popup, text="Keep duplicates")
        dupl_group.grid(row=1, column=1)
        self.dupl_desc = IntVar()
        rbtn_dupl_desc1 = Radiobutton(dupl_group, text="First", variable=self.dupl_desc, value=1)
        rbtn_dupl_desc1.grid(row=2, column=1)
        rbtn_dupl_desc2 = Radiobutton(dupl_group, text="Last", variable=self.dupl_desc, value=2)
        rbtn_dupl_desc2.grid(row=2, column=2)
        rbtn_dupl_desc3 = Radiobutton(dupl_group, text="None", variable=self.dupl_desc, value=3)
        rbtn_dupl_desc3.grid(row=2, column=3)
        self.dupl_desc.set(1)

        # columns for analysis group in popup window
        columns_group = LabelFrame(self.popup, text="Column analysis")
        columns_group.grid(row=3, column=1)
        self.use_columns = IntVar()
        check_btn = Checkbutton(columns_group, text="Select columns for analysis", variable=self.use_columns, command=check_column_analysis)
        check_btn.grid(row=4, column=1, columnspan=3)
        pop_lbl1 = ttk.Label(columns_group, text="Columns for analysis")
        pop_lbl1.grid(row=5, column=3)
        pop_lbl2 = ttk.Label(columns_group, text="Columns")
        pop_lbl2.grid(row=5, column=1)
        self.pop_list_orig = Listbox(columns_group, height=15, width=20)
        self.pop_list_orig.grid(row=7, column=1, rowspan=15)
        self.pop_list_new = Listbox(columns_group, height=15, width=20)
        self.pop_list_new.grid(row=7, column=3, rowspan=15)
        pop_btn_add = ttk.Button(columns_group, text="Add", command=add_row)
        pop_btn_add.grid(row=11, column=2)
        pop_btn_del = ttk.Button(columns_group, text="Remove", command=remove_row)
        pop_btn_del.grid(row=12, column=2)

        Frame(height=2, bd=1, relief=SUNKEN).grid(row=23)

        self.pop_btn = ttk.Button(self.popup, text="Analyse", command=self.file_analysis)
        self.pop_btn.grid(row=24, column=1)

        # get input parameters and return columns for analysis into listbox in popup window

        self.pop_list_orig.bind('<<ListboxSelect>>', get_selected_row_add)
        self.pop_list_new.bind('<<ListboxSelect>>', get_selected_row_remove)

        # listbox + buttons disable while opening the popup window
        check_column_analysis()

        self.popup.mainloop()


window = Tk()
Window(window)
window.mainloop()
