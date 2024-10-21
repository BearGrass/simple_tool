const sidebar = require('./components/sidebar');
const toolView = require('./components/toolView');

document.addEventListener('DOMContentLoaded', () => {
    sidebar.init(document.getElementById('sidebar'));
    toolView.init(document.getElementById('main-content'));
});