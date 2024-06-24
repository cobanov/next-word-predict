let currentSuggestions = [];

async function sendText() {
    let text = document.getElementById("inputText").value.trim();
    if (text.length === 0) return;

    try {
        let response = await fetch("http://localhost:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: text }),
        });
        let data = await response.json();
        currentSuggestions = data.suggestions;
        updateSuggestions();
    } catch (error) {
        console.error('Error fetching suggestions:', error);
    }
}

function updateSuggestions() {
    let suggestions = document.getElementById("suggestions");
    suggestions.innerHTML = "";
    currentSuggestions.forEach(suggestion => {
        let li = document.createElement("li");
        li.textContent = suggestion;
        li.onclick = () => addSuggestion(suggestion);
        suggestions.appendChild(li);
    });
}

function checkSpace(event) {
    if (event.key === " ") {
        sendText();
    }
}

function checkTab(event) {
    if (event.key === "Tab") {
        event.preventDefault();
        addFirstSuggestion();
    }
}

function addFirstSuggestion() {
    if (currentSuggestions.length > 0) {
        let inputText = document.getElementById("inputText");
        inputText.value = inputText.value.trim() + " " + currentSuggestions[0];
        inputText.focus();
        sendText();
    }
}

function addSuggestion(suggestion) {
    let inputText = document.getElementById("inputText");
    inputText.value = inputText.value.trim() + " " + suggestion;
    inputText.focus();
    sendText();
}
