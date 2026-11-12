# -*- coding: utf-8 -*-
"""
各学历平均工资情况 —— 带部门切片器的交互柱形图复现

产出（写入本脚本上一级目录的 docs/ 目录）：
    docs/chart5.html   交互网页版：顶部切片器切换部门，柱形高度与数值、
                       网格线高度同步变化（模拟 Excel 数据透视图）
    docs/chart5.png    matplotlib 静态复现图（默认：财务）
    docs/chart5.svg    矢量版（同一套坐标）

尺寸按原图 739×635 截图实测：切片器面板高 135，图表卡片 728×495。
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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(HERE), "docs")
os.makedirs(OUT_DIR, exist_ok=True)

# ------------------------------------------------------------------ 设计参数
W, H = 739, 635
PANEL_H = 135                      # 切片器面板高度
CARD = (7, 135, 728, 495)          # 图表卡片 x, y, w, h

CARD_FILL = "#1A1E43"
GRID = "#454866"                   # 网格虚线
BLUE_TOP = (0, 112, 192)           # 柱顶色
BLUE_BOT = (0, 176, 240)           # 柱底色（自上而下渐变）
TITLE_COLOR = "#E8EAF6"
NOTE_COLOR = "#B9BDD4"
CAT_COLOR = "#E2E4F0"
VAL_COLOR = "#F0F1F8"

TITLE = "各学历平均工资情况"
NOTE_TEXT = "*注：数据来源于人力资源管理系统，统计日期截至2022.03.31"

EDU = ["本科", "博士", "高中", "硕士", "专科"]

# 部门 → 五个学历的平均工资（小数两位）
DATA = {
    "财务":     [6569.11, 4317.00, 3614.25, 7412.70, 3467.60],
    "工程":     [None, None, 3468.00, None, None],
    "后勤":     [None, None, 2693.00, None, None],
    "人力资源": [6760.56, 4990.33, 2776.60, 9711.13, 4489.07],
    "市场拓展": [6138.32, 7187.00, 5853.63, 6739.01, 6908.04],
    "销售":     [7154.78, 8839.20, 5627.30, 7304.73, 6518.84],
    "行政":     [6296.69, 10035.31, 6289.34, 5696.10, 5036.50],
}
DEPTS = list(DATA.keys())
DEFAULT = "财务"

# 切片器面板
PANEL_TITLE_X, PANEL_TITLE_Y = 22, 15     # “部门”文字基线
PANEL_BG = "#FFFFFF"
PANEL_BORDER = "#5B9BD5"
PANEL_DIV = "#DDDDDD"
BTN_BORDER = "#CCCCCC"
BTN_TEXT = "#262626"
CHIP_BG = "#BDD7EE"

BTN_Y0, BTN_Y1 = 38, 64                   # 第一行按钮
BTN_Y2, BTN_Y3 = 69, 95                   # 第二行按钮
BTN_W = 169                               # 按钮宽（含边框）
BTN_X = [19, 198, 375, 553]               # 四列左边界（第一行）
BTN_X2 = [19, 198, 375]                   # 第二行三列
ROW1 = ["财务", "工程", "后勤", "人力资源"]
ROW2 = ["市场拓展", "销售", "行政"]

# 图表卡片内几何（卡片局部坐标）
GRID_Y = [140, 209, 278, 348, 417]        # 五条横向虚线（卡片顶部为 0）
BASE_Y = 417                              # 基线
GRID_X0, GRID_X1 = 40, 677
SLOT_X = [109, 234, 359, 487, 613]        # 五根柱中心（卡片局部坐标）
BAR_W = 40
PLOT_TOP = 296                            # 数据最高点距基线的像素（12000 对应）
MAX_REF = 12000.0
TITLE_Y = 66                              # 卡片标题基线
CAT_Y = 446
NOTE_Y = 470


def bar_height(v):
    """数值 → 柱高（像素）。与网格对应：每格 69px ≈ 2400 元。"""
    return PLOT_TOP * v / MAX_REF


def _lerp(c0, c1, t):
    return "#%02X%02X%02X" % tuple(
        int(round(c0[i] + (c1[i] - c0[i]) * t)) for i in range(3)
    )


# ------------------------------------------------------------------ matplotlib
def draw_static(dept=DEFAULT, path=None, auto_scale=False):
    """auto_scale=True 时曲线会按当前系列自动缩放（原图 Excel 行为：
    单系列只显示一根柱时，柱顶顶到图表上部）。这里默认关闭，
    以保持柱高与网格刻度的真实比例。"""
    vals = DATA[dept]
    cx, cy, cw, ch = CARD

    fig = plt.figure(figsize=(W / 100.0, H / 100.0), dpi=100)
    fig.patch.set_facecolor("#FFFFFF")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")

    # ---- 切片器面板
    ax.add_patch(Rectangle((0, 0), W, PANEL_H, facecolor=PANEL_BG,
                           edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((8.5, 1.5), W - 17, PANEL_H - 12,
                           facecolor="none", edgecolor=PANEL_BORDER,
                           linewidth=1.0, zorder=1))
    ax.text(PANEL_TITLE_X, PANEL_TITLE_Y + 12, "部门", fontsize=17,
            color="#1A1A1A", ha="left", va="center", zorder=4)
    ax.plot([36, 724], [31, 31], color=PANEL_BORDER, linewidth=1.0, zorder=2)

    # 右上角两个图标（简化为线描）
    _draw_icons(ax)

    # 按钮
    for row, ys, xs in ((ROW1, (BTN_Y0, BTN_Y1), BTN_X),
                        (ROW2, (BTN_Y2, BTN_Y3), BTN_X2)):
        for i, name in enumerate(row):
            x0 = xs[i]
            on = name == dept
            if on:
                ax.add_patch(Rectangle((x0 + 1, ys[0] + 1), BTN_W - 1,
                                       ys[1] - ys[0] - 1, facecolor=CHIP_BG,
                                       edgecolor="none", zorder=2))
            ax.add_patch(Rectangle((x0, ys[0]), BTN_W, ys[1] - ys[0],
                                   facecolor="none", edgecolor=BTN_BORDER,
                                   linewidth=1.0, zorder=3))
            ax.text(x0 + 7, (ys[0] + ys[1]) / 2.0 + 1, name, fontsize=14.5,
                    color=BTN_TEXT, ha="left", va="center", zorder=4)

    # ---- 图表卡片
    ax.add_patch(Rectangle((cx, cy), cw, ch, facecolor=CARD_FILL,
                           edgecolor="none", zorder=1))
    ax.text(cx + 41, cy + TITLE_Y, TITLE, fontsize=25, fontweight="bold",
            color=TITLE_COLOR, ha="left", va="baseline", zorder=6)

    # 网格虚线
    for gy in GRID_Y:
        ax.plot([cx + GRID_X0, cx + GRID_X1], [cy + gy, cy + gy],
                color=GRID, linewidth=1.0, linestyle=(0, (7, 5)), zorder=2)
    # 基线（实线）
    ax.plot([cx + GRID_X0, cx + GRID_X1], [cy + BASE_Y, cy + BASE_Y],
            color=GRID, linewidth=1.0, zorder=2)

    # 柱子（渐变：上深下亮，用多条横带模拟）
    for i, v in enumerate(vals):
        if v is None:
            continue
        h = bar_height(v)
        x0 = cx + SLOT_X[i] - BAR_W / 2.0
        top = cy + BASE_Y - h
        n = max(1, int(round(h)))
        for k in range(n):
            t = k / max(1, n - 1)
            ax.add_patch(Rectangle((x0, top + h * k / n), BAR_W, h / n + 0.6,
                                   facecolor=_lerp(BLUE_TOP, BLUE_BOT, t),
                                   edgecolor="none", zorder=4))
        # 数值标签
        ax.text(cx + SLOT_X[i], top - 9, f"{v:.2f}", fontsize=13.5,
                color=VAL_COLOR, ha="center", va="baseline", zorder=6)

    # 类目
    for i, name in enumerate(EDU):
        ax.text(cx + SLOT_X[i], cy + CAT_Y, name, fontsize=14.5,
                color=CAT_COLOR, ha="center", va="baseline", zorder=6)

    ax.text(cx + 34, cy + NOTE_Y, NOTE_TEXT, fontsize=12.5, color=NOTE_COLOR,
            ha="left", va="baseline", zorder=6)

    path = path or os.path.join(OUT_DIR, "chart5.png")
    fig.savefig(path, dpi=100, facecolor="#FFFFFF")
    plt.close(fig)
    return path


def _draw_icons(ax):
    """右上角的「清单」与「漏斗+叉」图标，用简单线段近似。"""
    ix, iy = 655, 8
    # 清单图标：三行「对勾 + 横线」
    for k in range(3):
        y = iy + 3 + k * 6.5
        ax.plot([ix, ix + 2.6, ix + 6], [y, y + 3.2, y - 3.2],
                color="#404040", linewidth=1.5, solid_capstyle="butt")
        ax.plot([ix + 9, ix + 17], [y, y], color="#404040", linewidth=1.5)
    # 漏斗
    fx, fy = 690, 2
    ax.plot([fx, fx + 20, fx + 11.5, fx + 11.5],
            [fy, fy, fy + 14, fy + 34], color="#404040", linewidth=1.4)
    ax.plot([fx + 20, fx, fx + 8.5, fx + 8.5],
            [fy, fy, fy + 14, fy + 34], color="#404040", linewidth=1.4)
    # 红色叉
    ax.plot([fx + 13, fx + 27], [fy + 14, fy + 28], color="#E8443A", linewidth=1.8)
    ax.plot([fx + 27, fx + 13], [fy + 14, fy + 28], color="#E8443A", linewidth=1.8)


# ------------------------------------------------------------------ SVG
def build_svg(dept=DEFAULT, path=None):
    vals = DATA[dept]
    cx, cy, cw, ch = CARD
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" '
         f'font-family="PingFang SC, Microsoft YaHei, Noto Sans CJK SC, sans-serif">',
         '<defs>'
         f'<linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="#0070C0"/>'
         f'<stop offset="1" stop-color="#00B0F0"/></linearGradient>'
         '</defs>',
         f'<rect width="{W}" height="{PANEL_H}" fill="#fff"/>',
         f'<rect x="8.5" y="1.5" width="{W-17}" height="{PANEL_H-12}" '
         f'fill="none" stroke="{PANEL_BORDER}" stroke-width="1"/>',
         f'<text x="{PANEL_TITLE_X}" y="{PANEL_TITLE_Y+12}" font-size="17" '
         f'fill="#1A1A1A" dominant-baseline="middle">部门</text>',
         f'<line x1="36" y1="31" x2="724" y2="31" stroke="{PANEL_BORDER}" '
         f'stroke-width="1"/>',
         f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="{CARD_FILL}"/>',
         f'<text x="{cx+41}" y="{cy+TITLE_Y}" font-size="25" font-weight="700" '
         f'fill="{TITLE_COLOR}">{TITLE}</text>']

    # 按钮
    for row, ys, xs in ((ROW1, (BTN_Y0, BTN_Y1), BTN_X),
                        (ROW2, (BTN_Y2, BTN_Y3), BTN_X2)):
        for i, name in enumerate(row):
            x0 = xs[i]
            if name == dept:
                p.append(f'<rect x="{x0+1}" y="{ys[0]+1}" width="{BTN_W-1}" '
                         f'height="{ys[1]-ys[0]-1}" fill="{CHIP_BG}"/>')
            p.append(f'<rect x="{x0}" y="{ys[0]}" width="{BTN_W}" '
                     f'height="{ys[1]-ys[0]}" fill="none" stroke="{BTN_BORDER}" '
                     f'stroke-width="1"/>')
            p.append(f'<text x="{x0+7}" y="{(ys[0]+ys[1])/2+1}" font-size="14.5" '
                     f'fill="{BTN_TEXT}" dominant-baseline="middle">{name}</text>')

    # 网格
    for gy in GRID_Y:
        p.append(f'<line x1="{cx+GRID_X0}" y1="{cy+gy}" x2="{cx+GRID_X1}" '
                 f'y2="{cy+gy}" stroke="{GRID}" stroke-width="1" '
                 f'stroke-dasharray="7 5"/>')
    p.append(f'<line x1="{cx+GRID_X0}" y1="{cy+BASE_Y}" x2="{cx+GRID_X1}" '
             f'y2="{cy+BASE_Y}" stroke="{GRID}" stroke-width="1"/>')

    for i, v in enumerate(vals):
        if v is None:
            continue
        h = bar_height(v)
        x0 = cx + SLOT_X[i] - BAR_W / 2.0
        top = cy + BASE_Y - h
        p.append(f'<rect x="{x0:.1f}" y="{top:.2f}" width="{BAR_W}" '
                 f'height="{h:.2f}" fill="url(#barGrad)"/>')
        p.append(f'<text x="{cx+SLOT_X[i]}" y="{top-9:.2f}" font-size="13.5" '
                 f'fill="{VAL_COLOR}" text-anchor="middle">{v:.2f}</text>')

    for i, name in enumerate(EDU):
        p.append(f'<text x="{cx+SLOT_X[i]}" y="{cy+CAT_Y}" font-size="14.5" '
                 f'fill="{CAT_COLOR}" text-anchor="middle">{name}</text>')
    p.append(f'<text x="{cx+34}" y="{cy+NOTE_Y}" font-size="12.5" '
             f'fill="{NOTE_COLOR}">{NOTE_TEXT}</text>')
    p.append("</svg>")

    path = path or os.path.join(OUT_DIR, "chart5.svg")
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
  body{display:flex;justify-content:center;align-items:flex-start;min-height:100vh;padding:20px;
       font-family:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC","Hiragino Sans GB",sans-serif}
  .wrap{width:739px;background:#fff;box-shadow:0 10px 34px rgba(20,30,60,.14)}
  .panel{position:relative;height:135px;background:#fff}
  .panel .frame{position:absolute;left:8px;top:1px;right:8px;bottom:11px;
                border:1px solid #5B9BD5}
  .panel .ttl{position:absolute;left:22px;top:8px;font-size:17px;color:#1A1A1A;line-height:24px}
  .panel .hr{position:absolute;left:36px;right:15px;top:31px;height:1px;background:#5B9BD5}
  .panel .icons{position:absolute;right:14px;top:6px;display:flex;gap:14px;align-items:flex-start}
  .panel .icons svg{display:block}
  .chips{position:absolute;left:19px;right:19px;top:38px;
         display:grid;grid-template-columns:repeat(4,1fr);gap:10px 10px}
  .chip{height:26px;border:1px solid #CCCCCC;background:#fff;font-size:14.5px;color:#262626;
        line-height:24px;padding:0 6px;cursor:pointer;user-select:none;text-align:left;
        font-family:inherit;transition:background .16s,box-shadow .16s;
        white-space:nowrap;overflow:hidden}
  .chip:nth-child(5){grid-column:1}
  .chip:hover{background:#F2F8FD}
  .chip.on{background:#BDD7EE;border-color:#CCCCCC}
  .chip:focus-visible{outline:2px solid #2E75B6;outline-offset:1px}

  .card{position:relative;width:728px;height:495px;margin:0 auto 0 7px;background:#1A1E43}
  .card svg{display:block;width:100%;height:100%}
  .bar{transition:y .48s cubic-bezier(.25,.8,.3,1),height .48s cubic-bezier(.25,.8,.3,1)}
  .vlab{transition:transform .48s cubic-bezier(.25,.8,.3,1)}
  .gl{transition:opacity .3s}
  .hint{position:absolute;right:12px;bottom:8px;font-size:11px;color:#61679A;
        opacity:0;transition:opacity .3s;pointer-events:none}
  .card:hover .hint{opacity:1}
</style>
</head>
<body>
<div class="wrap">
  <div class="panel">
    <div class="frame"></div>
    <div class="ttl">部门</div>
    <div class="hr"></div>
    <div class="icons">
      <svg width="26" height="24" viewBox="0 0 26 24">
        <g stroke="#404040" stroke-width="1.6" fill="none">
          <path d="M2,4 L5,7 L9,1.5"/><path d="M12,4 H22"/>
          <path d="M2,10.5 L5,13.5 L9,8"/><path d="M12,10.5 H22"/>
          <path d="M2,17 L5,20 L9,14.5"/><path d="M12,17 H22"/>
        </g>
      </svg>
      <svg width="34" height="26" viewBox="0 0 34 26">
        <g stroke="#404040" stroke-width="1.5" fill="none">
          <path d="M3,1 H23 L14,12 V24 H12 L12,12 Z"/>
        </g>
        <g stroke="#E8443A" stroke-width="1.9" stroke-linecap="round">
          <path d="M18.5,13 L27,21.5"/><path d="M27,13 L18.5,21.5"/>
        </g>
      </svg>
    </div>
    <div class="chips" id="chips"></div>
  </div>

  <div class="card">
    <svg id="chart" viewBox="0 0 728 495" role="img" aria-label="__TITLE__">
      <defs>
        <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#0070C0"/>
          <stop offset="1" stop-color="#00B0F0"/>
        </linearGradient>
      </defs>
      <text x="41" y="62" fill="#E8EAF6" font-size="25" font-weight="700">__TITLE__</text>
      <g id="grid"></g>
      <g id="bars"></g>
      <g id="cats"></g>
      <text x="34" y="470" fill="#B9BDD4" font-size="12.5">__NOTE__</text>
    </svg>
    <div class="hint">点击上方部门切换</div>
  </div>
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

const chipsBox = document.getElementById("chips");
const gridG = document.getElementById("grid");
const barsG = document.getElementById("bars");
const catsG = document.getElementById("cats");

let current = DATA.defaultDept;

/* ---- 部门按钮 ---- */
DATA.depts.forEach(name => {
  const b = document.createElement("button");
  b.className = "chip";
  b.type = "button";
  b.textContent = name;
  b.dataset.dept = name;
  b.setAttribute("aria-pressed", name === current ? "true" : "false");
  b.addEventListener("click", () => select(name));
  chipsBox.appendChild(b);
});

/* ---- 类目（静态） ---- */
DATA.edu.forEach((name, i) => {
  catsG.appendChild(mk("text", {x:D.slotX[i], y:D.catY, fill:"#E2E4F0",
                                "font-size":"14.5", "text-anchor":"middle"}, name));
});

function barH(v){ return D.plotTop * v / D.maxRef; }

function render(){
  /* 网格 */
  gridG.innerHTML = "";
  D.gridY.forEach(gy => {
    gridG.appendChild(mk("line", {x1:D.gridX0, y1:gy, x2:D.gridX1, y2:gy,
                                  stroke:"#454866", "stroke-width":"1",
                                  "stroke-dasharray":"7 5"}));
  });
  gridG.appendChild(mk("line", {x1:D.gridX0, y1:D.baseY, x2:D.gridX1, y2:D.baseY,
                                stroke:"#454866", "stroke-width":"1"}));

  /* 柱 + 数值 */
  const vals = DATA.series[current];
  barsG.innerHTML = "";
  vals.forEach((v, i) => {
    if (v == null) return;
    const h = barH(v);
    const x0 = D.slotX[i] - D.barW / 2;
    const top = D.baseY - h;
    barsG.appendChild(mk("rect", {"class":"bar", x:x0, y:top, width:D.barW,
                                  height:h, fill:"url(#barGrad)"}));
    barsG.appendChild(mk("text", {"class":"vlab", x:D.slotX[i], y:top - 9,
                                  fill:"#F0F1F8", "font-size":"13.5",
                                  "text-anchor":"middle"}, v.toFixed(2)));
  });

  /* 按钮态 */
  chipsBox.querySelectorAll(".chip").forEach(b => {
    const on = b.dataset.dept === current;
    b.classList.toggle("on", on);
    b.setAttribute("aria-pressed", on ? "true" : "false");
  });

  /* 淡入 */
  barsG.style.opacity = .25;
  requestAnimationFrame(() => { barsG.style.opacity = 1; });
}

function select(name){
  if (name === current) return;
  current = name;
  render();
}

render();
</script>
</body>
</html>
"""


def build_html(path=None):
    design = dict(
        gridY=GRID_Y, baseY=BASE_Y, gridX0=GRID_X0, gridX1=GRID_X1,
        slotX=SLOT_X, barW=BAR_W, plotTop=PLOT_TOP, maxRef=MAX_REF,
        catY=CAT_Y,
    )
    data = dict(edu=EDU, depts=DEPTS, defaultDept=DEFAULT,
                series={k: v for k, v in DATA.items()}, design=design)
    html = (HTML.replace("__TITLE__", TITLE)
                .replace("__NOTE__", NOTE_TEXT)
                .replace("__DATA__", json.dumps(data, ensure_ascii=False)))
    path = path or os.path.join(OUT_DIR, "chart5.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


if __name__ == "__main__":
    print("png :", draw_static())
    print("svg :", build_svg())
    print("html:", build_html())
