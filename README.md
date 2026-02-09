# Qumulo Directory Aggregates Reporter

A robust Python wrapper for the Qumulo CLI (`qq`) that fetches directory statistics and presents them in a human-readable, formatted terminal table.

This script simplifies storage analysis by converting raw byte values into readable formats (TB, PB), adding thousands separators to file counts, and sorting directories by data usage.

## 🚀 Features

* **Human-Readable Sizes:** Automatically converts raw bytes to KB, MB, GB, TB, or PB.
* **Formatted Numbers:** Adds thousands separators (e.g., `1.574.493.270`) for better readability.
* **Dynamic Host Selection:** prompts for IP or DNS name (with a configurable default).
* **Secure Authentication:** Prompts for credentials without echoing the password.
* **Smart Sorting:** Automatically sorts the output by **Data Usage** (descending).
* **Detailed Columns:** Displays Data Usage, Capacity Usage (with overhead), File Count, Directory Count, and Symlinks.
* **Summary Footer:** Shows total statistics for the queried path at the end of the report.

## 📋 Prerequisites

* **Python 3.x** installed on your machine.
* The **Qumulo CLI script (`qq`)**.
* You can download this directly from your Qumulo cluster's Web UI (API & Tools section).


* Network access to the Qumulo Cluster (Port 8000/443).

## 📂 Installation & Setup

1. **Clone this repository** (or download the script):
```bash
git clone https://github.com/JochenKanta/qumulo-aggregates-reporter.git
cd qumulo-aggregates-reporter

```


2. **Add the Qumulo CLI:**
Place the `qq` file (the python script downloaded from your cluster) into the same directory as `qumulo_report_complete.py`.
Your folder structure should look like this:
```text
/qumulo-reporter
├── README.md
├── qumulo_report.py
└── qq                  <-- The Qumulo CLI script

```



## ⚙️ Configuration

You can set a **Default Host** inside the script to speed up the login process.

Open `qumulo_report.py` and edit line 9:

```python
# --- CONFIGURATION ---
DEFAULT_HOST = "qumulo.your-company.local" # Or IP address like 10.x.x.x

```

## 🖥️ Usage

Run the script using Python:

```bash
python qumulo_report.py

```

### Interactive Steps:

1. **Host:** Enter the IP or DNS name (or press Enter to use the default).
2. **Login:** Enter your Qumulo Username and Password.
3. **Path:** Enter the file system path you want to analyze (e.g., `/fs/fs1`).

## 📊 Example Output

```text
--- Qumulo Aggregates Reporter ---
Cluster IP oder DNS-Name eingeben [Standard: whateverDNS]: 

=== Login für Qumulo Cluster: 192.168.1.45 ===
Username: admin
Password: 
Authentifiziere...
✅ Login erfolgreich als 'admin'

Pfad eingeben (z.B. /fs/fs1) oder 'q' zum Beenden: /fs/fs1
Lade Daten von 10.60.98.32 für /fs/fs1 ...

Report für Pfad: /fs/fs1
Einträge gefunden: 50
---------------------------------------------------------------------------------------------------------------------------------------
Name                                 |   Data Usage |   Cap. Usage |           Files |         Dirs |   Symlinks
---------------------------------------------------------------------------------------------------------------------------------------
Gdata                                |      2.83 PB |      2.83 PB |   1.574.493.270 |   69.558.881 |    125.566
AI_training                          |    832.20 TB |    832.21 TB |       2.085.427 |        6.734 |          0
AI_training                          |    504.35 TB |    504.36 TB |           8.768 |          599 |          0
AI_training                          |    440.66 TB |    441.18 TB |     127.064.605 |   10.358.757 |          0
...
---------------------------------------------------------------------------------------------------------------------------------------
GESAMT ÜBERSICHT (TOTALS) für '/fs/fs1':
  Data Usage:    7.59 PB         |  Capacity Used: 7.60 PB
  Total Files:   3.800.114.798   |  Total Dirs:    93.475.685      |  Symlinks: 147.086
=======================================================================================================================================

```

## 🛠️ Troubleshooting

* **"Die Datei 'qq' wurde nicht gefunden!"**:
Ensure the `qq` file is in the same folder as the script.
* **Login Failed**:
Check if the IP/DNS is reachable and your credentials are correct.

## 📜 License

This project is open-source and available under the MIT License.

---

**Note:** This script is a wrapper around the official Qumulo CLI. It is not an official product of Qumulo.
