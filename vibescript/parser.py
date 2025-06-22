"""
VibeScript Parser

This module parses tokenized VibeScript code into an Abstract Syntax Tree (AST).
"""

from vibescript.grammar import TOKEN_TYPES

class ParserError(Exception):
    """Exception raised when an error occurs during parsing"""
    
    def __init__(self, message, token):
        self.message = message
        self.token = token
        super().__init__(f"{message} at line {token.line}, column {token.column}")

# AST Node classes
class Node:
    """Base class for all AST nodes"""
    pass

class Program(Node):
    """Root node of the program"""
    
    def __init__(self, statements):
        self.statements = statements

class Statement(Node):
    """Base class for all statement nodes"""
    pass

class ExpressionStatement(Statement):
    """A statement consisting of an expression"""
    
    def __init__(self, expression):
        self.expression = expression

class PrintStatement(Statement):
    """A print statement (spill_the_tea)"""
    
    def __init__(self, expression):
        self.expression = expression

class InputStatement(Statement):
    """An input statement (vibe_check)"""
    
    def __init__(self, variable):
        self.variable = variable

class VariableDeclaration(Statement):
    """A variable declaration statement"""
    
    def __init__(self, name, data_type, value=None):
        self.name = name
        self.data_type = data_type
        self.value = value

class AssignmentStatement(Statement):
    """An assignment statement"""
    
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

class IfStatement(Statement):
    """An if statement (no_cap)"""
    
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

class WhileStatement(Statement):
    """A while loop statement (lowkey)"""
    
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

class ForStatement(Statement):
    """A for loop statement (highkey)"""
    
    def __init__(self, init, condition, update, block):
        self.init = init
        self.condition = condition
        self.update = update
        self.block = block

class FunctionDeclaration(Statement):
    """A function declaration (rizz_up)"""
    
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ReturnStatement(Statement):
    """A return statement (slay)"""
    
    def __init__(self, expression=None):
        self.expression = expression

class BreakStatement(Statement):
    """A break statement (and_i_oop)"""
    pass

class ContinueStatement(Statement):
    """A continue statement (as_if)"""
    pass

class BlockStatement(Statement):
    """A block of statements (lets_go ... yeet)"""
    
    def __init__(self, statements):
        self.statements = statements

class Expression(Node):
    """Base class for all expression nodes"""
    pass

class BinaryExpression(Expression):
    """A binary expression (e.g., a + b)"""
    
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryExpression(Expression):
    """A unary expression (e.g., -a)"""
    
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class VariableExpression(Expression):
    """A variable reference"""
    
    def __init__(self, name):
        self.name = name

class LiteralExpression(Expression):
    """A literal value (integer, string, boolean)"""
    
    def __init__(self, value, value_type):
        self.value = value
        self.value_type = value_type

class FunctionCallExpression(Expression):
    """A function call"""
    
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

