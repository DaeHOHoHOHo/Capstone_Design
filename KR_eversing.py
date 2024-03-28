import tkinter as tk
from toolBarMenu import file_menu, compile_menu, func_listbox_double_click

app = tk.Tk()
app.geometry("1000x600")

# == 툴바 =================================================================================================
toolbar_frame = tk.Frame(app, bg="lightgrey")
toolbar_frame.pack(side=tk.TOP, fill=tk.X)
file_button = tk.Button(toolbar_frame, text="파일", padx=10, pady=5)
file_button.pack(side=tk.LEFT, padx=5, pady=5)
compile_button = tk.Button(toolbar_frame, text="컴파일러", padx=10, pady=5)
compile_button.pack(side=tk.LEFT, padx=5, pady=5)

file_button.bind("<Button-1>", lambda event, button=file_button: file_menu(app, button, listbox))
compile_button.bind("<Button-1>", lambda event, button=compile_button: compile_menu(app, button, listbox, func_listbox))
# == 툴바 =================================================================================================

paned_window = tk.PanedWindow(app, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(paned_window)
paned_window.add(left_frame)

right_paned_window = tk.PanedWindow(paned_window, orient=tk.VERTICAL)
paned_window.add(right_paned_window)

func_listbox = tk.Listbox(left_frame, selectmode=tk.SINGLE, height=30, width=30)
func_listbox.pack(fill=tk.BOTH, expand=True)

listbox = tk.Listbox(right_paned_window, selectmode=tk.SINGLE, height=20, width=60)
right_paned_window.add(listbox)

sub_listbox = tk.Listbox(right_paned_window, selectmode=tk.SINGLE, height=10, width=60)
right_paned_window.add(sub_listbox)

func_listbox.bind("<Double-1>", lambda event: func_listbox_double_click(event, func_listbox, listbox))

app.mainloop()
