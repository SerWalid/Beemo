var messages = [], // array that holds the record of each string in chat
    lastUserMessage = "", // keeps track of the most recent input string from the user
    botName = 'BMO', // name of the chatbot
    userName = 'Client', // name of the user
    talking = true; // when false the speech function doesn't work

// this runs each time enter is pressed or send button is clicked.
function newEntry() {
    // if the message from the user isn't empty then run
    if (document.getElementById("chatbox").value != "") {
        // pulls the value from the chatbox and sets it to lastUserMessage
        lastUserMessage = document.getElementById("chatbox").value;
        // sets the chat box to be clear
        document.getElementById("chatbox").value = "";
        // adds the value of the chatbox to the array messages
        messages.push(`<span class="bold">${userName}:</span> ${lastUserMessage}`);
        // calls the function to get the chatbot's response
        getBotResponse(lastUserMessage);
    }
}

// function to get the chatbot's response from the Flask backend
function getBotResponse(userMessage) {
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({prompt: userMessage})
    })
    .then(response => response.json())
    .then(data => {
        let botMessage = data.response;
        // add the chatbot's name and message to the array messages
        messages.push(`<span class="bold">${botName}:</span> ${botMessage}`);
        // outputs the last few array elements of messages to html
        for (var i = 1; i < 8; i++) {
            if (messages[messages.length - i]) {
                let messageElement = document.getElementById("chatlog" + i);
                messageElement.innerHTML = messages[messages.length - i];
                if (messages[messages.length - i].includes(userName)) {
                    messageElement.className = "chatlog user-message";
                } else {
                    messageElement.className = "chatlog bot-message";
                }
            }
        }
        // says the message using the text to speech function
        Speech(botMessage);
    });
}

// text to Speech
function Speech(say) {
    if ('speechSynthesis' in window) {
        var utterance = new SpeechSynthesisUtterance(say);
        utterance.lang = 'en-US'; // Set language to English (US)
        speechSynthesis.speak(utterance);
    }
}

// runs the keypress() function when a key is pressed
document.onkeypress = keyPress;
// if the key pressed is 'enter' runs the function newEntry()
function keyPress(e) {
    var x = e || window.event;
    var key = (x.keyCode || x.which);
    if (key == 13 || key == 3) {
        // runs this function when enter is pressed
        newEntry();
    }
}

// clears the placeholder text in the chatbox
function placeHolder() {
    document.getElementById("chatbox").placeholder = "";
}
