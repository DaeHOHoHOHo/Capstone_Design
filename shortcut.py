import tkinter as tk
from toolBarMenu import perform_decompile, print_decompiled_code, perform_gpt

def f5_pressed(event, app, text_box, func_box):
    perform_decompile(text_box, func_box)

def f4_pressed(event, app, text_box):
    print_decompiled_code(text_box)

def ctrl_f1_pressed(event, gpttext):
    perform_gpt(gpttext)

def set_shortcut(app, text_box, func_box, gpttext):
    app.bind("<KeyPress-F5>", lambda event: f5_pressed(event, app, text_box, func_box))
    app.bind("<KeyPress-F4>", lambda event: f4_pressed(event, app, text_box))
    app.bind("<Control-KeyPress-F1>", lambda event: ctrl_f1_pressed(event, gpttext))
