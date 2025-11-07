import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from process_emissions import load_norway_emissions
import io
import base64

fil= r"C:\Users\henrikha\OneDrive - Nor Tekstil AS\Dokumenter\Python Studie\PythonProsjekt\PythonProsjekt\Data\co2-emissions-by-fuel-line\co2-emissions-by-fuel-line.csv"

# Last inn data
data = load_norway_emissions(fil)

# Opprett Dash-app (kunne ikke bruke streamlit på grunn av sikkerhet)
app = dash.Dash(__name__)
server = app.server # Hvis det skal deployes senere

# Velg min og max for intervall
min_year = int(data['Year'].min())
max_year = int(data['Year'].max())


# Layout app
app.layout = html.Div([
    html.H1("CO₂-utslipp i Norge per drivstofftype"),
    
    # Container for graf og slider
    html.Div([
        html.Img(id='line-plot', style={'width': '97%', 'display': 'block', 'margin': '0 auto'}),
        dcc.RangeSlider(
            id='year-slider',
            min=min_year,
            max=max_year,
            step=1,
            value=[min_year, max_year],
            marks = {str(year): str(year) for year in [1750, 1800, 1850, 1900, 1950, 2000, 2023]},
            tooltip={"placement": "bottom", "always_visible": True},
        )
    ], style={'width': '80%', 'margin': '0 auto'})  # Samme bredde som grafen
])



# Callback for å oppdatere grafen dynamisk
@app.callback(
    Output('line-plot', 'src'),
    Input('year-slider', 'value')
)

def update_graph(year_range):
    filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

    
    # Lag figur med Seaborn
    plt.figure(figsize=(12, 7))
    sns.lineplot(
        data=filtered_data,
        x="Year",
        y="CO₂ Emissions",
        hue="Fuel Type",
        marker="o"
    )
    plt.title(f"CO₂-utslipp i Norge per drivstofftype ({year_range[0]}–{year_range[1]})")
    plt.ylabel("CO₂-utslipp (tonn)")
    plt.xlabel("År")
    plt.legend(title="Drivstofftype")
    plt.tight_layout()

    
    # Konverter figur til base64 for visning i Dash
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{encoded}"

if __name__ == '__main__':
    app.run(debug=True)