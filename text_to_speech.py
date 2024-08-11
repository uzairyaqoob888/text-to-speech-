import pyttsx3
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from gtts import gTTS
import os

class TextToSpeechApp:
    def __init__(self, root):
        self.engine = pyttsx3.init()
        self.root = root
        self.root.title("Text to Speech")

        # Create a label for text input
        self.label = tk.Label(root, text="Enter text:")
        self.label.pack(pady=10)

        # Create a text entry widget
        self.text_entry = scrolledtext.ScrolledText(root, width=50, height=10)
        self.text_entry.pack(pady=10)

        # Create a speak button
        self.speak_button = tk.Button(root, text="Speak", command=self.speak_text)
        self.speak_button.pack(pady=10)

        # Create a download button
        self.download_button = tk.Button(root, text="Download Voice", command=self.download_voice)
        self.download_button.pack(pady=10)

        # Create a quit button
        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=10)

        # Create volume control
        self.volume_label = tk.Label(root, text="Volume:")
        self.volume_label.pack(pady=5)
        self.volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_volume)
        self.volume_scale.set(90)  # Set default volume level
        self.volume_scale.pack(pady=5)

        # Create rate control
        self.rate_label = tk.Label(root, text="Rate:")
        self.rate_label.pack(pady=5)
        self.rate_scale = tk.Scale(root, from_=50, to=300, orient=tk.HORIZONTAL, command=self.update_rate)
        self.rate_scale.set(120)  # Set default rate level to 120
        self.rate_scale.pack(pady=5)

        # Initialize StringVar for voice selection
        self.voice_var = tk.StringVar(root)
        self.voice_var.set("Select Voice")  # Default value

        # Create voice selection label
        self.voice_label = tk.Label(root, text="Voice:")
        self.voice_label.pack(pady=5)

        # Populate voice options and map them
        self.voice_map = self.get_voice_map()
        self.voice_options = list(self.voice_map.keys())

        # Create voice selection menu
        self.voice_menu = tk.OptionMenu(root, self.voice_var, *self.voice_options)
        self.voice_menu.pack(pady=5)

        # Bind Enter key to speak_text function
        self.root.bind('<Return>', self.on_enter_pressed)

    def get_voice_map(self):
        voices = self.engine.getProperty('voices')
        voice_map = {}
        for voice in voices:
            print(f"Voice ID: {voice.id}, Name: {voice.name}")
            if "David" in voice.name or "Zira" in voice.name:
                voice_map[voice.name] = voice.id
        return voice_map

    def update_volume(self, value):
        volume = int(value) / 100.0
        self.engine.setProperty('volume', volume)

    def update_rate(self, value):
        rate = int(value)
        self.engine.setProperty('rate', rate)

    def speak_text(self, event=None):
        text = self.text_entry.get("1.0", tk.END).strip()
        if text:
            selected_voice_name = self.voice_var.get()
            voice_id = self.voice_map.get(selected_voice_name)
            if voice_id:
                self.engine.setProperty('voice', voice_id)
            else:
                print(f"Voice '{selected_voice_name}' not found.")
            self.engine.say(text)
            self.engine.runAndWait()

    def download_voice(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if text:
            # Determine default file name based on current voice
            selected_voice_name = self.voice_var.get()
            if "David" in selected_voice_name:
                default_filename = "mspeech.mp3"
            elif "Zira" in selected_voice_name:
                default_filename = "fmspeech.mp3"
            else:
                # Fallback default file name if no voice selected
                default_filename = "speech.mp3"

            # Open file dialog to get the save path with default filename
            file_path = filedialog.asksaveasfilename(
                defaultextension=".mp3",
                filetypes=[("MP3 files", "*.mp3")],
                initialfile=default_filename
            )
            if file_path:
                # Save the MP3 file
                tts = gTTS(text=text, lang='en')
                tts.save(file_path)
                print(f"Downloaded as {file_path}")

    def on_enter_pressed(self, event):
        self.speak_text()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
