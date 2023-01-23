# TODO: create cutom user interface
import tkinter as tk
from tkinter import filedialog
from wordcloud import WordCloud
import numpy as np
from PIL import ImageTk, Image

def show_wordcloud():

    text = 'Gegenüberstellung der Demand und Supply Seiten (Stellenanzeigen und LinkedIn-Profile), es konnte festgestellt werden, dass obwohl Big Data und Data Analytics in der Literatur für Controller-Jobs als wichtig erachtet werden, diese Skills in der Praxis noch nicht relevant sind. Vielmehr werden von Controllern "traditional controlling practices" verlangt, während Data Analytics von anderen Stellen ausgeführt werden.'
    wordcloud = WordCloud().generate(text)
    wordcloud.to_file("wordcloud.png")
    from PIL import Image
    img = Image.open("wordcloud.png")
    img = img.resize((400, 300), resample=Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(20, 20, anchor=tk.NW, image=img)


root = tk.Tk()
root.title("Wordcloud Viewer")

frame = tk.Frame(root)
frame.pack()



canvas = tk.Canvas(frame, width=420, height=320)
canvas.pack()

root.mainloop()
