import pandas as pd
import re
import matplotlib.pyplot as plt

file_path = '/Users/abedard/Desktop/Excel recherche.xlsx'

# Charger les données
df = pd.read_excel(file_path)
df1 = pd.read_excel(file_path, sheet_name=0, engine="openpyxl")  # Première feuille
df2 = pd.read_excel(file_path, sheet_name=1, engine="openpyxl")  # Deuxième feuille

# Fusionner les deux DataFrames
df = pd.concat([df1, df2], ignore_index=True)

# Vérifier si la colonne "Histologie" contient à la fois "prostate" et "vessie"
cancer_prostate_vessie = df[
    df["Stade Patho Finale"].str.contains("prostate", case=False, na=False) &
    df["Stade Patho Finale"].str.contains("vessie", case=False, na=False)
]

incidence_prostate_vessie = len(cancer_prostate_vessie)
print(f"Incidence du cancer prostate + vessie : {incidence_prostate_vessie}")
print(f"############")

# Convertir la colonne "Date de la chirurgie" en format datetime
df["Date de la chirurgie"] = pd.to_datetime(df["Date de la chirurgie"], errors='coerce')

# Définir la date limite pour l'inclusion
date_limite_5_ans = pd.Timestamp("2019-07-01")
date_limite_10_ans = pd.Timestamp("2014-07-01")

survie_5_ans = df[
    df["Stade Patho Finale"].str.contains("prostate", case=False, na=False) &
    df["Stade Patho Finale"].str.contains("vessie", case=False, na=False) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_5_ans)
]
survie_5_ans = len(survie_5_ans)

nb_total = incidence_prostate_vessie

nb_non_survivants = nb_total - survie_5_ans

# Calculer le taux de survie à 5 ans vessie et prostate
taux_survie_5_ans = (survie_5_ans / nb_total) * 100

print(f"Nombre total de patients avec cancer de la vessie et de la prostate : {nb_total}")
print(f"Nombre de survivants à 5 ans : {survie_5_ans}")
print(f"Taux de survie à 5 ans : {taux_survie_5_ans:.2f} %")
print(f"############")

# Calculer taux de survie à 5 ans et 10 ans vessie seule
cancer_vessie = df[df["Stade Patho Finale"].str.contains("vessie", case=False, na=False)]
cancer_vessie = len(cancer_vessie)
survie_5_ans_vessie = df[
    df["Stade Patho Finale"].str.contains("vessie", case=False, na=False) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_5_ans)
]
survie_5_ans_vessie = len(survie_5_ans_vessie)

taux_survie_5_ans_vessie = (survie_5_ans_vessie / cancer_vessie) * 100

survie_10_ans_vessie = df[
    df["Stade Patho Finale"].str.contains("vessie", case=False, na=False) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_10_ans)
]
survie_10_ans_vessie = len(survie_10_ans_vessie)

taux_survie_10_ans_vessie = (survie_10_ans_vessie / cancer_vessie) * 100



# Définir les groupes selon la chimiothérapie - Chimiopostop

Chimiopostop = df[
    df["Chimio ou Pas"].str.contains("Chimio post-op.", case=False, na=False)
]
Chimiopostop = len(Chimiopostop)

survie_5_ans_chimiopostop = df[
    df["Chimio ou Pas"].str.contains("Chimio post-op.", case=False, na=False) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_5_ans)
]
survie_5_ans_chimiopostop = len(survie_5_ans_chimiopostop)

survie_10_ans_chimiopostop = df[
    df["Chimio ou Pas"].str.contains("Chimio post-op.", case=False, na=False) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_10_ans)
]
survie_10_ans_chimiopostop = len(survie_10_ans_chimiopostop)

taux_survie_5_ans_chimiopostop = (survie_5_ans_chimiopostop / Chimiopostop) * 100
taux_survie_10_ans_chimiopostop = (survie_10_ans_chimiopostop / Chimiopostop) * 100

print(f"Nombre total de patients avec de la chimio post op  : {Chimiopostop}")
print(f"Nombre de survivants à 5 ans ayant eu de la chimio post op: {survie_5_ans_chimiopostop}")
print(f"Taux de survie à 5 ans ayant eu de la chimio post op : {taux_survie_5_ans_chimiopostop:.2f} %")
print(f"Nombre de survivants à 10 ans ayant eu de la chimio post op: {survie_10_ans_chimiopostop}")
print(f"Taux de survie à 10 ans ayant eu de la chimio post op: {taux_survie_10_ans_chimiopostop:.2f} %")
print(f"############")