class Parser:
    """Parser for VibeScript language"""
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self, message):
        """Raise a parser error with the current token"""
        raise ParserError(message, self.current_token)
    
    def eat(self, token_type):
        """
        Compare the current token type with the passed token type and
        if they match, 'eat' the current token and assign the next token
        to the current token, otherwise raise an exception.
        """
        if self.current_token.type == token_type:
            current_token = self.current_token
            self.current_token = self.lexer.get_next_token()
            return current_token
        else:
            self.error(
                f"Expected token of type {token_type}, got {self.current_token.type}"
            )
    
    def parse(self):
        """Parse the input and return an AST"""
        node = self.program()
        
        if self.current_token.type != TOKEN_TYPES['EOF']:
            self.error("Expected end of input")
            
        return node
    
    def program(self):
        """
        program : statement_list
        """
        statements = self.statement_list()
        return Program(statements)
    
    def statement_list(self):
        """
        statement_list : statement*
        """
        statements = []
        
        while self.current_token.type != TOKEN_TYPES['EOF'] and self.current_token.type != TOKEN_TYPES['YEET']:
            statement = self.statement()
            if statement:
                statements.append(statement)
                
        return statements
    
    def statement(self):
        """
        statement : print_statement
                  | input_statement
                  | variable_declaration
                  | assignment_statement
                  | if_statement
                  | while_statement
                  | for_statement
                  | function_declaration
                  | return_statement
                  | break_statement
                  | continue_statement
                  | block_statement
                  | expression_statement
        """
        token = self.current_token
        
        if token.type == TOKEN_TYPES['SPILL_THE_TEA']:
            return self.print_statement()
        elif token.type == TOKEN_TYPES['VIBE_CHECK']:
            return self.input_statement()
        elif token.type in (TOKEN_TYPES['LIT'], TOKEN_TYPES['TEA'], TOKEN_TYPES['MOOD'], TOKEN_TYPES['STAN']):
            return self.variable_declaration()
        elif token.type == TOKEN_TYPES['IDENTIFIER']:
            # Simple lookahead for assignment by checking the next character
            current_pos = self.lexer.pos
            # Look for '=' character after the identifier
            temp_text = self.lexer.text[current_pos:]
            has_assign = '=' in temp_text.split(';')[0] and temp_text.split(';')[0].strip().endswith('=') is False and '=' in temp_text.split(';')[0].split()[0:2]
            
            # More reliable check: peek ahead for assignment
            peek_ahead = ""
            temp_pos = current_pos
            while temp_pos < len(self.lexer.text) and self.lexer.text[temp_pos] not in [';', '\n']:
                peek_ahead += self.lexer.text[temp_pos]
                temp_pos += 1
            
            if '=' in peek_ahead and not '==' in peek_ahead and not '!=' in peek_ahead and not '>=' in peek_ahead and not '<=' in peek_ahead:
                return self.assignment_statement()
            else:
                return self.expression_statement()
        elif token.type == TOKEN_TYPES['NO_CAP']:
            return self.if_statement()
        elif token.type == TOKEN_TYPES['LOWKEY']:
            return self.while_statement()
        elif token.type == TOKEN_TYPES['HIGHKEY']:
            return self.for_statement()
        elif token.type == TOKEN_TYPES['RIZZ_UP']:
            return self.function_declaration()
        elif token.type == TOKEN_TYPES['SLAY']:
            return self.return_statement()
        elif token.type == TOKEN_TYPES['AND_I_OOP']:
            return self.break_statement()
        elif token.type == TOKEN_TYPES['AS_IF']:
            return self.continue_statement()
        elif token.type == TOKEN_TYPES['LETS_GO']:
            return self.block_statement()
        else:
            return self.expression_statement()
    
    def print_statement(self):
        """
        print_statement : SPILL_THE_TEA expression SEMICOLON
        """
        self.eat(TOKEN_TYPES['SPILL_THE_TEA'])
        expression = self.expression()
        self.eat(TOKEN_TYPES['SEMICOLON'])
        return PrintStatement(expression)
    
    def input_statement(self):
        """
        input_statement : VIBE_CHECK IDENTIFIER SEMICOLON
        """
        self.eat(TOKEN_TYPES['VIBE_CHECK'])
        variable = self.eat(TOKEN_TYPES['IDENTIFIER']).value
        self.eat(TOKEN_TYPES['SEMICOLON'])
        return InputStatement(variable)
    
    def variable_declaration(self):
        """
        variable_declaration : type IDENTIFIER (ASSIGN expression)? SEMICOLON
        """
        data_type = self.current_token.type
        self.eat(data_type)
        name = self.eat(TOKEN_TYPES['IDENTIFIER']).value
        
        value = None
        if self.current_token.type == TOKEN_TYPES['ASSIGN']:
            self.eat(TOKEN_TYPES['ASSIGN'])
            value = self.expression()
            
        self.eat(TOKEN_TYPES['SEMICOLON'])
        return VariableDeclaration(name, data_type, value)
    
    def assignment_statement(self):
        """
        assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON
        """
        variable = self.eat(TOKEN_TYPES['IDENTIFIER']).value
        self.eat(TOKEN_TYPES['ASSIGN'])
        expression = self.expression()
        self.eat(TOKEN_TYPES['SEMICOLON'])
        return AssignmentStatement(variable, expression)
    
    def if_statement(self):
        """
        if_statement : NO_CAP LPAREN expression RPAREN statement (CAP statement)?
        """
        self.eat(TOKEN_TYPES['NO_CAP'])
        self.eat(TOKEN_TYPES['LPAREN'])
        condition = self.expression()
        self.eat(TOKEN_TYPES['RPAREN'])
        if_block = self.statement()
        
        else_block = None
        if self.current_token.type == TOKEN_TYPES['CAP']:
            self.eat(TOKEN_TYPES['CAP'])
            else_block = self.statement()
            
        return IfStatement(condition, if_block, else_block)
    
    def while_statement(self):
        """
        while_statement : LOWKEY LPAREN expression RPAREN statement
        """
        self.eat(TOKEN_TYPES['LOWKEY'])
        self.eat(TOKEN_TYPES['LPAREN'])
        condition = self.expression()
        self.eat(TOKEN_TYPES['RPAREN'])
        block = self.statement()
        return WhileStatement(condition, block)
    
    def for_statement(self):
        """
        for_statement : HIGHKEY LPAREN statement expression SEMICOLON expression RPAREN statement
        """
        self.eat(TOKEN_TYPES['HIGHKEY'])
        self.eat(TOKEN_TYPES['LPAREN'])
        
        # Initialization
        init = self.statement()
        
        # Condition
        condition = self.expression()
        self.eat(TOKEN_TYPES['SEMICOLON'])
        
        # Update
        update = self.expression()
        self.eat(TOKEN_TYPES['RPAREN'])
        
        # Body
        block = self.statement()
        
        return ForStatement(init, condition, update, block)
    
    def function_declaration(self):
        """
        function_declaration : RIZZ_UP IDENTIFIER LPAREN parameters RPAREN block_statement
        """
        self.eat(TOKEN_TYPES['RIZZ_UP'])
        name = self.eat(TOKEN_TYPES['IDENTIFIER']).value
        self.eat(TOKEN_TYPES['LPAREN'])
        
        # Parameters
        params = []
        if self.current_token.type != TOKEN_TYPES['RPAREN']:
            params = self.parameters()
            
        self.eat(TOKEN_TYPES['RPAREN'])
        
        # Function body
        body = self.block_statement()
        
        return FunctionDeclaration(name, params, body)
    
    def parameters(self):
        """
        parameters : IDENTIFIER (COMMA IDENTIFIER)*
        """
        params = [self.eat(TOKEN_TYPES['IDENTIFIER']).value]
        
        while self.current_token.type == TOKEN_TYPES['COMMA']:
            self.eat(TOKEN_TYPES['COMMA'])
            params.append(self.eat(TOKEN_TYPES['IDENTIFIER']).value)
            
        return params
    
    def return_statement(self):
        """
        return_statement : SLAY (expression)? SEMICOLON
        """
        self.eat(TOKEN_TYPES['SLAY'])
        
        expression = None
        if self.current_token.type != TOKEN_TYPES['SEMICOLON']:
            expression = self.expression()
            
        self.eat(TOKEN_TYPES['SEMICOLON'])
        return ReturnStatement(expression)
    
    def break_statement(self):
        """
        break_statement : AND_I_OOP SEMICOLON
        """
        self.eat(TOKEN_TYPES['AND_I_OOP'])
        self.eat(TOKEN_TYPES['SEMICOLON'])
        return BreakStatement()
    
    def continue_statement(self):
        """
        continue_statement : AS_IF SEMICOLON
        """
        self.eat(TOKEN_TYPES['AS_IF'])
        self.eat(TOKEN_TYPES['SEMICOLON'])
        return ContinueStatement()
    
    def block_statement(self):
        """
        block_statement : LETS_GO statement_list YEET
        """
        self.eat(TOKEN_TYPES['LETS_GO'])
        statements = self.statement_list()
        self.eat(TOKEN_TYPES['YEET'])
        return BlockStatement(statements)
    
    def expression_statement(self):
        """
        expression_statement : expression SEMICOLON
        """
        expr = self.expression()
        self.eat(TOKEN_TYPES['SEMICOLON'])
        return ExpressionStatement(expr)
    
    def expression(self):
        """
        expression : logical_or
        """
        return self.logical_or()
    
    def logical_or(self):
        """
        logical_or : logical_and (OR logical_and)*
        """
        node = self.logical_and()
        return node
    
    def logical_and(self):
        """
        logical_and : equality (AND equality)*
        """
        node = self.equality()
        return node
    
    def equality(self):
        """
        equality : comparison ((EQUALS | NOT_EQUALS) comparison)*
        """
        node = self.comparison()
        
        while self.current_token.type in (TOKEN_TYPES['EQUALS'], TOKEN_TYPES['NOT_EQUALS']):
            operator = self.current_token
            self.eat(operator.type)
            right = self.comparison()
            node = BinaryExpression(node, operator, right)
            
        return node
    
    def comparison(self):
        """
        comparison : addition ((GREATER_THAN | GREATER_EQUALS | LESS_THAN | LESS_EQUALS) addition)*
        """
        node = self.addition()
        
        while self.current_token.type in (TOKEN_TYPES['GREATER_THAN'], TOKEN_TYPES['GREATER_EQUALS'], 
                                         TOKEN_TYPES['LESS_THAN'], TOKEN_TYPES['LESS_EQUALS']):
            operator = self.current_token
            self.eat(operator.type)
            right = self.addition()
            node = BinaryExpression(node, operator, right)
            
        return node
    
    def addition(self):
        """
        addition : multiplication ((PLUS | MINUS) multiplication)*
        """
        node = self.multiplication()
        
        while self.current_token.type in (TOKEN_TYPES['PLUS'], TOKEN_TYPES['MINUS']):
            operator = self.current_token
            self.eat(operator.type)
            right = self.multiplication()
            node = BinaryExpression(node, operator, right)
            
        return node
    
    def multiplication(self):
        """
        multiplication : unary ((MULTIPLY | DIVIDE | MODULO) unary)*
        """
        node = self.unary()
        
        while self.current_token.type in (TOKEN_TYPES['MULTIPLY'], TOKEN_TYPES['DIVIDE'], TOKEN_TYPES['MODULO']):
            operator = self.current_token
            self.eat(operator.type)
            right = self.unary()
            node = BinaryExpression(node, operator, right)
            
        return node
    
    def unary(self):
        """
        unary : (PLUS | MINUS) unary | primary
        """
        if self.current_token.type in (TOKEN_TYPES['PLUS'], TOKEN_TYPES['MINUS']):
            operator = self.current_token
            self.eat(operator.type)
            operand = self.unary()
            return UnaryExpression(operator, operand)
        
        return self.primary()
    
    def primary(self):
        """
        primary : INTEGER
                | STRING
                | THIS_SLAPS
                | IM_DEAD
                | GHOST
                | IDENTIFIER (LPAREN arguments RPAREN)?
                | LPAREN expression RPAREN
        """
        token = self.current_token
        
        if token.type == TOKEN_TYPES['INTEGER']:
            self.eat(TOKEN_TYPES['INTEGER'])
            return LiteralExpression(token.value, 'INTEGER')
        
        elif token.type == TOKEN_TYPES['STRING']:
            self.eat(TOKEN_TYPES['STRING'])
            return LiteralExpression(token.value, 'STRING')
        
        elif token.type == TOKEN_TYPES['THIS_SLAPS']:
            self.eat(TOKEN_TYPES['THIS_SLAPS'])
            return LiteralExpression(True, 'BOOLEAN')
        
        elif token.type == TOKEN_TYPES['IM_DEAD']:
            self.eat(TOKEN_TYPES['IM_DEAD'])
            return LiteralExpression(False, 'BOOLEAN')
        
        elif token.type == TOKEN_TYPES['GHOST']:
            self.eat(TOKEN_TYPES['GHOST'])
            return LiteralExpression(None, 'NULL')
        
        elif token.type == TOKEN_TYPES['IDENTIFIER']:
            name = token.value
            self.eat(TOKEN_TYPES['IDENTIFIER'])
            
            # Check for function call
            if self.current_token.type == TOKEN_TYPES['LPAREN']:
                self.eat(TOKEN_TYPES['LPAREN'])
                
                # Arguments
                arguments = []
                if self.current_token.type != TOKEN_TYPES['RPAREN']:
                    arguments = self.arguments()
                    
                self.eat(TOKEN_TYPES['RPAREN'])
                return FunctionCallExpression(name, arguments)
            else:
                return VariableExpression(name)
        
        elif token.type == TOKEN_TYPES['LPAREN']:
            self.eat(TOKEN_TYPES['LPAREN'])
            expr = self.expression()
            self.eat(TOKEN_TYPES['RPAREN'])
            return expr
        
        else:
            self.error(f"Unexpected token: {token.type}")
    
    def arguments(self):
        """
        arguments : expression (COMMA expression)*
        """
        args = [self.expression()]
        
        while self.current_token.type == TOKEN_TYPES['COMMA']:
            self.eat(TOKEN_TYPES['COMMA'])
            args.append(self.expression())
            
        return args
