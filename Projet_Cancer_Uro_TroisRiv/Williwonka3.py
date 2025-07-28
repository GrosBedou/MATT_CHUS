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

# Filtrer selon date de chirurgie pour permettre 5-10 ans de suivi
df = df[df['Date de la chirurgie'] <= pd.Timestamp("2019-07-01")]

# Colonnes de survie
df['event'] = df['Date de décès'].notna().astype(int)
df['survival_time'] = (df['Date de décès'] - df['Date de la chirurgie']).dt.days
df['survival_time'] = df['survival_time'].fillna((pd.to_datetime('today') - df['Date de la chirurgie']).dt.days)
df['survival_time_years'] = df['survival_time'] / 365.25

# Nettoyer les stades
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

# Groupes à garder
groupes_conserves = ['T0 (vessie)', 'T1', 'TiS', 'CiS', 'T2', 'T3', 'T4']
df = df[df['Stade Groupe'].isin(groupes_conserves)]

# Initialisation
kmf = KaplanMeierFitter()
couleurs = {
    'T0 (vessie)': 'blue',
    'T1': 'green',
    'TiS': 'purple',
    'CiS': 'cyan',
    'T2': 'orange',
    'T3': 'red',
    'T4': 'black'
}

# Tracer
fig, ax = plt.subplots(figsize=(12, 8))

kmfs = []
for group in groupes_conserves:
    subset = df[df['Stade Groupe'] == group]
    kmf_group = KaplanMeierFitter()
    kmf_group.fit(subset['survival_time_years'], event_observed=subset['event'], label=f"{group} (n={len(subset)})")
    kmf_group.plot_survival_function(ax=ax, ci_show=False, color=couleurs[group], linewidth=2)
    kmfs.append(kmf_group)

# Mise en page
plt.title("Survie selon stade pathologique final (Kaplan-Meier)", fontsize=18)
plt.xlabel("Temps depuis la chirurgie (années)", fontsize=16)
plt.ylabel("Survie (%)", fontsize=16)
plt.xlim(0, 10)
plt.ylim(0, 1.05)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12, loc='lower left')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

# ✅ Ajouter uniquement "At risk"
add_at_risk_counts(
    *kmfs,
    labels=groupes_conserves,
    ax=ax,
    rows_to_show=['At risk']  # << Seule ligne affichée
)

plt.tight_layout()

# Exporter en PDF haute qualité
plt.savefig("courbe_survie_stades_detaillees_sans_censored.pdf", format='pdf', dpi=300)

# Afficher
plt.show()