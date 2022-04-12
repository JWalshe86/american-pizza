const Pty = require('node-pty');
const fs = require('fs');

exports.install = function() {

    ROUTE('/');
    WEBSOCKET('/', socket, ['raw']);

};

function socket() {

    this.encodedecode = false;
    this.autodestroy();

    this.on('open', function(client) {

        // Spawn terminal
        client.tty = Pty.spawn('python3', ['run.py'], {
            name: 'xterm-color',
            cols: 80,
            rows: 24,
            cwd: process.env.PWD,
            env: process.env
        });

        client.tty.on('exit', function(code, signal) {
            client.tty = null;
            client.close();
            console.log("Process killed");
        });

        client.tty.on('data', function(data) {
            client.send(data);
        });

    });

    this.on('close', function(client) {
        if (client.tty) {
            client.tty.kill(9);
            client.tty = null;
            console.log("Process killed and terminal unloaded");
        }
    });

    this.on('message', function(client, msg) {
        client.tty && client.tty.write(msg);
    });
}

if (process.env.CREDS != null) {
    console.log("Creating creds.json file.");
    fs.writeFile('creds.json', process.env.CREDS, 'utf8', function(err) {
        if (err) {
            console.log('Error writing file: ', err);
            socket.emit("console_output", "Error saving credentials: " + err);
        }
    });
}

const mediaQuery = window.matchMedia('(max-width: 749px)');
if (mediaQuery.matches) {
    let container = document.createElement("div")
    container.setAttribute("id", "mobile-container")
    container.style.padding = "10px"
    container.style.textAlign = "center"
    let warning = document.createElement("p")
    warning.innerText = "Sorry!\nThis content is not available for devices under 750px"
    container.appendChild(warning)
    document.getElementById("terminal").appendChild(container);
}