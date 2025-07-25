"""
VibeScript Interpreter

This module interprets the AST generated by the parser and executes the program.
"""

import sys
from io import StringIO
from vibescript.grammar import TOKEN_TYPES

class InterpreterError(Exception):
    """Exception raised when an error occurs during interpretation"""
    
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class InputRequestException(Exception):
    """Exception raised when input is requested from user"""
    
    def __init__(self, variable_name):
        self.variable_name = variable_name
        super().__init__(f"Input requested for variable: {variable_name}")

class SymbolTable:
    """Symbol table for storing variables and functions"""
    
    def __init__(self, enclosing=None):
        self.symbols = {}
        self.enclosing = enclosing
    
    def define(self, name, value):
        """Define a new symbol in the current scope"""
        self.symbols[name] = value
    
    def assign(self, name, value):
        """Assign a value to an existing symbol"""
        if name in self.symbols:
            self.symbols[name] = value
            return True
        elif self.enclosing:
            return self.enclosing.assign(name, value)
        else:
            return False
    
    def get(self, name):
        """Get the value of a symbol"""
        if name in self.symbols:
            return self.symbols[name]
        elif self.enclosing:
            return self.enclosing.get(name)
        else:
            return None
    
    def contains(self, name):
        """Check if a symbol exists in the current or enclosing scopes"""
        if name in self.symbols:
            return True
        elif self.enclosing:
            return self.enclosing.contains(name)
        else:
            return False

class Function:
    """Represents a function in VibeScript"""
    
    def __init__(self, declaration, environment, interpreter):
        self.declaration = declaration
        self.environment = environment
        self.interpreter = interpreter
    
    def call(self, arguments):
        """Call the function with the given arguments"""
        # Create a new environment for the function scope
        environment = SymbolTable(self.environment)
        
        # Bind parameters to arguments
        for i, param in enumerate(self.declaration.params):
            if i < len(arguments):
                environment.define(param, arguments[i])
            else:
                environment.define(param, None)
        
        # Execute the function body with the new environment
        previous_environment = self.interpreter.environment
        self.interpreter.environment = environment
        
        return_value = None
        try:
            self.interpreter.execute(self.declaration.body)
        except ReturnValue as ret:
            return_value = ret.value
        finally:
            self.interpreter.environment = previous_environment
        
        return return_value

class ReturnValue(Exception):
    """Exception used to handle return statements"""
    
    def __init__(self, value):
        self.value = value
        super().__init__()

