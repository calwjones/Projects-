class CalculatorModel:
    def __init__(self):
        # initialise all the state variables
        self.current_expression = ""
        self.history_expression = ""
        self.is_result_displayed = False

    # adds a character to the current expression string
    def append_to_expression(self, char):
        if self.is_result_displayed:
            if char in '%/+-*': # chain the calculation
                self.is_result_displayed = False
            else: # start a new calculation
                self.current_expression = ""
        self.current_expression += char

    # performs the backspace operation on the string
    def backspace(self):
        if not self.is_result_displayed:
            self.current_expression = self.current_expression[:-1]

    # resets all state variables to their initial values
    def clear(self):
        self.current_expression = ""
        self.history_expression = ""
        self.is_result_displayed = False

    # evaluates the current expression
    def evaluate(self):
        # don't calculate on an empty string or a result
        if self.is_result_displayed or not self.current_expression:
            return None # return nothing if there's nothing to do
        
        # save the expression for history recall
        self.history_expression = self.current_expression
        try:
            # handle percentage and then evaluate
            processed_expression = self.current_expression.replace('%', '/100')
            numeric_total = eval(processed_expression)
            
            # format the result to be clean
            if numeric_total == int(numeric_total):
                total_str = str(int(numeric_total))
            else:
                total_str = str(round(numeric_total, 8))
            # use scientific notation for very large/small numbers
            if abs(numeric_total) > 1e12 or (abs(numeric_total) < 1e-6 and numeric_total != 0):
                total_str = f"{numeric_total:.4g}"

            # set the new expression for chaining and update state
            self.current_expression = total_str
            self.is_result_displayed = True
            return total_str
            
        except (SyntaxError, ZeroDivisionError, NameError):
            # handle errors
            self.current_expression = ""
            self.is_result_displayed = True
            return "Error"
