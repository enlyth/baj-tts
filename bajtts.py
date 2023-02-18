import os
from TTS.utils.synthesizer import Synthesizer
from tkinter import Button, Entry, Label, StringVar, Text, messagebox, IntVar, Checkbutton
import tkinter as tk
import time
import pygame
import json

pygame.mixer.init()

base_model_path = ".\\models\\"
config_path = base_model_path + "config.json"
sample_rate = 22050
synthesizers: dict[str, Synthesizer] = {}
voices = {}
with open("models.json", "r") as f:
    models = json.load(f)
    for voice in models["voices"]:
        voices[voice["name"]] = voice


window = tk.Tk()

window.title("BajTTS")
window.geometry("640x480")

model_label = Label(text="Select model:")
model_label.pack()

model_var = StringVar(window)
model_var.set("xqc")
model_dropdown = tk.OptionMenu(window, model_var, *voices.keys())
model_dropdown.pack()

text_label = Label(text="Enter text:")
text_label.pack()

text_input = Text(
    window,
    height=10,
    width=50,
    wrap=tk.WORD,
    borderwidth=2,
    relief=tk.GROOVE,
    padx=5,
    pady=5,
)

text_input.pack()

play_output_var = IntVar()
play_output_var.set(1)
play_output_checkbox = Checkbutton(window, text="Play output", variable=play_output_var)
play_output_checkbox.pack()

use_cuda_var = IntVar()
use_cuda_var.set(1)
use_cuda_checkbox = Checkbutton(window, text="Use CUDA", variable=use_cuda_var)
use_cuda_checkbox.pack()


output_label = Label(text="Output directory:")
output_label.pack()

output_input = Entry(window)
output_input.insert(0, ".\\output\\")
output_input.pack()


def synthesize(text: str, voice: str, output_dir: str):
    global synthesizer

    if not os.path.exists(output_dir):
        messagebox.showerror("Error", "Output directory does not exist.")
        return

    model_file = base_model_path + voices[voice]["model"]
    if not os.path.exists(model_file):
        messagebox.showerror("Error", f"Model file {voices[voice]['model']} does not exist.")
        return

    if not os.path.exists(config_path):
        messagebox.showerror("Error", f"Config file {config_path} does not exist.")
        return

    print(voices[voice]["model"])
    if voice not in synthesizers:
        synthesizers[voice] = Synthesizer(
            tts_config_path=config_path,
            tts_checkpoint=model_file,
            use_cuda=bool(use_cuda_var.get()),
        )
    wav = synthesizers[voice].tts(text)

    output_filename = f"{int(time.time())}_{voice}.wav"
    path = os.path.join(output_dir, output_filename)
    synthesizers[voice].save_wav(wav, path)

    if bool(play_output_var.get()):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()


def on_click():
    text = text_input.get("1.0", "end")
    output_dir = output_input.get()
    voice = model_var.get()
    synthesize(text, voice, output_dir)


window.bind("<Return>", lambda _: on_click())

synthesize_button = Button(window, text="Synthesize", command=on_click)
synthesize_button.pack()

window.mainloop()