class Interpreter:
    """Interpreter for VibeScript AST"""
    
    def __init__(self, parser):
        self.parser = parser
        self.environment = SymbolTable()
        self.output_stream = StringIO()
        self.output = ""
        self.input_values = {}
    
    def error(self, message):
        """Raise an interpreter error"""
        raise InterpreterError(message)
    
    def interpret(self):
        """Interpret the program"""
        # Parse the program
        program = self.parser.parse()
        
        # Execute the program
        return self.execute(program)
    
    def execute(self, node):
        """Execute a node in the AST"""
        # Execute the appropriate method based on the node type
        method_name = f"execute_{node.__class__.__name__}"
        method = getattr(self, method_name, self.execute_unknown)
        return method(node)
    
    def execute_unknown(self, node):
        """Handle unknown node types"""
        self.error(f"Unknown node type: {node.__class__.__name__}")
    
    def execute_Program(self, node):
        """Execute a Program node"""
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result
    
    def execute_PrintStatement(self, node):
        """Execute a PrintStatement node (spill_the_tea)"""
        value = self.evaluate(node.expression)
        print_value = str(value)
        
        # Write to output stream for web interface
        self.output_stream.write(print_value + "\n")
        self.output = self.output_stream.getvalue()
    
    def execute_InputStatement(self, node):
        """Execute an InputStatement node (vibe_check)"""
        # Check if we have a pre-provided input value
        if hasattr(self, 'input_values') and node.variable in self.input_values:
            value = self.input_values[node.variable]
            self.environment.assign(node.variable, value)
            # Don't show input message - just silently assign the value
            self.output = self.output_stream.getvalue()
        else:
            # Request input from user
            raise InputRequestException(node.variable)
    
    def execute_VariableDeclaration(self, node):
        """Execute a VariableDeclaration node"""
        value = None
        if node.value:
            value = self.evaluate(node.value)
        
        # Initialize with default values based on type if no value is provided
        if value is None:
            if node.data_type == TOKEN_TYPES['LIT']:
                value = 0
            elif node.data_type == TOKEN_TYPES['TEA']:
                value = ""
            elif node.data_type == TOKEN_TYPES['MOOD']:
                value = False
            elif node.data_type == TOKEN_TYPES['STAN']:
                value = []
        
        self.environment.define(node.name, value)
    
    def execute_AssignmentStatement(self, node):
        """Execute an AssignmentStatement node"""
        value = self.evaluate(node.expression)
        
        if not self.environment.assign(node.variable, value):
            self.error(f"Undefined variable: {node.variable}")
    
    def execute_IfStatement(self, node):
        """Execute an IfStatement node (no_cap)"""
        if self.is_truthy(self.evaluate(node.condition)):
            return self.execute(node.if_block)
        elif node.else_block:
            return self.execute(node.else_block)
    
    def execute_WhileStatement(self, node):
        """Execute a WhileStatement node (lowkey)"""
        while self.is_truthy(self.evaluate(node.condition)):
            try:
                self.execute(node.block)
            except BreakException:
                break
            except ContinueException:
                continue
    
    def execute_ForStatement(self, node):
        """Execute a ForStatement node (highkey)"""
        # Initialize
        self.execute(node.init)
        
        # Execute loop
        while self.is_truthy(self.evaluate(node.condition)):
            try:
                # Execute block
                self.execute(node.block)
                
                # Update
                self.evaluate(node.update)
            except BreakException:
                break
            except ContinueException:
                # Still need to update the loop variable
                self.evaluate(node.update)
                continue
    
    def execute_FunctionDeclaration(self, node):
        """Execute a FunctionDeclaration node (rizz_up)"""
        function = Function(node, self.environment, self)
        self.environment.define(node.name, function)
    
    def execute_ReturnStatement(self, node):
        """Execute a ReturnStatement node (slay)"""
        value = None
        if node.expression:
            value = self.evaluate(node.expression)
        
        raise ReturnValue(value)
    
    def execute_BreakStatement(self, node):
        """Execute a BreakStatement node (and_i_oop)"""
        raise BreakException()
    
    def execute_ContinueStatement(self, node):
        """Execute a ContinueStatement node (as_if)"""
        raise ContinueException()
    
    def execute_BlockStatement(self, node):
        """Execute a BlockStatement node (lets_go ... yeet)"""
        # Create a new environment for the block
        previous_environment = self.environment
        self.environment = SymbolTable(previous_environment)
        
        try:
            for statement in node.statements:
                self.execute(statement)
        finally:
            # Restore the previous environment
            self.environment = previous_environment
    
    def execute_ExpressionStatement(self, node):
        """Execute an ExpressionStatement node"""
        return self.evaluate(node.expression)
    
    def evaluate(self, node):
        """Evaluate an expression node"""
        # Evaluate the appropriate method based on the node type
        method_name = f"evaluate_{node.__class__.__name__}"
        method = getattr(self, method_name, self.evaluate_unknown)
        return method(node)
    
    def evaluate_unknown(self, node):
        """Handle unknown expression node types"""
        self.error(f"Unknown expression node type: {node.__class__.__name__}")
    
    def evaluate_BinaryExpression(self, node):
        """Evaluate a BinaryExpression node"""
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        
        if node.operator.type == TOKEN_TYPES['PLUS']:
            # Handle string concatenation
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif node.operator.type == TOKEN_TYPES['MINUS']:
            return left - right
        elif node.operator.type == TOKEN_TYPES['MULTIPLY']:
            return left * right
        elif node.operator.type == TOKEN_TYPES['DIVIDE']:
            if right == 0:
                self.error("Division by zero")
            return left / right
        elif node.operator.type == TOKEN_TYPES['MODULO']:
            if right == 0:
                self.error("Division by zero")
            return left % right
        elif node.operator.type == TOKEN_TYPES['EQUALS']:
            return left == right
        elif node.operator.type == TOKEN_TYPES['NOT_EQUALS']:
            return left != right
        elif node.operator.type == TOKEN_TYPES['LESS_THAN']:
            return left < right
        elif node.operator.type == TOKEN_TYPES['GREATER_THAN']:
            return left > right
        elif node.operator.type == TOKEN_TYPES['LESS_EQUALS']:
            return left <= right
        elif node.operator.type == TOKEN_TYPES['GREATER_EQUALS']:
            return left >= right
        
        self.error(f"Unknown binary operator: {node.operator.type}")
    
    def evaluate_UnaryExpression(self, node):
        """Evaluate a UnaryExpression node"""
        operand = self.evaluate(node.operand)
        
        if node.operator.type == TOKEN_TYPES['MINUS']:
            return -operand
        elif node.operator.type == TOKEN_TYPES['PLUS']:
            return operand
        
        self.error(f"Unknown unary operator: {node.operator.type}")
    
    def evaluate_VariableExpression(self, node):
        """Evaluate a VariableExpression node"""
        value = self.environment.get(node.name)
        
        if value is None and not self.environment.contains(node.name):
            self.error(f"Undefined variable: {node.name}")
            
        return value
    
    def evaluate_LiteralExpression(self, node):
        """Evaluate a LiteralExpression node"""
        return node.value
    
    def evaluate_FunctionCallExpression(self, node):
        """Evaluate a FunctionCallExpression node"""
        function = self.environment.get(node.function)
        
        if not function or not callable(getattr(function, 'call', None)):
            self.error(f"'{node.function}' is not a function")
            
        # Evaluate arguments
        arguments = [self.evaluate(arg) for arg in node.arguments]
        
        # Call the function
        return function.call(arguments)
    
    def is_truthy(self, value):
        """Determine if a value is truthy"""
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            return len(value) > 0
        elif isinstance(value, list):
            return len(value) > 0
        return True

class BreakException(Exception):
    """Exception used to handle break statements"""
    pass

class ContinueException(Exception):
    """Exception used to handle continue statements"""
    pass
