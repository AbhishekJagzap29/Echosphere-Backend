/** @odoo-module **/

console.log("%c🔥 Echosphere POS Branding - LOADED", "color: green; font-size: 14px; font-weight: bold;");

const BRAND = "Echosphere";

// Safe function that won't throw errors
function safeBrandReplace() {
    try {
        // Change title safely
        if (typeof document !== 'undefined' && document.title) {
            if (document.title.includes('Odoo')) {
                document.title = document.title.replace(/Odoo/g, BRAND);
            }
        }
        
        // Safely find brand element
        if (document.querySelector) {
            const brandElement = document.querySelector('.brand span, .brand-text, .o_menu_brand');
            if (brandElement && brandElement.textContent && brandElement.textContent.includes('Odoo')) {
                brandElement.textContent = BRAND;
            }
        }
    } catch (e) {
        // Silently fail - no errors
        console.log('Brand replace attempted');
    }
}

// Run when safe
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(safeBrandReplace, 100);
} else {
    document.addEventListener('DOMContentLoaded', safeBrandReplace);
}

// Run after a delay
setTimeout(safeBrandReplace, 500);
setTimeout(safeBrandReplace, 1000);
setTimeout(safeBrandReplace, 2000);

/** @odoo-module **/

console.log("%c🧾 Oakmont Receipt - Powered By", "color: green; font-size: 14px; font-weight: bold;");

// const BRAND = "Oakmont";

function fixPoweredByText() {
    // Find all receipt footers
    const receiptFooters = document.querySelectorAll('.receipt-footer');
    
    receiptFooters.forEach(footer => {
        // Find paragraphs in footer
        const paragraphs = footer.querySelectorAll('p');
        paragraphs.forEach(p => {
            // Check if it contains "Powered by Odoo"
            if (p.textContent && p.textContent.includes('Powered by Odoo')) {
                p.textContent = 'Powered by ' + BRAND;
                console.log('✅ Fixed powered by text');
            }
            // Also check for just "Odoo" in footer
            else if (p.textContent && p.textContent.includes('Odoo') && 
                     p.textContent.includes('Powered')) {
                p.textContent = p.textContent.replace(/Odoo/g, BRAND);
            }
        });
    });
    
    // Also check for any element with powered by text
    const allElements = document.querySelectorAll('.receipt-screen p, .receipt-footer p, .order-receipt p');
    allElements.forEach(el => {
        if (el.textContent && el.textContent.includes('Powered by Odoo')) {
            el.textContent = 'Powered by ' + BRAND;
        }
    });
}

// Run when receipt is printed/displayed
function watchForReceipt() {
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) { // Element
                        if (node.classList && (node.classList.contains('receipt-screen') || 
                            node.classList.contains('receipt-footer') ||
                            node.classList.contains('order-receipt'))) {
                            setTimeout(fixPoweredByText, 100);
                        }
                    }
                });
            }
        });
    });
    
    if (document.body) {
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
}

// Run fixes
fixPoweredByText();
watchForReceipt();
setInterval(fixPoweredByText, 500);

