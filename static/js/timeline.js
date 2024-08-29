function toggleTimeline() {
  const timelineItems = document.querySelectorAll(".timeline-item");
  const toggleButton = document.getElementById("toggle-timeline");

  timelineItems.forEach((item, index) => {
    if (index >= 3) {
      // Toggle visibility with smooth height transition
      if (item.classList.contains("hidden")) {
        item.classList.remove("hidden");
        item.classList.add("max-h-[1000px]", "opacity-100");
      } else {
        item.classList.add("hidden");
        item.classList.remove("max-h-[1000px]", "opacity-100");
      }
    }
  });

  // Change button text
  toggleButton.innerText =
    toggleButton.innerText === "Read More" ? "Read Less" : "Read More";
}