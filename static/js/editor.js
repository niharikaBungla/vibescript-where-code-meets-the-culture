/**
 * VibeScript Editor Configuration
 * 
 * Sets up the CodeMirror editor with custom mode and theme for VibeScript syntax
 */

// Define CodeMirror mode for VibeScript
CodeMirror.defineMode("vibescript", function() {
  // VibeScript keywords
  const keywords = [
    'spill_the_tea', 'vibe_check', 'no_cap', 'cap', 'lowkey', 'highkey',
    'rizz_up', 'slay', 'lets_go', 'yeet', 'and_i_oop', 'as_if',
    'rent_free', 'main_character'
  ];

  // VibeScript data types
  const dataTypes = [
    'lit', 'tea', 'mood', 'stan'
  ];

  // VibeScript constants
  const constants = [
    'this_slaps', 'im_dead', 'ghost'
  ];

  return {
    startState: function() {
      return {
        inString: false,
        inComment: false,
        stringType: null,
      };
    },
    token: function(stream, state) {
      // Handle comments (// style)
      if (stream.match("//")) {
        stream.skipToEnd();
        return "comment";
      }

      // Handle strings
      if (state.inString) {
        if (stream.skipTo('"')) {
          stream.next();
          state.inString = false;
        } else {
          stream.skipToEnd();
        }
        return "string";
      }

      if (stream.peek() === '"') {
        stream.next();
        state.inString = true;
        return "string";
      }

      // Handle keywords, data types, and constants
      if (stream.eatSpace()) return null;

      if (stream.match(/^[a-zA-Z_][a-zA-Z0-9_]*/)) {
        const word = stream.current();
        if (keywords.includes(word)) return "keyword";
        if (dataTypes.includes(word)) return "type";
        if (constants.includes(word)) return "atom";
        return "variable";
      }

      // Handle numbers
      if (stream.match(/^[0-9]+/)) {
        return "number";
      }

      // Handle operators and other characters
      stream.next();
      return null;
    }
  };
});

// Create custom theme based on the VibeScript color scheme
CodeMirror.defineOption("theme", "vibescript", CodeMirror.defaults.theme);

// Simple VS Code-like editor setup
document.addEventListener('DOMContentLoaded', function() {
  // Set up run button
  const runButton = document.getElementById('run-button');
  if (runButton) {
    runButton.addEventListener('click', function() {
      runCode();
    });
  }
  
  // Setup clear console button
  const clearButton = document.getElementById('clear-console');
  if (clearButton) {
    clearButton.addEventListener('click', function() {
      clearConsole();
    });
  }
  
  // Setup keyboard shortcut (Ctrl+Enter to run code)
  const codeArea = document.getElementById('code-editor-area');
  if (codeArea) {
    codeArea.addEventListener('keydown', function(e) {
      // Ctrl+Enter or Cmd+Enter
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        runCode();
      }
      
      // Tab key for indentation
      if (e.key === 'Tab') {
        e.preventDefault();
        
        // Insert 2 spaces instead of tab
        const start = this.selectionStart;
        const end = this.selectionEnd;
        
        this.value = this.value.substring(0, start) + '  ' + this.value.substring(end);
        
        // Set cursor position after the inserted spaces
        this.selectionStart = this.selectionEnd = start + 2;
      }
    });
    
    // Add line numbering functionality
    codeArea.addEventListener('scroll', updateLineNumbers);
    codeArea.addEventListener('input', updateLineNumbers);
    
    // Initial line numbering
    setTimeout(updateLineNumbers, 100);
  }
});

// Function to update line numbers
function updateLineNumbers() {
  const codeArea = document.getElementById('code-editor-area');
  const lineNumbersDiv = document.getElementById('line-numbers');
  
  if (!codeArea || !lineNumbersDiv) return;
  
  // Count lines in the textarea
  const lines = codeArea.value.split('\n');
  const lineCount = lines.length;
  
  // Generate line numbers with exact spacing to match textarea
  let lineNumbers = [];
  for (let i = 1; i <= Math.max(lineCount, 20); i++) {
    lineNumbers.push(i.toString());
  }
  
  // Use the same line spacing as textarea
  lineNumbersDiv.innerHTML = lineNumbers.join('<br>');
  
  // Sync scroll position exactly
  lineNumbersDiv.scrollTop = codeArea.scrollTop;
  
  // Ensure same padding and margin as textarea
  const codeAreaStyle = window.getComputedStyle(codeArea);
  lineNumbersDiv.style.paddingTop = codeAreaStyle.paddingTop;
}

// Function to get the current code from the editor
function getCode() {
  const codeArea = document.getElementById('code-editor-area');
  if (codeArea) {
    return codeArea.value;
  }
  return ''; // Fallback
}

// Function to set code in the editor
function setCode(code) {
  if (!code) return;
  
  try {
    const codeArea = document.getElementById('code-editor-area');
    if (codeArea) {
      codeArea.value = code;
    }
  } catch (error) {
    console.error("Error setting code:", error);
  }
}

// Function to clear the console
function clearConsole() {
  const consoleOutput = document.getElementById('console-output');
  if (consoleOutput) {
    consoleOutput.textContent = '';
    consoleOutput.innerHTML = '';
  }
}
