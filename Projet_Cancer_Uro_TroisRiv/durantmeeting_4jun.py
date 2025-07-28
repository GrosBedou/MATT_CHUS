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

# Filtrage par date de chirurgie
#date_limite = pd.Timestamp("2019-07-01")
# df = df[df['Date de la chirurgie'] <= date_limite]

# Colonnes de survie
df['event'] = df['Date de décès'].notna().astype(int)
df['survival_time'] = (df['Date de décès'] - df['Date de la chirurgie']).dt.days
df['survival_time'] = df['survival_time'].fillna((pd.to_datetime('today') - df['Date de la chirurgie']).dt.days)
df['survival_time_years'] = df['survival_time'] / 365.25

# Regrouper en deux groupes : Chimio vs Nonchimio
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

# Séparer les groupes
chimio = df[df['Groupe'] == 'Chimio']
nonchimio = df[df['Groupe'] == 'Nonchimio']

# Fit des modèles Kaplan-Meier
kmf_chimio = KaplanMeierFitter()
kmf_nonchimio = KaplanMeierFitter()

kmf_chimio.fit(chimio['survival_time_years'], chimio['event'], label="Chimiothérapie")
kmf_nonchimio.fit(nonchimio['survival_time_years'], nonchimio['event'], label="Non chimiothérapie")

# Créer la figure
fig, ax = plt.subplots(figsize=(10, 7))

# Tracer les courbes
kmf_chimio.plot_survival_function(ax=ax, ci_show=True, linewidth=2)
kmf_nonchimio.plot_survival_function(ax=ax, ci_show=True, linewidth=2)

# Ajustements visuels
plt.title("Survie après chirurgie selon traitement", fontsize=16)
plt.xlabel("Temps depuis la chirurgie (années)", fontsize=14)
plt.ylabel("Survie (%)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xlim(0, 10)
plt.ylim(0, 1.05)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

# Ajouter les "n à risque"
add_at_risk_counts(kmf_chimio, kmf_nonchimio, ax=ax, labels=['Chimiothérapie', 'Non chimiothérapie'])

# Tracer les lignes verticales (médianes de survie)
plt.axvline(kmf_chimio.median_survival_time_, color='blue', linestyle='--', alpha=0.6)
plt.axvline(kmf_nonchimio.median_survival_time_, color='orange', linestyle='--', alpha=0.6)

# Tracer ligne horizontale à 50%
plt.axhline(0.5, color='gray', linestyle='--', alpha=0.6)

# Annoter les médianes de survie
plt.annotate(f"{kmf_chimio.median_survival_time_:.2f} ans",
             xy=(kmf_chimio.median_survival_time_, 0.5),
             xytext=(kmf_chimio.median_survival_time_ + 0.3, 0.55),
             arrowprops=dict(arrowstyle="->", color='blue'),
             fontsize=12, color='blue')

plt.annotate(f"{kmf_nonchimio.median_survival_time_:.2f} ans",
             xy=(kmf_nonchimio.median_survival_time_, 0.5),
             xytext=(kmf_nonchimio.median_survival_time_ + 0.3, 0.45),
             arrowprops=dict(arrowstyle="->", color='orange'),
             fontsize=12, color='orange')

# Suivi médian pour les patients censurés (event == 0)
followup_chimio = chimio[chimio['event'] == 0]['survival_time_years'].median()
followup_nonchimio = nonchimio[nonchimio['event'] == 0]['survival_time_years'].median()

print(f"Suivi médian (Chimio) : {followup_chimio:.2f} ans")
print(f"Suivi médian (Nonchimio) : {followup_nonchimio:.2f} ans")

# Annoter les suivis médians sur le graphe
plt.text(6, 0.20, f'Suivi médian (Chimio): {followup_chimio:.2f} ans', fontsize=12,
         bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.5'), color='blue')

plt.text(6, 0.14, f'Suivi médian (Nonchimio): {followup_nonchimio:.2f} ans', fontsize=12,
         bbox=dict(facecolor='white', edgecolor='orange', boxstyle='round,pad=0.5'), color='orange')

# Test log-rank
results = logrank_test(chimio['survival_time_years'], nonchimio['survival_time_years'],
                       event_observed_A=chimio['event'], event_observed_B=nonchimio['event'])
print(f"Test log-rank p-value: {results.p_value:.4f}")

# Annoter la p-value
plt.text(6, 0.08, f'p = {results.p_value:.4f}', fontsize=12,
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

# Finaliser et exporter
plt.tight_layout()
plt.savefig("courbe_survie_article.pdf", format='pdf', dpi=300)
plt.show()