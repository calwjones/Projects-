import tkinter as tk
from controller import CalculatorController

if __name__ == "__main__":
    # create the main window
    root = tk.Tk()
    root.title("Python Calculator")
    root.geometry("380x540")
    root.resizable(False, False)
    
    # create the controller, which initializes the model and view
    app = CalculatorController(root)
    
    # start the application
    root.mainloop()
