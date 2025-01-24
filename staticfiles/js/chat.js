function toggleChat() {
    const chatPopup = document.getElementById("chat-popup");
    if (chatPopup.style.display === "none" || !chatPopup.style.display) {
        chatPopup.style.display = "flex";
    } else {
        chatPopup.style.display = "none";
    }
}

function sendMessage() {
    const chatInput = document.getElementById("chat-input");
    const chatBody = document.getElementById("chat-body");
    const userMessage = chatInput.value.trim();

    if (userMessage === "") return;

    // Display user message
    const userMessageDiv = document.createElement("div");
    userMessageDiv.className = "message sent";
    userMessageDiv.innerText = userMessage;
    chatBody.appendChild(userMessageDiv);
    chatInput.value = "";

    // Scroll to the latest message
    chatBody.scrollTop = chatBody.scrollHeight;

    // Send message to backend
    fetch("/chat-response/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ message: userMessage }),
    })
        .then((response) => response.json())
        .then((data) => {
            // Display bot response
            const botMessageDiv = document.createElement("div");
            botMessageDiv.className = "message received";
            botMessageDiv.innerText = data.response;
            chatBody.appendChild(botMessageDiv);

            // Scroll to the latest message
            chatBody.scrollTop = chatBody.scrollHeight;
        })
        .catch(() => {
            const errorMessageDiv = document.createElement("div");
            errorMessageDiv.className = "message received";
            errorMessageDiv.innerText =
                "Sorry, I am having trouble responding right now. Please try again later.";
            chatBody.appendChild(errorMessageDiv);

            chatBody.scrollTop = chatBody.scrollHeight;
        });
}

function getCSRFToken() {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
    if (!csrfToken) {
        console.error("CSRF token not found in the DOM.");
    }
    return csrfToken;
}

