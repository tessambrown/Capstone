export function initGraphic() {
    // Grab the data returned from the backend
    // pull the data from sessionStorage, data saved by selection.js
    console.log("finding items...")
    const imageUrl = sessionStorage.getItem("imageUrl");
    const lyrics = sessionStorage.getItem("lyrics");
    const artist = sessionStorage.getItem("artist");
    const song = sessionStorage.getItem("song");
    const ratio = sessionStorage.getItem("ratio");

    // confirm if the session storage correctly grabbed data
    // CALL THE ERROR MENU IF THIS ISN'T FOUND
    console.log("imageURL from storage:", imageUrl);
    console.log("lyrics from storage:", lyrics);

    // if there's no imageURL
    if(!imageUrl){
        console.error("No image URL found");
        return;
    }

    // Image state variables
    let currentImageWrapper = null;

    // Lyric state variables
    let selectedLyric = null;
    let activeLyrics = new Set();

    // Lyric placement state variables
    let singleCellMode = null;
    const occupiedCells = new Map();

    // Ordered list of for auto placement
    const CELL_ORDER = [
        "middle-left",
        "top-left", "bottom-left",
        "center", "top-center",
        "bottom-center", "middle-right",
        "top-right", "bottom-right"
    ]

    // Typography customization state variables
    let currentFontSize = 36;
    let currentCaseStyle = "stentance";
    let currentTextAlignment = "center";
    let currentTextOpacity = 1;
    let currentStrokeWidth = 0;
    let currentStrokeColor = "#000000";
    let currentTextColor = "#ffffff";
    let currentStrokeOpacity = 1;
    let currentRotation = 0;
    let selectedFont = null;
    let currentLineHeight = 1.2;

    // Declare variable to display error on the frontend
    const lyricError = document.getElementById("lyric-error");
    const clearError = document.getElementById("clear-lyric-error");
    const gridError = document.getElementById("grid-full-error");
    const positionError = document.getElementById("position-full-error");
    const singleCellError = document.getElementById("single-cell-error");

    // Declare variables for generated image
    const container = document.getElementById("imageContainer");
    const img = document.createElement("img");
    img.src = imageUrl;
    img.alt = "Generated image";
    const wrapper = document.createElement("div");
    wrapper.classList.add("image-wrapper");
    wrapper.style.position = "relative";

    // Apply the selected ratio (from the selected canvas size) to the generated image
    if(ratio) {
        const [w, h] = ratio.split(":").map(Number);
        const aspectRatio = w/h;

        // wrapper.style.position = "relative";
        wrapper.style.width = "100%";
        wrapper.style.maxHeight = "100%";
        wrapper.style.aspectRatio = `${w} / ${h}`;

        if(h > w){
            wrapper.style.width = "auto";
            wrapper.style.height = "100%";
        }
        
        // Image needs to fill the wrapper absolutely
        img.style.position = "absolute";
        img.style.top = "0";
        img.style.left = "0";
        img.style.width = "100%";
        img.style.height = "100%";
        img.style.objectFit = "cover";
    }

    // Add the image to container
    wrapper.appendChild(img);
    container.appendChild(wrapper);
    currentImageWrapper = wrapper;

    // Place song/artist name on the bottom right corner of the image
    placeNames(song, artist);

    function placeNames(song, artist) {
        if (!currentImageWrapper) return;

        document
            .querySelectorAll(".name-text")
            .forEach(el => el.remove());

        const name = document.createElement("div");
        name.classList.add("name-text");
        name.innerText = `${song} by ${artist}`;
        if(selectedFont) div.dataset.font = selectedFont;

        currentImageWrapper.appendChild(name);

        positionName(name);
    }

    function positionName(element) {
        element.style.position = "absolute";
        element.style.bottom = "10px";
        element.style.right = "10px";
    }

    // ---------------- FONT DROPDOWN MENU FUNCTIONALITY ----------------

    // Grab font dropdown html elements
    const dropdown = document.querySelector(".font-dropdown");
    const dropdownBtn = document.getElementById("fontDropdownBtn");
    const options = document.querySelectorAll(".font-option");
    const label = dropdownBtn.querySelector(".font-label");

    // Check if the dropdown button was clicked and open
    dropdownBtn.addEventListener("click", () => {
        dropdown.classList.toggle("open");
    });

    // Loops through the curated collection of font options and adds a click listener
    options.forEach(option => {
        option.addEventListener("click", () => {
            selectedFont = option.dataset.font;

            // updates the label of the font menu to selected font
            label.textContent = option.textContent;
            dropdownBtn.style.fontFamily = selectedFont;

            // hides the rest of the font dropdown menu
            dropdown.classList.remove("open");

            // calls applyFont to apply selected font
            applyFont(selectedFont);
        })
    });

    // Apply the font the user selected from the dropdown to lyric window and artist + song displayed on the generated image
    function applyFont(fontName) {
        const targets = [
            ...document.querySelectorAll(".lyric-content"),
            ...document.querySelectorAll(".name-text"),
            ...document.querySelectorAll(".lyric-line"),
            ...document.querySelectorAll(".lyric-section")
        ];

        targets.forEach(el => {
            el.dataset.font = fontName;
            el.style.fontFamily = fontName;
        });
    }

    // ---------------- LYRIC WINDOW FUNCTIONALITY ----------------

    // Parse the lyrics returned from the backend to convert to an object
    let parsedLyrics;
    try {
        parsedLyrics = JSON.parse(lyrics);
    } catch (e) {
        //CALL THE ERROR MENU IF THIS ISN'T FOUND
        console.error("Could not parse lyrics from sessionStorage:", e);
        return;
    }

    // Add the lyrics to the lyric scrollable window
    displayLyrics(parsedLyrics);

    // Display the lyrics in the scrollable window
    function displayLyrics(lyricsData) {
        // Grab the lyrics container from the page
        const container = document.getElementById("lyricsContainer");
        container.innerHTML="";

        // Loops over each section of the lyrics
        Object.entries(lyricsData).forEach(
            ([section, lines]) => {

                // Render the section headers
                const header = document.createElement("div");
                header.classList.add("lyric-section");
                header.innerText = section;
                if(selectedFont) header.style.fontFamily = selectedFont;
                container.appendChild(header);

                // Loops over each line in the section
                lines.forEach((line, index) => {
                    if(!line.trim()) return;

                    // Render each lyric line
                    const div = document.createElement("div");
                    div.classList.add("lyric-line");
                    div.innerText = line;
                    div.dataset.lyricId = `${section}-${index}`;
                    if(selectedFont) div.style.fontFamily = selectedFont;

                    // Handle chlicking each lyric line
                    div.addEventListener("click", () => {

                        // Mark the past selected line as placed
                        document.querySelectorAll(".lyric-line").forEach(el => {
                            if (el.classList.contains("lyric-selected")) {
                                const isPlaced = [...document.querySelectorAll(".lyric-text")]
                                    .some(placed => placed.dataset.lyricId === el.dataset.lyricId);
                                el.classList.remove("lyric-selected");
                                if (isPlaced) el.classList.add("lyric-placed");
                            }
                        });

                        // Adds the lyric line selected to the clicked div and adds it to selectedLyric
                        div.classList.remove("lyric-placed");
                        div.classList.add("lyric-selected");

                        selectedLyric = line;
                        console.log("Selected:", selectedLyric);

                        // Check if this lyric is already on the image
                        const existingEl = [...document.querySelectorAll(".lyric-text")]
                            .find(el => el.dataset.lyricId === div.dataset.lyricId);

                        if (!existingEl) {
                            // Not placed yet — auto-place in next free cell
                            placeLyricOnImage(line, div);
                        } else {
                            // Already placed — select it so the position grid controls it
                            setSelection(existingEl);
                            console.log("Lyric re-selected for repositioning:", line);
                        }
                    });
                    container.appendChild(div);
                });
            });
    }

    // ---------------- APPLYING LYRIC TO IMAGE FUNCTIONALITY ----------------

    function placeLyricOnImage(text, windowDiv) {
        // Check to see if there is a generated image before placing the lyric line
        if (!currentImageWrapper) return;

        // find a free cell
        const targetCell = getNextFreeCell();

        // if all of the cells are full return an error to the front end
        if(!targetCell) {
            gridError.removeAttribute("hidden");
            return
        }
        // Hide the error message
        gridError.setAttribute("hidden", "");

        // Create a container for the lyric line
        const lyric = document.createElement("div");
        lyric.classList.add("lyric-text");

        // Create text elements for lyric line and apply text styles
        const textNode = document.createElement("span");
        textNode.classList.add("lyric-content");

        lyric.addEventListener("click", (e) => {
            e.stopPropagation();
            setSelection(lyric);
        });

        // Grab global state variables tracking and updating user's choices
        textNode.style.textAlign = currentTextAlignment;
        textNode.style.opacity = currentTextOpacity;
        textNode.style.webkitTextStroke = `${currentStrokeWidth}px ${currentStrokeColor}`;
        textNode.style.color = currentTextColor;
        if(selectedFont) textNode.dataset.font = selectedFont;
        textNode.style.lineHeight = currentLineHeight;
        textNode.innerText = text;

        // Ensure the text fills the container
        textNode.style.display = "block";
        textNode.style.width = "100%";
        textNode.style.whiteSpace = "normal";

        // Attach the text to the image
        lyric.appendChild(textNode);
        lyric.dataset.originalText = text;
        currentImageWrapper.appendChild(lyric);

        // Add class to lyric window after placing it
        // const windowLine = [...document.querySelectorAll(".lyric-line")].find(el => el.innerText === text);
        // if (windowLine) windowLine.classList.add("lyric-placed");
        lyric.dataset.lyricId = windowDiv.dataset.lyricId;

        // Clear any remaining lyrics in activeLyrics and add new lyric to activeLyrics
        activeLyrics.clear();
        activeLyrics.add(lyric);

        // Default the lyric rotation to zero
        lyric.dataset.rotation = 0;

        // Wait until the element exists before applying lyric customizations
        requestAnimationFrame(() => {
            lyric.style.fontSize = `${currentFontSize}px`;
            lyric.getBoundingClientRect();
            assignLyricToCell(lyric, targetCell)
        });
    }

    // Check to see if the user clicks the clear lyrics button and clears any lyrics placed on image
    document.getElementById("clearLyricsBtn").addEventListener("click", () => {
        if(!currentImageWrapper) return;

        const placedLyrics = currentImageWrapper.querySelectorAll(".lyric-text");
    
        if (placedLyrics.length === 0) {
            clearError.removeAttribute("hidden");
            return;
        }
        // Hide the error message
        clearError.setAttribute("hidden", "");

        placedLyrics.forEach(el => el.remove());
        activeLyrics.clear();
        occupiedCells.clear();

        // Reset the style of all lines in window to defualt state
        document.querySelectorAll(".lyric-line").forEach(el => el.classList.remove("lyric-placed", "lyric-selected"));
    });

    //---------------- AUTO PLACING LYRICS FUNCTIONALITY ---------------- 
    // Return the first cell that doesn't already have a lyric in it, if all are full return null
    function getNextFreeCell() {
        return CELL_ORDER.find(pos => !occupiedCells.has(pos)) ?? null;
    }
    
    // Assign lyric element to a cell, updated occupiedCells map
    function assignLyricToCell(lyric, position) {
        const oldPos = lyric.dataset.position;
        if (oldPos && occupiedCells.get(oldPos) === lyric) {
            occupiedCells.delete(oldPos);
        }
        occupiedCells.set(position, lyric);
        positionLyric(lyric, position);
        applyLyricTransform(lyric);
    }

    // Set the current lyric selection
    function setSelection(lyric) {
        // Deselect other lyric elements
        document.querySelectorAll(".lyric-text").forEach(l => l.classList.remove("active"));
        activeLyrics.clear();

        // Select only the clicked lyric
        activeLyrics.add(lyric);
        lyric.classList.add("active");
    }

    //---------------- POSITION LYRICS FUNCTIONALITY ---------------- 
    // Check if user wants to reposition lyrics on generated image
    document.querySelectorAll("#positionGrid button")
        .forEach(btn => {
            btn.addEventListener("click", () => {
                // Displays an error if there are no lyrics placed on image
                if (activeLyrics.size === 0) {
                    lyricError.removeAttribute("hidden");
                    return;
                }
                // Hide the error message
                lyricError.setAttribute("hidden", "");

                const position = btn.dataset.pos;

                // Check if the target cell is already taken by a previous lyric
                const occupant = occupiedCells.get(position);
                const movingLyrics = [...activeLyrics];
                const cellTaken = occupant && !movingLyrics.includes(occupant);

                if(cellTaken) {
                    positionError.removeAttribute("hidden");
                    return;
                }
                // Hide the error message
                positionError.setAttribute("hidden", "");

                // Activates selected button
                document.querySelectorAll("#positionGrid button").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");

                activeLyrics.forEach(lyric => assignLyricToCell(lyric, position));

                // activeLyrics.forEach(lyric => {
                //     positionLyric(lyric, position);
                //     applyLyricTransform(lyric);
                // });
            });
    });

    // Positions lyric based on selected grid cell 
    function positionLyric(element, position) {
        // Stores the position
        element.dataset.position = position;
        element.style.position = "absolute";

        // Get image dimensions
        const pw = currentImageWrapper.offsetWidth;
        const ph = currentImageWrapper.offsetHeight;

        // Define the same margin on all sides of the generated image
        const margin = 16;

        // Calculate the inner width of the image 
        const innerWidth  = pw - margin * 2;
        const innerHeight = ph - margin * 2;

        // Divides the area into a 3x3 grid
        const cellWidth  = innerWidth  / 3;
        const cellHeight = innerHeight / 3;

        // Map the position names to grid coordinates
        const gridMap = {
            "top-left": [0,0],
            "top-center": [1,0],
            "top-right": [2,0],

            "middle-left": [0,1],
            "center": [1,1],
            "middle-right": [2,1],

            "bottom-left": [0,2],
            "bottom-center": [1,2],
            "bottom-right": [2,2],
        };
        const [col, row] = gridMap[position];

        // Calculate the top position
        const top  = margin + row * cellHeight + cellHeight / 2;

        // Check to see if the user wants the lyrics to fill one cell
        if(singleCellMode) {
            // Calculate the left position and width
            const left = margin + col * cellWidth;
            element.style.left = left + "px";
            element.style.width = cellWidth + "px";

        // Defult to have the lyrics to fill the rest of the row
        } else {
            // Calculate the left position and width
            const left = margin + col * cellWidth;
            element.style.left = left + "px";
            element.style.width = (innerWidth - col * cellWidth) + "px";
        }
        element.style.top = top + "px";
    }

    // Check to see if the user wants the lyrics to be in one cell
    document.getElementById("singleCellToggle").addEventListener("change", (e) => {
        singleCellMode = e.target.checked;

        // reposition the existing lyrics to fix within the cell
        activeLyrics.forEach(lyric => {
            const pos = lyric.dataset.position || "center";

            // Check to see if the position is on the right, and throw an error
            if(pos.includes("right")){
                singleCellError.removeAttribute("hidden");
                return;
            }
            // Hide the error message
            singleCellError.setAttribute("hidden", "");

            positionLyric(lyric, pos);
            applyLyricTransform(lyric);
        });
    });

    //---------------- FONT SIZE FUNCTIONALITY ----------------  
    const fontSlider = document.getElementById("fontSizeSlider");

    // Apply the font size to lyrics displayed on the image
    fontSlider.addEventListener("input", () => {
        currentFontSize = fontSlider.value;
        const lyrics = document.querySelectorAll(".lyric-text");
        lyrics.forEach(lyric => {
            lyric.style.fontSize = `${currentFontSize}px`;
        });
    });

    // Make the slider icons interactive
    const fontSizeMinusBtn = document.querySelector(".slider-icons .text-minus-icon");
    const fontSizePlusBtn = document.querySelector(".slider-icons .text-plus-icon");

    // Update the font size based on icon clicked
    fontSizeMinusBtn.addEventListener("click", () => {
        fontSlider.value = Math.min(fontSlider.min, parseFloat(fontSlider.value) - parseFloat(fontSlider.step));
        fontSlider.dispatchEvent(new Event("input"));
    });

    fontSizePlusBtn.addEventListener("click", () => {
        fontSlider.value = Math.min(fontSlider.max, parseFloat(fontSlider.value) + parseFloat(fontSlider.step));
        fontSlider.dispatchEvent(new Event("input"));
    });

    //---------------- LINE SPACING FUNCTIONALITY ----------------
    const lineHeightSlider = document.getElementById("lineHeightSlider");

    // Apply the line height to the displayed lyrics on the image
    lineHeightSlider.addEventListener("input", () => {
        currentLineHeight = lineHeightSlider.value/10;
        updateLineSpacing();
    });

    function updateLineSpacing(){
        document.querySelectorAll(".lyric-content").forEach(el => {
            el.style.lineHeight = currentLineHeight;
        });
    }

    // line height slider icons
    const lineHeightMinusBtn = document.querySelector(".slider-icons .line-minus-icon");
    const lineHeightPlusBtn = document.querySelector(".slider-icons .line-plus-icon");

    // Update line spacing based on icon clicked
    lineHeightMinusBtn.addEventListener("click", () => {
        lineHeightSlider.value = Math.max(lineHeightSlider.min, parseFloat(lineHeightSlider.value) - parseFloat(lineHeightSlider.step));
        lineHeightSlider.dispatchEvent(new Event("input"));
    });

    lineHeightPlusBtn.addEventListener("click", () => {
        lineHeightSlider.value = Math.min(lineHeightSlider.max, parseFloat(lineHeightSlider.value) + parseFloat(lineHeightSlider.step));
        lineHeightSlider.dispatchEvent(new Event("input"));
    });
    

    //---------------- TEXT CASE SYTLE FUNCTIONALITY ----------------
    // Format the lyrics on the image to selected case style 
    function formatLyricCase(text, style) {
        if (style === "upper") {
            return text.toUpperCase();
        }

        if (style === "lower") {
            return text.toLowerCase();
        }
        // if it's default (sentance case) return the text 
        return text
    }

    // Update the lyric case of the lyrics placed on the image
    function updateLyricCase() {
        
        const lyrics = document.querySelectorAll(".lyric-text");

        lyrics.forEach(lyric => {

            const original = lyric.dataset.originalText;

            const content = lyric.querySelector(".lyric-content");

            if (!content || !original) return;

            content.textContent =
                formatLyricCase(
                    original,
                    currentCaseStyle
                );
        });
    }

    // Checks to see which case button that's pressed
    document.getElementById("caseDefault").addEventListener("click", () => {
        currentCaseStyle = "sentance";
        updateLyricCase();
    });

    document.getElementById("caseUpper").addEventListener("click", () => {
        currentCaseStyle = "upper";
        updateLyricCase();
    });

    document.getElementById("caseLower").addEventListener("click", () => {
        currentCaseStyle = "lower";
        updateLyricCase();
    });

    //---------------- TEXT ALIGNMENT FUNCTIONALITY ----------------
    // Update the text alignment on the image based on users choice
    function updateTextAlignment() {
        const lyrics = document.querySelectorAll(".lyric-content");
        lyrics.forEach(content => {
            content.style.textAlign = currentTextAlignment;
        });
    }

    // Checks to see which alignment button that's pressed
    document.getElementById("alignLeft").addEventListener("click", () => {
        currentTextAlignment = "left";
        updateTextAlignment();
    });

    document.getElementById("alignCenter").addEventListener("click", () => {
        currentTextAlignment = "center";
        updateTextAlignment();
    });

    document.getElementById("alignRight").addEventListener("click", () => {
        currentTextAlignment = "right";
        updateTextAlignment();
    });

    // Apply the desired transformation to the position and rotation of lyrics
    function applyLyricTransform(lyric) {
        const rotation = lyric.dataset.rotation || 0;
        if (singleCellMode) {
            // lyric.style.transform = `translate(-50%, -50%) rotate(${rotation}deg)`;
            lyric.style.transform = `translateY(-50%) rotate(${rotation}deg)`;
        } else {
            lyric.style.transform = `translateY(-50%) rotate(${rotation}deg)`;
        }
    }

    //---------------- TEXT ROTATION FUNCTIONALITY ----------------
    // Update the text rotation based on slider input
    function updateTextRotation() {
        if(activeLyrics.size === 0)
            return;
        activeLyrics.forEach(lyric => {
            lyric.dataset.rotation = currentRotation;
            applyLyricTransform(lyric);
        });
    }

    const rotationSlider = document.getElementById("rotationSlider");
    // Record and update text rotation
    rotationSlider.addEventListener("input", () => {
        currentRotation = parseInt(rotationSlider.value);

        updateTextRotation();
    });

    // rotation slider icons
    const leftRotationBtn = document.querySelector(".rotate-icons .left-rotation-icon");
    const rightRotationBtn = document.querySelector(".rotate-icons .right-rotation-icon");

    // Update rotation based on slider icon that's pressed
    leftRotationBtn.addEventListener("click", () => {
        rotationSlider.value = Math.max(rotationSlider.min, parseFloat(rotationSlider.value) - parseFloat(rotationSlider.step));
        currentRotation = parseInt(rotationSlider.value);
        updateTextRotation();
    });

    rightRotationBtn.addEventListener("click", () => {
        rotationSlider.value = Math.min(rotationSlider.max, parseFloat(rotationSlider.value) + parseFloat(rotationSlider.step));
        currentRotation = parseInt(rotationSlider.value);
        updateTextRotation();
    });

    //---------------- TEXT COLOR FUNCTIONALITY ----------------
    // Update the text color based on which text color button is pressed
    function updatetextColor() {
        const lyrics = document.querySelectorAll(".lyric-content");
        const name = document.querySelectorAll(".name-text")
        lyrics.forEach(content => {
            content.style.color = currentTextColor;
        });
        name.forEach(content => {
            content.style.color = currentTextColor;
        });
    }

    // Listen and update text color based on while button is pressed
    document.addEventListener("click", (e) => {
        if(!e.target.classList.contains("text-color"))
            return;
        currentTextColor = e.target.dataset.color;
        console.log("Text color:", currentTextColor);
        updatetextColor();
    });

    //---------------- TEXT OPACITY FUNCTIONALITY ----------------
    const opacitySlider = document.getElementById("opacitySlider");

    // Listen and update text opacity based on user's desired opacity
    opacitySlider.addEventListener("input", () => {
        currentTextOpacity = parseFloat(opacitySlider.value);
        console.log("current text opacity:", currentTextOpacity);
        updateTextOpacity();
    });

    // Update the text opacity
    function updateTextOpacity () {
        const lyrics = document.querySelectorAll(".lyric-content");

        lyrics.forEach(content => {
            content.style.opacity = currentTextOpacity;
        });
    }

    // opacity slider icons
    const opacityMinusBtn = document.querySelector(".slider-icons .opacity-minus-icon");
    const opacityPlusBtn = document.querySelector(".slider-icons .opacity-plus-icon");

    // Update the text opacity based on which icon is pressed
    opacityMinusBtn.addEventListener("click", () => {
        opacitySlider.value = Math.max(opacitySlider.min, parseFloat(opacitySlider.value) - parseFloat(opacitySlider.step));
        opacitySlider.dispatchEvent(new Event("input"));
    });

    opacityPlusBtn.addEventListener("click", () => {
        opacitySlider.value = Math.min(opacitySlider.max, parseFloat(opacitySlider.value) + parseFloat(opacitySlider.step));
        opacitySlider.dispatchEvent(new Event("input"));
    });

    //---------------- STROKE CONTAINER FUNCTIONALITY ----------------
    const strokeToggle = document.getElementById("strokeToggle");
    const strokeControls = document.getElementById("strokeControls");
    
    // Check to see if the user wants to customize text stroke
    strokeToggle.addEventListener("change", () => {
        const isOn = strokeToggle.checked;

        // show/hide stroke UI
        strokeControls.style.display = isOn ? "block" : "none";

        // when the toggle turns off, clear the stroke
        if(!isOn){
            const lyrics = document.querySelectorAll(".lyric-content");
            console.log("Lyric elements found:", lyrics.length); // is it finding them?
            lyrics.forEach(el => {
                el.style.removeProperty("-webkit-text-stroke");
                el.style.removeProperty("webkit-text-stroke");
            });
        } else {
            // re-apply the users settings when toggled back on
            updateTextStroke();
        }
    });

    // ---------------- STROKE WEIGHT FUNCTIONALITY ---------------- 
    // Update text's stroke based on slider input 
    function updateTextStroke() {

        const lyrics = document.querySelectorAll(".lyric-content");

        const strokeColorRGBA =
            hexToRGBA(
                currentStrokeColor,
                currentStrokeOpacity
            );

        lyrics.forEach(content => {

            if (currentStrokeWidth === 0) {
                content.style.webkitTextStroke = "none";
                return;
            }

            content.style.webkitTextStroke =
                `${currentStrokeWidth}px ${strokeColorRGBA}`;
        });
    }

    const strokeSlider = document.getElementById("strokeSlider");

    // Listen and update stroke weight based on slider input
    strokeSlider.addEventListener("input", () => {
        currentStrokeWidth = parseFloat(strokeSlider.value);
        updateTextStroke();
    });

    // stroke weight slider icons
    const strokeWeightMinusBtn = document.querySelector(".slider-icons .stroke-minus-icon");
    const strokeWeightPlusBtn = document.querySelector(".slider-icons .stroke-plus-icon");

    // Update stroke weight based on which icon is clicked
    strokeWeightMinusBtn.addEventListener("click", () => {
        strokeSlider.value = Math.max(strokeSlider.min, parseFloat(strokeSlider.value) - parseFloat(strokeSlider.step));
        strokeSlider.dispatchEvent(new Event("input"));
    });

    strokeWeightPlusBtn.addEventListener("click", () => {
        strokeSlider.value = Math.min(strokeSlider.max, parseFloat(strokeSlider.value) + parseFloat(strokeSlider.step));
        strokeSlider.dispatchEvent(new Event("input"));
    });

    // ---------------- STROKE COLOR FUNCTIONALITY ---------------- 
    // Update the stroke color based on which stroke color button is clicked
    document.addEventListener("click", (e) => {
        if(!e.target.classList.contains("stroke-color"))
            return;
        
        currentStrokeColor = e.target.dataset.color;

        console.log("Stroke color:", currentStrokeColor);
        
        updateTextStroke();
    });

    // ---------------- STROKE OPACITY FUNCTIONALITY ---------------- 
    // helper function for stroke opacity that returns the rgba value (a is the opacity)
    function hexToRGBA(hex, alpha) {
        const r = parseInt(hex.slice(1,3), 16);
        const g = parseInt(hex.slice(3,5), 16);
        const b = parseInt(hex.slice(5,7), 16);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    const strokeOpacitySlider = document.getElementById("strokeOpacitySlider");

    // Listen and update the stroke's opacity based on slider input 
    strokeOpacitySlider.addEventListener("input", () => {
        currentStrokeOpacity = parseFloat(strokeOpacitySlider.value);
        updateTextStroke();
    });

    // stroke opacity slider icons
    const strokeOpacityMinusBtn = document.querySelector(".slider-icons .stroke-opacity-minus-icon");
    const strokeOpacityPlusBtn = document.querySelector(".slider-icons .stroke-opacity-plus-icon");

    // Update the strokes opacity based on which icon that's selected
    strokeOpacityMinusBtn.addEventListener("click", () => {
        strokeOpacitySlider.value = Math.max(strokeOpacitySlider.min, parseFloat(strokeOpacitySlider.value) - parseFloat(strokeOpacitySlider.step));
        strokeOpacitySlider.dispatchEvent(new Event("input"));
    });

    strokeOpacityPlusBtn.addEventListener("click", () => {
        strokeOpacitySlider.value = Math.min(strokeOpacitySlider.max, parseFloat(strokeOpacitySlider.value) + parseFloat(strokeOpacitySlider.step));
        strokeOpacitySlider.dispatchEvent(new Event("input"));
    });

    // ---------------- IMAGE OPACITY FUNCTIONALITY ----------------
    // Update the opacity of the generated image based on user input 
    function updateImageOpacity(opacity) {
        if(!currentImageWrapper)
            return;
        
        const img = currentImageWrapper.querySelector("img");

        if(!img)
            return;

        img.style.opacity = opacity;
    }

    const imageOpacitySlider = document.getElementById("imageOpacitySlider");

    // Listen and update the image opacity based on slider value
    imageOpacitySlider.addEventListener("input", () => {
        const opacity = parseFloat(imageOpacitySlider.value);
        console.log("Image opacity:", opacity);
        updateImageOpacity(opacity);
    });

    // image opacity slider icons
    const imageOpacityMinusBtn = document.querySelector(".slider-icons .image-minus-icon");
    const imageOpacityPlusBtn = document.querySelector(".slider-icons .image-plus-icon");

    // Update the image opacity based on which icon thats clicked
    imageOpacityMinusBtn.addEventListener("click", () => {
        imageOpacitySlider.value = Math.max(imageOpacitySlider.min, parseFloat(imageOpacitySlider.value) - parseFloat(imageOpacitySlider.step));
        imageOpacitySlider.dispatchEvent(new Event("input"));
    });

    imageOpacityPlusBtn.addEventListener("click", () => {
        imageOpacitySlider.value = Math.min(imageOpacitySlider.max, parseFloat(imageOpacitySlider.value) + parseFloat(imageOpacitySlider.step));
        imageOpacitySlider.dispatchEvent(new Event("input"));
    }); 
    
    // ---------------- NAME TOGGLE FUNCTIONALITY ----------------
    const nameToggle = document.getElementById("nameToggle");

    // Remove or add the name in the bottom right hand corner based on toggle value 
    nameToggle.addEventListener("change", () => {
        const names = document.querySelectorAll(".name-text");

        if (!names) return;

        names.forEach(name => {
            name.style.display = nameToggle.checked ? "block" : "none";
        });
    });

    // ---------------- DOWNLOAD BUTTON FUNCTIONALITY ----------------
    // Download the generated image + customized lyrics
    document.getElementById("downloadBtn").addEventListener("click", async () => {
        // Target the container that has the image + text
        const container = document.querySelector(".image-wrapper");

        const canvas = await html2canvas(container, {
            useCORS: true,
            allowTaint: false,
            scale: 2
        });


        // Convert canvas to a PNG
        const link = document.createElement("a");
        link.download = `${song}-${artist}.png`;
        link.href = canvas.toDataURL("image/png");
        link.click();

        // Redirect to confirmation page when the download is complete
        setTimeout(() => {
            window.location.href = "download.html";
        }, 500);
    });
}