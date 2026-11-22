#!/usr/bin/env python3
"""Draw the news-image-20261122 front page: one 1024x1024 newspaper page
summing up Sunday 22 November 2026. Pillow only, no network, no randomness:
running this script twice writes byte-identical PNGs.

Stories, verified by web search on 22 Nov 2026 (BBC, AP via CNN / LA Post /
europesays, The Times, Reuters via Dainik Jagran, Daily Perspective,
IQMIA world summary, News Media House):
- LEAD, 22 Nov: Mexico captures Fausto Isidro Meza Flores, "El Chapo
  Isidro", an FBI Ten Most Wanted fugitive with a $5m reward, in a Friday
  night special-forces raid on Guasave, Sinaloa. Four soldiers and seven
  gunmen are killed; cartel roadblocks and gunfire empty a baseball
  stadium; he is flown to Mexico City on Saturday.
- ANTALYA: COP31, in double overtime, releases a new draft in the early
  hours of Sunday that still contains no mention of fossil fuels; the EU
  calls it a backwards step. The draft keeps a 35%-electricity-by-2035
  goal and a gigatonne carbon-capture goal, and drops the $120bn-a-year
  adaptation-finance target.
- WASHINGTON: the FBI investigates an apparent hack of its NCIC criminal
  database, used by federal and local police to share records.
- INDONESIA: a fire at a confectionery factory kills at least 3 people;
  36 are still missing.
- GULF OF FINLAND: a Russian cargo ship is hit by drones and catches
  fire, in a spillover of the war at sea.
- ALSO TODAY: Max Verstappen wins an extraordinary Las Vegas Grand Prix
  with 34 lead changes as the Ferraris collide; Victor Wembanyama scores
  50 as the Spurs beat the Pelicans 114-91; Leeds stun Chelsea 4-1 at
  Stamford Bridge, their first win there since 1999; GTA VI's $3.79bn
  launch-day haul sets a record; Iran strikes an industrial site in
  Bahrain; Zelensky calls the Crimean Bridge strikes a fair response;
  Poland accuses Russia of an airspace violation and NATO pledges to defend
  every inch of Polish territory; UN states reach a tentative deal on autonomous weapons;
  at least 24 die as a boat capsizes on a funeral trip in Nigeria; Amazon
  nears a $7.5bn deal for Israeli AI start-up Decart.
"""
import math

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
CRIMSON = (163, 24, 44)
NAVY = (24, 68, 112)
SEA = (52, 110, 158)
LAND = (216, 195, 140)
MUTED = (88, 88, 88)
FAINT = (232, 226, 207)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"


