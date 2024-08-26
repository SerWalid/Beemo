document
  .getElementById("chat-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const userInput = document.getElementById("user-input").value.trim();
    document.getElementById("user-input").value = "";
    if (userInput === "") {
      alert("Please enter a message.");
      return;
    }

    const chatBubbles = document.getElementById("chat-bubbles");

    // Add user input bubble
    const userBubble = document.createElement("li");
    userBubble.className =
      "max-w-2xl ms-auto flex justify-end gap-x-2 sm:gap-x-4";
    userBubble.innerHTML = `
        <div class="grow text-end space-y-3">
            <div class="inline-block bg-blue-600 rounded-lg p-2 shadow-sm">
                <p class="text-sm text-white">${userInput}</p>
            </div>
        </div>
        <span class="shrink-0 inline-flex items-center justify-center size-[38px] rounded-md bg-gray-600">
            <span class="text-sm font-medium text-white leading-none">AZ</span>
        </span>
    `;
    chatBubbles.appendChild(userBubble);

    // Show loading state
    const loadingBubble = document.createElement("li");
    loadingBubble.className = "flex gap-x-2 sm:gap-x-4";
    loadingBubble.innerHTML = `
        <span
              class="inline-flex justify-center items-center w-[38px] h-[38px] rounded-md bg-[#63bda4] overflow-hidden"
            >
              <img
                src="./static/PageOff/assets/images/beemo-face2.jpg"
                alt=""
                class="object-contain w-full h-full"
              />
            </span>
        <div class="bg-white border border-gray-200 rounded-lg p-4 space-y-3 white:bg-neutral-900 dark:border-neutral-700">
            <p class="text-sm text-gray-800 dark:text-white">Beemo is typing...</p>
        </div>
    `;
    chatBubbles.appendChild(loadingBubble);

    // Scroll to the bottom of the chat after appending user bubble and loading bubble
    userBubble.scrollIntoView({ behavior: "smooth" });

    // Send user input to the server and get the response
    try {
      const response = await fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userInput }),
      });

      const result = await response.json();

      // Remove loading bubble
      chatBubbles.removeChild(loadingBubble);

      // Add chatbot response bubble
      const responseBubble = document.createElement("li");
      responseBubble.className = "flex gap-x-2 sm:gap-x-4";
      responseBubble.innerHTML = `
            <span
              class="inline-flex justify-center items-center w-[38px] h-[38px] rounded-md bg-[#63bda4] overflow-hidden"
            >
              <img
                src="./static/PageOff/assets/images/beemo-face2.jpg"
                alt=""
                class="object-contain w-full h-full"
              />
            </span>
            <div class="grow max-w-[90%] md:max-w-2xl w-full space-y-3">

            <div class="bg-white border border-gray-200 rounded-lg p-4 space-y-3 white:bg-neutral-900 white:border-neutral-700">
                <p class="text-sm text-gray-800 dark:white">${result.response}</p>
            </div>
            <div>
                <div class="sm:flex sm:justify-between">
                  <div class="mt-1 sm:mt-0">
                    <button
                      type="button"
                      class="py-2 px-3 inline-flex items-center gap-x-2 text-sm rounded-full border border-transparent text-gray-500 hover:bg-gray-50 focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:text-neutral-400 dark:hover:bg-neutral-800 dark:focus:bg-neutral-800"
                    >
                      <svg
                        class="size-3.5"
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        fill="currentColor"
                        viewBox="0 0 16 16"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"
                        />
                        <path
                          d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"
                        />
                      </svg>
                      New answer
                    </button>
                  </div>
                </div>
              </div>
            </div>
        `;
      chatBubbles.appendChild(responseBubble);

      // Scroll to the bottom after the response is added
      requestAnimationFrame(() => {
        responseBubble.scrollIntoView({ behavior: "smooth" });
      });
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });

// Clear the chat bubbles when "New chat" is clicked
document.getElementById("new-chat").addEventListener("click", function () {
  document.getElementById("chat-bubbles").innerHTML = "";
});

// Detect "Enter" key press in the textarea to submit the form
document
  .getElementById("user-input")
  .addEventListener("keypress", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      document.getElementById("chat-form").dispatchEvent(new Event("submit"));
    }
  });
