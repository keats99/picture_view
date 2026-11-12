import plotly.graph_objects as go
import numpy as np
import os

# ==========================================
# 1. 准备数据
# ==========================================
months = ['1月', '2月', '3月', '4月']
depts = ['人力部', '行政部', '财务部', '工程部', '采购部', '销售部']

data = {
    '1月': {'total': 1664, 'vals': [130, 226, 238, 293, 326, 451]},
    '2月': {'total': 1682, 'vals': [138, 205, 228, 305, 349, 456]},
    '3月': {'total': 1638, 'vals': [130, 217, 255, 314, 316, 406]},
    '4月': {'total': 1637, 'vals': [129, 226, 226, 264, 359, 433]}
}

# 从内到外的颜色：紫、深蓝、浅蓝、黄、红、亮粉 (对应原图)
colors = ['#8e44ad', '#2980b9', '#00a8ff', '#f1c40f', '#e74c3c', '#ff4d6d']

# 参数设置
max_val = 500  # 假设最大值为500，映射为180度
base_radius = 80  # 最内圈半径
radius_gap = 35  # 跑道间距

# ==========================================
# 2. 构建图表 Traces (半圆跑道 + 左侧引线)
# ==========================================
traces = []

for m_idx, month in enumerate(months):
    is_visible = (m_idx == 0)  # 默认显示1月
    vals = data[month]['vals']

    for i, val in enumerate(vals):
        R = base_radius + i * radius_gap

        # 计算圆弧跨度
        extent = (val / max_val) * 180
        # 核心修复：起点 90度(正上方)，终点 90 - extent。配合逆时针方向，实现向右画半圆
        end_angle = 90 - extent

        theta_arc = np.linspace(90, end_angle, 100)
        r_arc = [R] * 100

        # 画跑道圆弧
        traces.append(go.Scatterpolar(
            r=r_arc, theta=theta_arc, mode='lines',
            line=dict(color=colors[i], width=16),  # 线条粗细
            visible=is_visible, hoverinfo='none', showlegend=False
        ))

        # 画左侧的灰色引线 (使用直角坐标系，固定在文字右侧)
        traces.append(go.Scatter(
            x=[0.38, 0.42], y=[0.78 - i * 0.05, 0.78 - i * 0.05],
            mode='lines', line=dict(color='#a0a0a0', width=1.5),
            visible=is_visible, hoverinfo='none', showlegend=False, xaxis='x', yaxis='y'
        ))

# ==========================================
# 3. 制作下拉菜单和动态文字标签
# ==========================================
buttons = []
initial_annotations = []

for m_idx, month in enumerate(months):
    # 独立控制可见性
    visibility = [False] * (len(months) * 12)
    for i in range(12):
        visibility[m_idx * 12 + i] = True

    # 基础标注 (右上角月份 + 左下角备注)
    anns = [
        dict(text=f"{month}", x=0.82, y=0.95, xref="paper", yref="paper", showarrow=False,
             font=dict(size=20, color='#b0b0b0')),
        dict(text="*注：数据来源公司人力资源系统", x=0.02, y=-0.1, xref="paper", yref="paper", showarrow=False,
             font=dict(size=14, color='#a0a0a0'))
    ]

    # 动态文本标签
    vals = data[month]['vals']
    for i in range(len(depts)):
        anns.append(dict(
            text=f"{depts[i]} {vals[i]}",
            x=0.35,  # 放在引线左侧
            y=0.78 - i * 0.05,  # 从上往下排
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14, color='white'),
            xanchor='right',  # 右对齐
            align='right'
        ))

    if m_idx == 0:
        initial_annotations = anns

    buttons.append(dict(
        label=month, method="update",
        args=[
            {"visible": visibility},
            {
                "title.text": f"{month}公司总人数为{data[month]['total']}",
                "annotations": anns
            }
        ]
    ))

# ==========================================
# 4. 布局设置 (核心：修正方向)
# ==========================================
layout = go.Layout(
    title=dict(text="1月公司总人数为1664", font=dict(size=30, color='white'), x=0.05, y=0.95),
    paper_bgcolor='#1a1f3d',  # 匹配原图深蓝底色
    plot_bgcolor='#1a1f3d',
    font=dict(color='white', family='Microsoft YaHei'),

    # 极坐标设置
    polar=dict(
        bgcolor='rgba(0,0,0,0)',
        radialaxis=dict(visible=False, range=[0, base_radius + 6 * radius_gap]),
        angularaxis=dict(
            visible=False,
            direction="counterclockwise",  # 默认逆时针
            rotation=90  # 关键：把 90 度旋转到正上方！
        )
    ),

    # 空白直角坐标系(用于画引线)
    xaxis=dict(visible=False, range=[0, 1]),
    yaxis=dict(visible=False, range=[0, 1]),

    updatemenus=[dict(
        buttons=buttons, direction="down", showactive=True,
        x=0.85, xanchor="right", y=1.15, yanchor="top",
        bgcolor="white", bordercolor="gray", font=dict(color="black", size=14)
    )],

    annotations=initial_annotations,
    margin=dict(t=100, b=80, l=80, r=80)
)

fig = go.Figure(data=traces, layout=layout)

# ==========================================
# 5. 保存到 docs 文件夹
# ==========================================
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docs_dir = os.path.join(base_dir, 'docs')
os.makedirs(docs_dir, exist_ok=True)

html_path = os.path.join(docs_dir, 'chart2.html')
fig.write_html(html_path)
print(f"✅ 成功生成动态网页: {html_path}")

try:
    img_path = os.path.join(docs_dir, 'chart2.png')
    fig.write_image(img_path, width=1000, height=600, scale=2)
    print(f"✅ 成功生成预览图片: {img_path}")
except Exception as e:
    print(f"⚠️ 图片生成失败: {e}")