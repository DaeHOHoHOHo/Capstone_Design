import tkinter as tk
from fileMenu import perform_save, perform_save_as
from tkinter import filedialog
from Diassembly import disassemble_file
import subprocess
import os
import re

file_opened = False
opened_file_path = None
decompiled_content = "" 

def file_menu(app, file_button, text_box):
    file_menu_popup = tk.Menu(app, tearoff=0)
    file_menu_popup.add_command(label="불러오기", command=lambda: perform_open(app, file_button, text_box))
    file_menu_popup.add_command(label="저장", command=perform_save)
    file_menu_popup.add_command(label="다른 이름으로 저장", command=perform_save_as)
    x = file_button.winfo_rootx()
    y = file_button.winfo_rooty() + file_button.winfo_height()
    file_menu_popup.post(x, y)

def compile_menu(app, compile_button, text_box, func_box):
    compile_menu_popup = tk.Menu(app, tearoff=0)
    compile_menu_popup.add_command(label="컴파일", command=lambda: perform_decompile(text_box, func_box))
    x = compile_button.winfo_rootx()
    y = compile_button.winfo_rooty() + compile_button.winfo_height()
    compile_menu_popup.post(x, y)

def perform_open(app, file_button, text_box):
    global file_opened, opened_file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        opened_file_path = file_path
        file_opened = True
        disassembled_content = disassemble_file(file_path)
        display_result(text_box, disassembled_content)

def display_result(code_listbox, content):
    code_listbox.delete(0, tk.END)
    content_lines = content.split('\n')
    max_lengths = [0] * 3
    formatted_lines = []
    for line in content_lines:
        parts = line.split('\t')
        for i, part in enumerate(parts):
            max_lengths[i] = max(max_lengths[i], len(part))
        formatted_lines.append(parts)
    for parts in formatted_lines:
        formatted_line = ''
        for i, part in enumerate(parts):
            formatted_part = part.ljust(max_lengths[i] + 2)
            if i > 0:
                formatted_line += '          '
            formatted_line += formatted_part
        code_listbox.insert(tk.END, formatted_line.rstrip())

def perform_decompile(text_box, func_box):
    global file_opened, opened_file_path, decompiled_content 
    if file_opened:
        os.chdir("RetDec/bin")
        command2 = f'retdec-decompiler "{opened_file_path}"'
        try:
            subprocess.run(command2, shell=True, check=True)
            print("Decompilation completed successfully.")
            decompiled_file_path = opened_file_path + '.c'
            with open(decompiled_file_path, 'r') as f:
                decompiled_content = f.read()

            func_prototypes = extract_func_prototypes(decompiled_content)
            display_result(func_box, func_prototypes)

            display_result(text_box, decompiled_content)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    else:
        print("파일을 열어주세요.")

def extract_func_prototypes(content):
    func_prototypes = []
    within_comment = False
    for line in content.split('\n'):
        if "// ------------------- Function Prototypes --------------------" in line:
            within_comment = True
        elif "// --------------------- Global Variables ---------------------" in line:
            within_comment = False
            break
        elif within_comment and line.strip():
            match = re.search(r'\bfunction_\w+\b', line)
            if match:
                func_name = match.group()
                func_prototypes.append(func_name)
    return '\n'.join(func_prototypes)

def func_listbox_double_click(event, func_listbox, listbox):
    selected_index = func_listbox.curselection()
    if selected_index:
        selected_item = func_listbox.get(selected_index)
        listbox.delete(0, tk.END)
        function_content = extract_function_content(decompiled_content, selected_item)
        listbox.insert(tk.END, function_content)

def extract_function_content(decompiled_content, selected_item):
    start_marker = "// ------------------------ Functions -------------------------"
    end_marker = "// --------------------- Meta-Information ---------------------"
    
    start_index = decompiled_content.find(start_marker)
    if start_index == -1:
        return "Start marker not found"

    end_index = decompiled_content.find(end_marker)
    if end_index == -1:
        return "End marker not found"

    item_marker = "// Address range: 0x" + selected_item.split('_')[1]
    item_index = decompiled_content.find(item_marker, start_index, end_index)
    if item_index == -1:
        return "Function not found"

    content_start_index = decompiled_content.find('\n', item_index) + 1

    next_marker_index = decompiled_content.find("// Address range", content_start_index, end_index)
    if next_marker_index != -1:
        function_content = decompiled_content[content_start_index:next_marker_index].strip()
    else:
        function_content = decompiled_content[content_start_index:end_index].strip()

    return function_content










