document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const inputBox = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    sendButton.addEventListener('click', async () => {
        const userMessage = inputBox.value.trim();
        if (!userMessage) return;

        appendMessage('You', userMessage);
        inputBox.value = '';

        // Send user input to backend
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage })
        });

        const data = await response.json();
        appendMessage('Bot', data.reply);
    });

    function appendMessage(sender, text) {
        const msg = document.createElement('div');
        msg.classList.add('message');
        msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