def load(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def serif_b(size):
    return load("LiberationSerif-Bold.ttf", size)


def serif(size):
    return load("LiberationSerif-Regular.ttf", size)


def serif_i(size):
    return load("LiberationSerif-Italic.ttf", size)


def sans_b(size):
    return load("LiberationSans-Bold.ttf", size)


def sans(size):
    return load("LiberationSans-Regular.ttf", size)


page = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
pen = ImageDraw.Draw(page)

LEFT = 36
RIGHT = CANVAS_W - LEFT
SPAN = RIGHT - LEFT


def split_lines(text, face, width):
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if pen.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def block(text, face, x, y, width, gap, colour=INK):
    for line in split_lines(text, face, width):
        pen.text((x, y), line, font=face, fill=colour)
        y += gap
    return y


def hline(x0, y, x1, thick=2, colour=INK):
    pen.line([(x0, y), (x1, y)], fill=colour, width=thick)


def star(cx, cy, r, colour):
    """Five-pointed star, drawn as a polygon."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    pen.polygon(pts, fill=colour)


# ---------------- masthead ----------------
pen.text((CANVAS_W // 2, 16), "THE WORLD", font=serif_b(82),
         fill=INK, anchor="ma")
pen.text((CANVAS_W // 2, 102), "The day's news in one page",
         font=serif_i(19), fill=MUTED, anchor="ma")
hline(LEFT, 132, RIGHT, 3)
hline(LEFT, 137, RIGHT, 1)
pen.text((LEFT, 144), "SUNDAY, 22 NOVEMBER 2026", font=sans_b(18), fill=CRIMSON)
pen.text((RIGHT, 144), "WORLD NEWS  •  ONE IMAGE", font=sans_b(18),
         fill=INK, anchor="ra")
hline(LEFT, 170, RIGHT, 1)

# ---------------- lead: El Chapo Isidro captured ----------------
y = 182
pen.text((LEFT, y), "MEXICO  —  THE KINGPIN FALLS", font=sans_b(19),
         fill=CRIMSON)
y = 206
y = block("Mexico captures \u2018El Chapo Isidro\u2019 after a night of gunfire",
          serif_b(43), LEFT, y, SPAN, 49)
y += 2
y = block("FBI Ten Most Wanted fugitive Fausto Isidro Meza Flores is seized "
          "in Guasave, Sinaloa; four soldiers and seven gunmen are killed "
          "as cartel roadblocks burn.", serif_i(20), LEFT, y, SPAN, 26,
          colour=(62, 62, 62))
y += 8

map_x, map_y, map_w, map_h = LEFT, y, SPAN, 102
# Night over Sinaloa: dark sky, the coast of Mexico, the Gulf of California.
pen.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(16, 26, 46))
pen.polygon([(map_x, map_y), (map_x + 620, map_y),
             (map_x + 560, map_y + 44), (map_x + 470, map_y + 40),
             (map_x + 400, map_y + 74), (map_x + 300, map_y + 70),
             (map_x + 180, map_y + 118), (map_x, map_y + 118)],
            fill=(58, 84, 66))
pen.polygon([(map_x + 660, map_y), (map_x + map_w, map_y),
             (map_x + map_w, map_y + 118), (map_x + 700, map_y + 118),
             (map_x + 660, map_y + 60)], fill=(24, 48, 74))
pen.text((map_x + 16, map_y + 8), "MEXICO", font=sans_b(17),
         fill=(220, 220, 200))
pen.text((map_x + 16, map_y + 74), "SINALOA", font=sans_b(15),
         fill=(220, 220, 200))
pen.text((map_x + 700, map_y + 8), "GULF OF CALIFORNIA", font=sans_b(13),
         fill=(180, 200, 220))
# Guasave: gold star on the coast, with roadblock fires nearby.
gx, gy = map_x + 330, map_y + 62
star(gx, gy, 13, (255, 210, 60))
pen.text((gx + 18, gy - 9), "GUASAVE", font=sans_b(14), fill=(255, 255, 255))
for (rx, ry) in [(map_x + 420, map_y + 78), (map_x + 250, map_y + 88),
                 (map_x + 480, map_y + 52)]:
    pen.ellipse([rx - 4, ry - 4, rx + 4, ry + 4], fill=(255, 90, 40))
    pen.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=(255, 190, 60))
pen.text((map_x + map_w - 14, map_y + map_h - 24),
         "CAPTURED FRIDAY NIGHT  •  FLOWN TO MEXICO CITY SATURDAY  •  "
         "11 KILLED  •  $5M REWARD",
         font=sans_b(13), fill=(255, 255, 255), anchor="ra")
y = map_y + map_h + 8
y = block("Special forces took Meza Flores, 44, with US intelligence help "
          "after a stealth approach; gunfire emptied a baseball stadium in "
          "Guasave and helicopters fired on cartel gunmen below.",
          serif(18), LEFT, y, SPAN, 24)
y += 4
hline(LEFT, y, RIGHT, 1)
y += 8

# ---------------- row two: two columns ----------------
HALF = 464
top2 = y


def draft_doc(x0, y0, w, h):
    """The COP31 draft: a page whose key words are struck out."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(255, 255, 255),
                  outline=(150, 150, 150), width=1)
    pen.text((x0 + 12, y0 + 5), "COP31  •  DRAFT DECISION", font=sans_b(12),
             fill=INK)
    for i, ly in enumerate(range(y0 + 26, y0 + h - 8, 10)):
        if y0 + 30 <= ly <= y0 + 52:
            continue  # keep the struck-out line clear of grey rules
        pen.line([(x0 + 12, ly), (x0 + w - 12, ly)], fill=(190, 190, 190),
                 width=2)
    # The struck-out line.
    pen.text((x0 + 12, y0 + 34), "FOSSIL FUELS", font=sans_b(13),
             fill=(120, 120, 120))
    pen.line([(x0 + 10, y0 + 42), (x0 + 118, y0 + 42)], fill=CRIMSON,
             width=3)
    pen.text((x0 + w - 12, y0 + 34), "35% BY 2035", font=sans_b(13),
             fill=CRIMSON, anchor="ra")


