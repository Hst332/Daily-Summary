from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

IN_MD = "daily_summary.md"
OUT_PDF = "daily_summary.pdf"

def main():
    c = canvas.Canvas(OUT_PDF, pagesize=A4)
    width, height = A4
    x = 2 * cm
    y = height - 2 * cm
    line_height = 12

    c.setFont("Helvetica", 10)

    with open(IN_MD, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.rstrip("\n")

            # grobes Umbruch-Limit pro Zeile (monospace-ähnlich)
            while len(line) > 110:
                c.drawString(x, y, line[:110])
                line = line[110:]
                y -= line_height
                if y < 2 * cm:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = height - 2 * cm

            c.drawString(x, y, line)
            y -= line_height
            if y < 2 * cm:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 2 * cm

    c.save()
    print("Wrote", OUT_PDF)

if __name__ == "__main__":
    main()
