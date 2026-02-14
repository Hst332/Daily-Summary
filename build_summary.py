import os
import pandas as pd
from datetime import datetime

INDIZES_CSV = "indizes/forecasts/daily_index_forecast.csv"
ROHSTOFFE_TXT = "rohstoffe/forecast_output.txt"
OUT_FILE = "daily_summary.md"

def read_indizes():
    if not os.path.exists(INDIZES_CSV):
        return "### Indizes\n⚠️ Datei nicht gefunden: `forecasts/daily_index_forecast.csv`\n"

    df = pd.read_csv(INDIZES_CSV)

    # robust: nur Spalten nehmen, die es wirklich gibt
    wanted = ["asset", "signal", "confidence", "prob_up", "prob_down", "close", "daily_return", "regime"]
    cols = [c for c in wanted if c in df.columns]
    df = df[cols].copy()

    # Formatierungen (falls Spalten existieren)
    if "daily_return" in df.columns:
        # in deinem Repo ist daily_return bereits Prozentwerte, wir formatieren sanft
        df["daily_return"] = df["daily_return"].map(lambda x: f"{x:.2f}%" if pd.notna(x) else "")
    for c in ["confidence", "prob_up", "prob_down"]:
        if c in df.columns:
            df[c] = df[c].map(lambda x: f"{x:.2f}" if pd.notna(x) else "")

    md = "### Indizes\n\n"
    md += df.to_markdown(index=False)
    md += "\n"
    return md

def read_rohstoffe():
    if not os.path.exists(ROHSTOFFE_TXT):
        return "### Rohstoffe\n⚠️ Datei nicht gefunden: `forecast_output.txt`\n"

    lines = open(ROHSTOFFE_TXT, "r", encoding="utf-8", errors="replace").read().splitlines()

    # kompakt: nimm die ersten ~120 Zeilen (da stehen i.d.R. Tabelle + Kernaussagen)
    head = lines[:120]

    md = "### Rohstoffe\n\n"
    md += "```\n" + "\n".join(head) + "\n```\n"
    return md

def main():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    md = f"# Daily Combined Summary\n\n_Generated: {now}_\n\n"
    md += read_indizes() + "\n"
    md += read_rohstoffe() + "\n"

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Wrote {OUT_FILE}")

if __name__ == "__main__":
    main()
