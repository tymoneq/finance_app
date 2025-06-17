import plotly.graph_objects as go
import plotly.offline as opy


def create_pie_chart(budget_form, formset, context):
    """Creates a pie chart based on the budget and allocation form data."""
    
    labels = []
    values = []
    percentage_sum = 100
    money_amount = int(budget_form.cleaned_data["money_amount"])

    for form in formset:
        percentage = form.cleaned_data.get("percentage")
        if percentage:
            percentage_sum -= percentage
            labels.append(form.cleaned_data.get("category").capitalize())
            values.append(percentage / 100 * money_amount)

    if percentage_sum < 0:
        context["error"] = "Total percentage cannot exceed 100%"
        return context

    if percentage_sum > 0:
        # Add an "Other" category if the percentages do not sum to 100%
        labels.append("Other")
        values.append(percentage_sum / 100 * money_amount)

    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, hoverinfo="label+percent+value", textinfo="label+percent")],
        layout=go.Layout(width=1000, height=800, font=dict(size=20, color="black", family="Arial, sans-serif")),
    )

    chart_html = opy.plot(fig, auto_open=False, output_type="div")
    context["chart"] = chart_html
    return context
