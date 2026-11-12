r"""
第11章 数据治理介绍 —— 基于 GB/T 36073-2018 DCMM
PDF文本提取 → 结构解析 → 框架图 + 自评估打分表 + 雷达图 + 词频图
运行环境：Windows + PyCharm，项目根目录 D:\Python_code\cda和数据可视化作业\商业数据分析平时作业
依赖：pandas, numpy, matplotlib, networkx, openpyxl；PDF读取三选一（pdfplumber/pypdf/PyPDF2）
"""

import os
import re
import random
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter

# ==================== 0. 路径与字体 ====================
BASE_DIR = r"D:\Python_code\cda和数据可视化作业\商业数据分析平时作业"
DATA_DIR = os.path.join(BASE_DIR, "data", "chapter11_data_governance")
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter11_data_governance")
PDF_PATH = os.path.join(DATA_DIR, "GBT 36073-2018 数据管理能力成熟度评估模型.pdf")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
my_font = fm.FontProperties(fname=FONT_PATH)
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# ==================== 1. 读取 PDF（三重兜底 + 打印具体错误） ====================
def read_pdf(path):
    if not os.path.exists(path):
        return None, f"文件不存在！请检查路径：{path}"

    # 优先 pdfplumber
    try:
        import pdfplumber
        parts = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                parts.append(page.extract_text() or "")
        text = "\n".join(parts)
        if text.strip():
            return text, "pdfplumber"
        else:
            print("  -> 提示：pdfplumber 成功打开文件，但没提取到文字（可能是扫描件/纯图片PDF）")
    except ImportError:
        print("  -> 提示：未安装 pdfplumber 库，尝试下一个库...")
    except Exception as e:
        print(f"  -> 提示：pdfplumber 读取失败，错误详情：{e}")

    # 其次 pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        text = "\n".join((p.extract_text() or "") for p in reader.pages)
        if text.strip():
            return text, "pypdf"
    except ImportError:
        print("  -> 提示：未安装 pypdf 库，尝试下一个库...")
    except Exception as e:
        print(f"  -> 提示：pypdf 读取失败，错误详情：{e}")

    # 最后 PyPDF2
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(path)
        text = "\n".join((p.extract_text() or "") for p in reader.pages)
        if text.strip():
            return text, "PyPDF2"
    except ImportError:
        print("  -> 提示：未安装 PyPDF2 库，尝试下一个库...")
    except Exception as e:
        print(f"  -> 提示：PyPDF2 读取失败，错误详情：{e}")

    return None, "三个库全部失败（请检查是否已 pip install pdfplumber）"


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"学兔兔.*?www\.bzfxw\.com", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ==================== 2. DCMM 结构兜底（PDF提取失败时用） ====================
DOMAIN_MAP = {
    "6": "数据战略", "7": "数据治理", "8": "数据架构", "9": "数据应用",
    "10": "数据安全", "11": "数据质量", "12": "数据标准", "13": "数据生存周期",
}

HARDCODE_DCMM = {
    "数据战略": ["数据战略规划", "数据战略实施", "数据战略评估"],
    "数据治理": ["数据治理组织", "数据制度建设", "数据治理沟通"],
    "数据架构": ["数据模型", "数据分布", "数据集成与共享", "元数据管理"],
    "数据应用": ["数据分析", "数据开放共享", "数据服务"],
    "数据安全": ["数据安全策略", "数据安全管理", "数据安全审计"],
    "数据质量": ["数据质量需求", "数据质量检查", "数据质量分析", "数据质量提升"],
    "数据标准": ["业务术语", "参考数据和主数据", "数据元", "指标数据"],
    "数据生存周期": ["数据需求", "数据设计和开发", "数据运维", "数据退役"],
}

