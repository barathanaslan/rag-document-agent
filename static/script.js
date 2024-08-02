const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const chatHistory = document.getElementById('chat-history');

sendButton.addEventListener('click', sendMessage);

async function sendMessage() {
    const userMessage = userInput.value;
    userInput.value = ''; // Clear the input

    displayMessage(userMessage, 'user'); // Display user's message

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query_text: userMessage })
        });

        const data = await response.json();
        displayMessage(data.response, 'bot'); // Display bot's response
    } catch (error) {
        console.error("Error fetching data:", error);
        displayMessage('An error occurred. Please try again.', 'bot');
    }
}

function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to bottom
}