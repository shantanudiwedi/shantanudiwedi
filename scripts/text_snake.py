import os

FONT = {
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    " ": ["....."] * 7,
}
TEXT = "HEY BUILDERS"
COLS, ROWS = 75, 11
TOP = 2
CELL, GAP, PAD = 10, 2, 16
P = CELL + GAP
STEP = 0.06
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
                lit.add((x0 + i * 6 + c, TOP + r))

L, R = x0 - 1, x0 + len(TEXT) * 6 - 1
U, D = TOP - 1, TOP + 7
path = []
path += [(c, U) for c in range(L, R + 1)]
path += [(R, r) for r in range(U + 1, D + 1)]
path += [(c, D) for c in range(R - 1, L - 1, -1)]
path += [(L, r) for r in range(D - 1, U, -1)]

N = len(path)
LAPS = 3
T = N * LAPS
DUR = round(T * STEP, 2)

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
out.append(f'<rect width="{W}" height="{H}" rx="8" fill="{BG}"/>')

for c in range(COLS):
    for r in range(ROWS):
        x, y = PAD + c * P, PAD + r * P
        if (c, r) in lit:
            col = LIT[(c * 3 + r) % 3]
            out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{col}"/>')
        else:
            out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{EMPTY}"/>')

for k in range(len(SNAKE) - 1, -1, -1):
    xs, ys = [], []
    for f in range(T):
        c, r = path[(f - k) % N]
        xs.append(str(PAD + c * P))
        ys.append(str(PAD + r * P))
    out.append(
        f'<rect x="-50" y="-50" width="{CELL}" height="{CELL}" rx="2" fill="{SNAKE[k]}">'
        f'<animate attributeName="x" calcMode="discrete" dur="{DUR}s" repeatCount="indefinite" values="{";".join(xs)}"/>'
        f'<animate attributeName="y" calcMode="discrete" dur="{DUR}s" repeatCount="indefinite" values="{";".join(ys)}"/>'
        f'</rect>'
    )

out.append("</svg>")
os.makedirs("dist", exist_ok=True)
with open("dist/text-snake.svg", "w") as f:
    f.write("\n".join(out))
print("done", N, "steps")
