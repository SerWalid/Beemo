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
    if (result.content === "No interactions found for today.") {
      reportResult.innerHTML = `<p class="text-red-500">${result.content}</p>`;
      buttonText.textContent = "No Report Generated";
      button.classList.remove("opacity-50", "cursor-not-allowed");
      return;
    }
    const content = JSON.parse(result.content);

    // Display the report content in the designated UI container
    let reportHTML = `<div class="space-y-4">
        <!-- Overview Section -->
        <div>
          <h3 class="text-base font-semibold text-gray-900">Overview of the Day</h3>
          <p class="text-sm text-gray-800">${content.overview}</p>
        </div>

        <!-- Emotional State Section -->
        <div>
          <h3 class="text-base font-semibold text-gray-900">Emotional State</h3>
          <p class="text-sm text-gray-800">${content.emotional_state}</p>
        </div>

        <!-- Behaviors Section -->
        <div>
          <h3 class="text-base font-semibold text-gray-900">Behaviors</h3>
          <p class="text-sm text-gray-800">${content.behaviors}</p>
        </div>

        <!-- Communication Skills Section -->
        <div>
          <h3 class="text-base font-semibold text-gray-900">Communication Skills</h3>
          <p class="text-sm text-gray-800">${content.communication_skills}</p>
        </div>
      `;

    // Create the Notable Moments section
    const notableMoments = content.notable_moments;
    let notableMomentsHTML = `
  <div>
    <h3 class="text-base font-semibold text-gray-900">Notable Moments</h3>
    <ul class="list-disc pl-5 text-sm text-gray-800">
`;

    notableMoments.forEach((moment) => {
      notableMomentsHTML += `<li>${moment}</li>`;
    });

    notableMomentsHTML += `
    </ul>
  </div>
`;

    // Append the Notable Moments section to the report HTML
    reportHTML += notableMomentsHTML;

    // Create the Recommendations section

    const recommendationsHTML = `<div>
          <h3 class="text-base font-semibold text-gray-900">Recommendations</h3>
          <p class="text-sm text-gray-800">${content.recommendations}</p>
        </div>
      </div>
      </div>
      </div>`;
    // Set the inner HTML of the reportResult container
    reportHTML += recommendationsHTML;
    reportResult.innerHTML = reportHTML;

    // Update button text to indicate completion
    buttonText.textContent = "Report Generated";
  } catch (error) {
    // Show error message in the UI if the request fails
    reportResult.innerHTML = `<p class="text-red-500">Error generating report. Please try again.</p>`;
    buttonText.textContent = "Error! Try Again";
  } finally {
    // Keep the button disabled (or re-enable if needed)
    button.disabled = false;
    button.classList.remove("opacity-50", "cursor-not-allowed");
  }
}
