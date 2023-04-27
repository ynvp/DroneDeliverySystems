import tkinter as tk
import run as r


class CurrentLocation:

    def __init__(self, parent):
        options = list(r.warehouses.keys())
        print(options)
        self.clicked = tk.StringVar()
        self.clicked.set(list(r.warehouses.keys())[0])
        top = self.top = tk.Toplevel(parent)
        top.geometry("230x200")
        self.myLabel = tk.Label(
            top, text='Select initial warehouse')
        self.myLabel.place(x=40, y=50)
        self.myEntryBox = tk.Entry(top)
        self.selectWarehouse = tk.OptionMenu(top, self.clicked, *options)
        self.selectWarehouse.place(x=60, y=90)
        self.submitButton = tk.Button(top, text='Submit', command=self.send)
        self.submitButton.place(x=90, y=150)
        self.selectWarehouse.focus()

    def send(self):
        self.location = self.clicked.get()
        self.top.destroy()
