import pandas as pd
import streamlit as st

# Charger les données
df_recap = pd.read_csv('Liste voyages - Récap.csv')
df_etapes = pd.read_csv('Liste voyages - Details_etapes.csv')
df_pratique = pd.read_csv('Liste voyages - Pratique.csv')

# Initialiser les variables dans session_state pour conserver la valeur sur toutes les pages
if "current_page" not in st.session_state:
    st.session_state.current_page = 0  
if "choix_periple" not in st.session_state:
    st.session_state.choix_periple = None
if "DureeMax" not in st.session_state:
    st.session_state.DureeMax = None
if "nb_etapes" not in st.session_state:
    st.session_state.nb_etapes = []
if "Periple_possible" not in st.session_state:
    st.session_state.Periple_possible = [] 
if "choix_voyage" not in st.session_state:
    st.session_state.choix_voyage = []
if "pratique_choose" not in st.session_state:
    st.session_state.pratique_choose = [df_pratique.iloc[0]]
if "choix_nb_etapes" not in st.session_state:
    st.session_state.choix_nb_etapes = 0 
   

# Définir les différentes pages
########### Page accueil avec texte de présentation et photo #######################################################
def accueil():
    #st.title("Bienvenue sur l'application des aventures du cyclos")
    # titre centré par chatgpt
    st.markdown(
    """
    <h1 style="text-align: center;">Bienvenue sur l'application des aventures du Cyclos</h1>
    """,
    unsafe_allow_html=True
    )
    st.write("Vous aimez le vélo, mais les voyages tout organisés sur voie verte ne suffisent pas à satisfaire votre soif d'aventure ?")
    st.write("Vous êtes au bon endroit!")
    st.write("Sur cette application, vous trouverez des voyages à vélo qui sont de véritables aventures. Vous relèverez un défi physique dans des paysages magnifiques. Chaque voyage est adapté au niveau de chacun.")
    st.image('accueil.jpg')

########### Page de choix de la pratique #######################################################
def choix_pratique():
    #st.title("Quelle pratique souhaitez vous ?")
    st.markdown(
    """
    <h1 style="text-align: center;">Quelle pratique souhaitez vous ?</h1>
    """,
    unsafe_allow_html=True
    )
    # On défini les types de pratiques du dataframe
    pratique = df_pratique['Pratique'] 
    # On choisi la pratique
    st.session_state.pratique_choose = st.selectbox("",pratique) 
    # On selectionne le commentaire selon le choix de la pratique
    commentaire_pratique = df_pratique.loc[df_pratique['Pratique']==st.session_state.pratique_choose,'Commentaires'].iloc[0] 
    # On affiche le commentaire selon le choix de la pratique
    st.write(f"{commentaire_pratique}") 

########### Page Choix de la durée  #######################################################
def duree_periple ():    
    #st.title("Pour combien de jours voulez partir ?")
    st.markdown(
    """
    <h1 style="text-align: center;">Combien de jours voulez partir ?</h1>
    """,
    unsafe_allow_html=True
    )
    # Définition du nombre de jours maximum selon le choix de pratique
    jourMax = df_recap["Nombre jours max"].loc[df_recap['Terrain'] == st.session_state.pratique_choose].max() 
    # Définition du nombre de jours minimum selon le choix de pratique
    jourMin = df_recap["Nombre jours min"].loc[df_recap['Terrain'] == st.session_state.pratique_choose].min() 
    # On défini une liste pour le curseur
    lenght = list(range(jourMin, jourMax + 1)) 
    # Choix du nombre de jours par le curseur
    st.session_state.DureeMax = st.select_slider("",
                                                 lenght, value=jourMax) 
    # On enregistre les périples qui restent                                             
    st.session_state.Periple_possible = df_recap.loc[
        (df_recap['Terrain'] == st.session_state.pratique_choose) & (df_recap["Nombre jours min"] <= st.session_state.DureeMax)
        ].reset_index() 

########### Page du choix du voyage #######################################################
def choix_voyage_final():
    #st.title("Selon vos critères nous avons ces voyages à vous proposer")
    st.markdown(
    """
    <h1 style="text-align: center;">Selon vos critères nous avons ces voyages à vous proposer</h1>
    """,
    unsafe_allow_html=True
    )
    col1, col2 = st.columns([1, 1])
    with col1:
        # On transforme le df restant en liste pour le choix
        list_voyage = st.session_state.Periple_possible['Nom périple'].tolist() 
        # On choisit le voyage
        st.session_state.choix_periple = st.radio("Choisissez votre voyage", list_voyage) # On choisit le voyage
        # affichage des infos du voyage
        st.write("Un total de ",
            df_recap['Kilomètres'].loc[df_recap['Nom périple'] == st.session_state.choix_periple].to_string(index = False), 
            "km avec ",
            df_recap['Dénivelé'].loc[df_recap['Nom périple'] == st.session_state.choix_periple].to_string(index = False),
            "m de dénivelé positif")
        
    with col2:
        # affichage de l'image
        st.image(f"{df_recap['Photo'].loc[df_recap['Nom périple'] == st.session_state.choix_periple].to_string(index = False)}") 
    
     # affichage du commentaire
    st.write(df_recap.loc[df_recap['Nom périple'] == st.session_state.choix_periple,'Commentaire'].iloc[0]) 