# Définir les groupes selon la chimiothérapie - Chimio

chimio = df[
    df["Chimio ou Pas"].str.contains("Chimio", case=False, na=False)
]
chimio = len(chimio)

nonchimio = df[
    df["Chimio ou Pas"].str.contains("Non", case=False, na=False)
]
nonchimio = len(nonchimio)

survie_5_ans_chimio = df[
    df["Chimio ou Pas"].str.contains("Chimio", case=False, na=False) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_5_ans)
]
survie_5_ans_chimio = len(survie_5_ans_chimio)

survie_5_ans_nonchimio = df[
    df["Chimio ou Pas"].str.contains("Non", case=False, na=False) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_5_ans)
]
survie_5_ans_nonchimio = len(survie_5_ans_nonchimio)

survie_10_ans_chimio = df[
    df["Chimio ou Pas"].str.contains("Chimio", case=False, na=False) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_10_ans)
]
survie_10_ans_chimio = len(survie_10_ans_chimio)

survie_10_ans_nonchimio = df[
    df["Chimio ou Pas"].str.contains("Non", case=False, na=False) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_10_ans)
]
survie_10_ans_nonchimio = len(survie_10_ans_nonchimio)

taux_survie_5_ans_chimio = (survie_5_ans_chimio / chimio) * 100
taux_survie_10_ans_chimio = (survie_10_ans_chimio / chimio) * 100

taux_survie_5_ans_nonchimio = (survie_5_ans_nonchimio / nonchimio) * 100
taux_survie_10_ans_nonchimio = (survie_10_ans_nonchimio / nonchimio) * 100

print(f"Nombre total de patients avec de la chimio  : {chimio}")
print(f"Nombre de survivants à 5 ans ayant eu de la chimio: {survie_5_ans_chimio}")
print(f"Taux de survie à 5 ans ayant eu de la chimio : {taux_survie_5_ans_chimio:.2f} %")
print(f"Nombre de survivants à 10 ans ayant eu de la chimio: {survie_10_ans_chimio}")
print(f"Taux de survie à 10 ans ayant eu de la chimio : {taux_survie_10_ans_chimio:.2f} %")
print(f"############")

print(f"Nombre total de patients SANS chimio  : {nonchimio}")
print(f"Nombre de survivants à 5 ans SANS chimio: {survie_5_ans_nonchimio}")
print(f"Taux de survie à 5 ans SANS : {taux_survie_5_ans_nonchimio:.2f} %")
print(f"Nombre de survivants à 10 ans SANS chimio: {survie_10_ans_nonchimio}")
print(f"Taux de survie à 10 ans SANS : {taux_survie_10_ans_nonchimio:.2f} %")
print(f"############")


# 3)	Incidence de T0 ou Tis (taux de survie de ceux ci)
incidence_T0_or_TiS = df[
    df["Stade Patho Finale"].str.contains("T0|Tis", case=False, na=False)
]
incidence_T0_or_TiS = len(incidence_T0_or_TiS)

incidence_T0_or_TiS_5ans = df[
    df["Stade Patho Finale"].str.contains("T0|TiS", case=False, na=False) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_5_ans)
]
incidence_T0_or_TiS_5ans = len(incidence_T0_or_TiS_5ans)

incidence_T0_or_TiS_10ans = df[
    df["Stade Patho Finale"].str.contains("T0|Tis", case=False, na=False) & df["Survie 10 ans"].str.contains("Oui", case=False, na=False) &
    (df["Date de la chirurgie"] <= date_limite_10_ans)
]
incidence_T0_or_TiS_10ans = len(incidence_T0_or_TiS_10ans)

taux_survie_5_ans_T0_or_TiS = (incidence_T0_or_TiS_5ans / incidence_T0_or_TiS) * 100
taux_survie_10_ans_T0_or_TiS = (incidence_T0_or_TiS_10ans / incidence_T0_or_TiS) * 100

