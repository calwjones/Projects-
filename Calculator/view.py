import tkinter as tk
from tkinter import ttk
import tkinter.font as font

class CalculatorView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # theming and styling
        self.BG_COLOR = "#1e1e1e"
        self.DISPLAY_BG_COLOR = "#2e2e2e"
        self.BUTTON_BG_COLOR = "#404040"
        self.OPERATOR_BG_COLOR = "#ff9f0a"
        self.TEXT_COLOR = "#ffffff"
        self.MAIN_FONT = ('Arial', 18)
        self.RESULT_FONT = ('Arial', 24, "bold")
        self.EXPRESSION_FONT = ('Arial', 16)
        
        root.configure(bg=self.BG_COLOR)
        
        # build the ui
        self._setup_displays()
        self._setup_buttons()
        self._configure_grid()
        self._update_scrollbar()

    def _setup_displays(self):
        self.expression_display = tk.Entry(self.root, font=self.EXPRESSION_FONT, bd=0, justify="right",
                                          bg=self.BG_COLOR, fg=self.TEXT_COLOR,
                                          readonlybackground=self.BG_COLOR, state='readonly',
                                          insertbackground=self.TEXT_COLOR)
        self.expression_display.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0), sticky="ew")

        scrollbar_frame = ttk.Frame(self.root, style='Dark.TFrame')
        scrollbar_frame.grid(row=1, column=0, columnspan=4, sticky='ew', padx=10)
        self._configure_scrollbar_style()
        self.scrollbar = ttk.Scrollbar(scrollbar_frame, orient='horizontal', command=self.expression_display.xview,
                                       style='custom.Horizontal.TScrollbar')
        self.expression_display.config(xscrollcommand=self.scrollbar.set)
        self.expression_display.bind("<Configure>", self._update_scrollbar)


        self.result_display = tk.Entry(self.root, font=self.RESULT_FONT, bd=0, width=14, justify="right",
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

    def _setup_buttons(self):
        button_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        button_frame.grid(row=3, column=0, columnspan=4, sticky="nsew")
        button_specs = [
            ('(', 1, 0), (')', 1, 1), ('%', 1, 2), ('AC', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
        ]
        for (text, row, col) in button_specs:
            bg_color = self.OPERATOR_BG_COLOR if text in '()%/AC*/-+= ' else self.BUTTON_BG_COLOR
            # commands now call the controller
            command = self._get_button_command(text)
            button = tk.Button(button_frame, text=text, font=self.MAIN_FONT, height=2, bd=0, relief='flat',
                               command=command, bg=bg_color, fg=self.TEXT_COLOR,
                               activebackground=bg_color, activeforeground=self.TEXT_COLOR)
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def _get_button_command(self, text):
        if text in '0123456789.()%/+-*': 
            return lambda t=text: self.controller.on_append_char(t)
        elif text == 'AC': 
            return self.controller.on_clear
        elif text == '=': 
            return self.controller.on_calculate

    def _configure_grid(self):
        self.root.grid_rowconfigure(0, weight=1); self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=2); self.root.grid_rowconfigure(3, weight=8)
        self.root.grid_columnconfigure(0, weight=1)
        button_frame = self.root.winfo_children()[-1]
        for i in range(1, 6): button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4): button_frame.grid_columnconfigure(i, weight=1)
    
    def _update_display_text(self, widget, text):
        is_readonly = (widget['state'] == 'readonly')
        if is_readonly: widget.config(state=tk.NORMAL)
        widget.delete(0, tk.END)
        widget.insert(0, text)
        if is_readonly: widget.config(state='readonly')
    
    def update_expression_display(self, text):
        self._update_display_text(self.expression_display, text)
        self.root.after(10, self._update_scrollbar)

    def update_result_display(self, text):
        self._update_display_text(self.result_display, text)
        
    def _update_scrollbar(self, event=None):
        display_font = font.Font(font=self.expression_display['font'])
        text_width = display_font.measure(self.expression_display.get())
        widget_width = self.expression_display.winfo_width()
        if text_width > widget_width: self.scrollbar.pack(fill='x', expand=True)
        else: self.scrollbar.pack_forget()
