import { initSelection } from "./pages/selection.js";
import { initGraphic } from "./pages/graphics.js";
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM READY");

    const page = document.body.dataset.page;
    console.log(document.body.dataset.page);

    if (page === "selection") {
        console.log("Running initSelection()")
        initSelection();
    }

    if (page === "graphics") {
        console.log("Running initGraphic()")
        initGraphic();
    }

});