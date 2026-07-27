odoo.define('custom_branding_pos.custom_content', function (require) {
    "use strict";
    console.log("Custom Branding JS loaded");

    setInterval(function () {
        document.title = document.title.replace('Odoo', 'Echosphere');
    }, 100);
});
