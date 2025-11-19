import random
import pyttsx3
import webbrowser
import datetime
import wikipedia
import google.generativeai as genai
import os
import customtkinter as ctk
import threading

genai.configure(api_key="your api")
model = genai.GenerativeModel("gemini-2.0-flash")

def Speak(Text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voices', voices[0].id)
    engine.setProperty('rate',170)
    engine.say(Text)
    engine.runAndWait()


def save_chat_history(user_text, bot_reply):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] USER: {user_text}\n")
        file.write(f"[{timestamp}] BOT : {bot_reply}\n\n")


def save_knowledge(key, value):
    with open("knowledge.txt", "a", encoding="utf-8") as f:
        f.write(f"{key}:{value}\n")

class JarvisBrain:
    def __init__(self):

        # Your original response database (censored for safety)
        self.responses = {
            'hi': ['Hello! Sir, I am ready to assist you.', 'Hi sir, I am ready to assist you.', 'Hello Sir, I am ready to assist you.'],
            'greetings': ['Hello! Sir, I am ready to assist you.', 'Hi sir, I am ready to assist you.', 'Hello Sir, I am ready to assist you.'],
            'my friends name' : ['Vikas Kumar, Kushagra', 'Pradeep'],
            'your owner' : ['Abhii Abhishek', 'Bhanu Pratap Singh'],
            'how are you' : ['I am fine, thank you for asking'],
            'hello' : ['Hello Sir, I am ready to assist you.'],
            'thank you jarvis': ['Welcome Sir!'],
            'introduce' : ['I am a computer program chatbot AI that can understand and respond to human speech.I was created by Abhii AbhishIek . I am named after the character Jarvis from the Iron Man movies.'],
            'who was created you':['I was created by Abhii Abhishek at NGF College, Palwal.'],
            'results' : ['Anything else Sir?'],
            'default': ['I am not sure how to respond to that.']
        }

    def get_predefined_response(self, text):
        for key in self.responses:
            if key in text:
                return random.choice(self.responses[key])
        return None

    def process_input(self, user_input):
        text = user_input.lower()

        # predefined response
        predefined = self.get_predefined_response(text)
        if predefined:
            return predefined

        # open websites
        if "open youtube" in text:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube Sir."
        if "open google" in text:
            webbrowser.open("https://www.google.com")
            return "Opening Google Sir."
        if "play music" in text or "play song" in text or "favourite song" in text:
            webbrowser.open("https://www.youtube.com/watch?v=r03GO2AlNUo&t=26s")
            return "Playing your favourite song Sir."
        if "open amazon" in text:
            webbrowser.open("https://www.amazon.com")
            return "Opening Amazon Sir."
        if "wikipedia" in text:
            Speak("Searching Wikipedia...")
            query = user_input.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            Speak("According to Wikipedia")
            return result
        
        # fallback => Gemini AI
        try:
            short_prompt = f"You are Chatbox who's named Jarvis & Answer in 1-2 short lines only, no extra details, no paragraphs. User asked: {user_input}"
            response = model.generate_content(short_prompt)
            return response.text
        except:
            return "Sorry Sir, I am unable to connect to Gemini."


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Jarvis Assistant Chat")
app.geometry("460x640")

ai=JarvisBrain()

chat_frame = ctk.CTkScrollableFrame(app, width=430, height=520, fg_color="#111111")
chat_frame.pack(pady=10, padx=10)

def smooth_scroll():
    for i in range(5):
        app.after(i * 25, lambda: chat_frame._parent_canvas.yview_moveto(1.0))


def add_bubble(message, sender="user"):
    if sender == "user":
        bubble_color = "#25D366"
        anchor_pos = "e"
        text_color = "black"
    else:
        bubble_color = "#2F2F2F"
        anchor_pos = "w"
        text_color = "white"

    bubble = ctk.CTkLabel(chat_frame, text=message, fg_color=bubble_color,
                          corner_radius=18, justify="left", text_color=text_color,
                          wraplength=260, padx=12, pady=8)
    bubble.pack(anchor=anchor_pos, pady=6, padx=6)

    smooth_scroll()

def bot_reply_thread(user_msg):
    reply = ai.process_input(user_msg)
    add_bubble(reply, "bot")
    Speak(reply)
    save_chat_history(user_msg, reply)

bottom_frame = ctk.CTkFrame(app, fg_color="#0D0D0D", corner_radius=0)
bottom_frame.pack(fill="x", padx=10, pady=5)

entry = ctk.CTkEntry(bottom_frame, placeholder_text="Type your message...", width=315,
                     corner_radius=22, fg_color="#222222", text_color="white",
                     border_width=2, border_color="#25D366")
entry.pack(side="left", padx=5, pady=8)

def send_message(event=None):
    user_msg = entry.get().strip()
    if user_msg:
        add_bubble(user_msg, "user")
        entry.delete(0, ctk.END)

    
    if user_msg.lower() in ["exit", "quit", "bye", "close", "stop"]:
            add_bubble("Goodbye Sir, shutting down...", "bot")
            Speak("Goodbye Sir, shutting down")
            app.after(1000, app.destroy)  # closes GUI smoothly
            return

    threading.Thread(target=bot_reply_thread, args=(user_msg,), daemon=True).start()

# bind Enter to the now-defined handler
entry.bind("<Return>", send_message)

send_btn = ctk.CTkButton(bottom_frame, text="Send", width=80, corner_radius=22,
                         fg_color="#25D366", text_color="black",
                         command=send_message)
send_btn.pack(side="right", padx=5)

app.mainloop()