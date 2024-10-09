document.addEventListener('DOMContentLoaded', function() {
    // Select the checkbox and the 'Try Now' link
    const checkBox = document.getElementById('check');
    const tryNowLink = document.querySelector('.nav ul li a[href="#GrammarChecker"]');

    // Add click event listener to the 'Try Now' link
    tryNowLink.addEventListener('click', function(event) {
        if (checkBox.checked) {
            checkBox.checked = false;
        }
    });
});

// Function to hide the menu after a link is clicked
document.querySelectorAll('.nav ul li a').forEach(link => {
    link.addEventListener('click', function () {
        document.getElementById('check').checked = false;
        document.querySelector('.home-content').style.display = 'block';
    });
});

function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.classList.add('hidden');
    });

    // Show the target section
    const targetSection = document.getElementById(sectionId);
    targetSection.classList.remove('hidden');
}


let timeout = null;

document.getElementById('grammarTextarea').addEventListener('input', function () {
    clearTimeout(timeout);
    const textInput = this.value;

    // Check if the first letter is capitalized
    const isFirstLetterCapitalized = textInput.charAt(0) === textInput.charAt(0).toUpperCase();

    if (!isFirstLetterCapitalized && textInput.length > 0) {
        // Notify the user or take action if the first letter is not capitalized
        alert('Please start your sentence with a capitalized letter.');
        return; // Stop execution if the condition is not met
    }

    // Hide previous predictions and suggestions
    const predictionsContent = document.getElementById('predictionsContent');
    const suggestionsContent = document.getElementById('suggestionsContent');
    const suggestionsHeader = document.getElementById('suggestionsHeader');

    predictionsContent.innerHTML = '';
    suggestionsContent.innerHTML = '';
    suggestionsHeader.classList.add('hidden');

    // Show loading icon and set text to "Loading..."
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = 'flex';
        loadingElement.querySelector('p').textContent = 'Loading...';
    }

    // Log the input text before sending it
    console.log("Input Text:", textInput);

    timeout = setTimeout(async () => {
        try {
            const response = await fetch('/get_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text_input: textInput })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Log the received data for debugging
            console.log("Received Data:", data);

            // Check if there are any spelling errors
            const hasSpellingErrors = data.highlighted_text && data.highlighted_text.includes('error');

            if (hasSpellingErrors) {
                // Display only spell suggestions if there are errors
                predictionsContent.innerHTML = data.highlighted_text || 'No errors detected.'; 
            } else {
                // Display grammatical predictions if no spelling errors
                if (data.grammar_predictions && data.grammar_predictions.length) {
                    data.grammar_predictions.forEach((predictionArray) => {
                        const prediction = Array.isArray(predictionArray) ? predictionArray[0] : predictionArray;
                        let predictionText = '';
                        if (prediction === 0) {
                            predictionText = `Grammatically correct.<br>`;
                            predictionsContent.innerHTML += predictionText; 
                        } else {
                            predictionText = `Grammatical error detected.<br>`;

                            if (data.highlighted_text.includes(' ng ')) {
                                predictionText += 'Try changing to "nang".<br>';
                                data.highlighted_text = data.highlighted_text.replace('ng', '<span class="highlight">ng</span>');
                            } 
                            if (data.highlighted_text.includes(' nang ')) {
                                predictionText += 'Try changing to "ng".<br>';
                                data.highlighted_text = data.highlighted_text.replace('nang', '<span class="highlight">nang</span>');
                            } 
                            if (data.highlighted_text.includes(' raw ')) {
                                predictionText += 'Try changing to "daw".<br>';
                                data.highlighted_text = data.highlighted_text.replace('raw', '<span class="highlight">raw</span>');
                            } 
                            if (data.highlighted_text.includes(' daw ')) {
                                predictionText += 'Try changing to "raw".<br>';
                                data.highlighted_text = data.highlighted_text.replace('daw', '<span class="highlight">daw</span>');
                            } 
                            if (data.highlighted_text.includes(' rin ')) {
                                predictionText += 'Try changing to "din".<br>';
                                data.highlighted_text = data.highlighted_text.replace('rin', '<span class="highlight">rin</span>');
                            } 
                            if (data.highlighted_text.includes(' din ')) {
                                predictionText += 'Try changing to "rin".<br>';
                                data.highlighted_text = data.highlighted_text.replace('din', '<span class="highlight">din</span>');
                            }
                            if (data.highlighted_text.includes(' rito ')) {
                                predictionText += 'Try changing to "dito".<br>';
                                data.highlighted_text = data.highlighted_text.replace('rito', '<span class="highlight">rito</span>');
                            } 
                            if (data.highlighted_text.includes(' dito ')) {
                                predictionText += 'Try changing to "rito".<br>';
                                data.highlighted_text = data.highlighted_text.replace('dito', '<span class="highlight">dito</span>');
                            }
                            if (data.highlighted_text.includes(' roon ')) {
                                predictionText += 'Try changing to "doon".<br>';
                                data.highlighted_text = data.highlighted_text.replace('roon', '<span class="highlight">roon</span>');
                            } 
                            if (data.highlighted_text.includes(' doon ')) {
                                predictionText += 'Try changing to "roon".<br>';
                                data.highlighted_text = data.highlighted_text.replace('doon', '<span class="highlight">doon</span>');
                            }
                            predictionsContent.innerHTML += predictionText;
                            predictionsContent.innerHTML += `<p>${data.highlighted_text}</p>`;
                        }
                    });
                } else {
                    predictionsContent.innerHTML = 'No grammatical predictions available.';
                }
            }

            // Add click event listeners for highlighted errors (if any)
            document.querySelectorAll('.error').forEach(element => {
                element.addEventListener('click', function () {
                    const suggestions = this.getAttribute('data-suggestions').split(',<br>');
                    showSuggestions(suggestions, this);
                });
            });

        } catch (error) {
            console.error('Error:', error);
            predictionsContent.innerHTML = 'Error retrieving data. Maybe you forgot a period?.';
        } finally {
            // Change loading text to "Complete"
            loadingElement.querySelector('p').textContent = 'Complete';

            // Hide loading icon after a short delay
            setTimeout(() => {
                loadingElement.style.display = 'none';
            }, 500);
        }
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
