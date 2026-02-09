import subprocess
import json
import getpass
import sys
import os

# --- KONFIGURATION ---
# Standard-Host, falls der Nutzer nichts eingibt (Enter drückt)
DEFAULT_HOST = "hostname"

# Wir rufen 'qq' via 'python qq' auf. 
# Annahme: Die Datei 'qq' liegt im selben Verzeichnis wie dieses Script.
QQ_CMD = [sys.executable, "qq"]

def format_bytes(size):
    """Konvertiert Bytes in lesbare Einheiten (TB, PB, etc.)."""
    try:
        n = float(size)
        if n <= 0: return "0 B"
        labels = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
        x = 0
        while n >= 1024 and x < len(labels) - 1:
            n /= 1024
            x += 1
        return f"{n:.2f} {labels[x]}"
    except (ValueError, TypeError):
        return "0 B"

def format_number(num_str):
    """Formatiert Zahlen mit Tausender-Punkten (deutsch)."""
    try:
        # String zu Int, dann formatieren mit Komma, dann Komma zu Punkt ersetzen
        return f"{int(num_str):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "0"

def run_qq(args, host):
    """
    Wrapper für den Aufruf der QQ CLI.
    """
    # Hier wird der Host dynamisch in den Befehl eingebaut
    cmd = QQ_CMD + ["--host", host] + args
    
    try:
        # encoding='utf-8' ist wichtig für Sonderzeichen in Pfaden
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if res.returncode != 0:
            # Fehlerhandling, aber wir geben None zurück, damit das Hauptprogramm nicht crasht
            print(f"\n[ERROR] Befehl fehlgeschlagen: {' '.join(args)}")
            print(f"Server Antwort: {res.stderr.strip()}")
            return None
            
        return res.stdout
    except FileNotFoundError:
        print("\n[CRITICAL] Die Datei 'qq' wurde nicht gefunden!")
        print("Bitte stelle sicher, dass das Qumulo CLI Script im selben Ordner liegt.")
        sys.exit(1)

def do_login(host):
    """
    Handled den Login Prozess für einen spezifischen Host.
    """
    print(f"\n=== Login für Qumulo Cluster: {host} ===")
    user = input("Username: ").strip()
    if not user: return False
    
    pw = getpass.getpass("Password: ")
    
    print("Authentifiziere...", end="\r")
    # Host wird an run_qq übergeben
    result = run_qq(["login", "-u", user, "-p", pw], host)
    
    if result is not None:
        print(f"✅ Login erfolgreich als '{user}'\n")
        return True
    return False

def print_table(data, path):
    """Gibt die Daten als formatierte Tabelle aus + Summary Footer."""
    files = data.get("files", [])
    
    print(f"\nReport für Pfad: {path}")
    print(f"Einträge gefunden: {len(files)}")
    print("-" * 135)
    
    # Header Definition
    header = f"{'Name':<40} | {'Data Usage':>12} | {'Cap. Usage':>12} | {'Files':>15} | {'Dirs':>12} | {'Symlinks':>10}"
    print(header)
    print("-" * 135)

    # Sortierung: Absteigend nach Data Usage
    sorted_files = sorted(files, key=lambda x: int(x.get('data_usage', 0)), reverse=True)

    for item in sorted_files:
        name = item.get('name', 'N/A')
        # Namen kürzen, falls zu lang
        if len(name) > 38:
            name = name[:35] + "..."

        # Werte formatieren
        d_usage = format_bytes(item.get('data_usage', 0))
        c_usage = format_bytes(item.get('capacity_usage', 0))
        n_files = format_number(item.get('num_files', 0))
        n_dirs  = format_number(item.get('num_directories', 0))
        n_sym   = format_number(item.get('num_symlinks', 0))

        print(f"{name:<40} | {d_usage:>12} | {c_usage:>12} | {n_files:>15} | {n_dirs:>12} | {n_sym:>10}")
    
    print("=" * 135)
    
    # ---SUMMARY FUNKTION ---
    # Werte aus dem Root des JSONs holen
    t_data = format_bytes(data.get('total_data', 0))
    t_cap  = format_bytes(data.get('total_capacity', 0))
    t_files = format_number(data.get('total_files', 0))
    t_dirs  = format_number(data.get('total_directories', 0))
    t_sym   = format_number(data.get('total_symlinks', 0))

    print(f"GESAMT ÜBERSICHT (TOTALS) für '{path}':")
    print(f"  Data Usage:    {t_data:<15} |  Capacity Used: {t_cap}")
    print(f"  Total Files:   {t_files:<15} |  Total Dirs:    {t_dirs:<15} |  Symlinks: {t_sym}")
    print("=" * 135)
    print("\n")

def main():
    print("--- Qumulo Aggregates Reporter ---")
    
    # 1. Host abfragen
    host_input = input(f"Cluster IP oder DNS-Name eingeben [Standard: {DEFAULT_HOST}]: ").strip()
    
    # Wenn leer (Enter gedrückt), nimm den Standard
    if not host_input:
        host = DEFAULT_HOST
    else:
        host = host_input

    # 2. Login mit dem gewählten Host
    if not do_login(host):
        return

    # 3. Loop für Pfad-Abfragen
    while True:
        path = input("Pfad eingeben (z.B. /fs/fs1) oder 'q' zum Beenden: ").strip()
        
        if path.lower() in ['q', 'quit', 'exit']:
            print("Programm beendet.")
            break
            
        if not path:
            continue

        print(f"Lade Daten von {host} für {path} ...", end="\r")
        
        # Befehl ausführen mit Host und Pfad
        json_str = run_qq(["fs_read_dir_aggregates", "--path", path], host)

        if json_str:
            try:
                data = json.loads(json_str)
                print_table(data, path)
            except json.JSONDecodeError:
                print("\n[ERROR] Ungültiges JSON vom Server erhalten (Evtl. ist der Pfad falsch).")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer.")
