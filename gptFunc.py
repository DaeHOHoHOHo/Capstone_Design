import tkinter as tk
from tkinter import scrolledtext, messagebox
import openai
from openai import OpenAI


gptLogin = False
client = OpenAI()


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content


def perform_gpt(gpttext):
    gpt_window = tk.Toplevel()
    gpt_window.geometry("400x150")
    gpt_window.title("GPT Function")

    label = tk.Label(gpt_window, text="ChatGPT API key 입력:")
    label.pack()

    input_entry = tk.Entry(gpt_window)
    input_entry.pack()

    def get_input():
        client.api_key = input_entry.get()
        try:
        #Make your OpenAI API request here
            user_input = "GPT API key : " + input_entry.get()
            sub = "*" * 40
            sub_input = user_input[:-40] + sub
            gpttext.set(sub_input)
            gpt_window.destroy()
            global gptLogin
            gptLogin = True
            response = client.completions.create(
                prompt="Hello world",
                model="gpt-3.5-turbo-instruct"
            )
        except openai.APIError as e:
        #Handle API error here, e.g. retry or log
            user_input = "OpenAI API returned an API Error"

            gpttext.set(user_input)
            gpt_window.destroy()

            print(f"OpenAI API returned an API Error: {e}")
            pass
        except openai.APIConnectionError as e:
        #Handle connection error here
            user_input = "OpenAI API returned an API Error"

            gpttext.set(user_input)
            gpt_window.destroy()

            print(f"Failed to connect to OpenAI API: {e}")
            pass
        except openai.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
            user_input = "OpenAI API returned an API Error"

            gpttext.set(user_input)
            gpt_window.destroy()
            
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass

    submit_button = tk.Button(gpt_window, text="입력", command=get_input)
    submit_button.pack()

    gpt_window.mainloop()

def gpt_open():
    global gptLogin
    if gptLogin:
        chat_window = tk.Toplevel()
        chat_window.geometry("400x400")
        chat_window.title("ChatGPT 대화")

        chat_text = scrolledtext.ScrolledText(chat_window, wrap=tk.WORD, state="disabled")
        chat_text.pack(fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(chat_window)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X)

        input_entry = tk.Entry(input_frame)
        input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def send_message(event=None):
            message = input_entry.get()
            chat_text.configure(state="normal")
            chat_text.insert(tk.END, "\n" + message + "\n\n", "user")
            chat_text.insert(tk.END, "\n", "space")
            input_entry.delete(0, tk.END)
            gpt_response = "yes"
            chat_text.insert(tk.END,  "\n" + gpt_response + "\n\n", "gpt")
            chat_text.insert(tk.END, "\n", "space")
            chat_text.configure(state="disabled")
            chat_text.window_create(tk.END, window=tk.Button(chat_text, text="Yes", command=lambda: gpt_reply("Yes")))
            chat_text.window_create(tk.END, window=tk.Button(chat_text, text="No", command=lambda: gpt_reply("No")))

        def gpt_reply(choice): # 버튼 클릭 시 동작 함수
            messagebox.showinfo("Choice", f"You chose: {choice}")

        input_entry.bind("<Return>", send_message)

        send_button = tk.Button(input_frame, text="전송", command=send_message)
        send_button.pack(side=tk.RIGHT)

        chat_text.tag_configure("user", background="lightblue", relief="ridge", wrap=tk.WORD, borderwidth=1, foreground="black")
        chat_text.tag_configure("gpt", background="lightgreen", relief="ridge", wrap=tk.WORD, borderwidth=1, foreground="black")
        chat_text.tag_configure("space", spacing2=10)

    else:
        print("ChatGPT에 로그인되어 있지 않습니다.")
