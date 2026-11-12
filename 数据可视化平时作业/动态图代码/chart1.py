import plotly.graph_objects as go
import pandas as pd
import os

# ==========================================
# 1. 准备数据 (这里我用字典模拟了图片中的数据，你可以换成读Excel)
# ==========================================
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
data_dict = {
    '1月': [260, 250, 700, 520, 460, 390],
    '2月': [240, 270, 530, 330, 580, 290],
    '3月': [330, 340, 700, 540, 490, 310],
    '4月': [290, 350, 600, 270, 490, 390],
    '5月': [290, 320, 700, 490, 400, 310],
    '6月': [800, 380, 280, 570, 460, 800]
}
months = list(data_dict.keys())

# ==========================================
# 2. 创建图表 Traces (把每个月的数据变成一根根柱子)
# ==========================================
traces = []
for i, month in enumerate(months):
    traces.append(
        go.Bar(
            x=regions,
            y=data_dict[month],
            name=month,
            marker_color='#0099e5',  # 亮蓝色
            width=0.35,              # 柱子宽度
            visible=(i == 0)         # 默认只显示第一个月(1月)
        )
    )

# ==========================================
# 3. 创建下拉菜单按钮 (点击切换可见性)
# ==========================================
buttons = []
for i, month in enumerate(months):
    visibility = [False] * len(months)
    visibility[i] = True
    buttons.append(
        dict(
            label=month,
            method="update",
            args=[{"visible": visibility}]
        )
    )

# ==========================================
# 4. 配置图表布局 (颜色、字体、下拉菜单位置等，高度还原截图)
# ==========================================
layout = go.Layout(
    title=dict(
        text="2022年上半年各区域销售情况",
        font=dict(size=26, color='white', family='Microsoft YaHei'),
        x=0.05,
        y=0.95
    ),
    paper_bgcolor='#181d3a', # 深蓝色背景
    plot_bgcolor='#181d3a',
    font=dict(color='white', family='Microsoft YaHei'),
    yaxis=dict(
        range=[0, 850],
        tickvals=[0, 200, 400, 600, 800],
        gridcolor='rgba(255, 255, 255, 0.2)', # 半透明虚线网格
        griddash='dash',
        zeroline=False
    ),
    xaxis=dict(showgrid=False, tickfont=dict(size=14)),
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=0.95, xanchor="right", y=1.15, yanchor="top",
            bgcolor="white", bordercolor="gray", font=dict(color="black", size=14)
        )
    ],
    annotations=[
        dict(
            text="*注：数据来源公司销售系统",
            showarrow=False, xref="paper", yref="paper", x=0.02, y=-0.15,
            align="left", font=dict(size=12, color='#a0a0a0')
        )
    ],
    margin=dict(t=120, b=80, l=60, r=40)
)

fig = go.Figure(data=traces, layout=layout)

# ==========================================
# 5. 自动创建目录并保存文件 (核心逻辑)
# ==========================================
# 获取当前代码所在目录的上一级目录，也就是项目根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docs_dir = os.path.join(base_dir, 'docs')

# 如果 docs 文件夹不存在，就自动创建一个
if not os.path.exists(docs_dir):
    os.makedirs(docs_dir)
    print(" 成功创建 docs 文件夹")

# 导出动态网页
html_path = os.path.join(docs_dir, 'chart1.html')
fig.write_html(html_path)

# 导出静态预览图 (需要安装 kaleido 库)
try:
    img_path = os.path.join(docs_dir, 'chart1.png')
    fig.write_image(img_path, width=1000, height=600, scale=2)
    print(f"成功生成网页和图片到 docs 文件夹！")
except Exception as e:
    print(f"⚠图片生成失败，请确保在终端输入了 pip install kaleido。错误信息：{e}")

print(f"网页路径: {html_path}")

# 这是生成 index.html 的代码，你可以单独建个文件跑，也可以追加到上面
index_html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>我的动态图表作业展示</title>
    <style>
        body { font-family: 'Microsoft YaHei', sans-serif; background-color: #181d3a; color: white; text-align: center; padding-top: 50px; }
        h1 { margin-bottom: 40px; }
        .container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }
        .card { background: #252c52; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); width: 320px; transition: transform 0.3s; }
        .card:hover { transform: translateY(-10px); }
        .card img { width: 100%; border-radius: 5px; margin-bottom: 15px; }
        .card a { display: inline-block; padding: 10px 20px; background-color: #0099e5; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }
        .card a:hover { background-color: #007bb5; }
    </style>
</head>
<body>
    <h1>📊 数据可视化作业展示</h1>
    <div class="container">
        <!-- 图表1的卡片 -->
        <div class="card">
            <img src="chart1.png" alt="图表1预览">
            <h3>2022年上半年销售情况</h3>
            <a href="chart1.html" target="_blank">👉 点击体验动态图</a>
        </div>

        <!-- 如果你有第二张图，把上面这块复制一份，把 chart1 改成 chart2 即可 -->

    </div>
</body>
</html>
"""

index_path = os.path.join(docs_dir, 'index.html')
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_html_content)
print(f"✅ 导航首页生成成功: {index_path}")