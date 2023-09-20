import tkinter as tk
from tkinter import filedialog
import subprocess

file_path = ""
text = ""
results = ""

def main_window():
    root = tk.Tk()
    root.title("Repeated Phrases Analyzer")

    open_file_button = tk.Button(root, text="Open File", command=open_file)
    open_file_button.grid(row=0, column=0, padx=10, pady=10)

    save_file_button = tk.Button(root, text="Save Results", command=save_file)
    save_file_button.grid(row=0, column=1, padx=10, pady=10)

    min_words_label = tk.Label(root, text="Minimum number of words:")
    min_words_label.grid(row=1, column=0, padx=10, pady=10)

    min_words_entry = tk.Entry(root)
    min_words_entry.grid(row=1, column=1, padx=10, pady=10)

    max_words_label = tk.Label(root, text="Maximum number of words:")
    max_words_label.grid(row=2, column=0, padx=10, pady=10)

    max_words_entry = tk.Entry(root)
    max_words_entry.grid(row=2, column=1, padx=10, pady=10)
    max_words_entry.insert(0, "7")

    analyze_button = tk.Button(root, text="Analyze", command=lambda: analyze_text(text, int(min_words_entry.get()), int(max_words_entry.get())))
    analyze_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

    results_text = tk.Text(root, height=20, width=50)
    results_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    scroll_bar = tk.Scrollbar(root, command=results_text.yview)
    scroll_bar.grid(row=4, column=2, sticky="nsew")
    results_text["yscrollcommand"] = scroll_bar.set

    save_button = tk.Button(root, text="Save Results", command=save_results)
    save_button.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

    root.mainloop()

def open_file():
    global file_path, text
    file_path = filedialog.askopenfilename()
    with open(file_path, "r") as file:
        text = file.read()

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    with open(file_path, "w") as file:
        file.write(results_text.get("1.0", tk.END))

def save_results():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    with open(file_path, "w") as file:
        file.write(results_text.get("1.0", tk.END))
