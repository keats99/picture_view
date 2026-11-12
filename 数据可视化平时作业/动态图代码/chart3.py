#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复现 Excel 中的动态图表：2022年6月30日流量来源分布

原图结构（按原截图像素量取）：
  * 深色卡片 #1A1E43，外层白底
  * 双层圆环：内环 r=80~104，外环 r=104~150（大扇区外沿随占比外扩至 160）
  * 外环叠加 5 组同心弧（簇状描边），形成分段质感
  * 每个扇区一条折线引出标签，圆点落在扇区中线外缘
  * 右上角"近7天 / 近30天"切换按钮（单选小圆点）

产出：
  docs/chart3.png    matplotlib 复现图（近7天状态）
  docs/chart3.svg    同一几何引擎生成的矢量图
  docs/chart3.html   网页版：纯 SVG + JS，按钮可切换两组数据，带过渡动画

用法： python3 make_chart3.py
"""

import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle, Wedge

# ------------------------------------------------------------------ 基础配置
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK SC", "Source Han Sans SC", "Noto Sans CJK JP",
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
W, H = 773, 579                      # 画布
CARD = (15, 9, 726, 557)             # 深色卡片 x, y, w, h
BG_OUT = "#FFFFFF"
CARD_FILL = "#1A1E43"

TITLE = "2022年6月30日流量来源分布"
NOTE = "*注：数据来源公司网站"

CX, CY = 389.5, 307.5                # 圆环中心（原图实测）
R_HOLE = 78.0                        # 中心镂空（原图实测 74~93，取中值）
R_INNER = 104.0                      # 内环外沿（外环起点）
R_DOT = 149.0                        # 引线圆点半径
R_OUT_LO = 150.0                     # 外环常规外沿
R_OUT_HI = 160.0                     # 外环最大外沿（大扇区）

GAP_DEG = 0.9                        # 扇区间隙（度）
SEG_COUNT = 5                        # 外环沿周向的分段数
SEG_PAD = 1.2                        # 分段之间留白（度）

TXT = "#F2F2F2"
TXT_DIM = "#B5B6BD"

# 顺时针顺序与原图完全一致（角度由 12 点起算）：
#   首页推荐 0°→141.6° / 关注页面 141.6°→214° / 搜索 214°→264°
#   个人主页 264°→294.5° / 其他来源 294.5°→356.7°
# 配色取自原图像素：B=#4A5BD1（深蓝，出现两次）、L=#6073F3（浅蓝）、
#                   T=#11A7AD（青）、Y=#FFC000（黄）、R=#E66B4C（橙红）
# outer: 该扇区外沿半径（原图实测）；label/hline/side: 标签位置与引线
ITEMS = [
    dict(name="首页推荐", color="#4A5BD1", line="#4A5BD1", outer=156.0,
         span=(0.0, 141.6), v7=38, v30=44,
         label=(567, 181), hseg=(567, 195, 675), dot=(539.0, 232.0), side=1),
    dict(name="关注页面", color="#6073F3", line="#6073F3", outer=152.0,
         span=(141.6, 214.0), v7=21, v30=17,
         label=(459, 498), hseg=(459, 523, 561), dot=(439.0, 488.0), side=1),
    dict(name="搜索", color="#11A7AD", line="#11A7AD", outer=142.0,
         span=(214.0, 264.0), v7=15, v30=15,
         label=(162, 431), hseg=(127, 424, 236), dot=(274.0, 424.0), side=-1),
    dict(name="个人主页", color="#FFC000", line="#FFC000", outer=112.0,
         span=(264.0, 294.5), v7=9, v30=8,
         label=(137, 253), hseg=(120, 252, 227), dot=(253.0, 300.0), side=-1),
    dict(name="其他来源", color="#E66B4C", line="#E66B4C", outer=129.0,
         span=(294.5, 356.7), v7=17, v30=16,
         label=(175, 176), hseg=(171, 180, 283), dot=(307.0, 216.0), side=-1),
]

BTN_Y, BTN_H, BTN_W = 104, 45, 96
BTN_X = [529, 638]


# ------------------------------------------------------------------ 几何工具
def polar(angle_deg, r, cx=CX, cy=CY):
    """角度：0° 指向 12 点方向，顺时针为正 → 屏幕坐标（y 向下）。"""
    a = math.radians(angle_deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def sector_angles(values=None):
    """各扇区角度区间。"""
    return [it["span"] for it in ITEMS]


def outer_radius(item):
    """扇区外沿半径：直接取配置里的实测值。"""
    return item["outer"] if isinstance(item, dict) else float(item)


def outer_ring_start(angle):
    """外环内起点半径"""
    a = angle % 360.0
    return 82.5 + 4.5 * math.cos(math.radians(a - 60.0))


def deco_radii(rout):
    """外环内的同心弧半径"""
    n = 3
    step = (rout - R_INNER) / (n + 1)
    return [R_INNER + step * (k + 1) for k in range(n)]


def label_geometry(item, a0, a1):
    """标签引线"""
    x0, y, x1 = item["hseg"]
    lx, ly = item["label"]
    dot = item["dot"]
    return dot, (x0, y), (x1, y), (lx, ly)


# ------------------------------------------------------------------ matplotlib
def draw_static(key="v7", path=None):
    values = [it[key] for it in ITEMS]
    bounds = sector_angles(values)

    fig = plt.figure(figsize=(W / 100.0, H / 100.0), dpi=100)
    fig.patch.set_facecolor(BG_OUT)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")

    # 卡片
    x, y, w, h = CARD
    ax.add_patch(Rectangle((x, y), w, h, facecolor=CARD_FILL,
                           edgecolor="none", zorder=1))

    # 标题
    ax.text(52, 44, TITLE, fontsize=31, fontweight="bold", color="#FFFFFF",
            ha="left", va="top", zorder=9)

    # 切换按钮
    for i, (name, active) in enumerate([("近7天", key == "v7"),
                                        ("近30天", key == "v30")]):
        bx = BTN_X[i]
        ax.add_patch(Rectangle((bx, BTN_Y), BTN_W, BTN_H, facecolor="#8F909B",
                               edgecolor="#8F909B", linewidth=1, zorder=6))
        icx, icy = bx + 16, BTN_Y + BTN_H / 2.0
        ax.add_patch(Circle((icx, icy), 9.5,
                            facecolor="#FFFFFF" if active else "none",
                            edgecolor="#FFFFFF", linewidth=1.6, zorder=7))
        if active:
            ax.add_patch(Circle((icx, icy), 4.6, facecolor="#000000",
                                edgecolor="none", zorder=8))
        ax.text(icx + 13, icy, name, fontsize=15.5, color="#000000",
                ha="left", va="center", zorder=8)

    # 圆环
    for it, v, (a0, a1) in zip(ITEMS, values, bounds):
        lo, hi = a0 + GAP_DEG / 2.0, a1 - GAP_DEG / 2.0
        rout = outer_radius(it)
        r_start = R_HOLE
        ax.add_patch(Wedge((CX, CY), R_INNER, 90 - hi, 90 - lo,
                           width=R_INNER - r_start, facecolor=it["color"],
                           edgecolor="none", zorder=3))
        ax.add_patch(Wedge((CX, CY), rout, 90 - hi, 90 - lo,
                           width=rout - R_INNER, facecolor=it["color"],
                           edgecolor="#8D97EA", linewidth=0.8, zorder=4))
        span = hi - lo
        radii = deco_radii(rout)
        for k in range(SEG_COUNT):
            s0 = lo + span * k / SEG_COUNT + SEG_PAD
            s1 = lo + span * (k + 1) / SEG_COUNT - SEG_PAD
            if s1 - s0 < 1.5:
                continue
            for rr in radii:
                ax.add_patch(Arc((CX, CY), 2 * rr, 2 * rr, theta1=90 - s1,
                                 theta2=90 - s0, edgecolor=CARD_FILL,
                                 linewidth=0.85, alpha=0.65, zorder=5))

    # 标签与引线
    for it, v, (a0, a1) in zip(ITEMS, values, bounds):
        dot, text_edge, elbow, pos = label_geometry(it, a0, a1)
        ax.plot([dot[0], elbow[0]], [dot[1], elbow[1]], color=it["line"],
                linewidth=1.15, solid_capstyle="butt", zorder=6)
        ax.plot([elbow[0], text_edge[0]], [elbow[1], text_edge[1]],
                color=it["line"], linewidth=1.15, zorder=6)
        ax.add_patch(Circle(dot, 4.6, facecolor=it["line"], edgecolor="none",
                            zorder=7))
        ax.text(pos[0], pos[1], f'{it["name"]}, {v}%', fontsize=14.5,
                color=TXT, ha="left" if it["side"] == 1 else "right",
                va="baseline", zorder=8)

    # 脚注
    ax.text(52, 528, NOTE, fontsize=11.5, color=TXT_DIM, ha="left",
            va="center", zorder=8)

    path = path or os.path.join(OUT_DIR, "chart3.png")
    fig.savefig(path, dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


# ------------------------------------------------------------------ SVG
def svg_fragment(values):
    bounds = sector_angles(values)
    def P(ang, r):
        px, py = polar(ang, r, 0.0, 0.0)
        return f"{px:.2f},{py:.2f}"

    rings, labels = [], []
    for idx, (it, v, (a0, a1)) in enumerate(zip(ITEMS, values, bounds)):
        lo, hi = a0 + GAP_DEG / 2.0, a1 - GAP_DEG / 2.0
        rout = outer_radius(it)
        large = 1 if (hi - lo) > 180 else 0

        inner = (f"M{P(lo, R_HOLE)} L{P(lo, R_INNER)} "
                 f"A{R_INNER},{R_INNER} 0 {large} 1 {P(hi, R_INNER)} "
                 f"L{P(hi, R_HOLE)} "
                 f"A{R_HOLE},{R_HOLE} 0 {large} 0 {P(lo, R_HOLE)} Z")
        outer = (f"M{P(lo, R_INNER)} L{P(lo, rout)} "
                 f"A{rout},{rout} 0 {large} 1 {P(hi, rout)} "
                 f"L{P(hi, R_INNER)} "
                 f"A{R_INNER},{R_INNER} 0 {large} 0 {P(lo, R_INNER)} Z")

        arcs = []
        span = hi - lo
        radii = deco_radii(rout)
        for k in range(SEG_COUNT):
            s0 = lo + span * k / SEG_COUNT + SEG_PAD
            s1 = lo + span * (k + 1) / SEG_COUNT - SEG_PAD
            if s1 - s0 < 1.5:
                continue
            for rr in radii:
                arcs.append(f'<path d="M{P(s0, rr)} A{rr:.2f},{rr:.2f} 0 '
                            f'{large} 1 {P(s1, rr)}"/>')

        rings.append(
            f'<g class="seg">'
            f'<path d="{inner}" fill="{it["color"]}"/>'
            f'<path d="{outer}" fill="{it["color"]}" stroke="#8D97EA" '
            f'stroke-width="0.8"/>'
            f'<g fill="none" stroke="{CARD_FILL}" stroke-width="0.85" '
            f'stroke-opacity="0.65">{"".join(arcs)}</g>'
            f'</g>'
        )

        dot, text_edge, elbow, pos = label_geometry(it, a0, a1)
        d0 = (dot[0] - CX, dot[1] - CY)
        labels.append(
            f'<g class="lab">'
            f'<path d="M{d0[0]:.2f},{d0[1]:.2f} L{elbow[0] - CX:.2f},{elbow[1] - CY:.2f} '
            f'L{text_edge[0] - CX:.2f},{text_edge[1] - CY:.2f}" fill="none" '
            f'stroke="{it["line"]}" stroke-width="1.15"/>'
            f'<circle cx="{d0[0]:.2f}" cy="{d0[1]:.2f}" r="4.6" fill="{it["line"]}"/>'
            f'<text x="{pos[0] - CX}" y="{pos[1] - CY}" '
            f'text-anchor="{"start" if it["side"] == 1 else "end"}">'
            f'{it["name"]}, {v}%</text>'
            f'</g>'
        )

    return "".join(rings), "".join(labels)


def build_svg(values=None, path=None):
    values = values or [it["v7"] for it in ITEMS]
    rings, labels = svg_fragment(values)
    x, y, w, h = CARD
    bg_gray = 14
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="{BG_OUT}"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{CARD_FILL}"/>
  <text x="52" y="44" fill="#FFFFFF" font-size="31" font-weight="700"
        dominant-baseline="hanging"
        font-family="PingFang SC, Microsoft YaHei, Noto Sans CJK SC, sans-serif">{TITLE}</text>
  <g transform="translate({CX},{CY})">{rings}</g>
  <g transform="translate({CX},{CY})" font-size="14.5" fill="{TXT}"
     font-family="PingFang SC, Microsoft YaHei, Noto Sans CJK SC, sans-serif">{labels}</g>
  <text x="52" y="528" fill="{TXT_DIM}" font-size="11.5" dominant-baseline="middle"
        font-family="PingFang SC, Microsoft YaHei, Noto Sans CJK SC, sans-serif">{NOTE}</text>
</svg>
"""
    path = path or os.path.join(OUT_DIR, "chart3.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path


# ------------------------------------------------------------------ 网页版
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root{
    --card:#1A1E43;
    --text:#E8EAF2;
    --text-dim:#A9AEC5;
    --btn-bg:#8F909B;
    --btn-bg-hover:#9EA0AB;
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0;background:#fff}
  body{
    display:flex;align-items:center;justify-content:center;min-height:100vh;padding:24px;
    font-family:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC","Hiragino Sans GB",sans-serif;
  }
  .card{
    position:relative;width:726px;height:557px;background:var(--card);
    box-shadow:0 12px 40px rgba(26,30,67,.16);overflow:hidden;
  }
  .card svg{display:block;width:100%;height:100%}
  .title{fill:#fff;font-size:31px;font-weight:700;letter-spacing:.5px}
  .lab text{fill:var(--text);font-size:14.5px}
  .note{fill:var(--text-dim);font-size:11.5px}
  .btn{cursor:pointer;outline:none}
  .btn .btn-bg{fill:var(--btn-bg);transition:fill .2s}
  .btn:hover .btn-bg,.btn:focus-visible .btn-bg{fill:var(--btn-bg-hover)}
  .btn text{fill:#000;font-size:15.5px;pointer-events:none;user-select:none}
  .radio-hole{transition:opacity .2s}
  .seg,.lab{transition:opacity .38s ease}
</style>
</head>
<body>
<div class="card">
  <svg id="chart" viewBox="0 0 726 557" role="img" aria-label="__TITLE__">
    <text class="title" x="37" y="18" dominant-baseline="hanging">__TITLE__</text>

    <g class="btn" id="btn-7" data-key="d7" role="radio" tabindex="0" aria-checked="true">
      <rect class="btn-bg" x="514" y="95" width="96" height="45"/>
      <circle cx="530" cy="117.5" r="9.5" fill="#fff"/>
      <circle class="radio-hole" cx="530" cy="117.5" r="4.6" fill="#000"/>
      <text x="543" y="117.5" dominant-baseline="middle">近7天</text>
    </g>
    <g class="btn" id="btn-30" data-key="d30" role="radio" tabindex="0" aria-checked="false">
      <rect class="btn-bg" x="623" y="95" width="96" height="45"/>
      <circle cx="639" cy="117.5" r="9.5" fill="none" stroke="#fff" stroke-width="1.6"/>
      <circle class="radio-hole" cx="639" cy="117.5" r="4.6" fill="#000" opacity="0"/>
      <text x="652" y="117.5" dominant-baseline="middle">近30天</text>
    </g>

    <g id="donut" transform="translate(374.5,298.5)"></g>
    <g id="labels"></g>

    <text class="note" x="37" y="513" dominant-baseline="middle">__NOTE__</text>
  </svg>
</div>

<script>
const DATA = __DATA__;

const CX = 374.5, CY = 298.5;   
const R_HOLE = 80, R_INNER = 104, R_DOT = 149, R_OUT_LO = 150, R_OUT_HI = 160;
const GAP = 1.6, SEG_COUNT = 5, SEG_PAD = 1.5;
const CARD_FILL = "#1A1E43";

const NS = "http://www.w3.org/2000/svg";
const donutG = document.getElementById("donut");
const labelsG = document.getElementById("labels");

const rad = d => d * Math.PI / 180;
const pt = (a, r) => [r * Math.sin(rad(a)), -r * Math.cos(rad(a))];
const f2 = v => v.toFixed(2);

function sectorAngles(values){
  const total = values.reduce((a, b) => a + b, 0);
  let acc = 0;
  return values.map(v => {
    const span = 360 * v / total;
    const seg = [acc, acc + span];
    acc += span;
    return seg;
  });
}
function decoRadii(rout){
  const n = 3, step = (rout - R_INNER) / (n + 1), out = [];
  for (let k = 1; k <= n; k++) out.push(R_INNER + step * k);
  return out;
}
function annulus(a0, a1, rIn, rOut){
  const large = (a1 - a0) > 180 ? 1 : 0;
  const p1 = pt(a0, rOut), p2 = pt(a1, rOut), p3 = pt(a1, rIn), p4 = pt(a0, rIn);
  return `M${f2(p1[0])},${f2(p1[1])} A${rOut},${rOut} 0 ${large} 1 ${f2(p2[0])},${f2(p2[1])}`
       + ` L${f2(p3[0])},${f2(p3[1])} A${rIn},${rIn} 0 ${large} 0 ${f2(p4[0])},${f2(p4[1])} Z`;
}
function arcPath(a0, a1, r){
  const large = (a1 - a0) > 180 ? 1 : 0;
  const p1 = pt(a0, r), p2 = pt(a1, r);
  return `M${f2(p1[0])},${f2(p1[1])} A${r},${r} 0 ${large} 1 ${f2(p2[0])},${f2(p2[1])}`;
}
function mk(tag, attrs, text){
  const n = document.createElementNS(NS, tag);
  for (const k in attrs) n.setAttribute(k, attrs[k]);
  if (text != null) n.textContent = text;
  return n;
}

function render(key){
  const values = DATA.items.map(it => it[key]);
  const bounds = sectorAngles(values);

  donutG.innerHTML = "";
  DATA.items.forEach((it, i) => {
    const [a0, a1] = bounds[i];
    const lo = a0 + GAP / 2, hi = a1 - GAP / 2;
    const rout = it.outer;
    const g = mk("g", {"class": "seg"});
    g.appendChild(mk("path", {d: annulus(lo, hi, R_HOLE, R_INNER), fill: it.color}));
    g.appendChild(mk("path", {d: annulus(lo, hi, R_INNER, rout), fill: it.color,
                              stroke: "#8D97EA", "stroke-width": "0.8"}));
    const arcsG = mk("g", {fill: "none", stroke: CARD_FILL, "stroke-width": "0.85",
                           "stroke-opacity": "0.65"});
    const span = hi - lo, radii = decoRadii(rout);
    for (let k = 0; k < SEG_COUNT; k++){
      const s0 = lo + span * k / SEG_COUNT + SEG_PAD;
      const s1 = lo + span * (k + 1) / SEG_COUNT - SEG_PAD;
      if (s1 - s0 < 1.5) continue;
      radii.forEach(r => arcsG.appendChild(mk("path", {d: arcPath(s0, s1, r)})));
    }
    g.appendChild(arcsG);
    donutG.appendChild(g);
  });

  labelsG.innerHTML = "";
  DATA.items.forEach((it, i) => {
    const [lx, ly] = it.label;            
    const [x0, hy, x1] = it.hseg;         
    const [dotX, dotY] = it.dot;          
    const f1 = v => v.toFixed(1);
    const g = mk("g", {"class": "lab"});
    g.appendChild(mk("path", {
      d: `M${f1(dotX)},${f1(dotY)} L${f1(x1)},${f1(hy)} L${f1(x0)},${f1(hy)}`,
      fill: "none", stroke: it.line, "stroke-width": "1.15"
    }));
    g.appendChild(mk("circle", {cx: f1(dotX), cy: f1(dotY), r: 4.6, fill: it.line}));
    g.appendChild(mk("text", {
      x: f1(lx), y: f1(ly), "text-anchor": it.side === 1 ? "start" : "end"
    }, `${it.name}, ${values[i]}%`));
    labelsG.appendChild(g);
  });

  document.querySelectorAll(".btn").forEach(btn => {
    const on = btn.dataset.key === key;
    btn.setAttribute("aria-checked", on ? "true" : "false");
    const ring = btn.querySelector("circle");
    ring.setAttribute("fill", on ? "#fff" : "none");
    ring.setAttribute("stroke", on ? "none" : "#fff");
    ring.setAttribute("stroke-width", on ? "0" : "1.6");
    btn.querySelector(".radio-hole").setAttribute("opacity", on ? "1" : "0");
  });

  donutG.style.opacity = 0.3;
  labelsG.style.opacity = 0.3;
  requestAnimationFrame(() => {
    donutG.style.opacity = 1;
    labelsG.style.opacity = 1;
  });
}

let current = "d7";
document.querySelectorAll(".btn").forEach(btn => {
  const act = () => {
    const key = btn.dataset.key;
    if (key === current) return;
    current = key;
    render(key);
  };
  btn.addEventListener("click", act);
  btn.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); act(); }
  });
});

render("d7");
</script>
</body>
</html>
"""


def build_html(path=None):
    import json

    data = {
        "items": [
            dict(name=it["name"], color=it["color"], line=it["line"],
                 outer=it["outer"], label=list(it["label"]), side=it["side"],
                 hseg=list(it["hseg"]), dot=list(it["dot"]),
                 d7=it["v7"], d30=it["v30"])
            for it in ITEMS
        ]
    }
    html = (HTML_TEMPLATE
            .replace("__TITLE__", TITLE)
            .replace("__NOTE__", NOTE)
            .replace("__DATA__", json.dumps(data, ensure_ascii=False, indent=1)))
    path = path or os.path.join(OUT_DIR, "chart3.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


if __name__ == "__main__":
    print("png :", draw_static("v7"))
    print("svg :", build_svg())
    print("html:", build_html())