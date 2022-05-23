import streamlit as st
import pandas as pd
import myPlots
#from streamlit_option_menu import option_menu

import os
import os.path as path
import time

import investpy
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

def blank_line(numLines):
    for i in range(numLines):
        st.text("")

# create plots
def show_plot(kind: str):
    if kind == "Plotly Express":
        plot = plotly_plot(chart_type, df)
        plot.update_layout(height=1200)
        plot.update_traces(textposition='top center')

        st.plotly_chart(plot, use_container_width=True,height=1200)

    elif kind == "Altair":
        plot = altair_plot(chart_type, df)
        st.altair_chart(plot, use_container_width=True)


def is_file_older_than_x_seconds(file, seconds=60):
    file_time = path.getmtime(file)
    if ((time.time() - file_time) < seconds):
        return False
    else:
        return True

def is_file_older_than_x_seconds(file, seconds=60):
    file_time = path.getmtime(file)
    if ((time.time() - file_time) < seconds):
        return False
    else:
        return True


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
#st.sidebar.markdown('<p class="sidebarHeader"><span style=\"color: #ea4335\">boontu</span></p>', unsafe_allow_html=True)
#st.sidebar.write("")

st.sidebar.markdown('<p class="sidebarHeader">'
                    '<span style=\"color: #ea4335\">boontu</span>'
                    '</p>', unsafe_allow_html=True)

selected = st.sidebar.radio("Menu", ["Dollars", "DeepStock"])

st.sidebar.write("""
## Disclaimer
I don’t make any recommendations about buying/selling particular stocks. I think the price changes in the past don't tell us the price changes in the future. 

Here is a famous quote from Mark Twain.
>    “October. This is one of the peculiarly dangerous months to speculate in stocks. The others are July, January, September, April, November, May, March, June, December, August, and February.”

""")

# =====================================================================================
# Main
# =====================================================================================
if(selected == "Dollars"):
    st.markdown('<p class="sectionHeader">Investing in US Dollars</br></p>', unsafe_allow_html=True)
    st.info("Dollar Gap = US Dollar Index / US Dollar Korean Won * 100")
    blank_line(3)


    if(is_file_older_than_x_seconds('./dollar.csv',60*60)):
        with st.spinner('Retrieving the data from the server...'):
            date_end = (datetime.now() - relativedelta(days=1))
            date_begin = datetime.now() - relativedelta(weeks=52)
            date_begin = date_begin.strftime("%d/%m/%Y")
            date_end = date_end.strftime("%d/%m/%Y")
            date_begin = str(date_begin)
            date_end = str(date_end)

            # ====================================
            # US Dollar Korean Won
            # ====================================
            search_result = investpy.search_quotes(text="US Dollar Korean Won", countries=['south korea'], n_results=1)
            recent_data = search_result.retrieve_historical_data(from_date=date_begin, to_date=date_end)
            recent_data = recent_data.reset_index()
            df_result = recent_data[['Date', 'Close']].copy()
            df_result.rename(columns={'Close': 'USD/KRW'}, inplace=True)

            # ====================================
            # US Dollar Index
            # ====================================
            search_result = investpy.search_quotes(text='US Dollar Index', products=['indices'],
                                                   countries=['united states'], n_results=1)
            recent_data = search_result.retrieve_historical_data(from_date=date_begin, to_date=date_end)
            recent_data = recent_data.reset_index()
            USDIndex = recent_data[['Date', 'Close']].copy()
            USDIndex.rename(columns={'Close': 'USD Index'}, inplace=True)

            # ====================================
            # Merge and Save
            # ====================================
            df_result = pd.merge(left=df_result, right=USDIndex, how="inner", on="Date")
            df_result["Dollar Gap"] = df_result["USD Index"] / df_result["USD/KRW"] * 100.0
            df_result.to_csv("./dollar.csv", index=False)
            # ===================================================================================


    # ===================================================================================
    df_data = load_data('./dollar.csv')

    blank_line(2)
    st.write("last modified: %s" % time.ctime(os.path.getmtime('./dollar.csv')))
    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    col1.header("USD/KRW")
    colName = "USD/KRW"
    valMean = df_data[colName].mean()
    valNow = df_data[colName].iloc[-1]
    valDiff = valNow - valMean
    col1.metric("Today", "%.2f KRW" % valNow, "%.2f" % valDiff, delta_color="inverse")
    col1.metric("52-week average", "%.2f KRW" % df_data[colName].mean(), None,)


    col2.header("US Dollar Index")
    colName = "USD Index"
    valMean = df_data[colName].mean()
    valNow = df_data[colName].iloc[-1]
    valDiff = valNow - valMean
    col2.metric("Today", "%.2f" % valNow, "%.2f" % valDiff, delta_color="inverse")
    col2.metric("52-week average", "%.2f" % df_data[colName].mean(), None,)


    col3.header("US Dollar Gap")
    colName = "Dollar Gap"
    valMean = df_data[colName].mean()
    valNow = df_data[colName].iloc[-1]
    valDiff = valNow - valMean
    col3.metric("Today", "%.2f" % valNow, "%.2f" % valDiff, delta_color="inverse")
    col3.metric("52-week average", "%.2f" % df_data[colName].mean(), None,)

    st.markdown("---")
    blank_line(3)

    myPlots.show_plot(df_data, "Date", "USD/KRW", 300)
    myPlots.show_plot(df_data, "Date", "USD Index", 300)
    myPlots.show_plot(df_data, "Date", "Dollar Gap", 300)



elif(selected == "DeepStock"):
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












