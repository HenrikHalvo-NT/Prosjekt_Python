import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fillokasjon for datasett
fil= r"C:\Users\henrikha\OneDrive - Nor Tekstil AS\Dokumenter\Python Studie\PythonProsjekt\PythonProsjekt\Data\co2-emissions-by-fuel-line\co2-emissions-by-fuel-line.csv"

# Funksjon som laster datasettet slik at jeg kan bruke det dynamisk senere
def load_norway_emissions(fil):
    df = pd.read_csv(fil)
    norway_df = df[df['Entity'] == 'Norway']
    melted_df = norway_df.melt(
        id_vars=['Year'],
        value_vars=[
        
            'Annual CO₂ emissions from oil',
            'Annual CO₂ emissions from coal',
            'Annual CO₂ emissions from cement',
            'Annual CO₂ emissions from gas',
            'Annual CO₂ emissions from flaring',
            'Annual CO₂ emissions from other industry'
        ],
        var_name='Fuel Type',
        value_name='CO₂ Emissions'
   
    )  
    melted_df.dropna(subset=['CO₂ Emissions'], inplace=True)
    melted_df['Year'] = pd.to_numeric(melted_df['Year'], errors='coerce')
    return melted_df




# Funksjon for å plotte utslipp i Norge fra år 1750 frem til valgt år
def plot_emissions_until_year(max_year):
    mdf = load_norway_emissions(fil)
    data = mdf[mdf['Year'] <= max_year]
    plt.figure(figsize=(12, 7))
    sns.lineplot(
        data=data,
        x='Year',
        y='CO₂ Emissions',
        hue='Fuel Type',
        marker='o'
    )
    plt.title(f'CO₂-utslipp i Norge per drivstofftype (1750–{max_year})')
    plt.ylabel('CO₂-utslipp (tonn)')
    plt.xlabel('År')
    plt.legend(title='Drivstofftype')
    plt.tight_layout()
    plt.show()


# Eksempel: Lag en graf for 2020
#plot_emissions_until_year(2020)