import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# --- PREPARAZIONE DATASET (Stessa logica di prima) ---
def create_dataset():
    np.random.seed(42)
    data = []
    categories = {'Furniture': ['Chairs', 'Tables'], 'Technology': ['Phones', 'Machines']}
    states = ['California', 'Texas', 'New York', 'Florida', 'Illinois']
    
    for i in range(100):
        cat = np.random.choice(list(categories.keys()))
        sub_cat = np.random.choice(categories[cat])
        order_date = datetime(2022, 1, 1) + timedelta(days=np.random.randint(0, 730))
        sales = np.random.uniform(100, 1500)
        profit = sales * np.random.uniform(-0.1, 0.3)
        data.append([order_date.strftime('%Y-%m-%d'), cat, sub_cat, sales, profit, np.random.choice(states)])
    
    return pd.DataFrame(data, columns=['Order Date', 'Category', 'Sub-Category', 'Sales', 'Profit', 'State'])

df = create_dataset()

# --- PARTE 1: PULIZIA DATI ---
# 1. Conversione date
df['Order Date'] = pd.to_datetime(df['Order Date'])

# 2. Controllo nulli e duplicati
df = df.drop_duplicates().fillna(0)

# 3. Creazione colonna Year
df['Year'] = df['Order Date'].dt.year


# --- PARTE 2: ANALISI ESPLORATIVA (EDA) ---
# Impostiamo lo stile di Seaborn
sns.set_theme(style="whitegrid")

# Creiamo una figura con più sotto-grafici (Subplots)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Analisi Vendite e Redditività Store Online', fontsize=20)

# 4. Totale vendite e profitti per anno
yearly_data = df.groupby('Year')[['Sales', 'Profit']].sum().reset_index()
# Trasformiamo in formato long per Seaborn
yearly_long = yearly_data.melt(id_vars='Year', var_name='Metrica', value_name='Valore')

sns.barplot(data=yearly_long, x='Year', y='Valore', hue='Metrica', ax=axes[0, 0])
axes[0, 0].set_title('Vendite e Profitto Totale per Anno')

# 5. Top 5 sottocategorie più vendute
top_sub = df.groupby('Sub-Category')['Sales'].sum().nlargest(5).reset_index()
sns.barplot(
    data=top_sub, 
    x='Sales', 
    y='Sub-Category', 
    hue='Sub-Category', # Assegniamo la variabile y anche a hue
    palette='viridis', 
    legend=False,       # Togliamo la legenda che sarebbe ridondante
    ax=axes[0, 1]
)
axes[0, 1].set_title('Top 5 Sottocategorie per Vendite')

# 6. Distribuzione Vendite per Stato (Sostituto della mappa)
# Matplotlib/Seaborn non gestiscono mappe geografiche senza librerie esterne (come Geopandas).
# Lo standard è usare un grafico a barre per confrontare le regioni.
state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=False).reset_index()
sns.barplot(
    data=state_sales, 
    x='Sales', 
    y='State', 
    hue='State',        # Assegniamo la variabile y anche a hue
    palette='magma', 
    legend=False,       # Togliamo la legenda
    ax=axes[1, 0]
)
axes[1, 0].set_title('Vendite per Stato')

# Grafico Extra: Relazione Vendite/Profitto (Scatter Plot)
sns.scatterplot(data=df, x='Sales', y='Profit', hue='Category', style='Category', s=100, ax=axes[1, 1])
axes[1, 1].set_title('Correlazione Vendite vs Profitto')

# Ottimizzazione layout e mostriamo i grafici
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()