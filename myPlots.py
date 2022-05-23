import streamlit as st
import plotly.express as px
#https://towardsdatascience.com/a-clean-style-for-plotly-charts-250ba2f5f015

def show_plot(df, xaxis_name, column_name, plot_height):
    plot = px.line(
        data_frame=df,
        x=df[xaxis_name],
        y=column_name,
        title=f'<b>{column_name}</b>',
    )
    plot.update_layout(title_font_family="Arial Black", title_font_color="black", title_font_size=25)

    plot.update_layout(height=plot_height)
    plot.update_layout(
        margin=dict(l=0, r=0, t=40, b=0)
    )
    plot.update_layout(xaxis_title=xaxis_name)

    avg = df[column_name].mean()
    plot.add_hline(y=avg, line_width=1, line_dash="dash", line_color="red",
                   annotation_text="52-week average",
                   annotation_position="top right",
                   annotation_font_size=20,
                   annotation_font_color="red"
                   )

    st.plotly_chart(plot,use_container_width=True, height=plot_height)
