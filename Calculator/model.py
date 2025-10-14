class CalculatorModel:
    def __init__(self):
        # initialise all the state variables
        self.current_expression = ""
        self.history_expression = ""
        self.is_result_displayed = False
        # define operator precedence for the shunting-yard algorithm
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}

    def _tokenize(self, expression):
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            elif char.isdigit() or char == '.':
                start_index = i
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                number_str = expression[start_index:i]
                if tokens and tokens[-1] == ')':
                    tokens.append('*')
                tokens.append(number_str)
                continue

            elif char == '(':
                if tokens and (tokens[-1].replace('.', '', 1).isdigit() or tokens[-1] == ')'):
                    tokens.append('*')
                tokens.append(char)

            elif char in '*/%+-':
                tokens.append(char)
            
            elif char == ')':
                tokens.append(char)

            i += 1
        return tokens

    def _shunting_yard(self, tokens):
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                output_queue.append(token)
            elif token in self.precedence:
                while (operator_stack and operator_stack[-1] in self.precedence and
                       self.precedence[operator_stack[-1]] >= self.precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop() 

        while operator_stack:
            output_queue.append(operator_stack.pop())
            
        return output_queue

    # this is the final step: evaluating the RPN queue
    def _evaluate_rpn(self, rpn_queue):
        stack = []
        for token in rpn_queue:
            if token.replace('.', '', 1).isdigit():
                stack.append(float(token))
            elif token in self.precedence:
                # guard against insufficient operands
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for operator")
                b = stack.pop()
                a = stack.pop()
                if token == '+': result = a + b
                elif token == '-': result = a - b
                elif token == '*': result = a * b
                elif token == '/':
                    if b == 0: raise ZeroDivisionError("Division by zero")
                    result = a / b
                elif token == '%': result = a % b
                stack.append(result)
        
        if len(stack) == 1:
            return stack[0]
        else:
            raise ValueError("Invalid expression: operands remain on stack")

    def append_to_expression(self, char):
        if self.is_result_displayed:
            if char in '%/+-*':
                self.is_result_displayed = False
            else:
                self.current_expression = ""
                self.is_result_displayed = False
        self.current_expression += char

    def backspace(self):
        if not self.is_result_displayed:
            self.current_expression = self.current_expression[:-1]

    def clear(self):
        self.current_expression = ""
        self.history_expression = ""
        self.is_result_displayed = False

    # evaluates the current expression using our full parser
    def evaluate(self):
        if self.is_result_displayed or not self.current_expression:
            return None
        
        self.history_expression = self.current_expression
        try:
            tokens = self._tokenize(self.current_expression)
            
            if len(tokens) == 1 and tokens[0].replace('.', '', 1).isdigit():
                self.is_result_displayed = True
                self.current_expression = tokens[0]
                return tokens[0]

            rpn_queue = self._shunting_yard(tokens)
            numeric_total = self._evaluate_rpn(rpn_queue)

            # format the result to be clean
            if numeric_total == int(numeric_total): total_str = str(int(numeric_total))
            else: total_str = str(round(numeric_total, 8))
            if abs(numeric_total) > 1e12 or (abs(numeric_total) < 1e-6 and numeric_total != 0):
                total_str = f"{numeric_total:.4g}"
            
            self.current_expression = total_str
            self.is_result_displayed = True
            return total_str
            
        except (ValueError, ZeroDivisionError, IndexError):
            self.current_expression = ""
            self.is_result_displayed = True
            return "Error"

