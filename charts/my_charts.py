import plotly.graph_objects as go

def create_chart():
    # Create figure
    fig = go.Figure()

    # Add trace
    fig.add_trace(
        go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1])
    )

    # Add images
    fig.add_layout_image(
            dict(
                source="https://images.plot.ly/language-icons/api-home/python-logo.png",
                xref="x",
                yref="y",
                x=0,
                y=3,
                sizex=2,
                sizey=2,
                sizing="stretch",
                opacity=0.5,
                layer="below")
    )

    # Set templates
    fig.update_layout(template="plotly_white")
    img_bytes = fig.to_image(format="png")
    # img_bytes = fig.to_image(format="png", width=600, height=350, scale=2)
    return img_bytes