HARDCODE_LEVELS = [
    (1, "初始级", "数据需求的管理主要是在项目级体现，没有统一的管理流程，主要是被动式管理"),
    (2, "受管理级", "组织已意识到数据是资产，根据管理策略的要求制定了管理流程，指定了相关人员进行初步管理"),
    (3, "稳健级", "数据已被当做实现组织绩效目标的重要资产，在组织层面制定了系列的标准化管理流程"),
    (4, "量化管理级", "数据被认为是获取竞争优势的重要资源，数据管理的效率能量化分析和监控"),
    (5, "优化级", "数据被认为是组织生存和发展的基础，相关管理流程能实时优化，能在行业内进行最佳实践分享"),
]

# ==================== 3. 从 PDF 提取 DCMM 能力域结构 ====================
def extract_dcmm_from_text(text):
    if not text:
        return None
    pattern = re.compile(
        r"^\s*(\d+)\.(\d+)\s+([\u4e00-\u9fa5][\u4e00-\u9fa5（）()]{1,18}?)\s*$",
        re.MULTILINE,
    )
    matches = pattern.findall(text)
    if not matches:
        return None
    result, seen = {}, set()
    for ch, sub, title in matches:
        if ch not in DOMAIN_MAP:
            continue
        key = (ch, sub)
        if key in seen:
            continue
        seen.add(key)
        result.setdefault(DOMAIN_MAP[ch], []).append(title)
    if len(result) != 8:
        return None
    if any(len(v) < 3 for v in result.values()):
        return None
    return result

# ==================== 4. 从 PDF 提取成熟度等级 ====================
def extract_levels_from_text(text):
    if not text:
        return None
    names = ["初始级", "受管理级", "稳健级", "量化管理级", "优化级"]
    levels = []
    for i, name in enumerate(names, 1):
        pat = re.compile(
            r"5\.2\." + str(i) + r"\s*" + name + r"\s*(.*?)(?=5\.2\." + str(i + 1) + r"|##\s*6|$)",
            re.DOTALL,
        )
        m = pat.search(text)
        if m:
            desc = clean_text(m.group(1))[:100]
            levels.append((i, name, desc))
    if len(levels) == 5:
        return levels
    return None

# ==================== 5. 中文词频统计 ====================
def word_frequency(text, top_n=30):
    if not text:
        return pd.DataFrame()
    clean = re.sub(r"[^\u4e00-\u9fa5]", "|", text)
    tokens = [seg for seg in clean.split("|") if 2 <= len(seg) <= 4]
    return pd.DataFrame(Counter(tokens).most_common(top_n), columns=["词语", "频次"])

# ==================== 6. DCMM 框架图 ====================
def draw_dcmm_tree(dcmm):
    G = nx.DiGraph()
    root = "DCMM数据管理能力"
    G.add_node(root)
    for d, subs in dcmm.items():
        G.add_edge(root, d)
        for s in subs:
            G.add_edge(d, s)

    pos, colors = {}, {}
    y, palette = 0.0, plt.get_cmap("tab10")(np.linspace(0, 1, len(dcmm)))
    for i, (d, subs) in enumerate(dcmm.items()):
        colors[d] = palette[i]
        ys = [y + k for k in range(len(subs))]
        for s, yy in zip(subs, ys):
            pos[s] = (2.0, yy)
        pos[d] = (1.0, float(np.mean(ys)))
        y += len(subs) + 0.8
    total_h = y - 0.8
    pos[root] = (0.0, total_h / 2.0)

    fig, ax = plt.subplots(figsize=(14, 24))
    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        ax.plot([x1, x2], [y1, y2],
                color="black" if u == root else "gray",
                lw=2.0 if u == root else 0.8, alpha=0.6, zorder=1)

    for d, subs in dcmm.items():
        c = colors[d]
        x, yy = pos[d]
        ax.scatter(x, yy, s=260, c=[c], edgecolors="black", zorder=3)
        ax.text(x - 0.06, yy, d, fontproperties=my_font, fontsize=14,
                ha="right", va="center", fontweight="bold")
        for s in subs:
            sx, sy = pos[s]
            ax.scatter(sx, sy, s=70, c=[c], alpha=0.7, edgecolors="black", zorder=3)
            ax.text(sx + 0.05, sy, s, fontproperties=my_font, fontsize=10,
                    ha="left", va="center")

    rx, ry = pos[root]
    ax.scatter(rx, ry, s=700, c="darkred", edgecolors="black", zorder=3)
    ax.text(rx - 0.08, ry, "DCMM\n数据管理能力", fontproperties=my_font,
            fontsize=16, ha="right", va="center", fontweight="bold")

    ax.set_xlim(-1.9, 3.2)
    ax.set_ylim(-1.0, total_h + 1.0)
    ax.axis("off")
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "DCMM八大能力域框架图.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[OK] DCMM框架图已保存：{out}")

