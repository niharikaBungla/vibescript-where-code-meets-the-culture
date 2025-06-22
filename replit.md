# VibeScript IDE

## Overview

VibeScript is a Gen Z-inspired programming language with a web-based IDE. The project consists of a Flask web application that provides an online code editor for writing and executing VibeScript code. The language uses modern slang terms as keywords (e.g., `spill_the_tea` for print, `no_cap` for if statements) to make programming more culturally relevant and engaging for younger developers.

## System Architecture

### Frontend Architecture
- **Web Interface**: HTML5 template with Bootstrap 5 dark theme
- **Code Editor**: CodeMirror integration with custom VibeScript syntax highlighting
- **UI Framework**: Bootstrap 5 with custom CSS variables for theming
- **JavaScript**: Vanilla JavaScript for IDE functionality and API communication

### Backend Architecture
- **Web Framework**: Flask application serving both the IDE interface and code execution API
- **Language Implementation**: Custom interpreter built with lexer, parser, and interpreter components
- **Request Handling**: RESTful API endpoint for code execution (`/run`)
- **Error Handling**: Comprehensive error catching and user-friendly error messages

### Language Architecture
- **Lexer**: Tokenizes VibeScript source code into meaningful tokens
- **Parser**: Builds Abstract Syntax Tree (AST) from tokens using recursive descent parsing
- **Interpreter**: Executes the AST with symbol table management for variables and functions

## Key Components

### Core Language Components
1. **Lexer** (`vibescript/lexer.py`): Tokenizes source code with support for keywords, operators, strings, and comments
2. **Parser** (`vibescript/parser.py`): Builds AST nodes for statements, expressions, and control flow
3. **Interpreter** (`vibescript/interpreter.py`): Executes code with symbol table for variable/function management
4. **Grammar** (`vibescript/grammar.py`): Defines token types and language keywords

### Web Application Components
1. **Flask App** (`app.py`): Main web server with routes for IDE and code execution
2. **HTML Template** (`templates/index.html`): Web-based IDE interface
3. **Static Assets**: CSS styling and JavaScript for editor functionality
4. **Example Programs**: Sample VibeScript code demonstrating language features

### VibeScript Language Features
- **Variables**: `lit` (integer), `tea` (string), `mood` (boolean), `stan` (array)
- **Control Flow**: `no_cap` (if), `cap` (else), `lowkey` (while), `highkey` (for)
- **Functions**: `rizz_up` (function definition), `slay` (return)
- **I/O**: `spill_the_tea` (print), `vibe_check` (input)
- **Constants**: `this_slaps` (true), `im_dead` (false), `ghost` (null)

## Data Flow

1. **Code Input**: User writes VibeScript code in the CodeMirror editor
2. **Execution Request**: JavaScript sends POST request to `/run` endpoint with code
3. **Lexical Analysis**: Lexer tokenizes the source code
4. **Parsing**: Parser builds AST from tokens
5. **Interpretation**: Interpreter executes AST and captures output
6. **Response**: Flask returns execution results (output or errors) as JSON
7. **Display**: JavaScript updates the console output area with results

## External Dependencies

### Python Packages
- **Flask 3.1.1+**: Web framework for serving the IDE and handling requests
- **Gunicorn 23.0.0+**: WSGI HTTP server for production deployment
- **Email-validator 2.2.0+**: Email validation utilities
- **Flask-SQLAlchemy 3.1.1+**: Database ORM (configured but not actively used)
- **Psycopg2-binary 2.9.10+**: PostgreSQL adapter (available for future database features)

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme
- **Bootstrap Icons**: Icon library for UI elements
- **CodeMirror 5.65.13**: Code editor with syntax highlighting
- **Google Fonts**: Inter and Fira Code fonts for typography

## Deployment Strategy

### Replit Configuration
- **Runtime**: Python 3.11 with Nix package management
- **Production Server**: Gunicorn with autoscale deployment target
- **Development**: Flask development server with hot reload
- **Port Configuration**: Runs on port 5000 with proper binding

### Environment Setup
- **Package Management**: UV lock file for dependency resolution
- **System Dependencies**: OpenSSL and PostgreSQL packages via Nix
- **Session Security**: Configurable secret key via environment variables

## Changelog

- June 22, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.