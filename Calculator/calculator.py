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
        self.EXPRESSION_FONT = ('Arial', 16)

        # main state variables
        self.full_expression = ""
        self.result_displayed = False
        self.last_calculation = ""
        master.configure(bg=self.BG_COLOR)

        # setup ui
        self._setup_display(master)
        self._setup_buttons(master)
        self._configure_grid(master)

        # bind general keyboard keys to the main window
        master.bind("<Key>", self._on_keypress)
        self.expression_display.bind("<Configure>", self._update_scrollbar)
        self.master.after(100, self._update_scrollbar)

    def _setup_display(self, master):
        self.expression_display = tk.Entry(master, font=self.EXPRESSION_FONT, bd=0, justify="right",
                                          bg=self.BG_COLOR, fg=self.TEXT_COLOR,
                                          readonlybackground=self.BG_COLOR, state='readonly',
                                          insertbackground=self.TEXT_COLOR)
        self.expression_display.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0), sticky="ew")

        scrollbar_frame = ttk.Frame(master, style='Dark.TFrame')
        scrollbar_frame.grid(row=1, column=0, columnspan=4, sticky='ew', padx=10)
        self._configure_scrollbar_style()
        self.scrollbar = ttk.Scrollbar(scrollbar_frame, orient='horizontal', command=self.expression_display.xview,
                                       style='custom.Horizontal.TScrollbar')
        self.expression_display.config(xscrollcommand=self.scrollbar.set)

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
        if text in '0123456789.()%/+-*': return lambda t=text: self._button_press(t)
        elif text == 'AC': return self.clear
        elif text == '=': return self.equalpress

    def _configure_grid(self, master):
        master.grid_rowconfigure(0, weight=1); master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=2); master.grid_rowconfigure(3, weight=8)
        master.grid_columnconfigure(0, weight=1)
        button_frame = master.winfo_children()[-1]
        for i in range(1, 6): button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4): button_frame.grid_columnconfigure(i, weight=1)

    def _on_keypress(self, event):
        # general handler for when the display is NOT in edit mode
        if event.keysym == "Up":
            self._activate_edit_mode()
        elif event.keysym == "Return" or event.char == '=':
            self.equalpress()
        elif event.keysym == "Escape":
            self.clear()
        elif event.keysym == "BackSpace":
            self._button_backspace()
        elif event.char in '0123456789.()%/+-*':
            self._button_press(event.char)

    def _on_edit_keypress(self, event):
        # high-priority handler ONLY for when the display is in edit mode
        if event.keysym == "Return" or event.char == '=':
            self.equalpress()
            return "break"
        elif event.keysym == "Escape":
            self.clear()
            return "break"
        elif event.char in '0123456789.()%/+-*':
            pass # allow valid chars to be typed
        elif event.keysym in ("Up", "Left", "Right", "Down", "BackSpace", "Delete", "Home", "End"):
            pass # allow navigation
        else:
            return "break" # block letters and other characters

    def _sync_expression_from_display(self):
        self.full_expression = self.expression_display.get()
        self.master.after(10, self._update_scrollbar)

    def _set_display_text(self, widget, text):
        is_readonly = (widget['state'] == 'readonly')
        if is_readonly: widget.config(state=tk.NORMAL)
        widget.delete(0, tk.END)
        widget.insert(0, text)
        widget.xview_moveto(1)
        if is_readonly: widget.config(state='readonly')

    def _activate_edit_mode(self):
        self.expression_display.config(state=tk.NORMAL)
        self.expression_display.focus_set()
        # bind the specific, high-priority handler
        self.expression_display.bind("<Key>", self._on_edit_keypress)
        # unbind the general, low-priority handler to avoid double events
        self.master.unbind("<Key>")
        
        if self.result_displayed:
            self._set_display_text(self.result_display, "")
            self.result_displayed = False
        
        if self.last_calculation:
            self.full_expression = self.last_calculation
            self._set_display_text(self.expression_display, self.full_expression)
        
    def _deactivate_edit_mode(self):
        self.expression_display.config(state='readonly')
        # unbind the specific handler
        self.expression_display.unbind("<Key>")
        # re-bind the general handler
        self.master.bind("<Key>", self._on_keypress)
        self.master.focus_set()

    def _button_press(self, num):
        if self.result_displayed:
            if num in '%/+-*':
                self.result_displayed = False
            else:
                self.full_expression = ""
        self.full_expression += num
        self._set_display_text(self.expression_display, self.full_expression)
        self._sync_expression_from_display()

    def _button_backspace(self):
        if self.result_displayed: return
        self.full_expression = self.full_expression[:-1]
        self._set_display_text(self.expression_display, self.full_expression)
        self._sync_expression_from_display()

    def clear(self):
        self.full_expression = ""
        self.last_calculation = ""
        self.result_displayed = False
        self._set_display_text(self.result_display, "")
        self._set_display_text(self.expression_display, "")
        self._deactivate_edit_mode()

    def equalpress(self):
        self._sync_expression_from_display()
        if self.result_displayed or not self.full_expression: return
        
        self.last_calculation = self.full_expression
        try:
            processed_expression = self.full_expression.replace('%', '/100')
            numeric_total = eval(processed_expression)
            
            if numeric_total == int(numeric_total): total = str(int(numeric_total))
            else: total = str(round(numeric_total, 8))
            if abs(numeric_total) > 1e12 or (abs(numeric_total) < 1e-6 and numeric_total != 0):
                total = f"{numeric_total:.4g}"

            self._set_display_text(self.result_display, total)
            self._set_display_text(self.expression_display, self.full_expression + "=")
            self.full_expression = total
            self.result_displayed = True
            
        except (SyntaxError, ZeroDivisionError, NameError):
            self._set_display_text(self.result_display, "Error")
            self.full_expression = ""
            self.result_displayed = True
        
        self._deactivate_edit_mode()

    def _update_scrollbar(self, event=None):
        display_font = font.Font(font=self.expression_display['font'])
        text_width = display_font.measure(self.expression_display.get())
        widget_width = self.expression_display.winfo_width()
        if text_width > widget_width: self.scrollbar.pack(fill='x', expand=True)
        else: self.scrollbar.pack_forget()

if __name__ == '__main__':
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

