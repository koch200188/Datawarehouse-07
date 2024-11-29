import express from "express";
import pg from "pg";
const { Client } = pg;
const app = express();
const port = 3000;

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
    await clientDatawareHouse.connect();
    await clientDatawareHouse.query("LISTEN weather_data_updates");

    clientDatawareHouse.on("notification", async (msg) => {
      const payload = JSON.parse(msg.payload);

      const { operation, districtCode, date, temperature, wind, rainfall } =
        payload;

      const odsClient = new Client({
        user: "admin",
        host: "localhost",
        database: "ods",
        password: "Kennwort1",
        port: 5432,
      });

      await odsClient.connect();

      if (operation === "INSERT") {
        await odsClient.query(
          `INSERT INTO "RealtimeWeatherData" (districtCode, date, temperature, wind, rainfall)
           VALUES ($1, $2, $3, $4, $5)
           ON CONFLICT (districtCode, date) DO NOTHING`,
          [districtCode, date, temperature, wind, rainfall]
        );
        console.log(
          `Inserted data for districtCode: ${districtCode}, date: ${date}`
        );
      } else if (operation === "UPDATE") {
        await odsClient.query(
          `UPDATE "RealtimeWeatherData"
           SET temperature = $1, wind = $2, rainfall = $3
           WHERE districtCode = $4 AND date = $5`,
          [temperature, wind, rainfall, districtCode, date]
        );
        console.log(
          `Updated data for districtCode: ${districtCode}, date: ${date}`
        );
      } else if (operation === "DELETE") {
        await odsClient.query(
          `DELETE FROM "RealtimeWeatherData"
           WHERE districtCode = $1 AND date = $2`,
          [districtCode, date]
        );
        console.log(
          `Deleted data for districtCode: ${districtCode}, date: ${date}`
        );
      }
      await odsClient.end();
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
    await clientOds.connect();
    await clientOds.query("LISTEN ods_data_update");

    clientOds.on("notification", async (msg) => {
      const payload = JSON.parse(msg.payload);

      const { operation, districtCode, date, temperature, wind, rainfall } =
        payload;

      console.log("ods updated:", payload);
    });
  } catch (err) {
    console.error(
      "Error connecting to PostgreSQL or listening for notifications:",
      err
    );
  }
}

await DatawareHouseUpdater();
await OdsAction();

app.listen(port, () => console.log(`Server running on port ${port}`));
