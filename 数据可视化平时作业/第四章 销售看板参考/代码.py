# -*- coding: utf-8 -*-
"""
2022年化妆品销售情况 —— 可自由组合的柱线混合图复现

产出（写入本脚本同级的 docs/ 目录）：
    docs/chart4.html   交互网页版：销售额 / 利润额 / 利润率 三个图例可任意勾选，
                       支持两两组合与三者组合（共 7 种非空组合）
    docs/chart4.png    matplotlib 静态复现图（默认：销售额 + 利润率，同原图）
    docs/chart4.svg    矢量版（同一套几何坐标）

设计坐标按原图 845×600 截图实测：画布 830×592，深色卡片 #1A1E43。
"""

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK SC", "Noto Sans CJK JP", "Source Han Sans SC",
    "WenQuanYi Zen Hei", "Microsoft YaHei", "SimHei",
]
plt.rcParams["axes.unicode_minus"] = False

# ！！！此处是唯一修改的地方！！！
HERE = os.path.dirname(os.path.abspath(__file__))
# 获取上一级目录（即你的项目根目录），并在里面寻找 docs 文件夹
BASE_DIR = os.path.dirname(HERE)
OUT_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(OUT_DIR, exist_ok=True)

# ------------------------------------------------------------------ 设计参数
W, H = 830, 592
CARD_FILL = "#1A1E43"
GRID = "#262A4C"
BLUE = "#0070C0"
PINK = "#E74E69"
YELLOW = "#FFC000"
WHITE = "#FFFFFF"
BLACK = "#000000"
NOTE_COLOR = "#B5B6BD"
CAT_COLOR = "#E6E7EE"

TITLE = "2022年化妆品销售情况"
NOTE_TEXT = "*注：数据来源公司销售系统"

CATS = ["口红", "面膜", "隔离", "粉底液"]
SALES = [2800, 2564, 2282, 2353]
PROFIT = [1896, 1563, 986, 1324]
RATE = [68, 61, 43, 56]

# 图例：三个色块，文字黑色，勾选框白底黑框
LEGEND = [
    dict(key="sales",  label="销售额", color=BLUE,   on=True),
    dict(key="profit", label="利润额", color=PINK,   on=False),
    dict(key="rate",   label="利润率", color=YELLOW, on=True),
]
LEG_Y, LEG_H, LEG_W = 120, 36, 100
LEG_X = [102, 220, 356]
LEG_TEXT_DX = 36          # 文字左端（相对色块左边）
LEG_BOX_DX = 10           # 勾选框左端
LEG_BOX_SZ = 16

SLOT_X = [107, 296, 484, 672]
BAR_W = 42
BAR_W2 = 21               # 两条柱并排时的单柱宽
BASE_Y = 490
BASELINE_SEGS = [(41, 177), (229, 365), (418, 554), (606, 741)]
CAT_Y = 516

# 折线（利润率）
LINE_X = [133, 322, 510, 698]
LINE_Y = [202, 213, 245, 222]
RATE_MIN, RATE_MAX, RATE_Y0, RATE_Y1 = 21.0, 74.0, 202.0, 245.0
LINE_W = 2.4

# 柱形刻度：数值 → 柱顶 y
SALES_REF, SALES_TOP = 2800.0, 250.0
PROFIT_REF, PROFIT_TOP = 1896.0, 331.0


def bar_top(key, i):
    if key == "sales":
        return SALES_TOP + (BASE_Y - SALES_TOP) * (1 - SALES[i] / SALES_REF)
    return PROFIT_TOP + (BASE_Y - PROFIT_TOP) * (1 - PROFIT[i] / PROFIT_REF)


def rate_y(v):
    return RATE_Y0 + (RATE_Y1 - RATE_Y0) * (RATE_MAX - v) / (RATE_MAX - RATE_MIN)


def active_keys(active=None):
    if active is None:
        return {g["key"] for g in LEGEND if g["on"]}
    return set(active)


def bar_layout(show_sales, show_profit):
    """返回 [(key, 相对中心偏移, 颜色, 柱宽)]。"""
    if show_sales and show_profit:
        return [("sales", -BAR_W2 - 1, BLUE, BAR_W2),
                ("profit", 1, PINK, BAR_W2)]
    if show_sales:
        return [("sales", -BAR_W / 2.0, BLUE, BAR_W)]
    if show_profit:
        return [("profit", -BAR_W / 2.0, PINK, BAR_W)]
    return []


