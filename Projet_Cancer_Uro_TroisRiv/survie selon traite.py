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

# Filtrer pour un suivi suffisant
df = df[df['Date de la chirurgie'] <= pd.Timestamp("2023-07-01")]

# Colonnes de survie
df['event'] = df['Date de décès'].notna().astype(int)
df['survival_time'] = (df['Date de décès'] - df['Date de la chirurgie']).dt.days
df['survival_time'] = df['survival_time'].fillna((pd.to_datetime('today') - df['Date de la chirurgie']).dt.days)
df['survival_time_years'] = df['survival_time'] / 365.25

# Nettoyage du traitement
df['Chimio ou Pas'] = df['Chimio ou Pas'].str.lower().str.strip()
df = df[df['Chimio ou Pas'].isin(['chimio', 'non'])]

# Nettoyage des stades
def clean_stage(stage):
    if pd.isna(stage):
        return 'Non défini'
    stage = stage.upper().strip()
    if stage.startswith('T0'):
        return 'T0 (vessie)'
    elif stage == 'TIS':
        return 'TiS'
    elif 'CIS' in stage:
        return 'CiS'
    elif stage.startswith('T1'):
        return 'T1'
    elif stage.startswith('T2'):
        return 'T2'
    elif stage.startswith('T3'):
        return 'T3'
    elif stage.startswith('T4'):
        return 'T4'
    else:
        return 'Autre'

df['Stade Groupe'] = df['Stade Patho Finale'].apply(clean_stage)
groupes_conserves = ['T0 (vessie)', 'TiS', 'CiS', 'T1', 'T2', 'T3', 'T4']
df = df[df['Stade Groupe'].isin(groupes_conserves)]

# Palette
couleurs = {'chimio': 'blue', 'non': 'orange'}

# Tracer un graphique par stade
for stade in groupes_conserves:
    subset_stade = df[df['Stade Groupe'] == stade]
    if subset_stade.empty:
        continue

    fig, ax = plt.subplots(figsize=(10, 7))
    kmfs = []

    for traitement in ['chimio', 'non']:
        subset = subset_stade[subset_stade['Chimio ou Pas'] == traitement]
        if subset.empty:
            continue
        kmf = KaplanMeierFitter()
        label = f"{traitement} (n={len(subset)})"
        kmf.fit(subset['survival_time_years'], event_observed=subset['event'], label=label)
        kmf.plot_survival_function(ax=ax, color=couleurs[traitement], linewidth=2, ci_show=False)
        kmfs.append(kmf)

    plt.title(f"Survie selon traitement – {stade}", fontsize=18)
    plt.xlabel("Temps depuis la chirurgie (années)", fontsize=16)
    plt.ylabel("Survie (%)", fontsize=16)
    plt.xlim(0, 10)
    plt.ylim(0, 1.05)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12, loc='lower left')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

    # Tableau "At risk"
    add_at_risk_counts(*kmfs, ax=ax, rows_to_show=['At risk'])

    plt.tight_layout()
    plt.savefig(f"courbe_survie_{stade.replace(' ', '_').replace('(', '').replace(')', '')}.pdf", dpi=300)
    plt.show()