// Q1 - Simple Hello World Server
const express = require('express');

const app = express();
const PORT = 3001;

app.get('/', (req, res) => {
  res.send('Hello, world!');
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
// Q2 - DNS Registry Server
const dnsApp = express();
const DNS_PORT = 3000;

dnsApp.get('/getServer', (req, res) => {
  const serverUrl = `localhost:${PORT}`;
  res.json({ code: 200, server: serverUrl });
});

dnsApp.listen(DNS_PORT, () => {
  console.log(`DNS Registry Server is running on http://localhost:${DNS_PORT}`);
});