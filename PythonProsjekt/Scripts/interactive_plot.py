import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from process_emissions import load_norway_emissions

fil= r"C:\Users\henrikha\OneDrive - Nor Tekstil AS\Dokumenter\Python Studie\PythonProsjekt\PythonProsjekt\Data\co2-emissions-by-fuel-line\co2-emissions-by-fuel-line.csv"

# Last inn data
data = load_norway_emissions(fil)

# Velg år-intervall med slider
min_year = int(data['Year'].min())
max_year = int(data['Year'].max())
year_range = st.slider("Velg periode", min_year, max_year, (min_year, max_year))

# Filtrer data etter periode
filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

# Lag linjediagram med Seaborn
plt.figure(figsize=(12, 7))
sns.lineplot(
    data=filtered_data, 
    x = "Year",
    y = "CO₂ Emissions",
    hue = "Fuel Type",
    marker = "o"
)

plt.title(f"CO₂-utslipp i Norge per drivstofftype ({year_range[0]}–{year_range[1]})")
plt.ylabel("CO₂-utslipp (tonn)")
plt.xlabel("År")
plt.legend(title="Drivstofftype")
plt.tight_layout()
st.pyplot()


# Lagre figuren i en variabel og send den til Streamlit
fig = plt.gcf()
st.pyplot(fig)
plt.close(fig)
