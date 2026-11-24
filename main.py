# Draws one image summing up Monday 23 November 2026 world news.
# Deterministic: no network, no randomness, no time or date calls.
# Writes a 1024x1024 PNG under 1 MiB to /output/entry.png.
# Twelve stories across regions and fields, each with place and detail.
# Fonts are bundled in this repo (DejaVuSans*.ttf) so the program runs
# anywhere, even where the system has no fonts installed.
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 232)
NAVY = (15, 42, 68)
WHITE = (255, 255, 255)
DARK = (20, 30, 40)
GREY = (70, 80, 90)

HERE = os.path.dirname(os.path.abspath(__file__))

def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(HERE, name), size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Header
d.rectangle([0, 0, W, 160], fill=NAVY)
d.text((32, 12), "THE WORLD IN ONE PAGE", font=font(True, 26), fill=(255, 210, 90))
d.text((32, 42), "MONDAY, 23 NOVEMBER 2026", font=font(True, 46), fill=WHITE)
d.text((32, 98), "Twelve stories that defined the day", font=font(False, 24), fill=(200, 215, 230))
d.text((32, 128), "Riemann  •  Nvidia  •  Korea  •  Congo  •  Yemen  •  Europe", font=font(False, 16), fill=(170, 190, 210))

stories = [
    ("TECH  •  GLOBAL", "AI helps prove Riemann hypothesis", "Anthropic says AI proved the famous puzzle; debate follows.", (0, 128, 128)),
    ("BUSINESS  •  USA", "Nvidia reinstates Jensen Huang", "Board brings back Huang as CEO; shares rise about 30%.", (200, 100, 0)),
    ("SECURITY  •  EUROPE", "Russia plans nuclear-armed satellite", "NATO intel: Moscow plans a satellite armed with a nuclear weapon.", (178, 34, 34)),
    ("KOREA  •  SEOUL", "First woman to lead spy agency", "Kang Kum-sil becomes first woman to head the NIS.", (30, 80, 180)),
    ("THAILAND  •  BANGKOK", "Court cuts MP's jail term to 3 years", "Appeals court upholds royal defamation conviction, reduces term.", (90, 50, 140)),
    ("CONGO  •  ITURI", "Fighting traps Ebola teams", "Fighting disrupts Ebola response near a hospital.", (120, 70, 20)),
    ("CLIMATE  •  BARBADOS", "Guterres urges AI regulation", "UN chief calls for stronger global rules on AI.", (0, 100, 60)),
    ("INDONESIA", "Factory fire kills at least 24", "Blaze at a sweets factory leaves about 30 missing.", (200, 60, 60)),
    ("HEALTH  •  UK", "NHS trials AI in breast screening", "EDITH trial invites nearly 700,000 women to test AI mammograms.", (30, 110, 160)),
    ("ECONOMY  •  EUROPE", "Euro inflation rises to 4.0%", "Eurostat reports higher inflation; tech shares fall.", (60, 90, 120)),
    ("USA  •  WASHINGTON", "Trump blames Democrats for market rout", "President links $6tn market fall, Iran tensions and oil to midterms.", (140, 40, 40)),
    ("YEMEN  •  HODEIDA", "Saudi attack kills four in port city", "Houthi media: strike kills four and wounds 18 in Yemen's key port.", (100, 60, 100)),
]

# Grid 2 x 6
x0, y0 = 24, 176
pw, ph = 476, 124
gapx, gapy = 24, 12
for i, (tag, head, summ, col) in enumerate(stories):
    col_i = i % 2
    row_i = i // 2
    x = x0 + col_i * (pw + gapx)
    y = y0 + row_i * (ph + gapy)
    d.rounded_rectangle([x, y, x + pw, y + ph], radius=12, fill=WHITE, outline=(200, 195, 180), width=2)
    d.rectangle([x, y, x + pw, y + 8], fill=col)
    d.ellipse([x + 16, y + 20, x + 52, y + 56], fill=col)
    d.text((x + 28, y + 27), str(i + 1), font=font(True, 22), fill=WHITE)
    d.text((x + 62, y + 28), tag, font=font(True, 15), fill=col)
    lines = textwrap.wrap(head, width=30)
    yy = y + 58
    for ln in lines[:2]:
        d.text((x + 16, yy), ln, font=font(True, 20), fill=DARK)
        yy += 25
    # one-line summary only if headline took one line
    if len(lines) == 1:
        slines = textwrap.wrap(summ, width=58)
        if slines:
            d.text((x + 16, yy + 2), slines[0], font=font(False, 15), fill=GREY)

# Footer
d.text((32, 992), "Monday 23 November 2026", font=font(True, 20), fill=NAVY)
d.text((560, 992), "World news, one image", font=font(False, 20), fill=GREY)

out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
os.makedirs(out, exist_ok=True)
img.save(os.path.join(out, "entry.png"), optimize=True)  # deterministic bytes, no metadata
print("saved entry.png")
