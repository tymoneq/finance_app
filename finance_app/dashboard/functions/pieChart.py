import plotly.graph_objects as go
import plotly.offline as opy


class PieChartBuilder:
    """A class to build pie charts from budget and allocation data."""

    def __init__(self, amount, context):
        self.amount = amount
        self.labels = []
        self.values = []
        self.percentage_sum = 100
        self.context = context

    def add_allocation(self, label, percentage):
        self.percentage_sum -= percentage
        self.labels.append(label.capitalize())
        self.values.append(percentage / 100 * self.amount)

    def build_chart(self):
        if self.percentage_sum > 0:
            # Add an "Other" category if the percentages do not sum to 100%
            self.labels.append("Other")
            self.values.append(self.percentage_sum / 100 * self.amount)

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=self.labels,
                    values=self.values,
                    hoverinfo="label+percent+value",
                    textinfo="label+percent",
                )
            ],
            layout=go.Layout(
                width=1000,
                height=800,
                font=dict(size=20, color="black", family="Arial, sans-serif"),
            ),
        )

        self.context["chart"] = opy.plot(fig, auto_open=False, output_type="div")
        return self.context


def create_pie_chart_from_form(budget_form, formset, context):
    """Creates a pie chart based on the budget and allocation form data."""

    chart = PieChartBuilder(
        amount=int(budget_form.cleaned_data["money_amount"]), context=context
    )

    for form in formset:
        percentage = form.cleaned_data.get("percentage")
        if percentage:
            chart.add_allocation(
                label=form.cleaned_data.get("category"), percentage=percentage
            )

    if chart.percentage_sum < 0:
        context["error"] = "Total percentage cannot exceed 100%"
        return context

    return chart.build_chart()


def create_pie_chart_from_budget(context, amount):
    chart = PieChartBuilder(amount, context)

    for allocation in context["allocations"]:
        chart.add_allocation(
            label=allocation.category_name, percentage=allocation.percentage
        )
    return chart.build_chart()