print(f"Nombre total de patients ayant T0 ou Tis : {incidence_T0_or_TiS}")
print(f"Nombre de survivants à 5 ans ayant  T0 ou Tis : {incidence_T0_or_TiS_5ans}")
print(f"Taux de survie à 5 ans ayant  T0 ou Tis : {taux_survie_5_ans_T0_or_TiS:.2f} %")
print(f"Nombre de survivants à 10 ans ayant  T0 ou Tis : {incidence_T0_or_TiS_10ans}")
print(f"Taux de survie à 10 ans ayant  T0 ou Tis : {taux_survie_10_ans_T0_or_TiS:.2f} %")
print(f"############")


#4 ) Taux de survie selon stade du cancer
incidence_T0= df[df["Stade Patho Finale"].str.contains("T0", case=False, na=False)]
incidence_T0 = len(incidence_T0)

incidence_T1= df[df["Stade Patho Finale"].str.contains("T1", case=False, na=False)]
incidence_T1 = len(incidence_T1)

incidence_TiS= df[df["Stade Patho Finale"].str.contains("TiS", case=False, na=False)]
incidence_TiS = len(incidence_TiS)

incidence_T2= df[df["Stade Patho Finale"].str.contains("T2", case=False, na=False)]
incidence_T2 = len(incidence_T2)

incidence_T3= df[df["Stade Patho Finale"].str.contains("T3", case=False, na=False)]
incidence_T3 = len(incidence_T3)

incidence_T4= df[df["Stade Patho Finale"].str.contains("T4", case=False, na=False)]
incidence_T4 = len(incidence_T4)


incidence_T0_5ans = df[df["Stade Patho Finale"].str.contains("T0", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_5_ans) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False)]
incidence_T0_5ans = len(incidence_T0_5ans)

incidence_T1_5ans = df[df["Stade Patho Finale"].str.contains("T1", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_5_ans) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False)]
incidence_T1_5ans = len(incidence_T1_5ans)

incidence_TiS_5ans = df[df["Stade Patho Finale"].str.contains("TiS", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_5_ans) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False)]
incidence_TiS_5ans = len(incidence_TiS_5ans)

incidence_T2_5ans = df[df["Stade Patho Finale"].str.contains("T2", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_5_ans) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False)]
incidence_T2_5ans = len(incidence_T2_5ans)

incidence_T3_5ans = df[df["Stade Patho Finale"].str.contains("T3", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_5_ans) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False)]
incidence_T3_5ans = len(incidence_T3_5ans)

incidence_T4_5ans = df[df["Stade Patho Finale"].str.contains("T4", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_5_ans) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False)]
incidence_T4_5ans = len(incidence_T4_5ans)

incidence_T0_10ans = df[df["Stade Patho Finale"].str.contains("T0", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_10_ans) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False)]
incidence_T0_10ans = len(incidence_T0_10ans)

incidence_T1_10ans = df[df["Stade Patho Finale"].str.contains("T1", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_10_ans) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False)]
incidence_T1_10ans = len(incidence_T1_10ans)

incidence_TiS_10ans = df[df["Stade Patho Finale"].str.contains("TiS", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_10_ans) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False)]
incidence_TiS_10ans = len(incidence_TiS_10ans)

incidence_T2_10ans = df[df["Stade Patho Finale"].str.contains("T2", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_10_ans) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False)]
incidence_T2_10ans = len(incidence_T2_10ans)

incidence_T3_10ans = df[df["Stade Patho Finale"].str.contains("T3", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_10_ans) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False)]
incidence_T3_10ans = len(incidence_T3_10ans)

incidence_T4_10ans = df[df["Stade Patho Finale"].str.contains("T3", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_10_ans) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False)]
incidence_T4_10ans = len(incidence_T4_10ans)

taux_survie_5_ans_T0 = (incidence_T0_5ans / incidence_T0) * 100
taux_survie_10_ans_T0 = (incidence_T0_10ans / incidence_T0) * 100
taux_survie_5_ans_T1 = (incidence_T1_5ans / incidence_T1) * 100
taux_survie_10_ans_T1 = (incidence_T1_10ans / incidence_T1) * 100
taux_survie_5_ans_T2 = (incidence_T2_5ans / incidence_T2) * 100
taux_survie_10_ans_T2 = (incidence_T2_10ans / incidence_T2) * 100
taux_survie_5_ans_T3 = (incidence_T3_5ans / incidence_T3) * 100
taux_survie_10_ans_T3 = (incidence_T3_10ans / incidence_T3) * 100
taux_survie_5_ans_T4 = (incidence_T4_5ans / incidence_T4) * 100
taux_survie_10_ans_T4 = (incidence_T4_10ans / incidence_T4) * 100

