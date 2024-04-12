import tkinter as tk
from fileMenu import perform_save, perform_save_as
from tkinter import filedialog
from Diassembly import disassemble_file
from gptFunc import perform_gpt, gpt_open, get_completion
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
    file_menu_popup.add_command(label="전체 코드 보기 (F4)", command=lambda: print_decompiled_code(text_box))
    x = file_button.winfo_rootx()
    x = file_button.winfo_rootx()
    y = file_button.winfo_rooty() + file_button.winfo_height()
    file_menu_popup.post(x, y)

def compile_menu(app, compile_button, text_box, func_box):
    compile_menu_popup = tk.Menu(app, tearoff=0)
    compile_menu_popup.add_command(label="컴파일 (F5)", command=lambda: perform_decompile(text_box, func_box))
    x = compile_button.winfo_rootx()
    y = compile_button.winfo_rooty() + compile_button.winfo_height()
    compile_menu_popup.post(x, y)

def gpt_menu(app, gpt_button, gpttext, gpt_box):
    gpt_menu_popup = tk.Menu(app, tearoff=0)
    gpt_menu_popup.add_command(label="ChatGpt 연동 (Ctrl + F1)", command=lambda: perform_gpt(gpttext))
    gpt_menu_popup.add_command(label="함수 이름 변경", command=lambda: gpt_renaming(gpt_box))
    gpt_menu_popup.add_command(label="GPT 열기 (Ctrl + F2)", command=lambda: gpt_open())
    x = gpt_button.winfo_rootx()
    y = gpt_button.winfo_rooty() + gpt_button.winfo_height()
    gpt_menu_popup.post(x, y)



def perform_open(app, file_button, text_box):
    global file_opened, opened_file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        opened_file_path = file_path
        file_opened = True
        disassembled_content = disassemble_file(file_path)
        display_result(text_box, disassembled_content)

def display_result(text_box, content):
    if isinstance(text_box, tk.Listbox):
        text_box.delete(0, tk.END)
        for line in content.split('\n'):
            text_box.insert(tk.END, line)
    else:
        text_box.delete('1.0', tk.END)
        text_box.insert('1.0', content)


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

def func_listbox_double_click(event, func_listbox, text):
    selected_index = func_listbox.curselection()
    if selected_index:
        selected_item = func_listbox.get(selected_index)
        text.delete('1.0', tk.END)
        function_content = extract_function_content(decompiled_content, selected_item)
        text.insert(tk.END, function_content)

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


def print_decompiled_code(text_box):
    global decompiled_content
    if decompiled_content:
        display_result(text_box, decompiled_content)
    else:
        print("디컴파일된 코드가 없습니다.")



def gpt_renaming(text_box):
    global decompiled_content
    if decompiled_content:
        prompt = decompiled_content + "한국 사용자가 기능을 알아보기 쉽도록 함수명과 변수명으로 변환해"
        display_result(text_box, get_completion(prompt))
    else:
        print("디컴파일된 코드가 없습니다.")