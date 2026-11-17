import tkinter as tk
import csv
import random
import os

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
        self.canvas_item = canvas.create_oval(-3+self.x, -3+self.y, 3+self.x, 3+self.y)

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

        self.canvas_item = self.canvas.create_rectangle(x-4, y-4, x+4, y+4, fill=col, outline='black')

    def move_to(self, x, y):
        self.canvas.coords(self.canvas_item, x-4, y-4, x+4, y+4)

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
        self.canvas = tk.Canvas(self, width=int(975/2), height=int(1300/2), bg='white')
        self.danmark_image = tk.PhotoImage(file='denmark.png')
        self.canvas.create_image((int(975/4),int(1300/4)), image = self.danmark_image)

        self.canvas.grid(row=0, column=0, rowspan=10)

        self.sl_k_means = tk.Scale(self, label="K", from_=1, to=20, orient=tk.HORIZONTAL)
        self.but_k_means = tk.Button(self, text="K-means", command= self.kmeans)
        self.sl_k_means.grid(row=0, column= 1)
        self.but_k_means.grid(row=1, column=1)

        self.pack()

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
