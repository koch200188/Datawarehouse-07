import express from "express";
import pg from "pg";
import http from "http";
import { WebSocketServer } from "ws";
import cors from "cors";

const { Client } = pg;
const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });
const port = 3000;

app.use(cors());

wss.on("connection", (ws) => {
  console.log("New WebSocket connection");

  ws.on("message", (message) => {
    console.log("Received:", message);
  });

  ws.on("close", () => {
    console.log("WebSocket connection closed");
  });
});

function broadcast(message) {
  wss.clients.forEach((client) => {
    if (client.readyState === 1) {
      client.send(JSON.stringify(message));
    }
  });
}

const temperatureTrigger = 30;
const windTrigger = 50;
const rainFallTrigger = 5;

const clientDatawareHouse = new Client({
  user: "admin",
  host: "localhost",
  database: "datawarehouse",
  password: "Kennwort1",
  port: 5432,
});

const clientOds = new Client({
  user: "admin",
  host: "localhost",
  database: "ods",
  password: "Kennwort1",
  port: 5432,
});

async function DatawareHouseUpdater() {
  try {
    console.log("Listening for updates on 'weather_data_updates' channel...");

    await clientDatawareHouse.query("LISTEN weather_data_updates");
    
    clientDatawareHouse.on("notification", async (msg) => {
      try {
        const payload = JSON.parse(msg.payload);
        console.log("Received notification from WeatherData:", payload);

        const { operation, districtCode, date, temperature, wind, rainfall } =
          payload;

        if (!operation || !districtCode || !date) {
          console.warn("Invalid notification payload received:", payload);
          return;
        }

        if (operation === "INSERT") {
          await clientOds.query(
            `INSERT INTO "RealtimeWeatherData" (districtCode, date, temperature, wind, rainfall)
             VALUES ($1, $2, $3, $4, $5)
             ON CONFLICT (districtCode, date) DO NOTHING`,
            [districtCode, date, temperature, wind, rainfall]
          );
          console.log(
            `Inserted new data into ODS for districtCode: ${districtCode}`
          );
        } else if (operation === "UPDATE") {
          await clientOds.query(
            `UPDATE "RealtimeWeatherData"
             SET temperature = $1, wind = $2, rainfall = $3
             WHERE districtCode = $4 AND date = $5`,
            [temperature, wind, rainfall, districtCode, date]
          );
          console.log(`Updated data in ODS for districtCode: ${districtCode}`);
        } else if (operation === "DELETE") {
          await clientOds.query(
            `DELETE FROM "RealtimeWeatherData"
             WHERE districtCode = $1 AND date = $2`,
            [districtCode, date]
          );
          console.log(
            `Deleted data from ODS for districtCode: ${districtCode}`
          );
        } else {
          console.warn("Unsupported operation:", operation);
        }
      } catch (err) {
        console.error("Error processing notification:", err);
      }
    });

    clientDatawareHouse.on("error", (err) => {
      console.error("Error with clientDatawareHouse:", err);
    });
  } catch (err) {
    console.error(
      "Error connecting to PostgreSQL or listening for notifications:",
      err
    );
  }
}

async function OdsAction() {
  try {
    await clientOds.query("LISTEN ods_data_update");

    clientOds.on("notification", async (msg) => {
      const payload = JSON.parse(msg.payload);

      const { operation, districtCode, date, temperature, wind, rainfall } =
        payload;

      if (temperature >= temperatureTrigger) {
        broadcast({
          text: `Temperature Warning ${temperature}`,
          temperature: temperature,
          date: new Date(),
        });
      }

      if (wind >= windTrigger) {
        broadcast({
          text: `Wind Warning ${wind}`,
          wind: wind,
          date: new Date(),
        });
      }

      if (rainfall >= rainFallTrigger) {
        broadcast({
          text: `Rainfall Warning ${rainfall}`,
          rainfall: rainfall,
          date: new Date(),
        });
      }

      console.log("ods updated:", payload);
    });
  } catch (err) {
    console.error(
      "Error connecting to PostgreSQL or listening for notifications:",
      err
    );
  }
}

await clientDatawareHouse.connect();
await clientOds.connect();
await DatawareHouseUpdater();
await OdsAction();

server.listen(port, () => console.log(`Server running on port ${port}`));
