document.addEventListener("DOMContentLoaded", () => {
  const chatMessages = document.getElementById("chat-messages")
  const userInput = document.getElementById("user-input")
  const sendButton = document.getElementById("send-button")
  const newChatButton = document.querySelector(".new-chat-btn")

  // Auto-resize textarea as user types
  userInput.addEventListener("input", function () {
    this.style.height = "auto"
    this.style.height = this.scrollHeight + "px"
  })

  // Send message when user clicks send button
  sendButton.addEventListener("click", sendMessage)

  // Send message when user presses Enter (but allow Shift+Enter for new lines)
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  })

  // Clear chat when user clicks new chat button
  newChatButton.addEventListener("click", () => {
    // Keep only the first welcome message
    while (chatMessages.children.length > 1) {
      chatMessages.removeChild(chatMessages.lastChild)
    }
    userInput.value = ""
    userInput.style.height = "auto"
  })


  async function sendMessageToBackend(userMessage) {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage })
    });
    const data = await response.json();
    return data.reply;
  }

  async function sendMessage() {
    const message = userInput.value.trim()
    if (message === "") return

    // Add user message to chat
    addUserMessage(message)

    // Clear input
    userInput.value = ""
    userInput.style.height = "auto"

    // Show typing indicator
    const typingIndicator = document.createElement("div")
    typingIndicator.className = "message assistant-message typing-indicator"
    typingIndicator.innerHTML = `
      <div class="message-avatar">
        <img src="psu-icon.png" alt="PSU Assistant" class="avatar-img">
      </div>
      <div class="message-content">
        <p>Typing...</p>
      </div>
    `
    chatMessages.appendChild(typingIndicator)
    chatMessages.scrollTop = chatMessages.scrollHeight

    // Call backend and display response
    try {
      const response = await sendMessageToBackend(message)
      chatMessages.removeChild(typingIndicator)
      addAssistantMessage(response)
    } catch (error) {
      chatMessages.removeChild(typingIndicator)
      addAssistantMessage("Sorry, there was an error connecting to the server.")
    }
  }

  // function sendMessage() {
  //   const message = userInput.value.trim()
  //   if (message === "") return

  //   // Add user message to chat
  //   addUserMessage(message)

  //   // Clear input
  //   userInput.value = ""
  //   userInput.style.height = "auto"

  //   // Simulate AI response (in a real app, this would be an API call)
  //   simulateResponse(message)
  // }

  function addUserMessage(message) {
    const userMessageDiv = document.createElement("div")
    userMessageDiv.className = "message user-message"
    userMessageDiv.innerHTML = `
            <div class="message-content">
                <p>${escapeHTML(message)}</p>
            </div>
        `
    chatMessages.appendChild(userMessageDiv)
    chatMessages.scrollTop = chatMessages.scrollHeight
  }

  function addAssistantMessage(message) {
    const assistantMessageDiv = document.createElement("div")
    assistantMessageDiv.className = "message assistant-message"
    assistantMessageDiv.innerHTML = `
            <div class="message-avatar">
                <img src="psu-icon.png" alt="PSU Assistant" class="avatar-img">
            </div>
            <div class="message-content">
                <p>${message}</p>
            </div>
        `
    chatMessages.appendChild(assistantMessageDiv)
    chatMessages.scrollTop = chatMessages.scrollHeight
  }

  // function simulateResponse(userMessage) {
  //   // Show typing indicator
  //   const typingIndicator = document.createElement("div")
  //   typingIndicator.className = "message assistant-message typing-indicator"
  //   typingIndicator.innerHTML = `
  //           <div class="message-avatar">
  //               <img src="psu-icon.png" alt="PSU Assistant" class="avatar-img">
  //           </div>
  //           <div class="message-content">
  //               <p>Typing...</p>
  //           </div>
  //       `
  //   chatMessages.appendChild(typingIndicator)
  //   chatMessages.scrollTop = chatMessages.scrollHeight

  //   // Simulate AI thinking time
  //   setTimeout(
  //     () => {
  //       // Remove typing indicator
  //       chatMessages.removeChild(typingIndicator)

  //       // Generate a response based on user message
  //       const response = generateResponse(userMessage)

  //       // Add AI response to chat
  //       addAssistantMessage(response)
  //     },
  //     1000 + Math.random() * 1000,
  //   ) // Random delay between 1-2 seconds
  // }

  // function generateResponse(userMessage) {
  //   // This is a simple rule-based response system
  //   // In a real application, this would be replaced with an actual AI service
  //   userMessage = userMessage.toLowerCase()

  //   if (userMessage.includes("hello") || userMessage.includes("hi") || userMessage.includes("hey")) {
  //     return "Hello! How can I help you with Portland State University today?"
  //   } else if (userMessage.includes("course") || userMessage.includes("class")) {
  //     return "PSU offers a wide range of courses across various disciplines. You can browse courses through the PSU Bulletin or Banweb. Would you like information about a specific department or program?"
  //   } else if (userMessage.includes("registration") || userMessage.includes("enroll")) {
  //     return "Course registration at PSU is done through Banweb. The registration dates depend on your class standing. Current students can check their registration date in Banweb. Would you like to know more about the registration process?"
  //   } else if (
  //     userMessage.includes("financial aid") ||
  //     userMessage.includes("scholarship") ||
  //     userMessage.includes("tuition")
  //   ) {
  //     return "PSU offers various financial aid options including scholarships, grants, loans, and work-study. You can apply for financial aid by submitting the FAFSA. The Office of Student Financial Aid can provide personalized assistance with your financial aid questions."
  //   } else if (
  //     userMessage.includes("housing") ||
  //     userMessage.includes("dorm") ||
  //     userMessage.includes("live on campus")
  //   ) {
  //     return "PSU offers several on-campus housing options including traditional residence halls and apartment-style living. University Housing and Residence Life manages all on-campus housing. Would you like information about a specific residence hall?"
  //   } else if (userMessage.includes("campus") || userMessage.includes("building") || userMessage.includes("location")) {
  //     return "PSU's main campus is located in downtown Portland. The campus includes academic buildings, residence halls, recreational facilities, and more. You can find campus maps on the PSU website. Is there a specific building you're looking for?"
  //   } else if (userMessage.includes("deadline") || userMessage.includes("calendar") || userMessage.includes("date")) {
  //     return "Important academic dates and deadlines can be found on the PSU Academic Calendar. This includes registration dates, tuition deadlines, holidays, and final exam schedules. The current academic calendar is available on the PSU website."
  //   } else if (
  //     userMessage.includes("club") ||
  //     userMessage.includes("organization") ||
  //     userMessage.includes("activity")
  //   ) {
  //     return "PSU has over 150 student clubs and organizations covering a wide range of interests including academic, cultural, recreational, and professional. Student Activities and Leadership Programs (SALP) oversees these organizations. Would you like information about a specific type of club?"
  //   } else if (userMessage.includes("thank")) {
  //     return "You're welcome! If you have any other questions about Portland State University, feel free to ask."
  //   } else {
  //     return "I'm here to help with information about Portland State University. You can ask me about courses, registration, campus facilities, financial aid, housing, academic deadlines, student clubs, and more. How can I assist you today?"
  //   }
  // }

  // Helper function to escape HTML to prevent XSS
  function escapeHTML(str) {
    return str.replace(
      /[&<>'"]/g,
      (tag) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          "'": "&#39;",
          '"': "&quot;",
        })[tag],
    )
  }
})
