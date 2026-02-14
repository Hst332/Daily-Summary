import os
import pandas as pd
from datetime import datetime

INDIZES_CSV = "indizes/forecasts/daily_index_forecast.csv"
ROHSTOFFE_TXT = "rohstoffe/forecast_output.txt"
OUT_FILE = "daily_summary.md"

def read_indizes():
    if not os.path.exists(INDIZES_CSV):
        return "## Indizes\n⚠️ Datei nicht gefunden.\n"

    df = pd.read_csv(INDIZES_CSV)

    wanted = ["asset","signal","confidence","prob_up","prob_down","close","daily_return","regime"]
    cols = [c for c in wanted if c in df.columns]
    df = df[cols]

    if "daily_return" in df.columns:
        df["daily_return"] = df["daily_return"].map(lambda x: f"{x:.2f}%" if pd.notna(x) else "")

    for c in ["confidence","prob_up","prob_down"]:
        if c in df.columns:
            df[c] = df[c].map(lambda x: f"{x:.2f}" if pd.notna(x) else "")

    return "## Indizes\n\n" + df.to_markdown(index=False) + "\n\n"


def read_rohstoffe():
    if not os.path.exists(ROHSTOFFE_TXT):
        return "## Rohstoffe\n⚠️ Datei nicht gefunden.\n"

    lines = open(ROHSTOFFE_TXT, "r", encoding="utf-8", errors="replace").read().splitlines()
    head = lines[:120]

    return "## Rohstoffe\n\n```\n" + "\n".join(head) + "\n```\n\n"


def main():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    md = f"# Daily Combined Summary\n\nGenerated: {now}\n\n"
    md += read_indizes()
    md += read_rohstoffe()

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(md)

    print("Summary created.")


if __name__ == "__main__":
    main()
