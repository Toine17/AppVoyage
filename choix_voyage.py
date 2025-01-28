# On demande le choix de la pratique
pratique_choose =  st.selectbox("Quel type de pratique souhaitez vous ?",pratique)

# On calcul les bornes de la durée du séjour
    # La durée max selon la pratique choisie
jourMax = df_recap["Nombre jours max"].loc[df_recap['Terrain'] == pratique_choose].max()
    # La durée min selon la pratique choisie
jourMin = df_recap["Nombre jours min"].loc[df_recap['Terrain'] == pratique_choose].min()
    # Les bornes du milieu
lenght = list(range(jourMin,jourMax))
lenght.append(jourMax)

# Choix de la durée du séjour
DureeMax = st.select_slider("Choisissez une durée en jours de votre voyage", lenght, value=jourMax)
test = df_recap.loc[(df_recap['Terrain'] == pratique_choose) & (df_recap["Nombre jours min"] <= DureeMax)].reset_index()


# On affiche le tableau des voyages
st.write(test)

# Sauvegarde dans une liste des voyages conservés
list_voyage = test['Nom périple'].tolist()

# sauvegarde du choix du voyage
choix = int(test['id périple'].loc[test['Nom périple'] == st.radio("Choisissez votre voyage", list_voyage)].iloc[0])