taux_survie_5_ans_TiS = (incidence_TiS_5ans / incidence_TiS) * 100
taux_survie_10_ans_TiS = (incidence_TiS_10ans / incidence_TiS) * 100



print(f"Nombre total de patients ayant T0 : {incidence_T0}")
print(f"Nombre de survivants à 5 ans ayant  T0 : {incidence_T0_5ans}")
print(f"Taux de survie à 5 ans ayant  T0  : {taux_survie_5_ans_T0:.2f} %")
print(f"Nombre de survivants à 10 ans ayant  T0 : {incidence_T0_10ans}")
print(f"Taux de survie à 10 ans ayant  T0  : {taux_survie_10_ans_T0:.2f} %")
print(f"############")

print(f"Nombre total de patients ayant T1 : {incidence_T1}")
print(f"Nombre de survivants à 5 ans ayant  T1 : {incidence_T1_5ans}")
print(f"Taux de survie à 5 ans ayant  T1  : {taux_survie_5_ans_T1:.2f} %")
print(f"Nombre de survivants à 10 ans ayant  T1 : {incidence_T1_10ans}")
print(f"Taux de survie à 10 ans ayant  T1  : {taux_survie_10_ans_T1:.2f} %")
print(f"############")

print(f"Nombre total de patients ayant T1 : {incidence_TiS}")
print(f"Nombre de survivants à 5 ans ayant  T1 : {incidence_TiS_5ans}")
print(f"Taux de survie à 5 ans ayant  T1  : {taux_survie_5_ans_TiS:.2f} %")
print(f"Nombre de survivants à 10 ans ayant  T1 : {incidence_TiS_10ans}")
print(f"Taux de survie à 10 ans ayant  T1  : {taux_survie_10_ans_TiS:.2f} %")
print(f"############")

print(f"Nombre total de patients ayant T2 : {incidence_T2}")
print(f"Nombre de survivants à 5 ans ayant  T2 : {incidence_T2_5ans}")
print(f"Taux de survie à 5 ans ayant  T2  : {taux_survie_5_ans_T2:.2f} %")
print(f"Nombre de survivants à 10 ans ayant  T2 : {incidence_T2_10ans}")
print(f"Taux de survie à 10 ans ayant  T2  : {taux_survie_10_ans_T2:.2f} %")
print(f"############")

print(f"Nombre total de patients ayant T3 : {incidence_T3}")
print(f"Nombre de survivants à 5 ans ayant  T3 : {incidence_T3_5ans}")
print(f"Taux de survie à 5 ans ayant  T3  : {taux_survie_5_ans_T3:.2f} %")
print(f"Nombre de survivants à 10 ans ayant  T3 : {incidence_T3_10ans}")
print(f"Taux de survie à 10 ans ayant  T3  : {taux_survie_10_ans_T3:.2f} %")
print(f"############")

print(f"Nombre total de patients ayant T4 : {incidence_T4}")
print(f"Nombre de survivants à 5 ans ayant  T4 : {incidence_T4_5ans}")
print(f"Taux de survie à 5 ans ayant  T4  : {taux_survie_5_ans_T4:.2f} %")
print(f"Nombre de survivants à 10 ans ayant  T4 : {incidence_T4_10ans}")
print(f"Taux de survie à 10 ans ayant  T4  : {taux_survie_10_ans_T4:.2f} %")
print(f"############")

#5) Perte de sang moyenne

# Nettoyer les valeurs : extraire uniquement les chiffres et convertir en numérique
df["Pertes sanguines lors de la chirurgie"] = df["Pertes sanguines lors de la chirurgie"].astype(str).apply(lambda x: re.sub(r"[^\d]", "", x))

# Supprimer les lignes où il n'y a pas de chiffre (évite d'inclure du texte vide dans le calcul)
df["Pertes sanguines lors de la chirurgie"] = df["Pertes sanguines lors de la chirurgie"].replace("", pd.NA)

