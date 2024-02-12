const express = require('express');
const bodyParser = require('body-parser');
const pool = require('./dbEcom');

const app = express();
app.use(bodyParser.json());

// Middleware to enable CORS
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*'); // Allow requests from any origin
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE'); // Allow the specified methods
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization'); // Allow the specified headers
    next();
});

// Route pour récupérer la liste de tous les produits
app.get('/products', (req, res) => {
    const query = 'SELECT * FROM products';

    // Exécuter la requête SQL
    pool.query(query, (err, result) => {
        if (err) {
            console.error('Erreur lors de l\'exécution de la requête :', err);
            res.status(500).json({ error: 'Erreur lors de la récupération des produits' });
        } else {
            res.json(result.rows);
        }
    });
});

// Helper function to generate unique IDs
function generateId() {
  return Math.random().toString(36).substr(2, 9);
}

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
