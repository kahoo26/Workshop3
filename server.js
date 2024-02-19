const express = require('express');

const app = express();
const PORT = 3001; 


app.get('/getServer', (req, res) => {
  const serverUrl = `localhost:${PORT}`;
  res.json({ code: 200, server: serverUrl });
});

// Starting the server
app.listen(PORT, () => {
  console.log(`DNS registry server is running on http://localhost:${PORT}`);
});
