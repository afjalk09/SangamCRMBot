async function sendMessage() {

    const input = document.getElementById("user-input");

    const question = input.value;

    if (!question) return;

    addMessage(question, "user");

    input.value = "";

    const response = await fetch("/ask", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            question: question
        })
    });

    const data = await response.json();

    addMessage(data.response, "bot");
}


function addMessage(text, sender) {

    const chatBox = document.getElementById("chat-box");

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");

    messageDiv.classList.add(sender);

    messageDiv.innerText = text;

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}