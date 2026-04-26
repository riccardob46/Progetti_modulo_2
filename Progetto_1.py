import pandas as pd
import numpy as np

df = pd.read_csv("progetto_1.csv")

print("\nParte 1\n")

#Visualizzazione prime 3 righe ed info dataset
print(df.head(3))
print("\n", df.info())
print("\n", df.describe())

print("\nParte 2\n")

#Puliza dati, inserimento e gestione valori mancanti/nulli, conversione date
df["Prodotto"] = df["Prodotto"].str.strip().str.title()
df["Vendite"] = df["Vendite"].fillna(0)
df["Prezzo"] = df["Prezzo"].fillna(df.groupby("Prodotto")["Prezzo"].transform("median"))
df.drop_duplicates()
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
df["Vendite"] = df["Vendite"].astype(int)

print(f"Dataset dopo la pulizia:\n {df}")


print("\nParte 3\n")

#Calcolo vendite totali per prodotto, individuazione prodotto più/meno venduto, calcolo media vendite giornaliere
vendite_tot_x_prodotto = df.groupby("Prodotto")["Vendite"].sum().sort_values(ascending=False)
print(f"Vendite totali per prodotto: \n{vendite_tot_x_prodotto}")

print(f"\nIl prodotto più venduto è: {vendite_tot_x_prodotto.idxmax()}")
print(f"\nIl prodotto meno venduto è: {vendite_tot_x_prodotto.idxmin()}")

media_vendite_giornaliera = df.groupby("Data")["Vendite"].sum().mean()
print(f"\nMedia delle vendite giornaliere: \n{media_vendite_giornaliera}")