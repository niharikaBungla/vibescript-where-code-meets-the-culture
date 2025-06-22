import os
import logging
import traceback
from flask import Flask, render_template, request, jsonify
from vibescript.lexer import Lexer
from vibescript.parser import Parser
from vibescript.interpreter import Interpreter

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "vibescript_secret_key")

@app.route('/')
def index():
    """Render the main IDE page"""
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    """Execute VibeScript code and return the results"""
    try:
        # Get code from request
        data = request.get_json()
        code = data.get('code', '') if data else ''
        
        if not code.strip():
            return jsonify({'output': 'No code to execute!', 'error': None})
        
        logger.debug(f"Executing code: {code[:100]}...")
        
        # Process the code through our interpreter
        lexer = Lexer(code)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        
        # Capture the output using the interpreter's output collector
        interpreter.interpret()
        
        return jsonify({
            'output': interpreter.output.strip() if interpreter.output else 'Code executed successfully (no output)',
            'error': None
        })
    
    except Exception as e:
        logger.exception("Error executing code")
        error_message = str(e)
        # Format the error message to be more user-friendly
        if "line" in error_message.lower() or "column" in error_message.lower():
            formatted_error = f"Syntax Error: {error_message}"
        else:
            formatted_error = f"Runtime Error: {error_message}"
        
        return jsonify({
            'output': '',
            'error': formatted_error
        })

@app.route('/examples/<example_name>')
def get_example(example_name):
    """Load an example from the examples directory"""
    try:
        file_path = f"examples/{example_name}.vs"
        logger.debug(f"Loading example from: {file_path}")
        
        if not os.path.exists(file_path):
            logger.error(f"Example file not found: {file_path}")
            return jsonify({'code': '', 'error': f"Example '{example_name}' not found"})
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        logger.debug(f"Loaded example {example_name}: {len(content)} characters")
        return jsonify({'code': content, 'error': None})
        
    except Exception as e:
        logger.exception(f"Error loading example {example_name}")
        return jsonify({'code': '', 'error': f"Could not load example: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
