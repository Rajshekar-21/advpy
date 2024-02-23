import streamlit as st
import plotly.express as px
import pandas as pd

import warnings
import matplotlib.pyplot as plt

df = pd.read_csv("Housings.csv")

warnings.filterwarnings('ignore')

st.set_page_config(page_title="House Price", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: Housing Prices Data")

col1, col2 = st.columns((2))
st.sidebar.header("Choose your filter: ")

region = st.sidebar.multiselect("FURNISHING STATUS", df["furnishingstatus"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["furnishingstatus"].isin(region)]

state = st.sidebar.multiselect("PICK THE PRICE", df2["price"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["price"].isin(state)]
city = st.sidebar.multiselect("PICK THE AREA SIZE", df3["area"].unique())
if not city:
    df4 = df3.copy()
else:
    df4 = df3[df3["area"].isin(city)]

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["furnishingstatus"].isin(region)]
elif not region and not city:
    filtered_df = df[df["price"].isin(state)]
elif state and city:
    filtered_df = df4[df4["price"].isin(state) & df4["area"].isin(city)]
elif region and city:
    filtered_df = df4[df4["furnishingstatus"].isin(region) & df4["area"].isin(city)]
elif region and state:
    filtered_df = df4[df4["furnishingstatus"].isin(region) & df4["price"].isin(state)]
elif city:
    filtered_df = df4[df4["City"].isin(city)]
else:
    filtered_df = df4[df4["furnishingstatus"].isin(region) & df4["price"].isin(state) & df4["area"].isin(city)]

category_df = filtered_df.groupby(by=["bedrooms"], as_index=False)["stories"].sum()

with col1:
    st.subheader("BEDROOMS ,STORIES ")
    fig = px.bar(category_df, x="bedrooms", y="stories",
                 text=['{:,.2f}'.format(x) for x in category_df["stories"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("FURNISHING STATUS ")
    fig = px.pie(filtered_df, values="stories", names="furnishingstatus", hole=0.5)
    fig.update_traces(text=filtered_df["furnishingstatus"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="bedrooms.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

with cl2:
    with st.expander("furnishingstatus_ViewData"):
        region = filtered_df.groupby(by="furnishingstatus", as_index=False)["stories"].mean()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="furnishingstatus.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')
columns = st.columns((1))

for col in columns:
    with col:
        st.subheader("BATHROOMS ,PARKING ")
        fig = px.pie(filtered_df, values="bathrooms", names="parking", hole=0.5)
        fig.update_traces(text=filtered_df["parking"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

yes_no_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']

for column in yes_no_columns:
    df[column] = df[column].replace({'yes': True, 'no': False})

fig, ax = plt.subplots(figsize=(10, 6))
for i, column in enumerate(yes_no_columns):
    ax.bar(column, df[column].sum())
ax.set_title('Yes/No Data Bar Graph')
ax.set_xlabel('Features')
ax.set_ylabel('Count of Yes')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)