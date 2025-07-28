import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from lifelines.plotting import add_at_risk_counts
from matplotlib.ticker import FuncFormatter

# Charger les données
file_path = '/Users/abedard/Desktop/Excel recherche_2.xlsx'
df = pd.concat([
    pd.read_excel(file_path, sheet_name=0, engine="openpyxl"),
    pd.read_excel(file_path, sheet_name=1, engine="openpyxl")
], ignore_index=True)

# Nettoyage des dates
df['Date de la chirurgie'] = pd.to_datetime(df['Date de la chirurgie'], errors='coerce')
df['Date de décès'] = pd.to_datetime(df['Date de décès'], errors='coerce')

# 🎯 Filtrer les patients opérés avant le 1er juillet 2019
# date_limite = pd.Timestamp("2019-07-01")
# df = df[df['Date de la chirurgie'] <= date_limite]

# Colonnes Kaplan-Meier
df['event'] = df['Date de décès'].notna().astype(int)
df['survival_time'] = (df['Date de décès'] - df['Date de la chirurgie']).dt.days
df['survival_time'] = df['survival_time'].fillna((pd.to_datetime('today') - df['Date de la chirurgie']).dt.days)
df['survival_time_years'] = df['survival_time'] / 365.25  # conversion en années

# Définir les groupes
def assign_group(val):
    if pd.isna(val):
        return 'Non défini'
    val = val.lower()
    if 'chimio' in val and 'post-op' not in val:
        return 'Chimio'
    elif 'non' in val or 'post-op' in val:
        return 'Nonchimio'
    else:
        return 'Non défini'

df['Groupe'] = df['Chimio ou Pas'].apply(assign_group)
df = df[df['Groupe'].isin(['Chimio', 'Nonchimio'])]

# Initialisation
kmf_chimio = KaplanMeierFitter()
kmf_nonchimio = KaplanMeierFitter()

# Séparer les groupes
chimio = df[df['Groupe'] == 'Chimio']
nonchimio = df[df['Groupe'] == 'Nonchimio']

# Fit des modèles
kmf_chimio.fit(chimio['survival_time_years'], chimio['event'], label="Chimiothérapie")
kmf_nonchimio.fit(nonchimio['survival_time_years'], nonchimio['event'], label="Non chimiothérapie")

# Créer la figure
fig, ax = plt.subplots(figsize=(10, 7))  # 10x7 pouces = bon format article

# Tracer avec des lignes plus épaisses
kmf_chimio.plot_survival_function(ax=ax, ci_show=True, linewidth=2)
kmf_nonchimio.plot_survival_function(ax=ax, ci_show=True, linewidth=2)

