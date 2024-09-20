async function generateReport() {
  const button = document.getElementById("generate-report-btn");
  const buttonText = document.getElementById("button-text");
  const reportResult = document.getElementById("report-result");

  // Disable the button and show loading state
  button.disabled = true;
  buttonText.textContent = "Generating...";
  button.classList.add("opacity-50", "cursor-not-allowed");

  try {
    // Send GET request to generate the report
    const response = await fetch("/generate_report", {
      method: "GET", // Ensure this matches the method used in your backend endpoint
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to generate the report");
    }

    const result = await response.json();

    // Display the report content in the designated UI container
    reportResult.innerHTML = `<p>${result.content}</p>`;

    // Update button text to indicate completion
    buttonText.textContent = "Report Generated";
  } catch (error) {
    // Show error message in the UI if the request fails
    reportResult.innerHTML = `<p class="text-red-500">Error generating report. Please try again.</p>`;
    buttonText.textContent = "Error! Try Again";
  } finally {
    // Keep the button disabled (or re-enable if needed)
    button.classList.remove("opacity-50", "cursor-not-allowed");
  }
}
