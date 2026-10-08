import os

FONT = {
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
}
TEXT = "SHANTANU"
COLS, ROWS = 53, 7
CELL, GAP, PAD = 12, 3, 20
P = CELL + GAP
STEP = 0.08
BG, EMPTY = "#0d1117", "#151b23"
LIT = ["#196c2e", "#2ea043", "#56d364"]
SNAKE = ["#C4B5FD", "#A78BFA", "#8B5CF6", "#7C3AED", "#6D28D9"]

W = COLS * P - GAP + PAD * 2
H = ROWS * P - GAP + PAD * 2

lit = set()
x0 = (COLS - (len(TEXT) * 6 - 1)) // 2
for i, ch in enumerate(TEXT):
    for r, row in enumerate(FONT[ch]):
        for c, v in enumerate(row):
            if v == "#":
                lit.add((x0 + i * 6 + c, r))

path = []
for c in range(COLS):
    rows = range(ROWS) if c % 2 == 0 else range(ROWS - 1, -1, -1)
    for r in rows:
        path.append((c, r))

N = len(path)
T = N + len(SNAKE) + 20
DUR = round(T * STEP, 2)
eaten = {cell: i for i, cell in enumerate(path)}

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
out.append(f'<rect width="{W}" height="{H}" rx="8" fill="{BG}"/>')

for c in range(COLS):
    for r in range(ROWS):
        x, y = PAD + c * P, PAD + r * P
        if (c, r) in lit:
            col = LIT[(c * 3 + r) % 3]
            te = round(eaten[(c, r)] / T, 4)
            out.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{col}">'
                f'<animate attributeName="fill" calcMode="discrete" dur="{DUR}s" '
                f'repeatCount="indefinite" values="{col};{EMPTY};{EMPTY}" keyTimes="0;{te};1"/></rect>'
            )
        else:
            out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{EMPTY}"/>')

for k in range(len(SNAKE) - 1, -1, -1):
    xs, ys = [], []
    for f in range(T):
        i = f - k
        if 0 <= i < N:
            c, r = path[i]
            xs.append(str(PAD + c * P))
            ys.append(str(PAD + r * P))
        else:
            xs.append("-50")
            ys.append("-50")
    out.append(
        f'<rect x="-50" y="-50" width="{CELL}" height="{CELL}" rx="3" fill="{SNAKE[k]}">'
        f'<animate attributeName="x" calcMode="discrete" dur="{DUR}s" repeatCount="indefinite" values="{";".join(xs)}"/>'
        f'<animate attributeName="y" calcMode="discrete" dur="{DUR}s" repeatCount="indefinite" values="{";".join(ys)}"/>'
        f'</rect>'
    )

out.append("</svg>")
os.makedirs("dist", exist_ok=True)
with open("dist/text-snake.svg", "w") as f:
    f.write("\n".join(out))
print("done", N, "steps")
