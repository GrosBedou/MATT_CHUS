import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from lifelines.plotting import add_at_risk_counts
from matplotlib.ticker import FuncFormatter

# 1. Charger les données
file_path = '/Users/abedard/Desktop/Excel recherche_2.xlsx'
df = pd.concat([
    pd.read_excel(file_path, sheet_name=0, engine="openpyxl"),
    pd.read_excel(file_path, sheet_name=1, engine="openpyxl")
], ignore_index=True)

# 2. Nettoyer les dates
df['Date de la chirurgie'] = pd.to_datetime(df['Date de la chirurgie'], errors='coerce')
df['Date de décès'] = pd.to_datetime(df['Date de décès'], errors='coerce')

# 3. Filtrer par date de chirurgie
df = df[df['Date de la chirurgie'] <= pd.Timestamp("2019-07-01")]

# 4. Calcul du temps de survie
df['event'] = df['Date de décès'].notna().astype(int)
df['survival_time'] = (df['Date de décès'] - df['Date de la chirurgie']).dt.days
df['survival_time'] = df['survival_time'].fillna((pd.to_datetime('today') - df['Date de la chirurgie']).dt.days)
df['survival_time_years'] = df['survival_time'] / 365.25

# 5. Définir les groupes
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

chimio = df[df['Groupe'] == 'Chimio']
nonchimio = df[df['Groupe'] == 'Nonchimio']

# 6. Kaplan-Meier
kmf_chimio = KaplanMeierFitter()
kmf_nonchimio = KaplanMeierFitter()

kmf_chimio.fit(chimio['survival_time_years'], chimio['event'], label="Chimiothérapie")
kmf_nonchimio.fit(nonchimio['survival_time_years'], nonchimio['event'], label="Non chimiothérapie")

# 7. Calcul des médianes de survie
mediane_chimio = kmf_chimio.median_survival_time_
mediane_nonchimio = kmf_nonchimio.median_survival_time_

print(f"Médiane de survie (Chimio) : {mediane_chimio:.2f} ans")
print(f"Médiane de survie (Nonchimio) : {mediane_nonchimio:.2f} ans")

# 8. Tracer la figure
fig, ax = plt.subplots(figsize=(10, 7))

kmf_chimio.plot_survival_function(ax=ax, ci_show=True, linewidth=2)
kmf_nonchimio.plot_survival_function(ax=ax, ci_show=True, linewidth=2)

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

# Lignes et texte pour les médianes de survie
plt.axhline(0.5, color='gray', linestyle='--', alpha=0.6)

plt.axvline(mediane_chimio, color='blue', linestyle='--', alpha=0.6)
plt.annotate(f"{mediane_chimio:.2f} ans",
             xy=(mediane_chimio, 0.5),
             xytext=(mediane_chimio + 0.2, 0.55),
             arrowprops=dict(arrowstyle="->", color='blue'),
             fontsize=12, color='blue')

plt.axvline(mediane_nonchimio, color='orange', linestyle='--', alpha=0.6)
plt.annotate(f"{mediane_nonchimio:.2f} ans",
             xy=(mediane_nonchimio, 0.5),
             xytext=(mediane_nonchimio + 0.2, 0.45),
             arrowprops=dict(arrowstyle="->", color='orange'),
             fontsize=12, color='orange')

# Ajouter les "n à risque"
add_at_risk_counts(kmf_chimio, kmf_nonchimio, ax=ax, labels=['Chimiothérapie', 'Non chimiothérapie'])

# Test log-rank
results = logrank_test(chimio['survival_time_years'], nonchimio['survival_time_years'],
                       event_observed_A=chimio['event'], event_observed_B=nonchimio['event'])

plt.text(6.2, 0.08, f'p = {results.p_value:.4f}', fontsize=11,
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

# Export et affichage
plt.tight_layout()
plt.savefig("courbe_survie_medianes_survie_seulement.pdf", dpi=300)
plt.show()