# ------------------------------------------------------------------ matplotlib
def draw_static(active=None, path=None):
    active = active_keys(active)
    show_s = "sales" in active
    show_p = "profit" in active
    show_r = "rate" in active

    fig = plt.figure(figsize=(W / 100.0, H / 100.0), dpi=100)
    fig.patch.set_facecolor(WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, H, facecolor=CARD_FILL, edgecolor="none",
                           zorder=0))

    # 标题
    ax.text(72, 60, TITLE, fontsize=33, fontweight="bold", color=WHITE,
            ha="left", va="center", zorder=9)

    # 图例（全部色块都画，勾选态区分）
    for g, bx in zip(LEGEND, LEG_X):
        on = g["key"] in active
        ax.add_patch(Rectangle((bx, LEG_Y), LEG_W, LEG_H, facecolor=g["color"],
                               edgecolor="none", zorder=4))
        cbx = bx + LEG_BOX_DX
        cby = LEG_Y + (LEG_H - LEG_BOX_SZ) / 2.0
        ax.add_patch(Rectangle((cbx, cby), LEG_BOX_SZ, LEG_BOX_SZ,
                               facecolor=WHITE, edgecolor=BLACK,
                               linewidth=1.5, zorder=5))
        if on:
            ax.plot([cbx + 3.4, cbx + 6.6, cbx + 12.8],
                    [cby + 8.2, cby + 12.0, cby + 3.4],
                    color=BLACK, linewidth=2.6, solid_capstyle="butt",
                    solid_joinstyle="miter", zorder=6)
        ax.text(bx + LEG_TEXT_DX, LEG_Y + LEG_H / 2.0 + 1, g["label"],
                fontsize=15, color=BLACK, ha="left", va="center", zorder=6)

    # 基线与分组短线
    for x0, x1 in BASELINE_SEGS:
        ax.plot([x0, x1], [BASE_Y, BASE_Y], color=GRID, linewidth=1.2, zorder=2)
    for cx in SLOT_X:
        if show_s:
            ax.plot([cx - 20, cx + 22], [BASE_Y, BASE_Y], color=BLUE,
                    linewidth=2.0, zorder=3)
        if show_p:
            ax.plot([cx - 6, cx + 36], [BASE_Y, BASE_Y], color=PINK,
                    linewidth=2.0, zorder=3)

    # 柱子
    layout = bar_layout(show_s, show_p)
    for i, cx in enumerate(SLOT_X):
        for key, off, color, bw in layout:
            x0 = cx + off
            top = bar_top(key, i)
            ax.add_patch(Rectangle((x0, top), bw, BASE_Y - top, facecolor=color,
                                   edgecolor="none", zorder=4))
            val = SALES[i] if key == "sales" else PROFIT[i]
            ax.text(x0 + 3.5, top + 11, str(val), fontsize=13, color=WHITE,
                    ha="left", va="baseline", zorder=6)

    # 利润率折线
    if show_r:
        ys = [rate_y(v) for v in RATE]
        ax.plot(LINE_X, ys, color=YELLOW, linewidth=LINE_W, zorder=7,
                solid_capstyle="butt", solid_joinstyle="miter")
        for i, x in enumerate(LINE_X):
            ax.text(x, ys[i] - 12, f"{RATE[i]}%", fontsize=14, color=WHITE,
                    ha="center", va="bottom", zorder=8)

    # 类目名与注脚
    for cx, name in zip(SLOT_X, CATS):
        ax.text(cx, CAT_Y, name, fontsize=15, color=CAT_COLOR, ha="center",
                va="center", zorder=8)
    ax.text(63, 562, NOTE_TEXT, fontsize=12, color=NOTE_COLOR, ha="left",
            va="center", zorder=8)

    path = path or os.path.join(OUT_DIR, "chart4.png")
    fig.savefig(path, dpi=100, facecolor=WHITE)
    plt.close(fig)
    return path


