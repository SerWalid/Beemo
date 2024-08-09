const chatbox = jQuery.noConflict();

chatbox(() => {
  chatbox(".chatbox-open").click(() => {
    chatbox(".chatbox-popup, .chatbox-close").fadeIn();
  });

  chatbox(".chatbox-close").click(() => {
    chatbox(".chatbox-popup, .chatbox-close").fadeOut();
  });

  chatbox(".chatbox-minimize").click(() => {
    chatbox(".chatbox-panel").fadeOut();
    chatbox(".chatbox-popup, .chatbox-open, .chatbox-close").fadeIn();
  });

  chatbox(".chatbox-panel-close").click(() => {
    chatbox(".chatbox-panel").fadeOut();
    chatbox(".chatbox-open").fadeIn();
  });

  // Function to send a message and receive a response
  function sendMessage(inputSelector, outputSelector) {
    const userInput = chatbox(inputSelector).val().trim();
    if (userInput === "") return;

    // Append user message to chat output
    chatbox(outputSelector).append('<div class="message message-user"><div class="message-content-container message-user-container"><div class="message-content">' + userInput + '</div></div></div>');

    // Clear input after sending message
    chatbox(inputSelector).val('');

    // Scroll to bottom of chat output
    chatbox(outputSelector).scrollTop(chatbox(outputSelector)[0].scrollHeight);

    // Send message to server and get response
    chatbox.ajax({
      url: '/get_response', // Replace with your server endpoint
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ prompt: userInput }),
      success: function(response) {
        // Append bot response to chat output
        chatbox(outputSelector).append('<div class="message message-bot"><div class="message-content-container message-bot-container"><div class="message-content">' + response.response + '</div></div></div>');

        // Scroll to bottom after appending bot response
        chatbox(outputSelector).scrollTop(chatbox(outputSelector)[0].scrollHeight);
      },
      error: function(error) {
        console.error('Error:', error);
      }
    });
  }

  // Event listener for sending messages from popup chat
  chatbox('#user-input-popup').keypress(function(e) {
    if (e.which === 13) {
      sendMessage('#user-input-popup', '#chat-output-popup');
      e.preventDefault(); // Prevent newline in textarea
    }
  });

  chatbox('.chatbox-popup__footer .fa-paper-plane').click(function() {
    sendMessage('#user-input-popup', '#chat-output-popup');
  });

  // Event listener for sending messages from panel chat
  chatbox('#user-input-panel').keypress(function(e) {
    if (e.which === 13) {
      sendMessage('#user-input-panel', '#chat-output-panel');
      e.preventDefault(); // Prevent newline in textarea
    }
  });

  chatbox('.chatbox-panel__footer .fa-paper-plane').click(function() {
    sendMessage('#user-input-panel', '#chat-output-panel');
  });

  // Event listener for the second button to open the chatbot
  chatbox("#read-more-button").click(() => {
    chatbox(".chatbox-popup, .chatbox-close").fadeIn();
  });
});
