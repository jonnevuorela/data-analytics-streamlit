import streamlit as st
import pandas as pd

URL_ROVANIEMI: str = "https://pxdata.stat.fi/PxWeb/sq/6b01cc5a-aa07-4026-b5eb-1221a143f4ef"
URL_KITTILA: str = "https://pxdata.stat.fi/PxWeb/sq/dad977b4-ad69-4156-9b12-07dd3cac34c6"


@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url)


rovaniemi: pd.DataFrame = load_data(URL_ROVANIEMI)
kittila: pd.DataFrame = load_data(URL_KITTILA)

metrics: list[str] = [c for c in rovaniemi.columns if c != 'Month']

st.title("Lapland Hotel Stats")

metric: str = st.selectbox("Metric", metrics)

st.subheader("Data Rovaniemi")
st.dataframe(rovaniemi[['Month', metric]], width='stretch')

st.subheader(f"Monthly trend: {metric}")
st.line_chart(rovaniemi, x='Month', y=metric)

st.markdown(
    "December is clearly the peak month every year. Summer months are quieter."
)

nights_col: str = [c for c in metrics if 'Nights spent' in c][0]
yearly: pd.Series = rovaniemi.groupby(rovaniemi['Month'].str[:4].astype(int))[nights_col].sum()
st.subheader("Yearly nights spent")
st.bar_chart(yearly)

st.markdown(
    "Covid hit hard in 2020, nights spent dropped by half. Took until 2023 to get back to 2019 levels."
)

domestic_col: str = [c for c in metrics if 'Domestic nights' in c][0]
foreign_col: str = [c for c in metrics if 'Foreign nights' in c][0]
domestic_foreign: pd.DataFrame = rovaniemi[['Month', domestic_col, foreign_col]].set_index('Month')
st.subheader("Domestic vs Foreign nights")
st.dataframe(domestic_foreign, width='stretch')
st.line_chart(domestic_foreign)

st.markdown(
    "Foreign visitors dominate in winter months Dec-Feb, while domestic tourism \
    leads in summer and early autumn. The pandemic nearly eliminated foreign nights in 2020-2021."
)

metric_suffix: str = metric.split(maxsplit=1)[1]
kittila_metric: str = f"Kittilä {metric_suffix}"
compare: pd.DataFrame = pd.DataFrame({
    'Month': rovaniemi['Month'],
    'Rovaniemi': rovaniemi[metric].values,
    'Kittilä': kittila[kittila_metric].values
}).set_index('Month')
st.subheader(f"Rovaniemi vs Kittilä: {metric_suffix}")
st.line_chart(compare)

st.markdown(
    "Rovaniemi has higher absolute numbers across all metrics due to its larger hotel capacity.\
    Kittilä shows a similar seasonal pattern but with steeper winter peaks relative to its size."
    )

st.download_button(
    "Download comparison CSV",
    compare.to_csv(),
    "comparison.csv",
    mime="text/csv"
)
