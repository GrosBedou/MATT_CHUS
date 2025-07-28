import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt

# 1. Charger les données
file_path = '/Users/abedard/Desktop/Excel recherche_2.xlsx'
df = pd.concat([
    pd.read_excel(file_path, sheet_name=0, engine='openpyxl'),
    pd.read_excel(file_path, sheet_name=1, engine='openpyxl')
], ignore_index=True)

# 2. Nettoyer la colonne "Métastases"
df['Métastases'] = df['Métastases'].astype(str).str.lower()

# 3. Dictionnaire de mots-clés par site anatomique
sites = {
    'foie': ['foie', 'hépatique', 'hépatiques'],
    'poumon': ['poumon', 'pulmonaire', 'pulmonaires', 'lobe supérieur', 'lobe inférieur', 'hilaires', 'médistinal'],
    'os': ['os', 'osseuse', 'osseuses', 'osseux', 'rachis', 'fémur', 'sacrum', 'iliaque', 'humérus', 'crête iliaque', 'aileron sacré', 'pubis', 'colonne', 'vertèbre', 'lombaire', 'côtes', 'sternum'],
    'ganglions': ['ganglion', 'ganglions', 'ganglionnaire', 'ganglionnaires', 'adénopathie', 'adénopathies', 'lymphatique', 'lymphatiques'],
    'cerveau': ['cerveau', 'cérébrale', 'cérébrales', 'méningée', 'méningées', 'intracrânien'],
    'rein': ['rein', 'rénal', 'rénaux'],
    'péritoine': ['péritoine', 'péritonéale', 'péritonéaux', 'rétropéritoine', 'rétropéritonéale', 'rétropéritonéal', 'péritonéal'],
    'vessie': ['vessie', 'néo-vessie', 'carcinome urothélial'],
    'pelvien': ['pelvien', 'pelvienne', 'pelviennes', 'bassin', 'obturateur', 'pénis', 'périnéal'],
    'rectum': ['rectum', 'rectale', 'rectal', 'rectosigmoïde'],
    'sein': ['sein'],
    'utérus': ['utérus', 'endomètre', 'endométriale'],
    'vésicules séminales': ['vésicules séminales'],
    'intestin': ['intestin', 'intestinal', 'iléon', 'iléale', 'grêle', 'colon', 'colique', 'côlon'],
    'mésentère': ['mésentère', 'mésentérique'],
    'pancréas': ['pancréas', 'pancréatique', 'pancréatiques'],
    'surrénales': ['surrénale', 'surrénales'],
    'ovaire': ['ovaire', 'ovariens', 'ovarique'],
    'prostate': ['prostate', 'prostatique'],
    'autre': ['diffus', 'plurimétastatique', 'nombreuses', 'multiples']
}

# 4. Compter les cas par site
site_counter = Counter()
for texte in df['Métastases']:
    for site, keywords in sites.items():
        if any(re.search(rf'\b{kw}\b', texte) for kw in keywords):
            site_counter[site] += 1

# 5. Résultats en DataFrame trié
resultats = pd.DataFrame(site_counter.most_common(), columns=['Site', 'Nombre de cas'])

# 6. Barplot avec étiquettes
plt.figure(figsize=(12, 6))
bars = plt.bar(resultats['Site'], resultats['Nombre de cas'], color='steelblue')

# Ajouter les valeurs au-dessus des barres
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height + 0.2, f'{int(height)}', ha='center', va='bottom', fontsize=10)

plt.title("Sites les plus fréquents de métastases", fontsize=16)
plt.xlabel("Site anatomique", fontsize=14)
plt.ylabel("Nombre de cas", fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# 7. Sauvegarde en PDF
plt.savefig("sites_metastases_frequents.pdf", dpi=300)
plt.show()