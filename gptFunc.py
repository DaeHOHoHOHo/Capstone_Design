import tkinter as tk

def perform_gpt(gpttext):
    gpt_window = tk.Toplevel()
    gpt_window.geometry("400x150")
    gpt_window.title("GPT Function")

    label = tk.Label(gpt_window, text="ChatGPT API key 입력:")
    label.pack()

    input_entry = tk.Entry(gpt_window)
    input_entry.pack()

    def get_input():
        user_input = "GPT API key : " + input_entry.get()
        gpttext.set(user_input)
        gpt_window.destroy()

    submit_button = tk.Button(gpt_window, text="입력", command=get_input)
    submit_button.pack()

    gpt_window.mainloop()
