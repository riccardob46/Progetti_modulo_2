import pandas as pd
import numpy as np
from datetime import date

# +++++++++++++++++++++++++++++++++++++++++++++ PARTE 1 +++++++++++++++++++++++++++++++++++++++++++++

n_ordini = 100_000
ordini = pd.DataFrame({
    "ClienteID": np.random.randint(1, 5001, n_ordini),
    "ProdottoID": np.random.randint(1, 21, n_ordini),
    "Quantità": np.random.randint(1, 50, n_ordini),
    "DataOrdine": pd.to_datetime(np.random.choice(pd.date_range('2025-01-01', '2025-12-31'), n_ordini))
})
ordini.to_csv("ordini_progetto_2.csv", index=False)


n_prodotti = 20
prodotti = pd.DataFrame({
        "ProdottoID": np.random.randint(1, 21, n_prodotti),
        "Categoria": np.random.choice(['Elettronica', 'Casa', 'Abbigliamento', 'Sport'], size=n_prodotti),
        "Fornitore": [f"Fornitore_{i}" for i in np.random.randint(1, 6, size=n_prodotti)],
        "Prezzo": np.round(np.random.uniform(10.0, 500.0, size=n_prodotti), 2)
})
prodotti.to_json("prodotti_progetto_2.json", index=False)

n_clienti = 5_000
clienti = pd.DataFrame({
    "ClienteID": np.random.randint(1, 5001, size=n_clienti),
    "Regione": np.random.choice(["Nord", "Centro", "Sud", "Isole"], n_clienti),
    "Segmento": np.random.choice (["Retail", "Corporate", "Premium"], n_clienti)
})
clienti.to_csv("clienti_progetto_2.csv", index=False)

# +++++++++++++++++++++++++++++++++++++++++++++ PARTE 2 +++++++++++++++++++++++++++++++++++++++++++++
df_ordini = pd.read_csv("ordini_progetto_2.csv")
df_prodotti = pd.read_json("prodotti_progetto_2.json")
df_clienti = pd.read_csv("clienti_progetto_2.csv")

#Unione DF
df_finale = df_ordini.merge(df_prodotti, on="ProdottoID").merge(df_clienti, on="ClienteID")

print("\nInfo DataFrame Originale: ", df_finale.info(memory_usage="deep"))

# +++++++++++++++++++++++++++++++++++++++++++++ PARTE 3 +++++++++++++++++++++++++++++++++++++++++++++
#Ottimizzazione DF
df_finale["ClienteID"] = pd.to_numeric(df_finale["ClienteID"], downcast="integer")
df_finale["ProdottoID"] = pd.to_numeric(df_finale["ProdottoID"], downcast="integer")
df_finale["Quantità"] = pd.to_numeric(df_finale["Quantità"], downcast="integer")
df_finale["DataOrdine"] = pd.to_datetime(df_finale["DataOrdine"])
df_finale["Categoria"] = df_finale["Categoria"].astype("category")
df_finale["Fornitore"] = df_finale["Fornitore"].astype("category")
df_finale["Regione"] = df_finale["Regione"].astype("category")
df_finale["Segmento"] = df_finale["Segmento"].astype("category")
df_finale["Prezzo"] = df_finale["Prezzo"].round(2).astype("float32")

pd.options.display.float_format = "{:.2f}".format #per vedere massimo 2 cifre decimali nel DF

print("\nInfo DataFrame Ottimizzato", df_finale.info(memory_usage="deep"))

# +++++++++++++++++++++++++++++++++++++++++++++ PARTE 4 +++++++++++++++++++++++++++++++++++++++++++++
#Creazione colonna valore totale
df_finale["ValoreTotale"] = df_finale["Prezzo"] * df_finale["Quantità"]

print (df_finale.head(5))

#Filtro ValoteTotale > 100 e cliente specifico Premium
df_filtrato = df_finale[(df_finale["ValoreTotale"] > 100) & (df_finale["Segmento"] == "Premium")]

print("\nDataFrame Filtrato: \n", df_filtrato.head(5))
