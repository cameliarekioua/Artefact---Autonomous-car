// scripts2.js

let activeCommands = {};

function sendCommand(command, action) {
    const url = `/api/move?direction=${command}&action=${action}`;
    fetch(url, { method: 'POST' })
        .then((response) => {
            if (!response.ok) {
                console.error(`Failed to send command: ${command}`);
            }
        })
        .catch((error) => console.error('Error:', error));
}

// Associe les touches aux commandes
const keyMap = {
    ArrowUp: 'forward',
    ArrowDown: 'backward',
    ArrowLeft: 'left',
    ArrowRight: 'right'
};

// Écoute les touches pressées
document.addEventListener('keydown', (event) => {
    const command = keyMap[event.key];
    if (command && !activeCommands[command]) {
        activeCommands[command] = true;
        sendCommand(command, 'start');
    }
});

// Écoute les touches relâchées
document.addEventListener('keyup', (event) => {
    const command = keyMap[event.key];
    if (command) {
        delete activeCommands[command];
        sendCommand(command, 'stop');
    }
});
