import tkinter as tk

def print_selected_word(event, text_box, sub_listbox):
    index = text_box.index(tk.CURRENT)
    line_number, column_number = map(int, index.split('.'))
    current_line = text_box.get(f"{line_number}.0", f"{line_number}.end")
    word_start = current_line.rfind(" ", 0, column_number) + 1
    word_end = current_line.find(" ", column_number)
    if word_end == -1:
        word_end = len(current_line)
    selected_word = current_line[word_start:word_end]
    sub_listbox.delete(0, tk.END)
    sub_listbox.insert(tk.END, selected_word)
