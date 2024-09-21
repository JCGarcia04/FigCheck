/*function showGrammarChecker() {
    var section = document.getElementById('GrammarChecker');
    if (section.classList.contains('hidden')) {
        section.classList.remove('hidden');
        section.style.display = 'block'; // Ensure it's visible
    } else {
        section.classList.add('hidden');
    }
}*/

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

document.getElementById('submitBtn').addEventListener('click', function() {
    const textInput = document.getElementById('grammarTextarea').value;

    fetch('/get_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Specify content type as JSON
        },
        body: JSON.stringify({ text_input: textInput })  // Send data as JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Handle and display the result in the frontend
        document.getElementById('result').innerHTML = data.highlighted_text;
    })
    .catch(error => console.error('Error:', error));
});

// window.onload = function() {
//     let timeout = null;
//     const suggestionsHeader = document.getElementById('suggestionsHeader');
//     const suggestionsContent = document.getElementById('suggestionsContent');

//     document.getElementById('grammarTextarea').addEventListener('input', function() {
//         clearTimeout(timeout);
//         timeout = setTimeout(async function() {
//             const formData = new FormData(document.getElementById('grammarForm'));
//             try {
//                 const response = await fetch('/get_text', {
//                     method: 'POST',
//                     body: formData
//                 });
                
//                 // Check if response is OK
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }

//                 const result = await response.json();
//                 console.log('Response:', result); // Logging the server response

//                 let output = '';
//                 if (result.highlighted_text) {
//                     output = result.highlighted_text;  // Add highlighted text with error spans
//                 } else {
//                     output = '<p>No suggestions. Your text is grammatically correct!</p>';
//                 }

//                 document.getElementById('result').innerHTML = output;

//                 // Clear previous suggestions
//                 suggestionsContent.innerHTML = '';
//                 suggestionsHeader.classList.add('hidden');  // Hide suggestions header

//                 // If there are any errors, display them and make suggestions clickable
//                 if (result.errors) {
//                     suggestionsHeader.classList.remove('hidden');  // Show suggestions header
//                     result.errors.forEach(error => {
//                         const errorElement = document.createElement('div');
//                         errorElement.classList.add('error-item');
//                         errorElement.innerText = `Error: ${error.text} - Suggestions: ${error.suggestions.join(', ')}`;
                        
//                         // Add an event listener to each error element
//                         errorElement.addEventListener('click', function() {
//                             alert(`Suggestions for "${error.text}": ${error.suggestions.join(', ')}`);
//                         });

//                         suggestionsContent.appendChild(errorElement);
//                     });
//                 }

//             } catch (error) {
//                 if (error.message === 'Failed to fetch') {
//                     console.error('Network or server error, unable to reach the server:', error);
//                     document.getElementById('result').innerText = 'Could not reach the server. Please check your network connection.';
//                 } else {
//                     console.error('There was a problem with the fetch operation:', error);
//                     document.getElementById('result').innerText = 'Error processing request. Please try again.';
//                 }
//             }
//         }, 1000);  // Delay of 1 second after typing stops
//     });
// };