# ==================== 7. 自评估打分表 ====================
def build_assessment(dcmm, levels):
    random.seed(42)
    rows = [{"能力域": d, "能力项": s, "自评得分(1-5)": random.randint(1, 5)}
            for d, subs in dcmm.items() for s in subs]
    df = pd.DataFrame(rows)
    summary = (df.groupby("能力域", sort=False)["自评得分(1-5)"]
                 .agg(平均分="mean", 最低分="min", 最高分="max", 能力项数="count")
                 .reset_index())
    summary["平均分"] = summary["平均分"].round(2)

    def to_level(avg):
        if avg < 1.8:   return "1级-初始级"
        if avg < 2.6:   return "2级-受管理级"
        if avg < 3.4:   return "3级-稳健级"
        if avg < 4.2:   return "4级-量化管理级"
        return "5级-优化级"
    summary["综合等级"] = summary["平均分"].apply(to_level)

    levels_df = pd.DataFrame(levels, columns=["等级", "名称", "说明"])

    df.to_csv(os.path.join(OUT_DIR, "DCMM自评估_打分明细.csv"),
              index=False, encoding="utf-8-sig")
    summary.to_csv(os.path.join(OUT_DIR, "DCMM自评估_能力域汇总.csv"),
                   index=False, encoding="utf-8-sig")
    print(f"[OK] 自评估CSV已保存到：{OUT_DIR}")

    excel = os.path.join(OUT_DIR, "DCMM自评估打分表.xlsx")
    try:
        with pd.ExcelWriter(excel, engine="openpyxl") as w:
            df.to_excel(w, sheet_name="打分明细", index=False)
            summary.to_excel(w, sheet_name="能力域汇总", index=False)
            levels_df.to_excel(w, sheet_name="成熟度等级说明", index=False)
        print(f"[OK] 自评估Excel已保存：{excel}")
    except Exception as e:
        print(f"[警告] Excel 写出失败（{e}），CSV 已保底。")
    return df, summary

# ==================== 8. 雷达图 ====================
def draw_radar(summary):
    labels = summary["能力域"].tolist()
    vals = summary["平均分"].tolist()
    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    vals_c = vals + vals[:1]
    ang_c = angles + angles[:1]

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(ang_c, vals_c, "o-", linewidth=2, color="steelblue")
    ax.fill(ang_c, vals_c, alpha=0.25, color="steelblue")
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontproperties=my_font, fontsize=11)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1级", "2级", "3级", "4级", "5级"],
                       fontproperties=my_font, fontsize=9)
    ax.set_title("DCMM八大能力域自评估雷达图", fontproperties=my_font,
                 fontsize=15, pad=20)
    out = os.path.join(OUT_DIR, "DCMM自评估雷达图.png")
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[OK] 雷达图已保存：{out}")

# ==================== 9. 词频柱状图 ====================
def draw_word_freq(df_word, top_n=20):
    if df_word is None or df_word.empty:
        print("[跳过] 词频为空，跳过画图。")
        return
    top = df_word.head(top_n).iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(top["词语"], top["频次"], color="teal")
    for i, v in enumerate(top["频次"]):
        ax.text(v, i, f" {v}", va="center", fontproperties=my_font, fontsize=9)
    ax.set_xlabel("出现次数", fontproperties=my_font, fontsize=11)
    ax.set_title(f"GB/T 36073-2018 全文 Top{top_n} 高频词",
                 fontproperties=my_font, fontsize=14)
    ax.tick_params(axis="y", labelsize=10)
    for lbl in ax.get_yticklabels():
        lbl.set_fontproperties(my_font)
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "DCMM标准高频词Top20.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[OK] 词频图已保存：{out}")

