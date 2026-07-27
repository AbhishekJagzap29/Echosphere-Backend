/** @odoo-module **/

const BRAND = "Echosphere";

document.title = BRAND;

window.addEventListener("DOMContentLoaded", () => {
    document.title = BRAND;
});

const titleElement = document.querySelector("title") || document.head;

const observer = new MutationObserver(() => {
    if (document.title !== BRAND) {
        document.title = BRAND;
    }
});

observer.observe(titleElement, {
    childList: true,
    subtree: true,
    characterData: true,
});