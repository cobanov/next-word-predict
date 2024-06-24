let currentSuggestions = [];

async function sendText() {
    let text = document.getElementById("inputText").value;
    let response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text }),
    });
    let data = await response.json();
    currentSuggestions = data.suggestions;
    let suggestions = document.getElementById("suggestions");
    suggestions.innerHTML = "";
    currentSuggestions.forEach(function(suggestion) {
        let li = document.createElement("li");
        li.textContent = suggestion;
        li.onclick = function() {
            addSuggestion(suggestion);
        };
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
        let text = inputText.value.trim();
        inputText.value = text + " " + currentSuggestions[0];
        inputText.focus();
    }
}

function addSuggestion(suggestion) {
    let inputText = document.getElementById("inputText");
    let text = inputText.value.trim();
    inputText.value = text + " " + suggestion;
    inputText.focus();
    sendText();
}
