import tkinter as tk
from tkinter import ttk
import threading
import speech_recognition as sr
import openai
from pyfiglet import Figlet

def start_listening():
    def listen():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            global text
            text = recognizer.recognize_google(audio)
            generate_completion(text)  # Generate completion using the recognized text
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error: {0}".format(e))

    thread = threading.Thread(target=listen)
    thread.start()

def generate_completion(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',  # GPT-3 model
        prompt=prompt,
        max_tokens=100  # Set the desired length of the completion
    )
    completion = response.choices[0].text.strip()
    chat_box.configure(state='normal')
    chat_box.insert(tk.END, completion + "\n")
    chat_box.configure(state='disabled')
    print(completion)
    
openai.api_key = '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'  # Replace with your OpenAI API key

root = tk.Tk()
root.title("Voice-to-Text")
root.geometry("700x800")
root.configure(bg='black')
fig = Figlet(font='big')
heading_text = fig.renderText("ZEUS")
heading_label = ttk.Label(root, text=heading_text.strip(), style="TLabel")
heading_label.pack()

# Create a themed style for the GUI
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=6, background='green', foreground='white')
style.configure("TLabel", font=("Helvetica", 14), background='black', foreground='green')

# Create a chatbox
chat_box = tk.Text(root, height=35, width=80, state='disabled', bg='black', fg='green', insertbackground='green')
chat_box.pack(pady=10)

# Create a button to start listening
listen_button = ttk.Button(root, text="Start Listening", command=start_listening, style="TButton")
listen_button.pack()

root.mainloop()
