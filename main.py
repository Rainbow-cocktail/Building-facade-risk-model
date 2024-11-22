import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time

st.sidebar.title('外墙风险模型评估')

selected = st.sidebar.selectbox('评估流程阶段', ['输入信息', '模型评估与展示'])

# 初始化状态
if 'input_dict' not in st.session_state:
    st.session_state['input_dict'] = {}

if selected == '输入信息':
    st.title('建筑外墙风险模型信息输入')
    with st.expander('模型参数说明'):
        st.write("本模型暂时仅供展示用途，不具备真实风险评估能力。")

    with st.form(key='选择外墙信息'):
        st.subheader('请输入该建筑的外墙信息')
        st.write(' **1. 选择省份和城市**')
        province_cn = st.selectbox('省份',
                               ['北京', '上海', '广东', '江苏', '浙江', '山东', '河南', '河北', '四川', '湖北', '湖南', '福建',
                                '安徽', '江西', '广西', '重庆', '辽宁', '吉林', '黑龙江', '陕西', '甘肃', '山西', '内蒙古',
                                '新疆', '云南', '贵州', '海南', '青海', '宁夏', '西藏'])
        # 以省会城市为例
        city_cn = st.selectbox('城市',
                                ['北京', '上海', '广州', '深圳', '杭州', '南京', '苏州', '无锡', '青岛', '济南', '郑州', '武汉',
                                 '长沙', '福州', '厦门', '合肥', '南昌', '广西', '重庆', '沈阳', '长春', '哈尔滨', '西安',
                                 '兰州', '太原', '呼和浩特', '乌鲁木齐', '昆明', '贵阳', '海口', '西宁', '银川', '拉萨'])

        st.write(' **2. 选择建筑高度**')
        height = st.number_input('建筑高度(m)', min_value=1, max_value=100, value=10)
        orientation = st.selectbox('朝向', ['东', '南', '西', '北'])

        st.write(' **3. 输入外墙检测信息**')
        # 裂缝条数
        crack_num = st.number_input('裂缝条数', min_value=0, max_value=100, value=1)
        # 输入空鼓信息
        hollow_num = st.number_input('空鼓个数', min_value=0, max_value=100, value=1)
        hollow_area = st.number_input('空鼓面积占比(%)', min_value=0.0, max_value=1.0, value=0.5)

        st.write(' **4. 输入外墙使用年份**')
        year = st.number_input('外墙使用年份', min_value=1, max_value=100, value=5)

        st.write(' **5. 初始施工质量参数化指标**')
        # 施工质量系数
        quality_factor = st.number_input('施工质量系数', min_value=0.0, max_value=1.0, value=0.8)
        # 施工质量参数化指标
        other_factor = st.number_input('其他调整系数', min_value=0.0, max_value=1.0, value=0.5)

        submitted = st.form_submit_button('Submit')


    input_dict = {}
    if submitted:
        st.write(' **下面是您输入的外墙信息** ')
        st.write('省份:', province_cn)
        st.write('城市:', city_cn)
        st.write('建筑高度:', height)
        st.write('朝向:', orientation)
        st.write('裂缝条数:', crack_num)
        st.write('空鼓个数:', hollow_num)
        st.write('空鼓面积占比:', hollow_area)
        st.write('外墙使用年份:', year)
        st.write('施工质量系数:', quality_factor)
        st.write('其他调整系数:', other_factor)

        st.session_state['input_dict'] = {
            '省份': province_cn, '城市': city_cn, '建筑高度': height, '朝向': orientation,
            '裂缝条数': crack_num, '空鼓个数': hollow_num,
            '空鼓面积占比': hollow_area, '外墙使用年份': year, '施工质量系数': quality_factor,
            '其他调整系数': other_factor
        }
        st.success("信息已保存！")


if selected == "模型评估与展示":
    st.title('建筑外墙风险模型评估与展示')
    if not st.session_state['input_dict']:
        st.warning('请先输入外墙信息！')
    else:
        st.write(' **以下是之前保存的外墙信息** ')
        for key, value in st.session_state['input_dict'].items():
            st.write(f"{key}: {value}")

    # 模型评估,按钮
    if st.button('点击开始模型评估'):
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)
        st.success('模型评估完成！')
        st.balloons()

        col1, col2 = st.columns(2)
        # 样式
        style_text = """
        <style>
            .highlight-box {
                background-color: #f0f0f0;
                padding: 20px;
                border-radius: 10px;
                border: 2px solid #ddd;
                text-align: center;
                font-weight: bold;
                font-size: 1.5rem;
                color: #333;
            }
            .highlight-box-risk {
                background-color: #ffdddd;
                padding: 20px;
                border-radius: 10px;
                border: 2px solid #ff6666;
                text-align: center;
                font-weight: bold;
                font-size: 1.5rem;
                color: #990000;
            }
        </style>
        """

        # 注入样式
        st.markdown(style_text, unsafe_allow_html=True)

        # 左侧内容
        with col1:
            st.markdown('<div class="highlight-box">当前可靠性概率<br><span style="color: #007BFF;">0.8</span></div>',
                        unsafe_allow_html=True)

        # 右侧内容
        with col2:
            st.markdown(
                '<div class="highlight-box-risk">当前风险等级<br><span style="color: #FF4500;">一般</span></div>',
                unsafe_allow_html=True)


        st.write(' ## 外墙脱落风险年份预测 ')

        # 数据,这里是随便捏造的
        years = np.linspace(1, 25, 500)  # 从 1 到 25 的年份
        risk = np.log(years + 1) / np.log(25 + 1)  # 归一化的对数函数，范围在 0-1

        # 创建 Plotly 图表
        fig = go.Figure()

        # 添加风险曲线
        fig.add_trace(go.Scatter(
            x=years, y=risk,
            mode='lines',
            line=dict(color='blue', width=3),
            name='外墙脱落风险'
        ))

        # 添加 90% 风险临界线
        fig.add_trace(go.Scatter(
            x=[1, 25], y=[0.9, 0.9],
            mode='lines',
            line=dict(color='red', dash='dash', width=2),
            name='90% 风险临界线'
        ))

        # 标注危险区域
        fig.add_annotation(
            x=24, y=0.92,
            text="危险区",
            showarrow=False,
            font=dict(size=12, color="red")
        )

        # 设置布局
        fig.update_layout(
            title='外墙脱落风险预测',
            xaxis_title='使用年份',
            yaxis_title='脱落风险概率',
            xaxis=dict(range=[1, 25]),
            yaxis=dict(range=[0, 1.05]),
            plot_bgcolor='rgba(240,240,240,0.9)',  # 背景色
            font=dict(size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        # 显示图表
        st.plotly_chart(fig)




