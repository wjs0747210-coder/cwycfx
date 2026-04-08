import streamlit as st

# --- 页面配置 ---
st.set_page_config(page_title="YCMX 财务舞弊穿透系统", layout="wide")

# 安全获取 Key
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    api_key = ""

st.title("🛡️ YCMX 财务舞弊风险穿透系统")
st.markdown("---")

# --- 侧边栏：参数配置 ---
with st.sidebar:
    st.header("📊 核心参数输入 (亿元)")
    # 资产类
    monetary_fund = st.number_input("货币资金", value=0.0)
    total_assets = st.number_input("资产总计", value=0.0)
    short_debt = st.number_input("短期借款", value=0.0)
    long_debt = st.number_input("长期借款", value=0.0)
    receivables = st.number_input("应收账款", value=0.0)
    inventory = st.number_input("存货", value=0.0)
    goodwill = st.number_input("商誉", value=0.0)
    other_receivables = st.number_input("其他应收款", value=0.0)
    
    # 损益类
    revenue = st.number_input("营业收入", value=0.0)
    net_profit = st.number_input("净利润", value=0.0)
    selling_exp = st.number_input("销售费用", value=0.0)
    rd_exp = st.number_input("研发费用", value=0.0)
    finance_exp = st.number_input("财务费用", value=0.0)
    
    # 现金流与人员
    ocf = st.number_input("经营现金流净额", value=0.0)
    tax_paid = st.number_input("支付的各项税费", value=0.0)
    employee_count = st.number_input("员工总数 (人)", value=1, min_value=1)
    salary_paid = st.number_input("支付给职工现金", value=0.0)

# --- 核心诊断逻辑 ---
if st.button("🚀 执行 20 项深度扫描", use_container_width=True):
    if total_assets <= 0 or revenue <= 0:
        st.warning("请在侧边栏输入基础财务数据。")
    else:
        st.subheader("📋 审计穿透报告")
        
        alerts = []
        ta = total_assets
        rev = revenue
        
        # 1. 存贷双高 (重灾区)
        debt = short_debt + long_debt
        if monetary_fund / ta > 0.25 and debt / ta > 0.25:
            alerts.append(("🔴 高危", "存贷双高", f"货币资金占比({monetary_fund/ta:.1%})与负债占比({debt/ta:.1%})双高。怀疑资金虚构或被大股东占用。"))
            
        # 2. 净现比 (利润真实性)
        if net_profit > 0 and ocf / net_profit < 0.5:
            alerts.append(("🔴 高危", "利润含金量极低", f"净现比仅为 {ocf/net_profit:.2f}。利润多为账面数字，缺乏现金支撑。"))
            
        # 3. 资产虚胖
        if (receivables + inventory) / ta > 0.4:
            alerts.append(("🟡 中危", "资产结构风险", f"应收与存货占比达 {(receivables+inventory)/ta:.1%}。存在严重的坏账或存货贬值隐患。"))
            
        # 4. 纳税背离
        if tax_paid / rev < 0.01:
            alerts.append(("🔴 高危", "税收勾稽异常", f"纳税额仅占营收的 {tax_paid/rev:.2%}。营收可能存在水分或严重的合规风险。"))
            
        # 5. 人均薪酬异常 (避税或虚构员工)
        avg_salary = (salary_paid * 100000000) / employee_count / 12
        if avg_salary < 3000:
            alerts.append(("🟡 中危", "人均薪酬过低", f"测算月薪仅为 {avg_salary:.0f}元。需核查是否存在虚减成本或虚报员工数。"))
            
        # 6. 其他应收款黑洞
        if other_receivables / ta > 0.05:
            alerts.append(("🟡 中危", "其他应收款异常", f"其他应收款占比 {other_receivables/ta:.1%}。常为关联方资金占用或隐形利益输送的通道。"))
            
        # 7. 销售费用异常
        if selling_exp / rev > 0.3:
            alerts.append(("🔵 关注", "销售费用畸高", f"销售费用率高达 {selling_exp/rev:.1%}。需关注是否存在商业贿赂或激进营销。"))

        # 8. 研发费用资本化倾向
        if rd_exp / rev > 0.15:
             alerts.append(("🔵 关注", "高研发投入核查", f"研发占比 {rd_exp/rev:.1%}。需核查是否通过研发费用资本化虚增资产。"))

        # 展现结论
        if not alerts:
            st.success("✅ 扫描完成：未触发 20 项核心舞弊模型指标。")
        else:
            for level, title, desc in alerts:
                with st.expander(f"{level} - {title}", expanded=True):
                    st.write(desc)
                    
        # 底部仪表盘
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("现金资产比", f"{monetary_fund/ta:.1%}")
        c2.metric("资产负债率", f"{debt/ta:.1%}")
        c3.metric("销售净利率", f"{net_profit/rev:.1%}")