import tkinter as tk
import csv
import random
import os
from PIL import Image, ImageTk

# Kortets størrelse i modelkoordinater (billedets pixels)
KORT_B, KORT_H = 488, 650

# set cwd to the directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

def _from_rgb(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

class By:
    def __init__(self, navn, x, y, indbyggertal, canvas):
        self.navn = navn
        #Koordinaterne divideres med 2, fordi billedets opløsning er halveret, for bedre at kunne være på skærmen
        self.x = int(x)//2
        self.y = int(y)//2
        self.indbyggertal = int(indbyggertal)

        self.canvas = canvas
        self.canvas_item = canvas.create_oval(0, 0, 0, 0)
        self.place()

    def place(self):
        # x og y er modelkoordinater; her omregnes de til skærmen
        k = self.canvas.skala
        self.canvas.coords(self.canvas_item, (self.x-3)*k, (self.y-3)*k, (self.x+3)*k, (self.y+3)*k)

    def change_color(self, s):
        self.canvas.itemconfig(self.canvas_item, fill=s)
        

class Distributionscenter:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas

        #Giv centeret en tilfældig farve
        r = random.randint(0,255)
        g= random.randint(0,255)
        b = random.randint(0,255)
        col = _from_rgb(r,g,b)
        self.farve = col
        self.byer = []

        self.canvas_item = self.canvas.create_rectangle(0, 0, 0, 0, fill=col, outline='black')
        self.place()

    def place(self):
        k = self.canvas.skala
        self.canvas.coords(self.canvas_item, (self.x-4)*k, (self.y-4)*k, (self.x+4)*k, (self.y+4)*k)

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.place()

    def get_wcss(self):
        # Denne metode skal du selv skrive
        pass

class Logistik(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master=master)

        #Her åbnes filen med data
        infile = open('danmarks_50_storste_byer.csv', mode='r', encoding="utf-8")
        #CSV-data læses
        reader = csv.DictReader(infile)
        
        self.build_user_interface()

        # Hver linje i filen laves til en by, og gemmes i en liste
        self.byer = []
        for line in reader:
            by = By(line['Navn'], line['X'], line['Y'], line['Indbyggertal'], self.canvas)
            self.byer.append(by)

        self.distributionscentre = []
        self.distributionscentre.append(Distributionscenter(50, 50, self.canvas))

    def build_user_interface(self):
        self.canvas = tk.Canvas(self, width=KORT_B, height=KORT_H, bg='white')
        self.canvas.skala = 1.0
        self.danmark_original = Image.open('denmark.png')
        self.danmark_image = ImageTk.PhotoImage(self.danmark_original)
        self.image_item = self.canvas.create_image((0, 0), image=self.danmark_image, anchor='nw')
        self.canvas.bind('<Configure>', self.on_resize)

        self.canvas.grid(row=0, column=0, rowspan=10, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(9, weight=1)

        self.sl_k_means = tk.Scale(self, label="K", from_=1, to=20, orient=tk.HORIZONTAL)
        self.but_k_means = tk.Button(self, text="K-means", command= self.kmeans)
        self.vaegtet = tk.BooleanVar(value=True)
        self.chk_vaegtet = tk.Checkbutton(self, text="Vægtet", variable=self.vaegtet)
        self.sl_k_means.grid(row=0, column= 1)
        self.chk_vaegtet.grid(row=2, column=1)
        self.but_k_means.grid(row=1, column=1)

        self.pack(fill=tk.BOTH, expand=True)

    def on_resize(self, event):
        # Skalér kortet ens i begge retninger, så det passer i canvas
        k = min(event.width / KORT_B, event.height / KORT_H)
        if k <= 0 or abs(k - self.canvas.skala) < 1e-6:
            return
        self.canvas.skala = k
        størrelse = (max(1, round(KORT_B * k)), max(1, round(KORT_H * k)))
        self.danmark_image = ImageTk.PhotoImage(
            self.danmark_original.resize(størrelse, Image.LANCZOS))
        self.canvas.itemconfig(self.image_item, image=self.danmark_image)
        for obj in getattr(self, 'byer', []) + getattr(self, 'distributionscentre', []):
            obj.place()
        # Kortet skal ligge bagved byer og centre
        self.canvas.tag_lower(self.image_item)

    def kmeans(self):
        # Her skal dannes K distributionscentre,
        # og algoritmen K-means skal finde deres placering
        k = int(self.sl_k_means.get())

        # Fjern gamle distributionscentre fra kortet
        for dc in self.distributionscentre:
            self.canvas.delete(dc.canvas_item)

        # Opret K centre på tilfældige steder inden for byernes udstrækning
        min_x = min(by.x for by in self.byer)
        max_x = max(by.x for by in self.byer)
        min_y = min(by.y for by in self.byer)
        max_y = max(by.y for by in self.byer)
        self.distributionscentre = [
            Distributionscenter(random.randint(min_x, max_x),
                                random.randint(min_y, max_y),
                                self.canvas)
            for _ in range(k)
        ]

        # K-means: gentag fordeling og flytning, indtil centrene ikke flytter sig
        while True:
            self.fordel_byer()
            flyttet = False
            for dc in self.distributionscentre:
                if not dc.byer:
                    continue  # tomt cluster: centret bliver stående
                if self.vaegtet.get():
                    # Vægtet gennemsnit: byerne vægtes med indbyggertal
                    w = sum(by.indbyggertal for by in dc.byer)
                    nx = round(sum(by.indbyggertal * by.x for by in dc.byer) / w)
                    ny = round(sum(by.indbyggertal * by.y for by in dc.byer) / w)
                else:
                    nx = round(sum(by.x for by in dc.byer) / len(dc.byer))
                    ny = round(sum(by.y for by in dc.byer) / len(dc.byer))
                if (nx, ny) != (dc.x, dc.y):
                    dc.move_to(nx, ny)
                    flyttet = True
            if not flyttet:
                break

    def fordel_byer(self):
        # Tilknyt hver by til det nærmeste center, og farv byen
        for dc in self.distributionscentre:
            dc.byer = []
        for by in self.byer:
            naermeste = min(
                self.distributionscentre,
                key=lambda dc: (dc.x - by.x) ** 2 + (dc.y - by.y) ** 2,
            )
            naermeste.byer.append(by)
            by.change_color(naermeste.farve)


def main():
    root = tk.Tk()
    prg = Logistik(master=root)
    prg.mainloop()
