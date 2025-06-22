/**
 * VibeScript IDE Main Logic
 *
 * Handles the interaction between the UI and the VibeScript interpreter
 */

// Execute the code in the editor
function runCode() {
  const code = getCode();
  const consoleOutput = document.getElementById('console-output');
  const errorContainer = document.getElementById('error-container');
  
  // Clear previous output and errors
  consoleOutput.textContent = '';
  errorContainer.innerHTML = '';
  
  // Disable run button during execution
  const runButton = document.getElementById('run-button');
  runButton.disabled = true;
  runButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Running...';
  
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
    // Display output or error
    if (data.output) {
      consoleOutput.textContent = data.output;
    }
    
    if (data.error) {
      errorContainer.innerHTML = `
        <div class="error-message">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>
          ${data.error}
        </div>
      `;
    }
  })
  .catch(error => {
    // Handle network or other errors
    errorContainer.innerHTML = `
      <div class="error-message">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        Failed to execute code: ${error.message}
      </div>
    `;
  })
  .finally(() => {
    // Re-enable run button
    runButton.disabled = false;
    runButton.innerHTML = '<i class="bi bi-play-fill me-2"></i>Run';
  });
}

// Load an example file
function loadExample(exampleName) {
  fetch(`/examples/${exampleName}`)
    .then(response => response.json())
    .then(data => {
      if (data.code) {
        setCode(data.code);
      } else if (data.error) {
        document.getElementById('error-container').innerHTML = `
          <div class="error-message">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            ${data.error}
          </div>
        `;
      }
    })
    .catch(error => {
      document.getElementById('error-container').innerHTML = `
        <div class="error-message">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>
          Failed to load example: ${error.message}
        </div>
      `;
    });
}

// Setup the examples dropdown
document.addEventListener('DOMContentLoaded', function() {
  // Ensure codeEditor is fully initialized before we try to use it
  if (typeof window.codeEditor === 'undefined') {
    window.codeEditor = {
      getValue: function() {
        return document.getElementById('code-editor').textContent || '';
      },
      setValue: function(text) {
        if (text) {
          document.getElementById('code-editor').textContent = text;
        }
      }
    };
  }
  
  const exampleLinks = document.querySelectorAll('.example-link');
  exampleLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const exampleName = this.getAttribute('data-example');
      loadExample(exampleName);
    });
  });
});
