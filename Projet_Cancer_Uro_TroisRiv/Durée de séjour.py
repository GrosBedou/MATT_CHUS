import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Charger les données
file_path = '/Users/abedard/Desktop/Excel recherche_2.xlsx'
df = pd.concat([
    pd.read_excel(file_path, sheet_name=0, engine="openpyxl"),
    pd.read_excel(file_path, sheet_name=1, engine="openpyxl")
], ignore_index=True)

# 2. Nettoyer les colonnes
# a. Durée séjour : extraire les chiffres (ex: "10 jours" → 10)
df['Durée séjour post-opération'] = (
    df['Durée séjour post-opération']
    .astype(str)
    .str.extract(r'(\d+)')  # extrait les chiffres
    .astype(float)
)

# b. Nettoyer la variable traitement
df['Chimio ou Pas'] = df['Chimio ou Pas'].str.lower().str.strip()
df = df[df['Chimio ou Pas'].isin(['chimio', 'non'])]

# 3. Garder les données valides
df_clean = df.dropna(subset=['Durée séjour post-opération'])

# 4. Statistiques globales
global_mean = df_clean['Durée séjour post-opération'].mean()
global_std = df_clean['Durée séjour post-opération'].std()
global_median = df_clean['Durée séjour post-opération'].median()
global_iqr = df_clean['Durée séjour post-opération'].quantile(0.75) - df_clean['Durée séjour post-opération'].quantile(0.25)

print(f"[GLOBAL] Moyenne : {global_mean:.2f} jours | Écart-type : {global_std:.2f}")
print(f"[GLOBAL] Médiane : {global_median:.1f} jours | IQR : {global_iqr:.1f}")

# 5. Statistiques par traitement
group_stats = df_clean.groupby('Chimio ou Pas')['Durée séjour post-opération'].agg([
    'count', 'mean', 'std', 'median',
    lambda x: x.quantile(0.75) - x.quantile(0.25)
])
group_stats.columns = ['n', 'moyenne', 'écart-type', 'médiane', 'IQR']
print("\n[PAR TRAITEMENT]")
print(group_stats.round(2))

# 6. Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_clean, x='Chimio ou Pas', y='Durée séjour post-opération', hue='Chimio ou Pas', palette='Set2', legend=False)
plt.title("Durée d'hospitalisation post-opératoire selon traitement", fontsize=16)
plt.xlabel("Traitement", fontsize=14)
plt.ylabel("Durée (jours)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("boxplot_duree_sejour_par_traitement.pdf", dpi=300)
plt.show()