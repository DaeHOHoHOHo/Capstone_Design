import tkinter as tk
import re

def print_selected_word(event, text_box, sub_listbox, func_listbox):
    index = text_box.index(tk.CURRENT)
    line_number, column_number = map(int, index.split('.'))
    current_line = text_box.get(f"{line_number}.0", f"{line_number}.end")

    word_regex = r'\b\w+\b'
    words = re.findall(word_regex, current_line)

    clicked_word = None
    for word in words:
        start_index = current_line.find(word)
        end_index = start_index + len(word)
        if start_index <= column_number <= end_index:
            clicked_word = word
            break

    if clicked_word:
        sub_listbox.delete(0, tk.END)
        sub_listbox.insert(tk.END, clicked_word)

        # if clicked_word in func_listbox.get(0, tk.END):
        #     func_listbox_double_click(None, func_listbox, text_box)

