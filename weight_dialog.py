import tkinter as tk


class MyDialog:

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.geometry("230x200")
        self.myLabel = tk.Label(top, text='Enter package weight below')
        self.myLabel.place(x=40, y=50)
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.place(x=60, y=90)
        self.mySubmitButton = tk.Button(top, text='Submit', command=self.send)
        self.mySubmitButton.place(x=90, y=150)

    def send(self):
        self.weight = self.myEntryBox.get()
        self.top.destroy()