########### Page qui détaille le voyage #######################################################
def details_voyage():
    #st.title("Détails du voyage")
    st.markdown(
    """
    <h1 style="text-align: center;">Détails du voyage</h1>
    """,
    unsafe_allow_html=True
    )
    # On défini l'id du voyage choisi dans la table df_recap
    choix = int(df_recap['id périple'].loc[df_recap['Nom périple'] == st.session_state.choix_periple].iloc[0])
    # On crée une liste avec le nombre d'étapes possibles
    st.session_state.nb_etapes = df_etapes['nb_etape_voyage'].loc[df_etapes['id_périple'] == choix].unique().tolist()
    # On supprime le nombre d'étape supérieur à la durée max choisi du voyage
    st.session_state.nb_etapes = [etape for etape in st.session_state.nb_etapes if etape <= st.session_state.DureeMax]
    # On choisi le nombre d'étape que l'on veut faire
    st.session_state.choix_nb_etapes = st.radio("En combien de jours voulez-vous faire ce voyage ?", st.session_state.nb_etapes)
    #On enregistre ce choix dans une variable
    st.session_state.choix_voyage = df_etapes.loc[
        (df_etapes['id_périple'] == choix) & (df_etapes['nb_etape_voyage'] == st.session_state.choix_nb_etapes)
    ]
    # On crée une liste d'entier allant de 1 au nombre d'étapes choisi
    liste_num_etape = list(range(1,st.session_state.choix_nb_etapes+1))
    # On affiche 2 colonnes
    col1, col2 = st.columns([1, 1])
    #Dans la colonne de gauche
    with col1:
        # le choix de l'étape
        num_etapes = st.radio("Vous avez le détail de chaque étape ci-contre", liste_num_etape)
        # On affcihe le commentaire sur l'étape
        #st.write(st.session_state.choix_voyage.loc[st.session_state.choix_voyage['num_etape'] == num_etapes,'Commentaire'].iloc[0])
  
    # Dans la colonne de droite    
    with col2:
        # Un affichage vide pour centrer avec la colonne de gauche
        st.write("")
        # On affiche les infos, départ, arrivée, km et dénivelé dans une phrase
        st.write("De",
        st.session_state.choix_voyage['depart_etape'].loc[st.session_state.choix_voyage['num_etape'] == num_etapes].to_string(index = False),
        " à ",
        st.session_state.choix_voyage['arrivee_etape'].loc[st.session_state.choix_voyage['num_etape'] == num_etapes].to_string(index = False))
        st.write("Un kilommétrage de",
        st.session_state.choix_voyage['kilomètres'].loc[st.session_state.choix_voyage['num_etape'] == num_etapes].to_string(index = False),"km")
        st.write("pour un dénivelé de ",
        st.session_state.choix_voyage['denivele'].loc[st.session_state.choix_voyage['num_etape'] == num_etapes].to_string(index = False),"m")
    if st.button("Je valide") :
        st.session_state.current_page += 1


########### Page de fin #######################################################
def validation():
    st.write("Merci beaucoup ! Nous espérons que votre aventure sera à la hauteur de vos attentes et qu'elle vous apportera de nombreux moments de plaisir. N'oubliez pas de profiter de chaque instant, de la beauté des paysages à la satisfaction de relever le défi. Bon voyage et à bientôt sur les routes !")
    st.write("Vous venez de valider le voyage ",st.session_state.choix_periple,"en",str(st.session_state.choix_nb_etapes),"jours"  )


# Liste des pages
pages = [accueil, choix_pratique,duree_periple, choix_voyage_final, details_voyage, validation]
page_names = ["Accueil", "Choix de la pratique","Durée du périple", "Liste des voyages", "Détails du voyage", "page de validation"]

# Navigation par boutons
col1, col2 = st.columns([4, 1])
with col1:
    if st.button("Page précédente"): 
        if st.session_state.current_page > 0 : # Si on est à la première page il ne se passe rien
            st.session_state.current_page -= 1

with col2:
    if st.button("Page suivante"): 
        if st.session_state.current_page < len(pages) - 1 : # Si on est à la dernière page il ne se passe rien
            st.session_state.current_page += 1

# Afficher la page actuelle
#st.sidebar.write(f"{page_names[st.session_state.current_page]}") #affiche le nom de la page actuelle sur le côté
pages[st.session_state.current_page]() # appelle la fonction de la page pour l'éxécuter ce qui rend la page active