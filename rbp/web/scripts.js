//interface.html

// Fonction pour activer le mode manuel via une requête POST
function activateManualMode() {
	const xhr = new XMLHttpRequest();
	xhr.open("POST", "/api/mode?manual", true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status === 200) {
			console.log("Manual mode 1 activated");
			// Redirige vers la page de contrôle manuel après activation
			window.location.href = "manual.html";
		} else if (xhr.readyState === 4) {
			console.error("Erreur lors de l'activation du mode 1 manuel");
		}
	};
	xhr.send();
}
function activateManualMode2() {
	const xhr = new XMLHttpRequest();
	xhr.open("POST", "/api/mode?manual2", true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status === 200) {
			console.log("Manual mode 2 activated");
			// Redirige vers la page de contrôle manuel2 après activation
			window.location.href = "manual2.html";
		} else if (xhr.readyState === 4) {
			console.error("Erreur lors de l'activation du mode 2 manuel");
		}
	};
	xhr.send();
}
// Fonction pour activer le mode automatique via une requête POST
function activateAutomaticMode() {
	const xhr = new XMLHttpRequest();
	xhr.open("POST", "/api/mode?automatic", true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status === 200) {
			console.log("Automatic mode activated");
			// Redirige vers la page de contrôle automatique après activation
			window.location.href = "automatic.html";
		} else if (xhr.readyState === 4) {
			console.error("Erreur lors de l'activation du mode automatique");
		}
	};
	xhr.send();
}




//manual.html

// Fonction pour envoyer une commande de mouvement
function sendCommand(direction) {
	const xhr = new XMLHttpRequest();
	xhr.open("POST", `/api/move?direction=${direction}`, true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4) {
			if (xhr.status === 200) {
				console.log(`Commande envoyée : ${direction}`);
			}
			else {
				console.error(`Erreur lors de l'envoi de la commande : ${direction}`);
			}
		}
	};

	xhr.send();
}


//automatic.html

function activateMode(mode) {
	if (mode === 'navigate') {
		document.getElementById('navigate-form').style.display = 'block';
		document.getElementById('status').innerText = 'Automatic mode: Navigate to Specific Case';
	} else if (mode === 'flaghunt') {
		document.getElementById('navigate-form').style.display = 'none';
		sendModeRequest('flaghunt');
	}
}

function sendNavigateRequest() {
	const startCell = document.getElementById('start-cell').value;
	const targetCell = document.getElementById('target-cell').value;

	// Validate inputs
	if (!startCell.match(/^[A-G][1-3]$/)) {
		alert('Invalid starting case format! Use format like A1.');
		return;
	}

	if (!targetCell.match(/^[A-G][1-3]$/)) {
		alert('Invalid target case format! Use format like B3.');
		return;
	}

	// Send request to server
	const xhr = new XMLHttpRequest();
	xhr.open("POST", `/api/launch?navigate&start=${startCell}&target=${targetCell}`, true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4) {
			if (xhr.status === 200) {
				document.getElementById('status').innerText = `Automatic Mode: Navigating from ${startCell} to ${targetCell}`;
				console.log(`Navigating from ${startCell} to ${targetCell}`);
			} else {
				console.error('Failed to send navigate request');
			}
		}
	};

	xhr.send();
}

function sendModeRequest(mode) {
	const xhr = new XMLHttpRequest();
	xhr.open("POST", `/api/automatic_mode?${mode}`, true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4) {
			if (xhr.status === 200) {
				document.getElementById('status').innerText = `Automatic mode: ${mode === 'flaghunt' ? 'Flag Hunt Active' : 'Active'}`;
				console.log(`${mode} automatic mode activated`);
			} else {
				console.error(`Failed to activate ${mode} automatic mode`);
			}
		}
	};

	xhr.send();
}
