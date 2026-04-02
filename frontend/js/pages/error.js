// Error messages for each HTTP response that the backend could respond
const ERROR_MESSAGES = {
    400: "We couldn't find the artist or the song that you choose. Please check your inputs or try a different song.",
    404: "We weren't able to find the elements from the song that we need to generate the design. Please enter a new song",
    500: "There was a technical issue generating the design on our end. Please try generating the design again.",
};

// Return the error message based on backend status
export function getErrorMessage(status) {
    return ERROR_MESSAGES[status] || `Unexpected error (code: ${status}).`;
}

// Show the error overlay
export function showError(message){
    // remove any existing error
    const existing = document.getElementById("error-banner");
    if(existing) existing.remove();

    // Add HTML code needed to make the error banner
    const banner = document.createElement("div");
    banner.id = "error-banner";
    banner.class = "error-layout";
    banner.innerHTML = `
        <img src="assets/error.png" alt="Error Chrome Guy" height="572" width="556" class="chrome-guy-error">
        <div class="error-center-panel start-3 col-7">
            <span class="error-message col-12">${message}</span>
            <button class="error-close primary-button start-5 col-4">Try again</button>
        </div>
    `;
    document.body.appendChild(banner);

    // Add listener to banner close button to redirect back to the selection page
    const closeBtn = banner.querySelector(".error-close");
    closeBtn.addEventListener("click", () => {
        banner.remove();
        window.location.href = "selection.html";
    });
}

// Show the confirmation message overlay 
export function showConfirmationMessage(potential_title, potential_artist){
    // remove any existing confirmation messages
    const existing = document.getElementById("confirmation-banner");
    if(existing) existing.remove();

    // Add necessary HTML to create the overlay
    const banner = document.createElement("div");
    banner.id = "confirmation-banner";
    banner.className = "confirmation-layout";
    banner.innerHTML = `
        <img src="assets/chromeGuy.svg" alt="Chrome Guy" height="572" width="556" class="confirmation-chrome-guy">
        <div class="confirmation-center-panel start-3 col-7">
            <h2 class="confirmation-header col-12">Is this what you meant?</h2>
            <span class="error-message col-12">${potential_title} by ${potential_artist}</span>
            <button class="confirmation-no secondary-button start-2 col-4">No</button>
            <button class="confirmation-yes primary-button start-8 col-4">Yes</button>
        </div>
    `
    document.body.appendChild(banner);

    // Check to see which button the user presses and return result to selection page
    return new Promise((resolve) => {
        banner.querySelector(".confirmation-yes").addEventListener("click", () => {
            banner.remove();
            resolve(true)
        });
        banner.querySelector(".confirmation-no").addEventListener("click", () => {
            banner.remove();
            resolve(false);
        });
    });
}