# ==================== 10. 主流程 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("第11章 数据治理介绍 —— GB/T 36073-2018 DCMM 全流程")
    print("=" * 60)

    # Step 1: 读 PDF
    print("\n[Step 1] 读取 PDF...")
    raw, source = read_pdf(PDF_PATH)
    if raw:
        print(f"[OK] 使用 {source} 读取成功，字符数：{len(raw)}")
        dump = os.path.join(DATA_DIR, "dcmm_原始提取文本.txt")
        with open(dump, "w", encoding="utf-8") as f:
            f.write(raw)
        print(f"[OK] 原始文本已存档：{dump}")
    else:
        print(f"[警告] PDF 读取失败：{source}，将回退硬编码结构。")

    # Step 2: 提取 DCMM 结构
    print("\n[Step 2] 从 PDF 提取能力域结构...")
    dcmm = extract_dcmm_from_text(raw) if raw else None
    if dcmm:
        total = sum(len(v) for v in dcmm.values())
        print(f"[OK] 从 PDF 提取成功：{len(dcmm)} 个能力域 / {total} 个能力项")
        pd.DataFrame([{"能力域": d, "能力项": s} for d, subs in dcmm.items() for s in subs]) \
            .to_csv(os.path.join(OUT_DIR, "PDF提取_DCMM能力域结构.csv"),
                    index=False, encoding="utf-8-sig")
    else:
        dcmm = HARDCODE_DCMM
        print("[警告] 从 PDF 提取失败，使用硬编码 DCMM 结构（与国标一致）")

    # Step 3: 提取成熟度等级
    print("\n[Step 3] 从 PDF 提取成熟度等级描述...")
    levels = extract_levels_from_text(raw) if raw else None
    if levels:
        print(f"[OK] 从 PDF 提取成功：{len(levels)} 个等级")
        for lv in levels:
            print(f"    {lv[0]}级 {lv[1]}: {lv[2][:40]}...")
    else:
        levels = HARDCODE_LEVELS
        print("[警告] 从 PDF 提取失败，使用硬编码等级描述")

    # Step 4: 词频
    print("\n[Step 4] 中文词频统计...")
    df_word = word_frequency(raw) if raw else pd.DataFrame()
    if not df_word.empty:
        wcsv = os.path.join(OUT_DIR, "DCMM标准高频词Top30.csv")
        df_word.to_csv(wcsv, index=False, encoding="utf-8-sig")
        print(f"[OK] 词频已保存：{wcsv}")
        print(f"    Top5：{df_word.head(5).to_dict('records')}")

    # Step 5: 图 + 表
    print("\n[Step 5] 生成图表与打分表...")
    draw_dcmm_tree(dcmm)
    _, summary = build_assessment(dcmm, levels)
    print("\n【能力域汇总预览】")
    print(summary.to_string(index=False))
    draw_radar(summary)
    draw_word_freq(df_word, top_n=20)

    with open(os.path.join(DATA_DIR, "数据来源说明.txt"), "w", encoding="utf-8") as f:
        f.write("数据来源：GB/T 36073-2018《数据管理能力成熟度评估模型》\n")
        f.write(f"PDF解析库：{source if raw else '失败，回退硬编码'}\n")
        f.write(f"能力域数量：{len(dcmm)}\n")
        f.write(f"能力项总数：{sum(len(v) for v in dcmm.values())}\n")
        f.write(f"成熟度等级数：{len(levels)}\n")
        f.write("自评估分数用 random.seed(42) 模拟，实际使用时替换为业务部门真实打分。\n")

    print("\n全部完成！输出目录：", OUT_DIR)