# Convertir en nombre (ignore les NaN automatiquement)
df["Pertes sanguines lors de la chirurgie"] = pd.to_numeric(df["Pertes sanguines lors de la chirurgie"], errors='coerce')

# Calculer la perte sanguine moyenne en excluant les valeurs vides
perte_sang_moyenne = df["Pertes sanguines lors de la chirurgie"].dropna().mean()


# Afficher le résultat
print(f"Pertes sanguines moyennes : {perte_sang_moyenne:.2f} cc")
print(f"###########3#")

#6)	Durée moyenne du séjour à l’hôpital

# Nettoyer les valeurs : extraire uniquement les chiffres et convertir en numérique
df["Durée séjour post-opération"] = df["Durée séjour post-opération"].astype(str).apply(lambda x: re.sub(r"[^\d]", "", x))

df["Durée séjour post-opération"] = df["Durée séjour post-opération"].replace("", pd.NA)

# Convertir en nombre (ignore les NaN automatiquement)
df["Durée séjour post-opération"] = pd.to_numeric(df["Durée séjour post-opération"], errors='coerce')

# Calculer la perte sanguine moyenne en excluant les valeurs vides
jour_moyen = df["Durée séjour post-opération"].dropna().mean()

print(f"Jours à l'hopital post op : {jour_moyen:.2f} jours")
print(f"############")


#7)	Incidence de ganglions positifs (la colonne N0, N1 ou N2) et métastases, et le taux de survie selon ce qu’ils ont
incidence_N0= df[df["Ganglions"].str.contains("N.0.", case=False, na=False)]
incidence_N0 = len(incidence_N0)

incidence_N1= df[df["Ganglions"].str.contains("N.1.", case=False, na=False)]
incidence_N1 = len(incidence_N1)

incidence_N2= df[df["Ganglions"].str.contains("N.2.", case=False, na=False)]
incidence_N2 = len(incidence_N2)

incidence_N0_5ans = df[df["Ganglions"].str.contains("N.0.", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_5_ans) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False)]
incidence_N0_5ans = len(incidence_N0_5ans)

incidence_N1_5ans = df[df["Ganglions"].str.contains("N.1.", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_5_ans) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False)]
incidence_N1_5ans = len(incidence_N1_5ans)

incidence_N2_5ans = df[df["Ganglions"].str.contains("N.2.", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_5_ans) &
    df["Survie 5 ans"].str.contains("Oui", case=False, na=False)]
incidence_N2_5ans = len(incidence_N2_5ans)

incidence_N0_10ans = df[df["Ganglions"].str.contains("N.0.", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_10_ans) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False)]
incidence_N0_10ans = len(incidence_N0_10ans)

incidence_N1_10ans = df[df["Ganglions"].str.contains("N.1.", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_10_ans) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False)]
incidence_N1_10ans = len(incidence_N1_10ans)

incidence_N2_10ans = df[df["Ganglions"].str.contains("N.2.", case=False, na=False) & (df["Date de la chirurgie"] <= date_limite_10_ans) &
    df["Survie 10 ans"].str.contains("Oui", case=False, na=False)]
incidence_N2_10ans = len(incidence_N2_10ans)

taux_survie_5_ans_N0 = (incidence_N0_5ans / incidence_N0) * 100
taux_survie_10_ans_N0 = (incidence_N0_10ans / incidence_N0) * 100
taux_survie_5_ans_N1 = (incidence_N1_5ans / incidence_N1) * 100
taux_survie_10_ans_N1 = (incidence_N1_10ans / incidence_N1) * 100
taux_survie_5_ans_N2 = (incidence_N2_5ans / incidence_N2) * 100
taux_survie_10_ans_N2 = (incidence_N2_10ans / incidence_N2) * 100

print(f"Nombre total de patients ayant N0 : {incidence_N0}")
print(f"Nombre de survivants à 5 ans ayant ganglions N0 : {incidence_N0_5ans}")
print(f"Taux de survie à 5 ans ayant ganglions N0  : {taux_survie_5_ans_N0:.2f} %")
print(f"Nombre de survivants à 10 ans ayant ganglions N0 : {incidence_N0_10ans}")
print(f"Taux de survie à 10 ans ayant ganglions N0  : {taux_survie_10_ans_N0:.2f} %")
print(f"############")

