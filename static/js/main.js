/**
 * VibeScript IDE Main Logic
 *
 * Handles the interaction between the UI and the VibeScript interpreter
 */

// Execute the code in the editor
function runCode(inputs = {}) {
  const code = getCode();
  const consoleOutput = document.getElementById('console-output');
  
  if (!consoleOutput) {
    console.error('Console output element not found');
    return;
  }
  
  // Clear previous output if this is the first run (no inputs)
  if (Object.keys(inputs).length === 0) {
    consoleOutput.innerHTML = '';
  }
  
  // Disable run button during execution
  const runButton = document.getElementById('run-button');
  if (runButton) {
    runButton.disabled = true;
    runButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Running...';
  }
  
  // Send code to server for execution
  fetch('/run', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      code: code,
      inputs: inputs 
    }),
  })
  .then(response => response.json())
  .then(data => {
    // Handle input request
    if (data.input_requested) {
      handleInputRequest(data.variable_name, inputs);
      return;
    }
    
    // Display output or error in console only
    if (data.error) {
      consoleOutput.innerHTML = `<div class="error-output"><i class="bi bi-exclamation-triangle-fill me-2"></i>${data.error}</div>`;
    } else if (data.output) {
      consoleOutput.innerHTML = `<div class="success-output">${data.output}</div>`;
    } else {
      consoleOutput.innerHTML = '<div class="success-output">Code executed successfully (no output)</div>';
    }
  })
  .catch(error => {
    // Handle network or other errors
    console.error('Error:', error);
    consoleOutput.innerHTML = `<div class="error-output"><i class="bi bi-exclamation-triangle-fill me-2"></i>Failed to execute code: ${error.message}</div>`;
  })
  .finally(() => {
    // Re-enable run button
    if (runButton) {
      runButton.disabled = false;
      runButton.innerHTML = '<i class="bi bi-play-fill me-2"></i>Run';
    }
  });
}

// Handle input requests from the interpreter
function handleInputRequest(variableName, currentInputs) {
  const consoleOutput = document.getElementById('console-output');
  
  // Create simple input prompt like a normal IDE
  const inputPrompt = document.createElement('div');
  inputPrompt.style.cssText = 'display: flex; align-items: center; padding: 5px 0; color: #d4d4d4;';
  inputPrompt.innerHTML = `
    <span style="margin-right: 10px;">${variableName}:</span>
    <input type="text" id="input-${variableName}" style="flex: 1; padding: 5px; background: #1e1e1e; border: 1px solid #3c3c3c; color: #d4d4d4; border-radius: 3px; max-width: 200px;" placeholder="Enter value..." />
  `;
  
  consoleOutput.appendChild(inputPrompt);
  
  // Focus on the input field
  setTimeout(() => {
    const inputField = document.getElementById(`input-${variableName}`);
    if (inputField) {
      inputField.focus();
      
      // Handle Enter key
      inputField.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
          submitInput(variableName);
        }
      });
    }
  }, 100);
}

// Submit input value and continue execution
function submitInput(variableName) {
  const inputField = document.getElementById(`input-${variableName}`);
  if (!inputField) return;
  
  const value = inputField.value.trim();
  if (!value) {
    alert('Please enter a value!');
    return;
  }
  
  // Remove the input prompt
  const inputPrompt = inputField.closest('div');
  if (inputPrompt) {
    inputPrompt.remove();
  }
  
  // Continue execution with the input - no display of input value
  const inputs = {};
  inputs[variableName] = value;
  
  runCode(inputs);
}

// Load an example file
function loadExample(exampleName) {
  const consoleOutput = document.getElementById('console-output');
  
  fetch(`/examples/${exampleName}`)
    .then(response => response.json())
    .then(data => {
      if (data.code) {
        setCode(data.code);
        // Clear console when loading new example
        if (consoleOutput) {
          consoleOutput.innerHTML = '<div class="success-output">Example loaded successfully!</div>';
        }
      } else if (data.error) {
        if (consoleOutput) {
          consoleOutput.innerHTML = `<div class="error-output"><i class="bi bi-exclamation-triangle-fill me-2"></i>${data.error}</div>`;
        }
      }
    })
    .catch(error => {
      console.error('Error loading example:', error);
      if (consoleOutput) {
        consoleOutput.innerHTML = `<div class="error-output"><i class="bi bi-exclamation-triangle-fill me-2"></i>Failed to load example: ${error.message}</div>`;
      }
    });
}

// Setup the examples dropdown
document.addEventListener('DOMContentLoaded', function() {
  console.log('Setting up VibeScript IDE...');
  
  // Setup example links
  const exampleLinks = document.querySelectorAll('.example-link');
  console.log(`Found ${exampleLinks.length} example links`);
  
  exampleLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const exampleName = this.getAttribute('data-example');
      console.log(`Loading example: ${exampleName}`);
      loadExample(exampleName);
    });
  });
  
  // Test initial console output
  const consoleOutput = document.getElementById('console-output');
  if (consoleOutput) {
    consoleOutput.innerHTML = '<div style="color: #a0a0a0;">Ready to run VibeScript code! Click an example or write your own code.</div>';
  }
  
  console.log('VibeScript IDE setup complete!');
});
