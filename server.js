require('dotenv').config();
const express = require('express');
const { MongoClient } = require('mongodb');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// MongoDB Connection
const mongoURI = process.env.DATABASE_URL;
const client = new MongoClient(mongoURI);

async function connectToDatabase() {
    try {
        await client.connect();
        console.log('Connected to MongoDB');
        const db = client.db();

        // Make the db object available to the app
        app.locals.db = db;

        // Start the server after connecting to the database
        app.listen(port, () => {
            console.log(`Server listening on port ${port}`);
        });
    } catch (error) {
        console.error('Error connecting to MongoDB:', error);
        process.exit(1);
    }
}

// Define a basic route
app.get('/', (req, res) => {
    res.send('Hello from Reality Checkers!');
});

// New API endpoint for searching
app.get('/api/search', async(req, res) => {
    try {
        const db = req.app.locals.db; // Access the db object from app.locals
        const sources = await db.collection('sources').find({}).toArray();
        res.json(sources);
    } catch (error) {
        console.error('Error fetching sources:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

db.sources.insertMany([{
        name: "The New York Times",
        url: "https://www.nytimes.com/",
        reliabilityScore: 8,
        bias: "center-left"
    },
    {
        name: "The Wall Street Journal",
        url: "https://www.wsj.com/",
        reliabilityScore: 9,
        bias: "center-right"
    },
    {
        name: "NPR",
        url: "https://www.npr.org/",
        reliabilityScore: 9,
        bias: "center-left"
    },
    {
        name: "The Guardian",
        url: "https://www.theguardian.com/",
        reliabilityScore: 8,
        bias: "left"
    },
    {
        name: "The Economist",
        url: "https://www.economist.com/",
        reliabilityScore: 9,
        bias: "center-right"
    },
    {
        name: "Al Jazeera",
        url: "https://www.aljazeera.com/",
        reliabilityScore: 8,
        bias: "center"
    },
    {
        name: "Bloomberg",
        url: "https://www.bloomberg.com/",
        reliabilityScore: 9,
        bias: "center-right"
    },
    {
        name: "Pew Research Center",
        url: "https://www.pewresearch.org/",
        reliabilityScore: 10,
        bias: "center"
    },
    {
        name: "FactCheck.org",
        url: "https://www.factcheck.org/",
        reliabilityScore: 10,
        bias: "center"
    },
    {
        name: "Snopes",
        url: "https://www.snopes.com/",
        reliabilityScore: 10,
        bias: "center"
    },
    {
        name: "ProPublica",
        url: "https://www.propublica.org/",
        reliabilityScore: 9,
        bias: "center-left"
    },
    {
        name: "USA Today",
        url: "https://www.usatoday.com/",
        reliabilityScore: 7,
        bias: "center"
    },
    {
        name: "Axios",
        url: "https://www.axios.com/",
        reliabilityScore: 8,
        bias: "center"
    },
    {
        name: "Politico",
        url: "https://www.politico.com/",
        reliabilityScore: 7,
        bias: "center-left"
    },
    {
        name: "The Hill",
        url: "https://thehill.com/",
        reliabilityScore: 7,
        bias: "center"
    },
    {
        name: "Christian Science Monitor",
        url: "https://www.csmonitor.com/",
        reliabilityScore: 9,
        bias: "center"
    },
    {
        name: "Vox",
        url: "https://www.vox.com/",
        reliabilityScore: 7,
        bias: "left"
    },
    {
        name: "ABC News",
        url: "https://abcnews.go.com/",
        reliabilityScore: 7,
        bias: "center"
    },
    {
        name: "CBS News",
        url: "https://www.cbsnews.com/",
        reliabilityScore: 7,
        bias: "center"
    },
    {
        name: "NBC News",
        url: "https://www.nbcnews.com/",
        reliabilityScore: 7,
        bias: "center-left"
    }
]);

// Connect to the database and start the server
connectToDatabase();