from model import Model
from display import Display
from controller import Controller
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Acoustics Modeler')
        self.geometry('1350x300')

        # create a model
        model = Model('default.wav')

        # create a view and place it on the root window
        display = Display(self)
        display.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, display)

        # set the controller to view
        display.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
