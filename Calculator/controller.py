from model import CalculatorModel
from view import CalculatorView

class CalculatorController:
    def __init__(self, root):
        self.model = CalculatorModel()
        self.view = CalculatorView(root, self)
        
        # bind keyboard events
        root.bind("<Key>", self._handle_global_keypress)

    def on_append_char(self, char):
        self.model.append_to_expression(char)
        self.view.update_expression_display(self.model.current_expression)

    def on_clear(self):
        self.model.clear()
        self.view.update_expression_display("")
        self.view.update_result_display("")
        self._disable_entry_editing()

    def on_calculate(self):
        self._sync_expression_from_display()
        
        # save pre-calculation expression for the display
        pre_calc_expression = self.model.current_expression
        
        result = self.model.evaluate()
        if result is not None:
            self.view.update_result_display(result)
            self.view.update_expression_display(pre_calc_expression + "=")
        
        self._disable_entry_editing()

    def on_backspace(self):
        self.model.backspace()
        self.view.update_expression_display(self.model.current_expression)

    def _handle_global_keypress(self, event):
        if event.keysym == "Up":
            self._enable_entry_editing()
        elif event.keysym == "Return" or event.char == '=':
            self.on_calculate()
        elif event.keysym == "Escape":
            self.on_clear()
        elif event.keysym == "BackSpace":
            self.on_backspace()
        elif event.char in '0123456789.()%/+-*':
            self.on_append_char(event.char)

    def _handle_entry_keypress(self, event):
        if event.keysym == "Return" or event.char == '=':
            self.on_calculate()
            return "break"
        elif event.keysym == "Escape":
            self.on_clear()
            return "break"
        elif event.char in '0123456789.()%/+-*' or \
             event.keysym in ("Up", "Left", "Right", "Down", "BackSpace", "Delete", "Home", "End"):
            pass
        else:
            return "break"

    def _sync_expression_from_display(self):
        # needed for edit mode, syncs the model with the edited view
        self.model.current_expression = self.view.expression_display.get()

    def _enable_entry_editing(self):
        # swap the key bindings
        self.view.expression_display.config(state="normal")
        self.view.expression_display.focus_set()
        self.view.expression_display.bind("<Key>", self._handle_entry_keypress)
        self.view.root.unbind("<Key>")
        
        if self.model.is_result_displayed:
            self.view.update_result_display("")
            self.model.is_result_displayed = False
        
        if self.model.history_expression:
            self.model.current_expression = self.model.history_expression
            self.view.update_expression_display(self.model.current_expression)
        
    def _disable_entry_editing(self):
        # swap the key bindings back to global
        self.view.expression_display.config(state="readonly")
        self.view.expression_display.unbind("<Key>")
        self.view.root.bind("<Key>", self._handle_global_keypress)
        self.view.root.focus_set()
