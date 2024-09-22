document.addEventListener('DOMContentLoaded', function() {
    // Select the checkbox and the 'Try Now' link
    const checkBox = document.getElementById('check');
    const tryNowLink = document.querySelector('.nav ul li a[href="#GrammarChecker"]');

    // Add click event listener to the 'Try Now' link
    tryNowLink.addEventListener('click', function(event) {
        if (checkBox.checked) {
            checkBox.checked = false; // Uncheck the checkbox to hide the menu
        }
    });
});

// Function to hide the menu after a link is clicked
document.querySelectorAll('.nav ul li a').forEach(link => {
    link.addEventListener('click', function () {
        document.getElementById('check').checked = false; // Uncheck the checkbox to hide the menu
        document.querySelector('.home-content').style.display = 'block'; // Show the home-content again
    });
});

function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.classList.add('hidden');
        section.classList.remove('active-section');
    });

    // Show the target section
    const targetSection = document.getElementById(sectionId);
    targetSection.classList.remove('hidden');
    targetSection.classList.add('active-section');
}

let timeout = null;

document.getElementById('grammarTextarea').addEventListener('input', function() {
    clearTimeout(timeout);
    const textInput = this.value;

    // Hide previous predictions and suggestions
    const predictionsContent = document.getElementById('predictionsContent');
    const suggestionsContent = document.getElementById('suggestionsContent');
    const predictionsHeader = document.getElementById('predictionsHeader');
    const suggestionsHeader = document.getElementById('suggestionsHeader');

    predictionsContent.innerHTML = ''; // Clear previous results
    suggestionsContent.innerHTML = ''; 
    predictionsHeader.classList.add('hidden'); // Hide predictions header
    suggestionsHeader.classList.add('hidden'); // Hide suggestions header

    // Show loading icon and set text to "Loading..."
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = 'flex';
        loadingElement.querySelector('p').textContent = 'Loading...';
    } else {
        console.error("Loading element not found in the DOM.");
    }

    timeout = setTimeout(() => {
        fetch('/get_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text_input: textInput })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            // Display grammatical predictions
            if (data.grammar_predictions && data.grammar_predictions.length) {
                predictionsHeader.classList.remove('hidden');
                data.grammar_predictions.forEach((prediction, index) => {
                    const predictionText = prediction === 1 
                        ? `Sentence ${index + 1}: Grammatical error detected.<br>`
                        : `Sentence ${index + 1}: Sentence is grammatically correct.<br>`;
                    predictionsContent.innerHTML += predictionText;
                });
            } else {
                predictionsContent.innerHTML = 'No grammatical predictions available.';
            }

            // Display highlighted text
            suggestionsContent.innerHTML = data.highlighted_text || 'No errors detected.';

            // Add click event listeners for highlighted errors
            document.querySelectorAll('.error').forEach(element => {
                element.addEventListener('click', function() {
                    const suggestions = this.getAttribute('data-suggestions').split(', ');
                    showSuggestions(suggestions, this);
                });
            });
        })
        .catch(error => {
            console.error('Error:', error);
            predictionsContent.innerHTML = 'Error retrieving data. Maybe you forgot a period?.';
        })
        .finally(() => {
            // Change loading text to "Complete"
            loadingElement.querySelector('p').textContent = 'Complete';

            // Hide loading icon after a short delay
            loadingElement.style.display = 'none';
        });
    }, 1000);
});

// Function to show suggestions in a text box
function showSuggestions(suggestions, errorElement) {
    const suggestionBox = document.createElement('div');
    suggestionBox.className = 'suggestion-box';
    suggestionBox.innerHTML = `<strong>Suggestions:</strong><br>${suggestions.join('<br>')}`;

    // Position the suggestion box near the clicked error element
    const rect = errorElement.getBoundingClientRect();
    suggestionBox.style.position = 'absolute';
    suggestionBox.style.left = `${rect.left}px`;
    suggestionBox.style.top = `${rect.bottom}px`;

    document.body.appendChild(suggestionBox);
    suggestionBox.addEventListener('click', () => {
        document.body.removeChild(suggestionBox);
    });
}
