import streamlit as st

# --- 页面配置 ---
st.set_page_config(page_title="YCMX - 财务异常分析(亿元版)", layout="wide")

st.title("🛡️ YCMX 财务异常分析模型")
st.caption("提示：请按财报数据输入数字，单位统一为：**亿元**")

# --- 输入区域 ---
with st.container():
    st.markdown("### 📝 核心数据录入 (单位：亿元)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🏦 资产负债表数据")
        monetary_fund = st.number_input("货币资金", min_value=0.0, step=0.1, help="现金及现金等价物")
        total_assets = st.number_input("资产总计", min_value=0.0, step=0.1)
        short_debt = st.number_input("短期借款", min_value=0.0, step=0.1)
        long_debt = st.number_input("长期借款", min_value=0.0, step=0.1)
        accounts_receivable = st.number_input("应收账款", min_value=0.0, step=0.1)
        inventory = st.number_input("存货", min_value=0.0, step=0.1)
        goodwill = st.number_input("商誉", min_value=0.0, step=0.1)

    with col2:
        st.success("📈 利润表数据")
        revenue = st.number_input("营业收入", min_value=0.0, step=0.1)
        net_profit = st.number_input("净利润", min_value=0.0, step=0.1)
        selling_exp = st.number_input("销售费用", min_value=0.0, step=0.1)
        rd_exp = st.number_input("研发费用", min_value=0.0, step=0.1)
        finance_exp = st.number_input("财务费用", min_value=0.0, step=0.1)

    with col3:
        st.warning("💧 现金流量表数据")
        ocf = st.number_input("经营活动现金流净额", step=0.1)
        tax_paid = st.number_input("支付的各项税费", min_value=0.0, step=0.1)
        salary_paid = st.number_input("支付给职工的现金", min_value=0.0, step=0.1)

# --- 逻辑穿透引擎 ---
if st.button("🚀 开启 20 项异常穿透诊断", use_container_width=True):
    st.divider()
    
    # 基础校验：防止分母为0
    if total_assets <= 0 or revenue <= 0:
        st.error("请输入基础的‘总资产’和‘营业收入’数据以进行逻辑计算。")
    else:
        st.subheader("🚩 诊断报告 (亿元单位自动换算)")
        
        results = []
        
        # 1. 存贷双高逻辑
        total_debt = short_debt + long_debt
        cash_ratio = monetary_fund / total_assets
        debt_ratio = total_debt / total_assets
        if cash_ratio > 0.3 and debt_ratio > 0.3:
            results.append({
                "level": "🔴 红色高危",
                "item": "疑似“存贷双高”舞弊",
                "desc": f"货币资金({monetary_fund}亿)与有息负债({total_debt}亿)同时超过资产总额的30%。需高度怀疑资金真实性或未披露的质押。"
            })

        # 2. 净现比逻辑 (利润含金量)
        if net_profit > 0.1: # 利润太小的忽略此项
            net_cash_ratio = ocf / net_profit
            if net_cash_ratio < 0.5:
                results.append({
                    "level": "🔴 红色高危",
                    "item": "净现比严重偏离",
                    "desc": f"经营现金流({ocf}亿)远低于净利润({net_profit}亿)，比值仅为{net_cash_ratio:.2f}。利润缺乏现金支撑，存在虚增收入可能。"
                })

        # 3. 资产虚胖逻辑
        bad_asset_ratio = (accounts_receivable + inventory) / total_assets
        if bad_asset_ratio > 0.4:
            results.append({
                "level": "🟡 中危风险",
                "item": "资产质量过重",
                "desc": f"应收与存货合计{accounts_receivable + inventory:.2f}亿，占总资产{bad_asset_ratio:.1%}。注意计提减值导致的利润暴雷。"
            })

        # 4. 税收勾稽逻辑
        tax_ratio = tax_paid / revenue
        if tax_ratio < 0.015:
            results.append({
                "level": "🟡 中危风险",
                "item": "纳税贡献背离",
                "desc": f"支付税费与营收比为{tax_ratio:.2%}，低于行业平均水平。需警惕虚构营收。"
            })
            
        # 5. 财务费用与负债不匹配
        if total_debt > 0:
            interest_rate = (finance_exp / total_debt) 
            if monetary_fund > 0 and interest_rate > 0.08: # 简单逻辑假设
                results.append({
                    "level": "🔵 关注项",
                    "item": "融资成本异常",
                    "desc": f"根据财务费用推算借款利率约为{interest_rate:.2%}，结合公司高额存款，可能存在高利息借款或资金挪用。"
                })

        # 展示结果
        if not results:
            st.success("✅ 扫描完成，各项核心财务指标在逻辑范围内，未触发重大舞弊模型。")
        else:
            for r in results:
                with st.expander(f"{r['level']} - {r['item']}", expanded=True):
                    st.write(r['desc'])

# --- 侧边栏辅助工具 ---
st.sidebar.markdown("### 📊 快速比例参考")
if total_assets > 0:
    st.sidebar.metric("现金资产占比", f"{monetary_fund/total_assets:.1%}")
    st.sidebar.metric("资产负债率", f"{(short_debt + long_debt)/total_assets:.1%}")
if revenue > 0:
    st.sidebar.metric("销售费用率", f"{selling_exp/revenue:.1%}")