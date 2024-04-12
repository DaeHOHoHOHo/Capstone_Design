import tkinter as tk
from toolBarMenu import file_menu, compile_menu, gpt_menu, func_listbox_double_click
from textDoubleClick import print_selected_word
from shortcut import set_shortcut

app = tk.Tk()
app.geometry("1000x600")

# == 툴바 =================================================================================================
toolbar_frame = tk.Frame(app, bg="lightgrey")
toolbar_frame.pack(side=tk.TOP, fill=tk.X)
file_button = tk.Button(toolbar_frame, text="파일", padx=10, pady=5)
file_button.pack(side=tk.LEFT, padx=5, pady=5)
compile_button = tk.Button(toolbar_frame, text="컴파일러", padx=10, pady=5)
compile_button.pack(side=tk.LEFT, padx=5, pady=5)
gpt_button = tk.Button(toolbar_frame, text="GPT", padx=10, pady=5)
gpt_button.pack(side=tk.LEFT, padx=5, pady=5)

gpttext = tk.StringVar()
gpt_text_label = tk.Label(toolbar_frame, textvariable=gpttext, bg="lightgrey")
gpt_text_label.pack(side=tk.LEFT, padx=5, pady=5)

file_button.bind("<Button-1>", lambda event, button=file_button: file_menu(app, button, textbox))
compile_button.bind("<Button-1>", lambda event, button=compile_button: compile_menu(app, button, textbox, func_listbox))
gpt_button.bind("<Button-1>", lambda event, button=gpt_button: gpt_menu(app, button, gpttext, gpt_textbox))
# == 툴바 =================================================================================================

paned_window = tk.PanedWindow(app, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(paned_window)
paned_window.add(left_frame)

right_paned_window = tk.PanedWindow(paned_window, orient=tk.VERTICAL)
paned_window.add(right_paned_window)

func_listbox = tk.Listbox(left_frame, selectmode=tk.SINGLE, height=30, width=30)
func_listbox.pack(fill=tk.BOTH, expand=True)

textbox = tk.Text(right_paned_window, wrap="word", height=20, width=60)
right_paned_window.add(textbox)

sub_textbox_paned_window = tk.PanedWindow(right_paned_window, orient=tk.HORIZONTAL)
right_paned_window.add(sub_textbox_paned_window)

sub_listbox = tk.Listbox(sub_textbox_paned_window, selectmode=tk.SINGLE, height=10, width=60)
sub_textbox_paned_window.add(sub_listbox)


gpt_textbox = tk.Text(sub_textbox_paned_window, wrap="word", height=20, width=60)
sub_textbox_paned_window.add(gpt_textbox)


func_listbox.bind("<Double-1>", lambda event: func_listbox_double_click(event, func_listbox, textbox))

textbox.bind("<Double-1>", lambda event: print_selected_word(event, textbox, sub_listbox, func_listbox))

set_shortcut(app, textbox, func_listbox, gpttext)

app.mainloop()
