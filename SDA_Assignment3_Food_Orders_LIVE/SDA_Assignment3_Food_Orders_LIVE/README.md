# SDA Assignment 3 – Live Food Orders Dashboard

## What this version does

This is the quickest live-demo version of the Food Orders dashboard.

A Python live producer creates a new simulated food order every 2 seconds. The order is written to `live_orders.json`, and the Streamlit dashboard automatically refreshes every 2 seconds and reads the new data.

```text
live_producer.py
      ↓
live_orders.json
      ↓
dashboard.py
      ↓
auto-refresh every 2 seconds
```

## Run it

### 1. Install packages

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Terminal 1 – start the live producer

```powershell
.\.venv\Scripts\python.exe live_producer.py
```

Leave this terminal running.

You should see:

```text
New event: FOOD2011 | REST104 | ₹...
New event: FOOD2012 | REST102 | ₹...
...
```

### 3. Terminal 2 – start the dashboard

Open another PowerShell in the same folder:

```powershell
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

Open the Local URL shown by Streamlit, normally:

```text
http://localhost:8501
```

### 4. Demonstrate that it is live

Keep both terminals running.

The dashboard should update automatically:

```text
Orders: 10
↓
11
↓
12
↓
13
...
```

Revenue, charts, and the latest-event table update as new orders arrive.

## Notes

This is a **simulated live stream for local demonstration**. It is intentionally independent of MongoDB Atlas so a network/TLS issue cannot stop the dashboard demo.

For a full production-style submission, the Kafka → consumer → MongoDB pipeline can be connected separately.
