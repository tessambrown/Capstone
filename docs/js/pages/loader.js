// --------- REUSABLE FUNCTIONS ----------

// Show the loading overlay
export function showLoader() {
    const overlay = document.getElementById("loadingOverlay");

    if (!overlay) return;      // lets you customize the message
    overlay.classList.remove("hidden");
}

// Hide the loading overlay
export function hideLoader() {
    const overlay = document.getElementById("loadingOverlay");

    if (!overlay) return;

    overlay.classList.add("hidden");
}

// Progress bar animation used on loading page
export function startProgressBar(durationMs = 60000) {
    const fill = document.getElementById('progressBarFill');
    const startTime = performance.now();

    // Start at zero percent
    fill.style.width = '0%';

    function tick(now) {
        const elapsed = now - startTime;
        // cap the progress at 99% until the generation is done
        const progress = Math.min((elapsed/ durationMs) * 100, 99);
        fill.style.width = progress + '%';

        if(elapsed < durationMs){
            requestAnimationFrame(tick); 
        }
    }
    requestAnimationFrame(tick);
}

// Completed progress bar
export function completeProgressBar() {
    const fill = document.getElementById('progressBarFill');
    fill.style.transition = 'width 0.3s ease-out';
    fill.style.width = '100%'
}