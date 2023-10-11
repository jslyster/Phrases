# import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox
import base64
import webbrowser
import os

import docs
import phrases


class PhrasesUI:
    # ERROR CONSTANTS

    ERR_LETTER_INVALID = 0
    ERR_MAX_GREATER_THAN_MIN = 1
    ERR_TOO_MANY_NUMBERS = 2
    ERR_NUMBER_TOO_LOW = 3
    ERR_NUMBER_TOO_HIGH = 4
    ERR_UNABLE_TO_OPEN_FILE = 5

    ERR_STR = ["Only numbers are permitted",
                "Minimum cannot be greater than maximum",
                "Too many numbers entered",
                "Number is too low",
               "Number is too high",
                "Unable to open file. Try again."]

    def __init__(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.title("Phrases")
        self.root.geometry('800x600')
        self.root.resizable(width=False, height=False)
        self.saved_flag = True
        self.minimum = 2
        self.maximum = 7
        self.file_path = ''
        self.results_dict = {}
        self.text = ''
        self.min = None
        self.max = None
        self.current_min = IntVar()
        self.current_max = IntVar()

        self.jsl_image = PhotoImage(data=base64.b64decode(docs.jon_image))

        self.file_name_label = None
        self.file_name = None
        self.reanalyze_file = None
        self.min_max_frame = None
        self.min_label = None
        self.min = None
        self.max_label = None
        self.max = None
        self.err_label = None
        self.results_frame = None
        self.results_textbox = None

        self._create_menubar()
        self.display_elements()

        self.root.mainloop()

    def _create_menubar(self):
        # create the menubar
        self.menubar = Menu(self.root)
        self.root.configure(menu=self.menubar)

        # File menu
        self.fileMenu = Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="Open Text File", command=self.open_text_file)
        self.fileMenu.add_command(label="Open ODT File", command=self.open_odt_file)
        self.fileMenu.add_command(label="Open DOCX File", command=self.open_docx_file)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Save Results in text file", command=self.save_results_text_file, state='disabled')
        self.fileMenu.add_command(label="Save Results in CSV file", command=self.save_results_csv_file, state='disabled')
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.on_close)

        # Help menu
        self.helpMenu = Menu(self.menubar)
        self.menubar.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="View Documentation", command=self.view_documentation)
        self.helpMenu.add_command(label="About Phrases", command=self.about_phrases)

    def display_elements(self):
        self.file_name_label = Label(self.root, text="File:")
        self.file_name = Entry(self.root, width=50)
        self.reanalyze_file = Button(self.root, text="Re-analyze File", width=30, state='disabled', command=self.display_results)
        self.file_name_label.grid(row=0, column=0, pady=10)
        self.file_name.grid(row=0, column=1, pady=10, sticky="W")
        self.reanalyze_file.grid(row=0, column=2, pady=10, padx=10, sticky="NEWS")

        self.file_name.config(disabledbackground='white', disabledforeground='black', state='disabled')

        self.min_max_frame = LabelFrame(self.root, text="Set Minimum and Maximum Words For Repeated Phrases Search")
        self.min_max_frame.grid(row=1, column=0, columnspan=3, sticky="news", padx=(5, 5), pady=(10,10))

        self.min_label = Label(self.min_max_frame, text="Minimum number of words:")
        self.min = Scale(self.min_max_frame, from_=self.minimum, to=self.maximum - 1, orient='horizontal', variable=self.current_min, command=self.min_validation)

        self.max_label = Label(self.min_max_frame, text="Maximum number:")
        self.max = Scale(self.min_max_frame, from_=self.minimum + 1, to=self.maximum, orient='horizontal', variable=self.current_max, command=self.max_validation)
        self.max.set(self.maximum)

        self.err_label = Label(self.min_max_frame, width=40, height=2, foreground="#810000")

        self.min_label.grid(row=0, column=0, sticky="S", padx=(5, 5), pady=(10,5))
        self.min.grid(row=1, column=0, sticky="N", padx=(5, 5), pady=(0,5))
        self.max_label.grid(row=0, column=1, sticky="S", padx=(5, 5), pady=(10,5))
        self.max.grid(row=1, column=1, sticky="N", padx=(5, 5), pady=(0,5))
        self.err_label.grid(row=0, column=2, columnspan=2, rowspan=2, sticky="NEWS", padx=(5,5), pady=(10,5))
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.min_max_frame.grid_columnconfigure(2, weight=1)

        self.results_frame = LabelFrame(self.root, text="Results")
        self.results_frame.grid(row=2, column=0, columnspan=3, sticky="news", padx=(5, 5), pady=(10,10))

        self.results_textbox = scrolledtext.ScrolledText(self.results_frame)
        self.results_textbox.pack(side="left", fill="both", expand=True)
        self.results_textbox.bind("<Key>", lambda e: "break")

    def min_validation(self, e):
        minimum = self.current_min.get()
        maximum = self.current_max.get()
        self.enable_reanalyze_button()
        self.show_err(None)

        if not (minimum < maximum):
            self.current_min.set(maximum - 1)
            self.show_err(1)

    def max_validation(self, e):
        minimum = self.current_min.get()
        maximum = self.current_max.get()
        self.enable_reanalyze_button()
        self.show_err(None)

        if not (minimum < maximum):
            self.current_max.set(minimum + 1)
            self.show_err(1)

    def show_err(self, err_code):
        if err_code is None:
            self.err_label['text'] = ""
            self.err_label['relief'] = "flat"
            return

        if err_code >= len(self.ERR_STR):
            return

        self.err_label['text'] = self.ERR_STR[err_code]
        self.err_label['borderwidth'] = 2
        self.err_label['relief'] = "groove"

    def open_text_file(self):
        self.text = ''
        file_types = [
            ('text files', '*.txt')
        ]
        self.file_path = filedialog.askopenfilename(title='Open a text file', filetypes=file_types)

        if self.file_path:
            self.text = phrases.open_file(self.file_path, "text")
        # print(text)
        if not self.text:
            return

        self.display_results()

    def open_odt_file(self):
        self.text = ''
        file_types = [
            ('ODT files', '*.odt')
        ]
        self.file_path = filedialog.askopenfilename(title='Open an OpenDocument file', filetypes=file_types)


        if self.file_path:
            count = 0
            self.text = False
            while count < 3 and not self.text:
                self.text = phrases.open_file(self.file_path, "odt")
                count += 1


        if not self.text:
            self.show_err(self.ERR_UNABLE_TO_OPEN_FILE)
            return

        self.display_results()

    def open_docx_file(self):
        self.text = ''
        file_types = [
            ('Word (DOCX) files', '*.docx')
        ]

        self.file_path = filedialog.askopenfilename(title='Open a Word file', filetypes=file_types)

        if self.file_path:
            self.text = phrases.open_file(self.file_path, "docx")

        if not self.text:
            return

        self.display_results()

    def display_results(self):
        self.results_dict = {}

        self.show_err(None)

        self.saved_flag = False
        self.mod_window_title()
        self.show_file_name()
        self.results_textbox.delete(0.0, END)

        minimum = self.current_min.get()
        maximum = self.current_max.get()

        self.results_dict = phrases.analyze_text(self.text, minimum, maximum)
        results_text = ""
        for item, value in self.results_dict.items():
            results_text += item + ": " + str(value) + "\n"
        self.results_textbox.insert(0.0, results_text)

        self.reanalyze_file.config(state='disabled')
        self.fileMenu.entryconfig("Save Results in text file", state='normal')
        self.fileMenu.entryconfig("Save Results in CSV file", state='normal')

    def enable_reanalyze_button(self):
        if self.text:
            self.reanalyze_file.config(state='normal')

    def mod_window_title(self):
        title_string = ''
        if self.file_path:
            if not self.saved_flag:
                title_string = "*"
            else:
                title_string = ""
        title_string += "Phrases"

        if self.file_path:
            title_string +=": " + self.file_path

        self.root.title(title_string)

    def show_file_name(self):
        path, file = os.path.split(self.file_path)
        self.file_name.config(state='normal')
        self.file_name.delete(0, END)
        self.file_name.insert(0, file)
        self.file_name.config(state='disabled')

    def save_results_text_file(self):
        file_types = [
            ('Text file', '*.txt')
        ]
        file_path = filedialog.asksaveasfilename(filetypes=file_types)
        if file_path:
            phrases.save_results_as_text(file_path, self.results_dict)
            self.saved_flag = True
            self.mod_window_title()

    def save_results_csv_file(self):
        file_types = [
            ('CSV file', '*.csv')
        ]
        file_path = filedialog.asksaveasfilename(filetypes=file_types)
        if file_path:
            phrases.save_results_as_csv(file_path, self.results_dict)
            self.saved_flag = True
            self.mod_window_title()

    def on_close(self):
        if not self.saved_flag:
            if messagebox.askokcancel("Quit", "You haven't saved your results yet. Are you sure you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()

    def exit_program(self):
        pass

    def view_documentation(self):
        doc_win = Toplevel()
        doc_win.title("Phrases")
        doc_win.geometry('800x600')
        doc_win.resizable(width=False, height=False)

        doc_view = scrolledtext.ScrolledText(doc_win, wrap='word')

        header_len = len(docs.doc_header)
        header_len = "1." + str(header_len)

        doc_view.insert("1.0", docs.doc_header)
        doc_view.insert(END, '\n\n')
        # doc_view.config(font=('Arial', 12, 'normal'))
        doc_view.insert(END, docs.doc_text)

        doc_view.tag_add('header', '1.0', header_len)
        doc_view.tag_configure('header', font='helvetica 14 bold')

        doc_view.pack(fill="both", expand=True, padx=(5,5), pady=(5,5))
        doc_view.bind("<Key>", lambda e: "break")

        ok_button = Button(doc_win, text="OK", width=10, command=doc_win.destroy)
        ok_button.pack(side=RIGHT, padx=(5,5), pady=(5,5))

        doc_win.mainloop()

    def about_phrases(self):
        about_win = Toplevel()
        about_win.title("About Phrases")
        # about_win.geometry("700x300")
        about_win.resizable(width=False, height=False)

        jsl_label = Label(about_win, image=self.jsl_image, anchor="n", justify=LEFT)
        jsl_label.grid(row=0, column=0, sticky="nw", padx=(5,0), pady=(5,0))

        jsl_bio_label = Label(about_win, text=docs.jon_bio, wraplength=500, anchor="n", justify=LEFT, padx=5, pady=5, border=True, borderwidth=5, relief=GROOVE)
        jsl_bio_label.grid(row=0, column=1, sticky="news", padx=(5,5), pady=(5,0))

        btn_web = Button(about_win, text="Author website", width="50", command=self.author_website)
        btn_web.grid(row=2, column=0, columnspan=2, sticky="W", padx=(5,5), pady=(5,5))

        btn_ok = Button(about_win, text="OK", width="10", command=about_win.destroy)
        btn_ok.grid(row=2, column=0, columnspan=2, sticky="E", padx=(5,5), pady=(5,5))

    def author_website(self):
        webbrowser.open_new("https://jslyster.com/")

def run_phrases():
    PhrasesUI()
