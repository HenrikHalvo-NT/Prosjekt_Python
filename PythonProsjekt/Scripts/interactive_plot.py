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

    # Hovedcontainer med to kolonner
    html.Div([
        # Venstre kolonne: graf og slider
        html.Div([
            html.Img(id='line-plot', style={'width': '100%', 'display': 'block', 'margin-bottom': '20px'}),
            dcc.RangeSlider(
                id='year-slider',
                min=min_year,
                max=max_year,
                step=1,
                value=[min_year, max_year],
                marks={str(year): str(year) for year in [1750, 1800, 1850, 1900, 1950, 2000, 2023]},
                tooltip={"placement": "bottom", "always_visible": True},
            )
        ], style={
            'width': '75%',           # Tar mest plass
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '10px',
            'margin-left': '20px'     # Litt pusterom fra venstre kant
        }),

        # Høyre kolonne: meny
        html.Div([
            html.H3("Meny"),
            html.Label("Velg drivstofftype:"),
            dcc.Dropdown(
                id='fuel-dropdown',
                options=[{'label': ft, 'value': ft} for ft in data['Fuel Type'].unique()],
                multi=True,
                placeholder="Velg en eller flere typer"
            ),
            html.Br(),
            html.Label("Vis Statistikk:"),
            dcc.Checklist(
                id='stats-checklist',
                options=[
                    {'label': 'Gjennomsnitt', 'value': 'mean'},
                    {'label': 'Maksimum', 'value': 'max'},
                    {'label': 'Minimum', 'value': 'min'}
                ],
                value=[]
            )
        ], style={
            'width': '20%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '20px',
            'margin-left': '10px',
            'border': '1px solid #ccc',
            'background-color': '#f9f9f9'
        })
    ], style={'display': 'flex', 'justify-content': 'flex-start'})  # Flex-container
])


# Callback for å oppdatere graf dynamisk
@app.callback(
    Output('line-plot', 'src'),
    [Input('year-slider', 'value'),
     Input('fuel-dropdown', 'value'),
     Input('stats-checklist', 'value')]
)


def update_graph(year_range, fuel_types, choice_of_stats):
    # Tekst til statistikken
    stats_text = []

    # Filtrer på år
    filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

    # Filtrer på drivstofftype
    if fuel_types and len(fuel_types) > 0:
        filtered_data = filtered_data[filtered_data['Fuel Type'].isin(fuel_types)]

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

    # Dersom statistikk er valgt, legg til tekst i grafen
    if choice_of_stats:
        for stat in choice_of_stats:
            if stat == 'mean':
                stats_text.append(f"Gj.snitt: {filtered_data['CO₂ Emissions'].mean():,.0f}")
            elif stat == 'max':
                stats_text.append(f"Maks: {filtered_data['CO₂ Emissions'].max():,.0f}")
            elif stat == 'min':
                stats_text.append(f"Min: {filtered_data['CO₂ Emissions'].min():,.0f}")

    
    plt.text(0.02, 0.95, "\n".join(stats_text), transform=plt.gca().transAxes,
                 fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))

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