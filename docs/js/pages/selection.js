// Import functions from other files
import { showLoader, hideLoader, startProgressBar, completeProgressBar } from "./loader.js";
import { getErrorMessage, showError, showConfirmationMessage } from "./error.js";
export function initSelection() {
    // store state variables
    let canvasInput = null;

    // Store error variables
    const canvasError = document.getElementById("canvas-error");
    const artistError = document.getElementById("artist-error");
    const songError = document.getElementById("song-error");
    const button = document.getElementById("generateBtn");

    // Canvas selection
    const canvasButtons = document.querySelectorAll(".canvas-btn");

    // Listen for canvas buttons
    canvasButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Remove the selected state to all of the buttons
            canvasButtons.forEach(btn => {
                btn.classList.remove("selected");
                btn.setAttribute("aria-pressed", "false");
                const icon = btn.querySelector(".btn-icon, .poster-btn-icon");
                if(icon && btn.dataset.originalSrc){
                    icon.src = btn.dataset.originalSrc;
                    icon.alt = btn.dataset.originalAlt;
                }
            });

            // Apply the selected state to only the cliced button
            button.classList.add("selected");
            button.setAttribute("aria-pressed", "true");

            // swap the canvas icon to checkmark for selected canvas button
            const icon = button.querySelector(".btn-icon, .poster-btn-icon");

            // Make sure that the icon exists
            if(icon){
               if(!button.dataset.originalSrc) {
                    button.dataset.originalSrc = icon.src;
                    button.dataset.originalAlt = icon.alt;
               } 
               icon.src = "assets/checkmark.png";
               icon.alt = "selected";
               
            }
            // Assign the canvas that's selected
            canvasInput = button.value
        });
    });

    // Wait for the image to be returned from the backend (accounts for ~ minute loading time)
    async function waitForImage(url, maxAttempts = 90, delay = 2000) {
        for (let attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                const response = await fetch(url, { method: "HEAD" });

                if (response.ok) {
                    return true;
                }
            } catch {
                console.log("Still waiting...");
            }

            await new Promise(resolve =>
                setTimeout(resolve, delay)
            );
        }
        return false;
    }

    if (!button) return; // safety check

    button.addEventListener("click", async () => {
        // Grab user input
        let artistInput = document.getElementById("artistInput").value;
        let songInput = document.getElementById("songInput").value;

        // If any of the necessary variables are missing throw an error 
        if(!artistInput){
            artistError.removeAttribute("hidden");
            return;
        }

        if(!songInput){
            songError.removeAttribute("hidden");
            return;
        }

        if (!canvasInput){
            canvasError.removeAttribute("hidden");
            return;
        }

        // Hide error messages
        canvasError.setAttribute("hidden", "");
        artistError.setAttribute("hidden", "");
        songError.setAttribute("hidden", "");

        // Show loading overlay
        showLoader();
        startProgressBar(60000);

        let response, data;

        // Fetch data from frontend
        try {
            response = await fetch("https://capstone-nukm.onrender.com/personlization", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({artistInput, songInput, canvasInput})}
            );
        } catch (err) {
            hideLoader();
            showError("Network error. Please check your connection");
            return;
        }


        // ask the user for confirmation if backend sends 202 response
        if(response.status === 202) {
            console.log("User confirmation needed");
            const data = await response.json();
            const { potential_title, potential_artist } = data;

            // Show confirmation message overlay
            let confirmed = await showConfirmationMessage(potential_title, potential_artist);

            // If that's the song and artist they meant, try again
            if(confirmed){
                artistInput = potential_artist;
                songInput = potential_title;

                try {
                    response = await fetch("http://127.0.0.1:5000/personlization", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({artistInput, songInput, canvasInput})}
                    );
                } catch (err) {
                    hideLoader();
                    showError("Network error. Please check your connection");
                    return;
                }
            } else {
                // If that isn't the song the user intended prompt the user to try again
                showError("Please try entering the song again.");
                return;
            }
        }

        // check the HTTP status
        if (!response.ok) {
            hideLoader();
            // get the error message
            const message = getErrorMessage(response.status)
            showError(message);
            return;
        }   

        data = await response.json();
        const ready = await waitForImage(data.imageUrl);
        console.log("finished fetching the image");

        // hide the loading screen when done
        await completeProgressBar();
        console.log("completed the progress bar");
        hideLoader();

        // If the image generation took too long, show an error
        if (!ready) {
            showError("The image took too long to generate. Please try again.");
            return;
        }

        // Declare variables from the backend
        const imageUrl = data.imageUrl;
        const lyrics = data.lyrics;
        const artist = data.artist;
        const song = data.song;
        const ratio = data.ratio;

        // Store the declared variables for the graphics page
        sessionStorage.setItem("imageUrl", imageUrl);
        sessionStorage.setItem("lyrics", JSON.stringify(lyrics));
        sessionStorage.setItem("artist", artist);
        sessionStorage.setItem("song", song);
        sessionStorage.setItem("ratio", ratio);
        
        // Once done, redirect to the next page
        console.log("Saved redirecting...")
        window.location.href = "graphics.html";
    });
}