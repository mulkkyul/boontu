import plotly.express as px
#This code was copied from https://github.com/discdiver/data-viz-streamlit/blob/main/app.py

def plotly_plot(chart_type: str, df):
    if chart_type == "Scatter":
        fig = px.scatter(
            data_frame=df,
            x="pb1",
            y="pb2",
            color="market",
            text="code",
        )
    elif chart_type == "Line":
        fig = px.line(
            data_frame=df,
            x="date",
            y="price",
            color="code"
        )

    return fig
