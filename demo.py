import streamlit as st
import pandas as pd
from make_plots import (
    plotly_plot,
)

# =====================================================================================
# Page setup
# =====================================================================================
st.set_page_config(layout='wide',initial_sidebar_state='expanded',page_title="boontu - financial timeseries analysis")
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
<style>
.week {
    font-size:35px !important;
     color :#C7BACC !important;
   font-family: 'Roboto', sans-serif;
   font-weight: bold;
}
.sidebarHeader {
    font-size:35px !important;
     color :#000000 !important;
    font-family: 'Roboto', sans-serif;
    font-weight: bold;
}
.sectionHeader {
    font-size:40px !important;
    color: #4285f4 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# create plots
def show_plot(kind: str):
    if kind == "Plotly Express":
        plot = plotly_plot(chart_type, df)
        plot.update_layout(height=1200)
        plot.update_traces(textposition='top center')

        st.plotly_chart(plot, use_container_width=True,height=1200)

    elif kind == "Altair":
        plot = altair_plot(chart_type, df)
        #plot.update_layout(height=1200)
        #plot.update_traces(textposition='top center')
        st.altair_chart(plot, use_container_width=True)



# =====================================================================================
# Load data
# =====================================================================================
@st.cache
def load_data(filename):
    df = pd.read_csv(filename, header=0, delimiter=',')
    return df



# =====================================================================================
# Sidebar
# =====================================================================================
st.sidebar.markdown('<p class="sidebarHeader">'
                    '<span style=\"color: #ea4335\">boontu</span>'
                    '</p>', unsafe_allow_html=True)
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")

st.sidebar.write("""
## Disclaimer
I don’t make any recommendations about buying/selling particular stocks. I think the price changes in the past don't tell us the price changes in the future. 

Here is a famous quote from Mark Twain.
>    “October. This is one of the peculiarly dangerous months to speculate in stocks. The others are July, January, September, April, November, May, March, June, December, August, and February.”

""")

# =====================================================================================
# Main
# =====================================================================================
st.markdown('<p class="sectionHeader">Stock Representation</br></p>', unsafe_allow_html=True)
st.info("The closer, the similar price changes. The stock price data collected between Mar - Aug 2020 was used in the analysis. "
        "Please see https://arxiv.org/abs/2007.06848 and https://mulkkyul.github.io/2020/07/20/deep-stock/ for details")

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
list_region = ['ALL','index','sp500','kospi']
market = st.radio("MARKET", options=list_region)

df_representation = load_data('./data/vis1.csv')
if(not market == "ALL"):
    df_target = df_representation[df_representation["market"] == market]
else:
    df_target = df_representation



chart_type = "Scatter"
df = df_target
show_plot(kind="Plotly Express")


st.markdown('<p class="sectionHeader">Similarity Analysis</br></p>', unsafe_allow_html=True)
df_representation = load_data('./data/target-005930-market-kospi.csv')
df = df_representation
chart_type = "Line"
#st.markdown('<p class="sectionHeader"><span style=\"font-size: 60% ; color: blue\">Target: Samsung Electronics (KR.0005930)</span></p>', unsafe_allow_html=True)
st.info("The price changes of 5 stocks that were most similar to that of Samsung Electronics (KR.0005930) are shown.")
show_plot(kind="Plotly Express")



st.markdown('<p class="sectionHeader"><span style=\"color: #000000\">Feature Roadmap</span></br></p>', unsafe_allow_html=True)
st.warning("This was just to test my idea about finding similar stocks. The following features will be added later for convenience.")
st.markdown('- [ ] Displaying company names, instead of their codes', unsafe_allow_html=True)
st.markdown('- [ ] Search box (for finding the target stock and its neighboring stocks)', unsafe_allow_html=True)
st.markdown('- [ ] Pretty plot - e.g. industry for color coding', unsafe_allow_html=True)
st.markdown('- [ ] Update the stock data', unsafe_allow_html=True)
st.markdown('- [ ] Add other financial data such as gold, gas, futures...', unsafe_allow_html=True)












