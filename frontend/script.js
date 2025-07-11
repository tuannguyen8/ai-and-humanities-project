document.addEventListener("DOMContentLoaded", () => {
  const chatMessages = document.getElementById("chat-messages");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const newChatButton = document.querySelector(".new-chat-btn");

  // Auto-resize textarea as user types
  userInput.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
  });

  // Send message when user clicks send button
  sendButton.addEventListener("click", sendMessage);

  // Send message when user presses Enter (but allow Shift+Enter for new lines)
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Clear chat when user clicks new chat button
  newChatButton.addEventListener("click", () => {
    while (chatMessages.children.length > 1) {
      chatMessages.removeChild(chatMessages.lastChild);
    }
    userInput.value = "";
    userInput.style.height = "auto";
  });

  async function sendMessageToBackend(userMessage) {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage }),
    });
    const data = await response.json();
    return data.reply;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;

    addUserMessage(message);
    userInput.value = "";
    userInput.style.height = "auto";

    showTypingIndicator();

    setTimeout(async () => {
      try {
        const reply = await sendMessageToBackend(message);
        removeTypingIndicator();
        addAssistantMessage(reply);
      } catch (error) {
        removeTypingIndicator();
        addAssistantMessage("Sorry, there was an error connecting to the server.");
      }
    }, 1500);
  }

  function showTypingIndicator() {
    const typingIndicator = document.createElement("div");
    typingIndicator.className = "message assistant-message typing-indicator";
    typingIndicator.innerHTML = `
      <div class="message-avatar">
        <img src="psu-icon.png" alt="PSU Assistant" class="avatar-img">
      </div>
      <div class="message-content">
        <p><span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></p>
      </div>
    `;
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function removeTypingIndicator() {
    const typing = document.querySelector(".typing-indicator");
    if (typing) chatMessages.removeChild(typing);
  }

  function addUserMessage(message) {
    const userMessageDiv = document.createElement("div");
    userMessageDiv.className = "message user-message";
    userMessageDiv.innerHTML = `
      <div class="message-content">
        <p>${escapeHTML(message)}</p>
      </div>
    `;
    chatMessages.appendChild(userMessageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function addAssistantMessage(htmlMessage) {
    const assistantMessageDiv = document.createElement("div");
    assistantMessageDiv.className = "message assistant-message";
    assistantMessageDiv.innerHTML = `
      <div class="message-avatar">
        <img src="psu-icon.png" alt="PSU Assistant" class="avatar-img">
      </div>
      <div class="message-content">
        ${htmlMessage}
      </div>
    `;
    chatMessages.appendChild(assistantMessageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, (tag) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "'": "&#39;",
      '"': "&quot;",
    }[tag]));
  }

  // Show sample questions when a sidebar topic is clicked
  const capabilityItems = document.querySelectorAll(".capabilities-list li");

  const sampleQuestionsMap = {
    academic: [
      "How do I register for classes?",
      "Where can I find the course schedule?",
      "When does registration open?",
      "How do I meet with an academic advisor?",
      "What are the degree requirements for CS?",
      "Can I change my major?"
    ],
    admission: [
      "What are the admission requirements for first-year undergraduate students at PSU?",
      "When is the application deadline for the fall term at Portland State University?",
      "How do I check the status of my admission application to PSU?"
    ],
    athletic: [
      "What NCAA division does Portland State University compete in?",
      "How can students get tickets to PSU Vikings games?",
      "Are there opportunities to join intramural or club sports at PSU?"
    ],
    studentlife: [
      "How can I join a student club?",
      "What clubs are available at PSU?",
      "Are there professional organizations on campus?"
    ],
    research: [
      "What types of research opportunities are available for undergraduate students at PSU?",
      "How can I get involved in faculty-led research projects at Portland State University?",
      "Does PSU offer funding or grants for student research initiatives?"
    ],
    about: [
      "Where is the Engineering Building?",
      "How do I get to Smith Memorial Student Union?",
      "Is there a campus map available?"
    ],
    contact: [
      "How do I contact the admissions office at Portland State University?",
      "Is there a general phone number or email for student support services at PSU?",
      "Who should I reach out to for questions about financial aid at PSU?"
    ]
  };

  capabilityItems.forEach((item) => {
    const topic = item.getAttribute("data-topic");
    item.addEventListener("click", () => {
      const questions = sampleQuestionsMap[topic];
      if (questions) {
        showTypingIndicator();
        setTimeout(() => {
          removeTypingIndicator();
          const listItems = questions.map(q => `<li>${q}</li>`).join("");
          const html = `
            <div class="response-intro">Here are some questions you can ask about <strong>${item.innerText.trim()}</strong>:</div>
            <ul class="question-list">${listItems}</ul>
          `;
          addAssistantMessage(html);
        }, 1000);
      }
    });
  });
});
