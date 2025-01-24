from django.shortcuts import render
import plotly.express as px
from .models import WaterQualityData
import pandas as pd
from django.http import JsonResponse
from django.utils.dateformat import format

from django.http import StreamingHttpResponse
import anomaly_queue as aq  # Import the shared queue
import json
import time


def dashboard_view(request):
    # Retrieve all data from WaterQualityData model
    data = WaterQualityData.objects.all().values(
        'timestamp', 'pH', 'turbidity', 'dissolved_oxygen', 'conductivity',
        'temperature', 'nitrate', 'phosphate', 'total_organic_carbon', 'chlorine',
        'ammonium', 'heavy_metals', 'fluoride', 'oxidation_reduction_potential',
        'biological_oxygen_demand'
    )
    df = pd.DataFrame(data)

    df = df.sort_values('timestamp')

    # Generate a time series chart for each parameter
    charts = {}
    parameters = [
        'pH', 'turbidity', 'dissolved_oxygen', 'conductivity', 'temperature',
        'nitrate', 'phosphate', 'total_organic_carbon', 'chlorine', 'ammonium',
        'heavy_metals', 'fluoride', 'oxidation_reduction_potential',
        'biological_oxygen_demand'
    ]

    for param in parameters:
        fig = px.line(df, x='timestamp', y=param, title=f'{param} over Time')
        charts[param] = fig.to_html(full_html=False)  # Convert Plotly figure to HTML

    return render(request, 'sensors/dashboard.html', {'charts': charts})


def sse_notifications_stream(request):
    """Generate notifications for SSE."""

    def event_stream():
        while True:
            try:
                # Retrieve anomalies from the queue
                anomaly = aq.get_next_item(10)
                # anomaly = anomaly_queue.get(timeout=10)  # Timeout to avoid hanging forever
                if anomaly is not None:
                    yield f"data: {json.dumps(anomaly)}\n\n"
                else:
                    # No anomalies, send a keep-alive message
                    yield f"data: Keep-alive at {time.time()}\n\n"
                time.sleep(1)  # Avoid busy-waiting
            except Exception as e:
                # Handle unexpected exceptions gracefully
                yield f"data: Error occurred: {str(e)}\n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


def get_chart_data(request):
    # Fetch the latest data from the database, you can set a limit if desired (e.g., 20 most recent records)
    data = WaterQualityData.objects.order_by('-timestamp')[:50]  # Latest 20 records
    data = data[::-1]  # Reverse to get ascending order by timestamp

    # Prepare data for each chart parameter
    chart_data = {
        "timestamp": [format(record.timestamp, 'Y-m-d H:i:s') for record in data],
        "pH": [record.pH for record in data],
        "turbidity": [record.turbidity for record in data],
        "dissolved_oxygen": [record.dissolved_oxygen for record in data],
        "conductivity": [record.conductivity for record in data],
        "temperature": [record.temperature for record in data],
        "nitrate": [record.nitrate for record in data],
        "phosphate": [record.phosphate for record in data],
        "total_organic_carbon": [record.total_organic_carbon for record in data],
        "chlorine": [record.chlorine for record in data],
        "ammonium": [record.ammonium for record in data],
        "heavy_metals": [record.heavy_metals for record in data],
        "fluoride": [record.fluoride for record in data],
        "oxidation_reduction_potential": [record.oxidation_reduction_potential for record in data],
        "biological_oxygen_demand": [record.biological_oxygen_demand for record in data],
    }

    return JsonResponse(chart_data)
