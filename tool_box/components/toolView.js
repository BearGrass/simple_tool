const axios = require('axios');

module.exports = {
    init: function(element) {
        this.element = element;
        window.addEventListener('toolSelected', (e) => this.showTool(e.detail));
    },

    showTool: function(tool) {
        this.element.innerHTML = `
            <h3>${tool}</h3>
            <input type="text" id="params" placeholder="Enter parameters">
            <button id="runTool">Run</button>
            <div id="result"></div>
        `;

        document.getElementById('runTool').addEventListener('click', () => {
            const params = document.getElementById('params').value;
            this.runTool(tool, params);
        });
    },

    runTool: async function(tool, params) {
        try {
            const response = await axios.post('http://localhost:5000/run_tool', {
                tool: tool,
                params: params
            });
            document.getElementById('result').textContent = response.data.result;
        } catch (error) {
            console.error('Error running tool:', error);
            document.getElementById('result').textContent = 'Error: ' + error.message;
        }
    }
};