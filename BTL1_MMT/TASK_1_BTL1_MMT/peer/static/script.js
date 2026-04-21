async function register() {
    await fetch('/register', { method: 'POST' });
}

async function loadPeers() {
    const res = await fetch('/peers');
    const data = await res.json();
    const ul = document.getElementById('peers');
    ul.innerHTML = '';
    data.peers.forEach(p => {
        const li = document.createElement('li');
        li.textContent = p.ip + ':' + p.port;
        ul.appendChild(li);
    });
}

async function sendMsg() {
    const msg = document.getElementById('msg').value;
    if (!msg) return;
    await fetch('/broadcast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ msg })
    });
    document.getElementById('chat').innerHTML += `<li>You: ${msg}</li>`;
    document.getElementById('msg').value = '';
}

async function loadMessages() {
    const res = await fetch('/messages');
    const data = await res.json();
    const chat = document.getElementById('chat');
    chat.innerHTML = '';
    data.messages.forEach(m => {
        const li = document.createElement('li');
        li.textContent = `[${m.time}] ${m.sender}: ${m.msg}`;
        chat.appendChild(li);
    });
}

setInterval(loadMessages, 2000);
