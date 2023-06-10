import sqlite3

import plotly.graph_objects as graph_objects


def fetch_data(query):
    """Fetch the data from SQLite3 database based on provided query

    Args:
        query (string): The sql query to execute

    Returns:
        list: list of the row fetched from the database according the query
    """
    # Establish a connection to the SQLite database
    connection = sqlite3.connect("data.db")

    # Create a cursor object to execute SQL statements
    cursor = connection.cursor()

    # Execute the SQL query
    cursor.execute(query)

    # Fetch all the rows returned by the query
    rows = cursor.fetchall()

    # Close the database connection
    connection.close()
    return rows


def generategraph(x_axis_data, y_axis_data, names,x_axis,y_axis):
    """
    Generate an interactive scatter plot graph using the provided data.

    Args:
        x_axis (list): The x-axis data.
        y_axis (list): The y-axis data.
        names (list): The names associated with each data point.

    Returns:
        str: The HTML string representing the graph.
    """
    # Create a new figure object
    fig = graph_objects.Figure()

    # Add a scatter plot trace for the markers and text labels
    fig.add_trace(
        graph_objects.Scatter(
            x=x_axis_data,
            y=y_axis_data,
            mode="markers+text",
            text=names,
            hoverinfo="text",
            textposition="top center",
        )
    )
    # Add a scatter plot trace for the lines
    fig.add_trace(
        graph_objects.Scatter(
            x=x_axis_data,
            y=y_axis_data,
            mode="lines",
            line=dict(color="blue", width=2),
            showlegend=False,
        )
    )

    # Set layout options
    fig.update_layout(
        title="Scatter Plot",
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        width=400,  # Set the width of the graph
        height=300,  # Set the height of the graph
        plot_bgcolor="rgba(0,0,0,0)",  # Set the plot background color to transparent
        paper_bgcolor="rgba(0,0,0,0)",  # Set the paper (outer) background color to transparent
        margin=dict(l=50, r=50, t=50, b=50),  # Set the margin around the graph
    )

    # Save the plot as an HTML string
    return fig.to_html(full_html=False)
