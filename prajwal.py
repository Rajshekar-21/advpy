import pandas as pd
import streamlit as st
import plotly.express as px

dataset=pd.read_excel('FinancialData.xlsx')

st.set_page_config(page_title="Financial Data",layout="wide")

st.sidebar.header("Filter By: ")

category=st.sidebar.multiselect("Filter By Category:",
                                options=dataset["business_unit"].unique(),
                                default=dataset["business_unit"].unique())

selection_query=dataset.query(
    "business_unit== @category"
)

st.title("Business Dashboard")

total_profit=(selection_query["Total"].sum())
avg_rating=round((selection_query["Rating"].mean()),2)

first_column,second_column=st.columns(2)

with first_column:
    st.markdown("### Total amount:")
    st.subheader(f'{total_profit} $')
with second_column:
    st.markdown("### AVG Products Rating")
    st.subheader(f'{avg_rating}')

st.markdown("---")

st.subheader("Data representation based on business unit")

profit_by_category=(selection_query.groupby(by=["business_unit"]).sum()[["Total"]])

profit_by_category_barchart=px.bar(profit_by_category,
                                   x="Total",
                                   y=profit_by_category.index,
                                   title="Profit By Category",
                                   color_discrete_sequence=["#17f50c"],
                                   )
profit_by_category_barchart.update_layout(plot_bgcolor = "rgba(0,0,0,0)",xaxis=(dict(showgrid=False)))


profit_by_category_piechart=px.pie(profit_by_category, names= profit_by_category.index,values= "Total",title="Profit % By Category",hole=.3,color=profit_by_category.index,color_discrete_sequence=px.colors.sequential.RdPu_r)


left_column,right_column=st.columns(2)
left_column.plotly_chart(profit_by_category_barchart,use_container_width=True)
right_column.plotly_chart(profit_by_category_piechart,use_container_width=True)

hide= """
   <style>
   #MainMenu {visibility:hidden;}
   footer {visibility:hidden;}
   header {visibility:hidden}
   </style>
"""
st.markdown(hide,unsafe_allow_html=True)