# ------------------------------------------------------------------ SVG（静态版）
def build_svg(active=None, path=None):
    active = active_keys(active)
    show_s = "sales" in active
    show_p = "profit" in active
    show_r = "rate" in active

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" '
         f'font-family="PingFang SC, Microsoft YaHei, Noto Sans CJK SC, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{CARD_FILL}"/>',
         f'<text x="72" y="60" fill="#fff" font-size="33" font-weight="700" '
         f'dominant-baseline="middle">{TITLE}</text>']

    for g, bx in zip(LEGEND, LEG_X):
        on = g["key"] in active
        cbx = bx + LEG_BOX_DX
        cby = LEG_Y + (LEG_H - LEG_BOX_SZ) / 2.0
        p.append(f'<rect x="{bx}" y="{LEG_Y}" width="{LEG_W}" height="{LEG_H}" '
                 f'fill="{g["color"]}"/>')
        p.append(f'<rect x="{cbx}" y="{cby}" width="{LEG_BOX_SZ}" height="{LEG_BOX_SZ}" '
                 f'fill="#fff" stroke="#000" stroke-width="1.5"/>')
        if on:
            p.append(f'<path d="M{cbx+3.4},{cby+8.2} L{cbx+6.6},{cby+12} '
                     f'L{cbx+12.8},{cby+3.4}" fill="none" stroke="#000" '
                     f'stroke-width="2.6"/>')
        p.append(f'<text x="{bx+LEG_TEXT_DX}" y="{LEG_Y+LEG_H/2+1}" fill="#000" '
                 f'font-size="15" dominant-baseline="middle">{g["label"]}</text>')

    for x0, x1 in BASELINE_SEGS:
        p.append(f'<line x1="{x0}" y1="{BASE_Y}" x2="{x1}" y2="{BASE_Y}" '
                 f'stroke="{GRID}" stroke-width="1.2"/>')
    for cx in SLOT_X:
        if show_s:
            p.append(f'<line x1="{cx-20}" y1="{BASE_Y}" x2="{cx+22}" y2="{BASE_Y}" '
                     f'stroke="{BLUE}" stroke-width="2"/>')
        if show_p:
            p.append(f'<line x1="{cx-6}" y1="{BASE_Y}" x2="{cx+36}" y2="{BASE_Y}" '
                     f'stroke="{PINK}" stroke-width="2"/>')

    for i, cx in enumerate(SLOT_X):
        for key, off, color, bw in bar_layout(show_s, show_p):
            x0 = cx + off
            top = bar_top(key, i)
            val = SALES[i] if key == "sales" else PROFIT[i]
            p.append(f'<rect x="{x0:.1f}" y="{top:.2f}" width="{bw}" '
                     f'height="{BASE_Y-top:.2f}" fill="{color}"/>')
            p.append(f'<text x="{x0+3.5:.1f}" y="{top+15:.2f}" fill="#fff" '
                     f'font-size="13">{val}</text>')

    if show_r:
        ys = [rate_y(v) for v in RATE]
        d = " ".join(f'{"M" if i == 0 else "L"}{LINE_X[i]},{ys[i]:.2f}'
                     for i in range(len(LINE_X)))
        p.append(f'<path d="{d}" fill="none" stroke="{YELLOW}" '
                 f'stroke-width="{LINE_W}"/>')
        for i, x in enumerate(LINE_X):
            p.append(f'<text x="{x}" y="{ys[i]-12:.2f}" fill="#fff" font-size="14" '
                     f'text-anchor="middle">{RATE[i]}%</text>')

    for cx, name in zip(SLOT_X, CATS):
        p.append(f'<text x="{cx}" y="{CAT_Y}" fill="{CAT_COLOR}" font-size="15" '
                 f'text-anchor="middle" dominant-baseline="middle">{name}</text>')
    p.append(f'<text x="63" y="562" fill="{NOTE_COLOR}" font-size="12" '
             f'dominant-baseline="middle">{NOTE_TEXT}</text>')
    p.append("</svg>")

    path = path or os.path.join(OUT_DIR, "chart4.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    return path


# ------------------------------------------------------------------ HTML
HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  *{box-sizing:border-box}
  html,body{margin:0;padding:0;background:#fff}
  body{display:flex;align-items:center;justify-content:center;min-height:100vh;padding:24px;
       font-family:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC","Hiragino Sans GB",sans-serif}
  .card{position:relative;width:830px;height:592px;background:#1A1E43;overflow:hidden;
        box-shadow:0 12px 40px rgba(26,30,67,.18)}
  .card svg{display:block;width:100%;height:100%}
  .legend{cursor:pointer;outline:none}
  .legend:hover .sw{filter:brightness(1.08)}
  .legend:focus-visible .ring{stroke:#fff;stroke-width:2;stroke-dasharray:3 2}
  .bar{transition:y .42s cubic-bezier(.3,0,.2,1),height .42s cubic-bezier(.3,0,.2,1)}
  .lab,.pline{transition:transform .42s cubic-bezier(.3,0,.2,1),opacity .3s}
  .hint{position:absolute;right:14px;bottom:10px;font-size:11px;color:#6F75A0;
        opacity:0;transition:opacity .3s;pointer-events:none}
  .card:hover .hint{opacity:1}
</style>
</head>
<body>
<div class="card">
  <svg id="chart" viewBox="0 0 830 592" role="group" aria-label="__TITLE__">
    <rect width="830" height="592" fill="#1A1E43"/>
    <text x="72" y="60" fill="#fff" font-size="33" font-weight="700"
          dominant-baseline="middle">__TITLE__</text>
    <g id="legend"></g>
    <g id="grid"></g>
    <g id="bars"></g>
    <g id="line"></g>
    <g id="cats"></g>
    <text x="63" y="562" fill="#B5B6BD" font-size="12" dominant-baseline="middle">__NOTE__</text>
  </svg>
  <div class="hint">点击图例自由组合</div>
</div>

<script>
const DATA = __DATA__;
const D = DATA.design;
const NS = "http://www.w3.org/2000/svg";
const mk = (t, a, txt) => {
  const n = document.createElementNS(NS, t);
  for (const k in a) n.setAttribute(k, a[k]);
  if (txt != null) n.textContent = txt;
  return n;
};

const legendG = document.getElementById("legend");
const gridG   = document.getElementById("grid");
const barsG   = document.getElementById("bars");
const lineG   = document.getElementById("line");
const catsG   = document.getElementById("cats");

let active = new Set(DATA.legend.filter(g => g.on).map(g => g.key));

/* ---------- 数值 → 坐标 ---------- */
function barTop(key, i){
  const ref = key === "sales" ? D.salesRef : D.profitRef;
  const top = key === "sales" ? D.salesTop : D.profitTop;
  const v   = key === "sales" ? DATA.sales[i] : DATA.profit[i];
  return top + (D.baseY - top) * (1 - v / ref);
}
function rateY(v){
  return D.rateY0 + (D.rateY1 - D.rateY0) * (D.rateMax - v) / (D.rateMax - D.rateMin);
}
function barLayout(s, p){
  if (s && p) return [["sales", -D.barW2 - 1, "#0070C0", D.barW2],
                      ["profit", 1, "#E74E69", D.barW2]];
  if (s) return [["sales", -D.barW / 2, "#0070C0", D.barW]];
  if (p) return [["profit", -D.barW / 2, "#E74E69", D.barW]];
  return [];
}

/* ---------- 图例 ---------- */
DATA.legend.forEach((g, i) => {
  const bx = D.legX[i], by = D.legY;
  const grp = mk("g", {"class":"legend", "data-key":g.key, tabindex:"0",
                       role:"checkbox", "aria-checked": g.on ? "true":"false",
                       "aria-label": g.label});
  grp.appendChild(mk("rect", {"class":"sw", x:bx, y:by, width:D.legW, height:D.legH,
                              fill:g.color, rx:0}));
  const cx = bx + D.legBoxDX, cy = by + (D.legH - D.legBoxSz) / 2;
  grp.appendChild(mk("rect", {"class":"ring", x:cx, y:cy, width:D.legBoxSz,
                              height:D.legBoxSz, fill:"#fff", stroke:"#000",
                              "stroke-width":"1.5"}));
  grp.appendChild(mk("path", {
    "class":"tick",
    d:`M${cx+3.4},${cy+8.2} L${cx+6.6},${cy+12} L${cx+12.8},${cy+3.4}`,
    fill:"none", stroke:"#000", "stroke-width":"2.6",
    "stroke-linecap":"butt", "stroke-linejoin":"miter",
    opacity: g.on ? 1 : 0
  }));
  grp.appendChild(mk("text", {x:bx + D.legTextDX, y:by + D.legH/2 + 1, fill:"#000",
                              "font-size":"15", "dominant-baseline":"middle",
                              "pointer-events":"none"}, g.label));
  const toggle = () => {
    const k = g.key;
    if (active.has(k) && active.size === 1) return;   /* 至少保留一项 */
    active.has(k) ? active.delete(k) : active.add(k);
    render();
  };
  grp.addEventListener("click", toggle);
  grp.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
  });
  legendG.appendChild(grp);
});

/* ---------- 静态层 ---------- */
catsG.innerHTML = "";
DATA.cats.forEach((name, i) => {
  catsG.appendChild(mk("text", {x:D.slotX[i], y:D.catY, fill:"#E6E7EE",
                                "font-size":"15", "text-anchor":"middle",
                                "dominant-baseline":"middle"}, name));
});

/* ---------- 渲染 ---------- */
function render(){
  const s = active.has("sales"), p = active.has("profit"), r = active.has("rate");

  legendG.querySelectorAll(".legend").forEach(g => {
    const on = active.has(g.dataset.key);
    g.setAttribute("aria-checked", on ? "true" : "false");
    g.querySelector(".tick").setAttribute("opacity", on ? 1 : 0);
  });

  /* 基线 + 分组短线 */
  gridG.innerHTML = "";
  D.baseSegs.forEach(([x0, x1]) => {
    gridG.appendChild(mk("line", {x1:x0, y1:D.baseY, x2:x1, y2:D.baseY,
                                  stroke:"#262A4C", "stroke-width":"1.2"}));
  });
  D.slotX.forEach(cx => {
    if (s) gridG.appendChild(mk("line", {x1:cx-20, y1:D.baseY, x2:cx+22, y2:D.baseY,
                                         stroke:"#0070C0", "stroke-width":"2"}));
    if (p) gridG.appendChild(mk("line", {x1:cx-6, y1:D.baseY, x2:cx+36, y2:D.baseY,
                                         stroke:"#E74E69", "stroke-width":"2"}));
  });

  /* 柱子 */
  barsG.innerHTML = "";
  const layout = barLayout(s, p);
  if (layout.length){
    DATA.cats.forEach((_, i) => {
      const cx = D.slotX[i];
      layout.forEach(([key, off, color, bw]) => {
        const x0 = cx + off, top = barTop(key, i);
        barsG.appendChild(mk("rect", {"class":"bar", x:x0, y:top, width:bw,
                                      height:D.baseY - top, fill:color}));
        const val = key === "sales" ? DATA.sales[i] : DATA.profit[i];
        barsG.appendChild(mk("text", {"class":"lab", x:x0 + 3.5, y:top + 15,
                                      fill:"#fff", "font-size":"13"}, String(val)));
      });
    });
  }

  /* 利润率折线 */
  lineG.innerHTML = "";
  if (r){
    const xs = D.lineX, ys = DATA.rate.map(rateY);
    const d = xs.map((x, i) => `${i ? "L" : "M"}${x},${ys[i].toFixed(2)}`).join(" ");
    lineG.appendChild(mk("path", {d:d, fill:"none", stroke:"#FFC000",
                                  "stroke-width":"2.4", "stroke-linejoin":"miter"}));
    xs.forEach((x, i) => {
      lineG.appendChild(mk("text", {"class":"pline", x:x, y:ys[i] - 12, fill:"#fff",
                                    "font-size":"14", "text-anchor":"middle"},
                           DATA.rate[i] + "%"));
    });
  }

  /* 淡入 */
  [barsG, lineG].forEach(g => { g.style.opacity = .35; });
  requestAnimationFrame(() => {
    [barsG, lineG].forEach(g => { g.style.opacity = 1; });
  });
}

render();
</script>
</body>
</html>
"""


def build_html(active=None, path=None):
    data = dict(
        cats=CATS, sales=SALES, profit=PROFIT, rate=RATE,
        legend=[dict(key=g["key"], label=g["label"], color=g["color"], on=g["on"])
                for g in LEGEND],
        design=dict(
            legY=LEG_Y, legH=LEG_H, legW=LEG_W, legX=LEG_X,
            legTextDX=LEG_TEXT_DX, legBoxDX=LEG_BOX_DX, legBoxSz=LEG_BOX_SZ,
            slotX=SLOT_X, baseY=BASE_Y, catY=CAT_Y,
            baseSegs=[list(s) for s in BASELINE_SEGS],
            barW=BAR_W, barW2=BAR_W2,
            salesTop=SALES_TOP, profitTop=PROFIT_TOP,
            salesRef=SALES_REF, profitRef=PROFIT_REF,
            lineX=LINE_X,
            rateY0=RATE_Y0, rateY1=RATE_Y1, rateMin=RATE_MIN, rateMax=RATE_MAX,
        ),
    )
    html = (HTML.replace("__TITLE__", TITLE)
                .replace("__NOTE__", NOTE_TEXT)
                .replace("__DATA__", json.dumps(data, ensure_ascii=False)))
    path = path or os.path.join(OUT_DIR, "chart4.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


if __name__ == "__main__":
    print("png :", draw_static())
    print("svg :", build_svg())
    print("html:", build_html())