print(f"Nombre total de patients ayant N1 : {incidence_N1}")
print(f"Nombre de survivants à 5 ans ayant ganglions N1 : {incidence_N1_5ans}")
print(f"Taux de survie à 5 ans ayant ganglions N1  : {taux_survie_5_ans_N1:.2f} %")
print(f"Nombre de survivants à 10 ans ayant ganglions N1 : {incidence_N1_10ans}")
print(f"Taux de survie à 10 ans ayant ganglions N1  : {taux_survie_10_ans_N1:.2f} %")
print(f"############")

print(f"Nombre total de patients ayant N2 : {incidence_N2}")
print(f"Nombre de survivants à 5 ans ayant ganglions N2 : {incidence_N2_5ans}")
print(f"Taux de survie à 5 ans ayant ganglions N2  : {taux_survie_5_ans_N2:.2f} %")
print(f"Nombre de survivants à 10 ans ayant ganglions N2 : {incidence_N2_10ans}")
print(f"Taux de survie à 10 ans ayant ganglions N2  : {taux_survie_10_ans_N2:.2f} %")
print(f"############")

# Données pour les graphiques en secteurs (pie charts)
labels = ["Taux sans chimio", "Taux avec chimio", "Taux chimio post op"]
sizes_5_ans = [taux_survie_5_ans_nonchimio, taux_survie_5_ans_chimio, taux_survie_5_ans_chimiopostop]
sizes_10_ans = [taux_survie_10_ans_nonchimio, taux_survie_10_ans_chimio, taux_survie_10_ans_chimiopostop]
explode = (0.1, 0, 0)  # Pour détacher visuellement la part des survivants avec chimio

# Création des figures côte à côte
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Graphique pour la survie à 5 ans
axs[0].pie(sizes_5_ans, labels=labels, autopct='%1.1f%%', explode=explode, startangle=140)
axs[0].set_title("Taux de survie à 5 ans avec/sans chimio")

# Graphique pour la survie à 10 ans
axs[1].pie(sizes_10_ans, labels=labels, autopct='%1.1f%%', explode=explode, startangle=140)
axs[1].set_title("Taux de survie à 10 ans avec/sans chimio")

# Affichage du graphique
plt.show()

# Data
labels = ['SANS chimio', 'Chimio', 'Chimio post-op']
survie_5 = [taux_survie_5_ans_nonchimio, taux_survie_5_ans_chimio, taux_survie_5_ans_chimiopostop]
survie_10 = [taux_survie_10_ans_nonchimio, taux_survie_10_ans_chimio, taux_survie_10_ans_chimiopostop]

x = range(len(labels))

# Plotting
plt.figure(figsize=(8, 5))
plt.bar(x, survie_5, width=0.4, label='Survie à 5 ans', align='center')
plt.bar([i + 0.4 for i in x], survie_10, width=0.4, label='Survie à 10 ans', align='center')

# Labels & aesthetics
plt.xticks([i + 0.2 for i in x], labels)
plt.ylabel("Taux de survie (%)")
plt.title("Survie à 5 et 10 ans selon traitement")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

sizes_5 = [survie_5[0], survie_5[1], survie_5[2]]
labels = ["Sans chimio", "Chimio", "Chimio post-op"]
explode = (0.1, 0, 0)

stades = ["T0", "T1", "T2", "T3", "T4", "TiS"]
survie_5_stades = [taux_survie_5_ans_T0, taux_survie_5_ans_T1, taux_survie_5_ans_T2, taux_survie_5_ans_T3, taux_survie_5_ans_T4, taux_survie_5_ans_TiS]
survie_10_stades = [taux_survie_10_ans_T0, taux_survie_10_ans_T1, taux_survie_10_ans_T2, taux_survie_10_ans_T3, taux_survie_10_ans_T4, taux_survie_10_ans_TiS]

plt.figure(figsize=(8, 5))
plt.plot(stades, survie_5_stades, marker='o', label="Survie 5 ans")
plt.plot(stades, survie_10_stades, marker='s', label="Survie 10 ans")
plt.ylabel("Taux de survie (%)")
plt.title("Survie selon le stade tumoral")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()