def servers(x0, y0, w, h):
    """The FBI database: a rack of servers under a warning."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(22, 30, 48))
    for i in range(3):
        sx = x0 + 14 + i * 118
        pen.rectangle([sx, y0 + 12, sx + 104, y0 + h - 12],
                      fill=(58, 66, 88))
        for r in range(3):
            pen.ellipse([sx + 10, y0 + 22 + r * 16, sx + 16, y0 + 28 + r * 16],
                        fill=(90, 200, 120))
            pen.line([(sx + 24, y0 + 25 + r * 16), (sx + 92, y0 + 25 + r * 16)],
                     fill=(150, 160, 180), width=2)
    # Warning triangle over the middle rack.
    tx, ty = x0 + w // 2, y0 + 8
    pen.polygon([(tx, ty), (tx - 16, ty + 26), (tx + 16, ty + 26)],
                fill=(255, 190, 0), outline=(150, 100, 0))
    pen.text((tx, ty + 6), "!", font=sans_b(16), fill=(18, 18, 18),
             anchor="ma")


x = LEFT
pen.text((x, top2), "ANTALYA  —  CLIMATE TALKS IN OVERTIME", font=sans_b(15),
         fill=CRIMSON)
yy = block("COP31's new draft still omits fossil fuels",
           serif_b(28), x, top2 + 22, HALF, 32)
yy += 4
draft_doc(x, yy, HALF, 74)
yy += 74 + 6
end_left = block("Released at 3 a.m. on Sunday, the text keeps a 35% "
                 "electricity goal and drops the $120bn adaptation-finance "
                 "target; the EU calls it a backwards step.",
                 serif(17), x, yy, HALF, 22)

x = RIGHT - HALF
pen.text((x, top2), "WASHINGTON  —  THE DATABASE BREACH", font=sans_b(15),
         fill=CRIMSON)
yy = block("FBI probes hack of its crime database",
           serif_b(28), x, top2 + 22, HALF, 32)
yy += 4
servers(x, yy, HALF, 74)
yy += 74 + 6
end_right = block("The NCIC system, used by federal and local police to "
                  "share fingerprints, warrants and missing-person records, "
                  "is under investigation after an apparent breach.",
                  serif(17), x, yy, HALF, 22)
y = max(end_left, end_right) + 6
hline(LEFT, y, RIGHT, 1)
y += 8

# ---------------- row three: two short items ----------------
def flame(cx, cy):
    pen.polygon([(cx, cy - 16), (cx + 9, cy - 2), (cx + 12, cy + 6),
                 (cx + 6, cy + 14), (cx - 6, cy + 14), (cx - 12, cy + 6),
                 (cx - 9, cy - 2)], fill=(255, 110, 20))
    pen.ellipse([cx - 5, cy + 2, cx + 5, cy + 14], fill=(255, 200, 60))


def ship(cx, cy):
    pen.polygon([(cx - 18, cy + 2), (cx + 18, cy + 2), (cx + 12, cy + 12),
                 (cx - 12, cy + 12)], fill=(70, 70, 80))
    pen.rectangle([cx - 4, cy - 10, cx + 4, cy + 2], fill=(70, 70, 80))
    pen.line([(cx - 22, cy + 16), (cx + 22, cy + 16)], fill=SEA, width=2)
    pen.line([(cx - 16, cy + 20), (cx + 16, cy + 20)], fill=SEA, width=2)


def short_item(x, kicker, head, body, draw_icon):
    pen.text((x + 44, y), kicker, font=sans_b(13), fill=CRIMSON)
    yy = block(head, sans_b(19), x + 44, y + 16, HALF - 44, 23)
    draw_icon(x + 20, y + 26)
    return block(body, serif(16), x + 44, yy + 2, HALF - 44, 21)


y2 = short_item(LEFT, "INDONESIA", "Factory fire kills 3, 36 missing",
                "A blaze at a confectionery factory leaves three dead and "
                "dozens unaccounted for as rescuers search the ruins.",
                flame)
y3 = short_item(RIGHT - HALF, "GULF OF FINLAND", "Drone hits Russian ship",
                "A Russia-bound cargo ship catches fire after a drone "
                "strike in the Gulf of Finland, in a spillover of the war "
                "at sea.", ship)
y = max(y2, y3) + 6
hline(LEFT, y, RIGHT, 1)
y += 6

# ---------------- also today ----------------
pen.text((LEFT, y), "ALSO TODAY", font=sans_b(15), fill=CRIMSON)
y = block("Verstappen wins a wild Las Vegas Grand Prix with 34 lead changes"
          " as the Ferraris collide  ·  Wembanyama scores 50 as the Spurs "
          "beat the Pelicans 114-91  ·  Leeds stun Chelsea 4-1 at Stamford "
          "Bridge, their first win there since 1999  ·  GTA VI's $3.79bn "
          "launch-day haul sets a record  ·  Iran strikes an industrial "
          "site in Bahrain  ·  Zelensky calls the Crimean Bridge strikes a "
          "fair response  ·  Poland accuses Russia of an airspace "
          "violation; NATO pledges to defend every inch of Polish "
          "territory  ·  UN states reach a tentative deal on autonomous weapons"
          "  ·  At least 24 die as a boat capsizes on a funeral trip in "
          "Nigeria  ·  Amazon nears a $7.5bn deal for AI start-up Decart",
          sans(15), LEFT + 118, y, RIGHT - LEFT - 118, 20, colour=(62, 62, 62))
y += 4
hline(LEFT, y, RIGHT, 1)
pen.text((CANVAS_W // 2, y + 5), "Compiled from the day's reporting  •  22 November 2026",
         font=sans(13), fill=MUTED, anchor="ma")

page.save("entry.png")
print("saved; final y =", y)