# Ajustements esthétiques
plt.title("Survie après chirurgie selon traitement", fontsize=16)
plt.xlabel("Temps depuis la chirurgie (années)", fontsize=14)
plt.ylabel("Survie (%)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xlim(0, 10)
plt.ylim(0, 1.05)

# Ticks + format pourcentage
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

# Ajouter "n à risque"
add_at_risk_counts(kmf_chimio, kmf_nonchimio, ax=ax, labels=['Chimiothérapie', 'Non chimiothérapie'])

# Afficher médianes
print("Médiane de survie (Chimiothérapie) :", round(kmf_chimio.median_survival_time_, 2), "ans")
print("Médiane de survie (Non chimiothérapie) :", round(kmf_nonchimio.median_survival_time_, 2), "ans")

# Tracer les lignes médianes
plt.axvline(kmf_chimio.median_survival_time_, color='blue', linestyle='--', alpha=0.6)
plt.axvline(kmf_nonchimio.median_survival_time_, color='orange', linestyle='--', alpha=0.6)

# Test log-rank
results = logrank_test(chimio['survival_time_years'], nonchimio['survival_time_years'],
                       event_observed_A=chimio['event'], event_observed_B=nonchimio['event'])
print(f"Test log-rank p-value: {results.p_value:.4f}")

# Ajouter p-value au graphe
plt.text(6, 0.1, f'p = {results.p_value:.4f}', fontsize=12,
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

plt.tight_layout()

# Enregistrer en haute résolution
plt.savefig("courbe_survie_article.pdf", format='pdf', dpi=300)

# Afficher
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.plotting import add_at_risk_counts
from matplotlib.ticker import FuncFormatter

# Charger les données
file_path = '/Users/abedard/Desktop/Excel recherche_2.xlsx'
df = pd.concat([
    pd.read_excel(file_path, sheet_name=0, engine="openpyxl"),
    pd.read_excel(file_path, sheet_name=1, engine="openpyxl")
], ignore_index=True)

# Nettoyage des dates
df['Date de la chirurgie'] = pd.to_datetime(df['Date de la chirurgie'], errors='coerce')
df['Date de décès'] = pd.to_datetime(df['Date de décès'], errors='coerce')

# 🎯 Filtrer les patients opérés avant 1er juillet 2019
date_limite = pd.Timestamp("2019-07-01")
df = df[df['Date de la chirurgie'] <= date_limite]

# Colonnes de survie
df['event'] = df['Date de décès'].notna().astype(int)
df['survival_time'] = (df['Date de décès'] - df['Date de la chirurgie']).dt.days
df['survival_time'] = df['survival_time'].fillna((pd.to_datetime('today') - df['Date de la chirurgie']).dt.days)
df['survival_time_years'] = df['survival_time'] / 365.25

# 🎯 Nettoyer les stades correctement
def clean_stage(stage):
    if pd.isna(stage):
        return 'Non défini'
    stage = stage.upper().strip()
    if 'T0' in stage:
        return 'T0 (vessie)'
    elif stage == 'TIS':
        return 'TiS'
    elif 'CIS' in stage:
        return 'CiS'
    elif 'T1' in stage:
        return 'T1'
    elif 'T2' in stage:
        return 'T2'
    elif 'T3' in stage:
        return 'T3'
    elif 'T4' in stage:
        return 'T4'
    else:
        return 'Autre'

df['Stade Groupe'] = df['Stade Patho Finale'].apply(clean_stage)

# 🎯 Garder seulement les groupes désirés
groupes_conserves = ['T0 (vessie)', 'T1', 'TiS', 'CiS', 'T2', 'T3', 'T4']
df = df[df['Stade Groupe'].isin(groupes_conserves)]

# Initialisation
kmf = KaplanMeierFitter()

# Couleurs publication-friendly
couleurs = {
    'T0 (vessie)': 'blue',
    'T1': 'green',
    'TiS': 'purple',
    'CiS': 'cyan',
    'T2': 'orange',
    'T3': 'red',
    'T4': 'black'
}

# Tracer Kaplan-Meier
fig, ax = plt.subplots(figsize=(12, 8))

for group in groupes_conserves:
    subset = df[df['Stade Groupe'] == group]
    kmf.fit(subset['survival_time_years'], event_observed=subset['event'], label=f"{group} (n={len(subset)})")
    kmf.plot_survival_function(ax=ax, ci_show=False, color=couleurs[group], linewidth=2)

# Mise en forme scientifique
plt.title("Survie selon stade pathologique final (Kaplan-Meier)", fontsize=18)
plt.xlabel("Temps depuis la chirurgie (années)", fontsize=16)
plt.ylabel("Survie (%)", fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xlim(0, 10)
plt.ylim(0, 1.05)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

# Ajouter les "n à risque"
kmfs = [KaplanMeierFitter().fit(df[df['Stade Groupe'] == g]['survival_time_years'],
                                event_observed=df[df['Stade Groupe'] == g]['event']) for g in groupes_conserves]
add_at_risk_counts(*kmfs, labels=groupes_conserves, ax=ax)

plt.tight_layout()

# Exporter en PDF haute qualité
plt.savefig("courbe_survie_stades_detaillees.pdf", format='pdf', dpi=300)

# Afficher
plt.show()