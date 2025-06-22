import plotly.express as px
import plotly.offline as opy


class LineChartBuilder:
    """Creates a line chart from provided data.
    Data format:
    {
        'x': [list of x values],
        'y': [list of y values]
    }
    This class is used to build a line chart with specified title, x-axis label, and y-axis label.
    """

    def __init__(self, data, context, title=None, x_axis_label=None, y_axis_label=None):
        self.title = title
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.data = data
        self.context = context

    def build_chart(self):
        """Builds the line chart using Plotly Express."""
        fig = px.line(
            x=self.data["x"],
            y=self.data["y"],
            title=self.title,
            labels={"x": self.x_axis_label, "y": self.y_axis_label},
            markers=True,
        )

        # Set layout properties
        fig.update_layout(
            width=1000,
            height=800,
            font=dict(size=20, color="black", family="Arial, sans-serif"),
            template="plotly_white",
            xaxis=dict(
                showgrid=True,
                gridcolor="LightGray",
                tickangle=45,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="LightGray",
            ),
            plot_bgcolor="white",
        )

        self.context["line_chart"] = opy.plot(fig, auto_open=False, output_type="div")
        return self.context


def create_line_chart(
    context, qs, fields, title, x_axis_label="Date", y_axis_label="Value"
):
    """Function to create a line chart from a queryset by transforming queryset to the dictionary of keys 'X' and 'Y'."""

    data = list(qs.values_list(*fields))
    chart_data = {
        "x": [d[0] for d in data],
        "y": [d[1] for d in data],
    }

    chart = LineChartBuilder(
        data=chart_data,
        context=context,
        title=title,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
    )

    return chart.build_chart()
