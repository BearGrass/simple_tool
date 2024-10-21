module.exports = {
    init: function(element) {
        element.innerHTML = `
            <h2>Tools</h2>
            <ul>
                <li><a href="#" data-tool="tool1">Tool 1</a></li>
                <li><a href="#" data-tool="tool2">Tool 2</a></li>
            </ul>
        `;

        element.addEventListener('click', (e) => {
            if (e.target.tagName === 'A') {
                const tool = e.target.getAttribute('data-tool');
                this.onToolSelect(tool);
            }
        });
    },

    onToolSelect: function(tool) {
        // 通知 toolView 显示选中的工具
        window.dispatchEvent(new CustomEvent('toolSelected', { detail: tool }));
    }
};