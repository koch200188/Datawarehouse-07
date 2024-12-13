import { CircleAlertIcon, CircleMinusIcon } from "lucide-react";
import React, { useState, useEffect } from "react";

// Define the structure of the warning data
interface WeatherWarning {
  text: string;
  temperature?: number;
  wind?: number;
  rainfall?: number;
  date: Date;
}

const App: React.FC = () => {
  const [warnings, setWarnings] = useState<WeatherWarning[]>([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:3000");
    ws.onopen = () => {
      console.log("WebSocket connection established");
    };

    ws.onmessage = (event) => {
      const data: WeatherWarning = JSON.parse(event.data);
      // console.log(data);
      setWarnings((prevWarnings) => [...prevWarnings, data]);
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div>
    <nav>
        <h1 style={{ fontSize: "20px" }}>Weather-Warner</h1>
      </nav>
    <div style={{ padding: "20px" }}>
      
      <div>
        <p style={{ fontWeight: "medium", marginTop: "20px" }}>
          Current Warnings:
        </p>
        {warnings.length > 0 ? (
          <ul style={{ listStyleType: "none", padding: 0, marginTop: "10px" }}>
            {warnings.map((warning, index) => (
              <li
                key={index}
                style={{
                  border: "1px solid #dcdcdc",
                  borderRadius: "5px",
                  marginBottom: "10px",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "10px",
                  color: "red",
                }}
              >
                <div style={{ display: "flex", alignItems: "center" }}>
                  <CircleAlertIcon style={{ marginRight: "10px" }} />
                  <p>{warning.text}</p>
                </div>
                <p>{new Date(warning.date).toLocaleTimeString("de")}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p
            style={{
              border: "1px solid #dcdcdc",
              borderRadius: "5px",
              marginTop: "10px",
              padding: "10px",
              display: "flex",
              justifyItems: "center",
            }}
          >
            <CircleMinusIcon style={{ marginRight: "10px" }} />
            No Warning found
          </p>
        )}
      </div>
    </div>
    </div>
  );
};

export default App;
