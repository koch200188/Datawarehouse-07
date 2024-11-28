const express = require("express");
const { Client } = require("pg");
const app = express();
const port = 3000;
const WebSocket = require("ws");

const wss = new WebSocket.Server({ port: 8983 });

const client = new Client({
  user: "admin",
  host: "localhost",
  database: "datawarehouse",
  password: "Kennwort1",
  port: 5432,
});

client.connect();

app.get("/weather/:districtCode", async (req, res) => {
  const { districtCode } = req.params;
  const { startDate, endDate } = req.query;

  const query = `
        SELECT * FROM WeatherData 
        WHERE districtCode = $1 AND date BETWEEN $2 AND $3
    `;
  const values = [districtCode, startDate, endDate];

  try {
    const result = await client.query(query, values);
    res.json(result.rows);
  } catch (err) {
    res.status(500).send(err.message);
  }
});

client.on("notification", (msg) => {
  const data = JSON.parse(msg.payload);
  wss.clients.forEach((ws) => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(data));
    }
  });
});

client.query("LISTEN data_updates");

app.listen(port, () => console.log(`Server running on port ${port}`));
