import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Saving Advisor", layout="wide")
st.title("AI Personal Saving Advisor")
st.markdown("Analyze your financial habits and receive inteligent,data driven advice.")
st.divider()

with st.sidebar:
    st.header("Financial Inputs")
    income = st.number_input("Monthly Net Income(Rs.)", min_value=0, value=50000, step=1000)

    st.subheader("Monthly Expenses")
    needs = st.number_input("Needs(Rent,Groceries,Bills)", min_value=0, value=25000)
    wants = st.number_input("wants(Dinning,Movies,Hobbies)", min_value=0, value=15000)
    savings = st.number_input("Savings/SIP", min_value=0, value=10000)

    st.divider()
    total_existing_savings = st.number_input("Emergency Fund (Total Savings)", min_value=0, value=50000)

total_expenses = needs + wants
remaining_balance = income - total_expenses - savings

# Logic combined from the provided video frame[cite: 2]
actual_savings_rate = (savings / income) * 100 if income > 0 else 0
wants_ratio = (wants / income) * 100 if income > 0 else 0
needs_ratio = (needs / income) * 100 if income > 0 else 0

monthly_expenses_avg = total_expenses
emergency_fund_months = total_existing_savings / monthly_expenses_avg if monthly_expenses_avg > 0 else 0

score = 100
if actual_savings_rate < 20:
    score -= 30
if wants_ratio > 30:
    score -= 20
if emergency_fund_months < 6:
    score -= 30
score = max(score, 0)

def get_level(score):
    if score >= 80:
        return "Healthy", "success"
    elif score >= 50:
        return "Moderate", "warning"
    else:
        return "Critical", "error"

level_text, level_type = get_level(score)

row1_col1, row1_col2 = st.columns([1,1])
with row1_col1:
    st.subheader("Intelligent Report")
    m1, m2 = st.columns(2)
    m1.metric("Score", f"{score}/100")
    m2.metric("Buffer", f"{emergency_fund_months:.1f} Months")

    if level_type == "success":
        st.success(f"Status: {level_text}")
    elif level_type == "warning":
        st.warning(f"Status: {level_text}")
    else:
        st.error(f"Status: {level_text}")

    rules = [
        {
            "name": "Emergency Fund",
            "check": lambda: emergency_fund_months < 6,
            "message": f"Aim for 6 months backup"
        },
        {
            "name": "Saving Rate",
            "check": lambda: actual_savings_rate<20,
            "message": f"Increasing saving to 20%."
        },
        {
            "name": "Wants Control",
            "check": lambda: wants_ratio >30,
            "message": f"Reduce wants below 30%"
        }
    ]
    advice_output = ""

    for rule in rules:
        if rule["check"]:
            st.info(f"**{rule['name']}** : {rule['message']}")
            advice_output += f"- {rule['name']}:{rule['message']}\n"
with row1_col2:
    st.subheader("Spending Breakdown")
    df_plot = pd.DataFrame({"Category": ["Needs", "Wants", "Savings"], "Amount": [needs, wants, savings]})
    fig = px.pie(df_plot, values="Amount", names="Category", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel,height=300)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

st.divider()
row2_col1, row2_col2 = st.columns([1, 1])

with row2_col1:
    st.subheader("50/30/20 Rule Comparison")
    comparison_data = {
        "Category": ["Needs", "Wants", "Savings"],
        "Current %": [round(needs_ratio, 1), round(wants_ratio, 1), round(actual_savings_rate, 1)],
        "Target %": [50, 30, 20]
    }
    st.table(pd.DataFrame(comparison_data))

with row2_col2:
    st.subheader("Wealth Projection (10 Yrs)")
    new_saving = st.slider("Adjust Monthly Saving Rs", 0, int(income), int(savings))

    monthly_r = 0.10 / 12
    months = 120
    projected_wealth=new_saving*(((1+monthly_r)**months-1)/monthly_r)*(1+monthly_r)
    st.metric("Future Wealth potential",f"Rs.{int(projected_wealth):,}")
    st.caption("Estimated at 10% annual returns.")
st.divider()
st.subheader("Download Your Financial PLan")

report_text = f"""
AI SAVINGS ADVISOR REPORT
Score: {score}/100 | Status: {level_text}
Monthly Income: ₹{income}
Breakdown: Needs {needs_ratio}%, Wants {wants_ratio}%, Savings {actual_savings_rate}%
Advice:
{advice_output if advice_output else "Everything looks great!"}
"""

st.download_button(
    label="Click here to Download Report",
    data=report_text,
    file_name="financial_report.txt",
    mime="text/plain",
    use_container_width=True
)

st.info("Pro Tip: Reduce 'Wants' first before cutting 'Needs' to improve your health")







