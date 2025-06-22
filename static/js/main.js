/**
 * VibeScript IDE Main Logic
 *
 * Handles the interaction between the UI and the VibeScript interpreter
 */

// Execute the code in the editor
function runCode() {
  const code = getCode();
  const consoleOutput = document.getElementById('console-output');
  
  if (!consoleOutput) {
    console.error('Console output element not found');
    return;
  }
  
  // Clear previous output
  consoleOutput.innerHTML = '';
  
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
    body: JSON.stringify({ code: code }),
  })
  .then(response => response.json())
  .then(data => {
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
