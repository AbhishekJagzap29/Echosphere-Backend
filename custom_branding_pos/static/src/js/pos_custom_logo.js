/** @odoo-module **/

console.log("%c🖼️ Oakmont Custom Logo Loaded", "color: green; font-size: 14px; font-weight: bold;");

function replacePOSLogo() {
    // Only run in POS
    if (!window.location.pathname.includes('/pos')) return;
    
    // Find the logo image
    const logoImg = document.querySelector('.pos-branding img.pos-logo');
    if (!logoImg) return;
    
    // Check if it's already replaced
    if (logoImg.src.includes('oakmont-logo.png')) return;
    
    // Replace with custom logo
    logoImg.src = '/custom_branding_pos/static/src/img/oakmont-logo.png';
    logoImg.alt = 'Oakmont Logo';
    console.log('✅ POS logo replaced with custom image');
}

// Run multiple times to ensure replacement
replacePOSLogo();
setTimeout(replacePOSLogo, 100);
setTimeout(replacePOSLogo, 300);
setTimeout(replacePOSLogo, 500);
setTimeout(replacePOSLogo, 1000);
setTimeout(replacePOSLogo, 2000);

// Watch for DOM changes (in case logo is loaded dynamically)
const observer = new MutationObserver(replacePOSLogo);
if (document.body) {
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}