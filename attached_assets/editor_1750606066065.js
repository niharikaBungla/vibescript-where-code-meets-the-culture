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
  document.getElementById('run-button').addEventListener('click', function() {
    runCode();
  });
  
  // Setup clear console button
  document.getElementById('clear-console').addEventListener('click', function() {
    document.getElementById('console-output').textContent = '';
    document.getElementById('error-container').innerHTML = '';
  });
  
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
    
    // Add line numbering visually (simple implementation)
    codeArea.addEventListener('scroll', updateLineHighlighting);
    codeArea.addEventListener('input', updateLineHighlighting);
    
    // Initial line highlighting
    setTimeout(updateLineHighlighting, 100);
  }
});

// Function to update line highlighting (provides a more VS Code feel)
function updateLineHighlighting() {
  const codeArea = document.getElementById('code-editor-area');
  if (!codeArea) return;
  
  // Update current line highlighting
  const lines = codeArea.value.split('\n');
  const pos = codeArea.selectionStart;
  let currentLine = 0;
  let charCount = 0;
  
  for (let i = 0; i < lines.length; i++) {
    charCount += lines[i].length + 1; // +1 for the newline
    if (charCount > pos) {
      currentLine = i;
      break;
    }
  }
  
  // Visual feedback for current line (VS Code style)
  codeArea.style.background = '#1e1e1e';
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
