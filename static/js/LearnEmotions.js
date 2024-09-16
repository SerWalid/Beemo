document.addEventListener('DOMContentLoaded', function () {
    const stack = document.querySelector(".stack");
    const description = document.getElementById('emotion-description');
    const cards = Array.from(stack.children).reverse().filter((child) => child.classList.contains("card"));

    // Emotion descriptions
    const emotionTexts = {
        happy: 'Feeling happy means experiencing joy and contentment. This emotion is often associated with smiles and laughter.',
        sad: 'Feeling sad is when you experience sorrow or unhappiness. It can be accompanied by tears and a sense of loss.',
        surprised: 'Feeling surprised happens when something unexpected occurs. It often leads to wide eyes and an open mouth.',
        angry: 'Feeling angry is when you experience strong displeasure or frustration. This emotion might be expressed with frowning or yelling.',
        fear: 'Feeling fear is when you are afraid or anxious about something. It can cause you to feel nervous or on edge.'
    };

    // Function to move cards
    function moveCard() {
        const lastCard = stack.lastElementChild;
        if (lastCard.classList.contains("card")) {
            lastCard.classList.add("swap");

            setTimeout(() => {
                lastCard.classList.remove("swap");
                stack.insertBefore(lastCard, stack.firstElementChild);
            }, 1200);
        }
    }

    // Autoplay interval
    let autoplayInterval = setInterval(moveCard, 4000);

    // Click event for cards
    cards.forEach(card => {
        card.addEventListener('click', function () {
            const emotion = this.getAttribute('data-emotion');
            description.textContent = emotionTexts[emotion];

            // Swap card if clicked
            if (this === stack.lastElementChild) {
                this.classList.add("swap");

                setTimeout(() => {
                    this.classList.remove("swap");
                    stack.insertBefore(this, stack.firstElementChild);
                }, 1200);
            }
        });
    });
});
