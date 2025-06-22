import os
import logging
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
        code = request.json.get('code', '')
        
        if not code.strip():
            return jsonify({'output': '', 'error': 'No code to execute!'})
        
        # Process the code through our interpreter
        lexer = Lexer(code)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        
        # Capture the output using the interpreter's output collector
        result = interpreter.interpret()
        
        return jsonify({
            'output': interpreter.output,
            'error': None
        })
    
    except Exception as e:
        logger.exception("Error executing code")
        error_message = str(e)
        return jsonify({
            'output': '',
            'error': error_message
        })

@app.route('/examples/<example_name>')
def get_example(example_name):
    """Load an example from the examples directory"""
    try:
        file_path = f"examples/{example_name}.vs"
        with open(file_path, 'r') as file:
            content = file.read()
        return jsonify({'code': content, 'error': None})
    except Exception as e:
        logger.exception(f"Error loading example {example_name}")
        return jsonify({'code': '', 'error': f"Could not load example: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
