import tkinter as tk
from tkinter import ttk
import tkinter.font as font

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Python Calculator")
        master.geometry("380x540")
        master.resizable(False, False)

        # colours and fonts
        self.BG_COLOR = "#1e1e1e"
        self.DISPLAY_BG_COLOR = "#2e2e2e"
        self.BUTTON_BG_COLOR = "#404040"
        self.OPERATOR_BG_COLOR = "#ff9f0a"
        self.TEXT_COLOR = "#ffffff"
        self.MAIN_FONT = ('Arial', 18)
        self.RESULT_FONT = ('Arial', 24, "bold")
        self.EXPRESSION_FONT = ('Arial', 16) # made this font bigger

        # main state variables
        self.full_expression = "" # for the top display
        self.result_displayed = False
        master.configure(bg=self.BG_COLOR)

        # setup the display
        self._setup_display(master)

        # setup the buttons
        self._setup_buttons(master)

        # configure the grid
        self._configure_grid(master)

        # bind keyboard keys
        master.bind("<Key>", self._on_keypress)
        # bind configure event to the top display for the scrollbar
        self.expression_display.bind("<Configure>", self._update_scrollbar)
        self.master.after(100, self._update_scrollbar) # initial scrollbar check

    def _setup_display(self, master):
        # top display for the full expression (now an Entry widget)
        self.expression_display = tk.Entry(master, font=self.EXPRESSION_FONT, bd=0, justify="right",
                                          bg=self.BG_COLOR, fg=self.TEXT_COLOR,
                                          readonlybackground=self.BG_COLOR, state='readonly')
        self.expression_display.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0), sticky="ew")

        # frame to hold the scrollbar, now under the top display
        scrollbar_frame = ttk.Frame(master, style='Dark.TFrame')
        scrollbar_frame.grid(row=1, column=0, columnspan=4, sticky='ew', padx=10)
        self._configure_scrollbar_style()
        
        # scrollbar is now linked to the top expression_display
        self.scrollbar = ttk.Scrollbar(scrollbar_frame, orient='horizontal', command=self.expression_display.xview,
                                       style='custom.Horizontal.TScrollbar')
        self.expression_display.config(xscrollcommand=self.scrollbar.set)

        # main display for results
        self.result_display = tk.Entry(master, font=self.RESULT_FONT, bd=0, width=14, justify="right",
                                     bg=self.DISPLAY_BG_COLOR, fg=self.TEXT_COLOR,
                                     readonlybackground=self.DISPLAY_BG_COLOR, state='readonly')
        self.result_display.grid(row=2, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="ew")

    def _configure_scrollbar_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TFrame', background=self.BG_COLOR)
        style.layout('custom.Horizontal.TScrollbar',
                     [('Horizontal.Scrollbar.trough', {'children':
                         [('Horizontal.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})],
                         'sticky': 'we'})])
        style.configure('custom.Horizontal.TScrollbar', troughcolor=self.BG_COLOR, borderwidth=0, relief='flat')
        style.map('custom.Horizontal.TScrollbar', background=[('active', self.OPERATOR_BG_COLOR), ('!active', self.OPERATOR_BG_COLOR)])

    def _setup_buttons(self, master):
        button_frame = tk.Frame(master, bg=self.BG_COLOR)
        button_frame.grid(row=3, column=0, columnspan=4, sticky="nsew")

        button_texts = [
            ('(', 1, 0), (')', 1, 1), ('%', 1, 2), ('AC', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
        ]

        for (text, row, col) in button_texts:
            bg_color = self.OPERATOR_BG_COLOR if text in '()%/AC*/-+= ' else self.BUTTON_BG_COLOR
            action = self._get_action(text)
            button = tk.Button(button_frame, text=text, font=self.MAIN_FONT, height=2, bd=0, relief='flat',
                               command=action, bg=bg_color, fg=self.TEXT_COLOR,
                               activebackground=bg_color, activeforeground=self.TEXT_COLOR)
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def _get_action(self, text):
        # return correct function for a button
        if text in '0123456789.()%/+-*':
            return lambda t=text: self.press(t)
        elif text == 'AC':
            return self.clear
        elif text == '=':
            return self.equalpress

    def _configure_grid(self, master):
        # make the grid responsive
        master.grid_rowconfigure(0, weight=1) # top expression display
        master.grid_rowconfigure(1, weight=0) # scrollbar
        master.grid_rowconfigure(2, weight=2) # main result display
        master.grid_rowconfigure(3, weight=8) # buttons
        master.grid_columnconfigure(0, weight=1)
        
        button_frame = master.winfo_children()[-1] # get the button frame to configure it
        for i in range(1, 6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)

    def _on_keypress(self, event):
        # handle keyboard input
        if event.char in '0123456789.()%/+-*':
            self.press(event.char)
        elif event.keysym == "Return" or event.char == '=':
            self.equalpress()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear()

    def _set_display_text(self, widget, text):
        # helper to update a display's text
        widget.config(state=tk.NORMAL)
        widget.delete(0, tk.END)
        widget.insert(0, text)
        widget.xview_moveto(1)
        widget.config(state='readonly')

    def press(self, num):
        # handle button presses
        if self.result_displayed:
            if num in '%/+-*': # use result in next calculation
                self.result_displayed = False
                self._set_display_text(self.result_display, "")
            else: # start a new calculation
                self.clear()
        
        self.full_expression += str(num)
        self._set_display_text(self.expression_display, self.full_expression)
        self.master.after(10, self._update_scrollbar)

    def clear(self):
        # clear display and memory
        self.full_expression = ""
        self.result_displayed = False
        self._set_display_text(self.result_display, "")
        self._set_display_text(self.expression_display, "")

    def backspace(self):
        # handle backspace
        if self.result_displayed:
            return # can't backspace a result
        
        self.full_expression = self.full_expression[:-1]
        self._set_display_text(self.expression_display, self.full_expression)

    def equalpress(self):
        # handle equals press
        if self.result_displayed: return
        try:
            if not self.full_expression: return
            
            expression_with_equals = self.full_expression + "="
            self._set_display_text(self.expression_display, expression_with_equals)
            
            processed_expression = self.full_expression.replace('%', '/100')
            numeric_total = eval(processed_expression)

            # format the result
            if numeric_total == int(numeric_total):
                total = str(int(numeric_total))
            else:
                total = str(round(numeric_total, 8))

            if abs(numeric_total) > 1e12 or (abs(numeric_total) < 1e-6 and numeric_total != 0):
                total = f"{numeric_total:.4g}"

            self._set_display_text(self.result_display, total)
            self.full_expression = total # store result for next calculation
            self.result_displayed = True
            
        except (SyntaxError, ZeroDivisionError, NameError):
            self._set_display_text(self.result_display, "Error")
            self.full_expression = ""
            self.result_displayed = True

    def _update_scrollbar(self, event=None):
        # check if scrollbar is needed for the top display
        display_font = font.Font(font=self.expression_display['font'])
        text_width = display_font.measure(self.expression_display.get())
        widget_width = self.expression_display.winfo_width()

        # show or hide scrollbar
        if text_width > widget_width:
            self.scrollbar.pack(fill='x', expand=True)
        else:
            self.scrollbar.pack_forget()

if __name__ == '__main__':
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

