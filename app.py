import streamlit as st
import pandas as pd


def bet(temps, montant, pwd, username, mode, message=None):
    df = pd.read_csv('data/paris.csv').fillna('')
    if 'Nouveau' not in mode:
        if len(df[(df['pwd'] == pwd) & (df['Pseudo'] == username)]) == 0:
            return 401
    if 'Changer' in mode:
        df.loc[(df['pwd'] == pwd) & (df['Pseudo'] == username), 'Temps'] = temps
        df.loc[(df['pwd'] == pwd) & (df['Pseudo'] == username), 'Montant'] = montant
        df.loc[(df['pwd'] == pwd) & (df['Pseudo'] == username), 'Message pour Lucas'] = message
    elif 'Supprimer' in mode:
        df = df[df['pwd'] != pwd]
    elif 'Nouveau' in mode:
        new = pd.DataFrame(columns=['Pseudo', 'Temps', 'Montant', 'Message pour Lucas', 'pwd'], data=[[username, temps, montant, message, pwd]])
        df = pd.concat([df, new])
    df.dropna().to_csv('data/paris.csv', index=None)
    return 200


st.image('img/logo2.png')

col1, col2, col3= st.columns([2,1,1])

with col1:
    st.write('')
    st.subheader('*Pariez sur le temps du coureur raleur !* 😠🏃')
with col2:
    st.header('75%')
    st.write('reversés à Lucas')
with col3:
    st.header('25%')
    st.write('pour le meilleur prono')


st.markdown("[Je parie !](#je-parie)", unsafe_allow_html=True)


st.markdown("""---""")

col1, col2= st.columns([2,1])
with col1:
    st.write('')
    st.write('')
    st.subheader('Quelle course ?')
    st.write('Lucas est inscrit au Harmonie Mutuelle Semi de Paris, qui aura lieu le Dimanche 5 Mars 2023. Retrouvez toutes les infos sur le semi ici : https://www.harmoniemutuellesemideparis.com/fr.')
with col2:
    st.image('img/logo_semi.jpeg')

st.markdown("""---""")

col1, col2= st.columns([1,2])
with col2:
    st.write('')
    st.write('')
    st.subheader('Comment aider Lucas ?')
    st.write("Les encouragements c'est bien, la thune c'est mieux 💸 ! Pariez ici sur le temps que fera Lucas au semi. 75% du montant total des paris sera reversé à Lucas - qu'importe son temps. Les 25% restants seront remis au parieur dont le pronostic sera le plus proche du temps réel de Lucas ☘️")
with col1:
    st.image('img/logo3.png')

st.markdown("""---""")
st.header('Les paris')
df = pd.read_csv('data/paris.csv').dropna()
df['Montant'] = df['Montant'].astype(int).astype(str) + ' euros'
del df['pwd']
st.markdown("""
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """, unsafe_allow_html=True)
st.table(df)

st.markdown("""---""")
st.header("Je parie !")
st.write('*Pas de paiement, simplement une promesse de pari à honorer après la course.*')

mode = st.radio(
     "",
     ('Nouveau pari', 'Changer mon pari', 'Supprimer mon pari'))

username = st.text_input('Pseudo')
pwd = st.text_input('Mot de passe')
if "Supprimer" not in mode:
    col1, col2, col3= st.columns([1,1,1])
    with col1:
        h = st.number_input('Heures', min_value=0, max_value=100)
    with col2:
        mn = st.number_input('Minutes', min_value=0, max_value=59)
    with col3:
        s = st.number_input('Secondes', min_value=0, max_value=59)
    temps = ":".join([str(i) for i in [h, mn, s]])
    montant = st.number_input('Montant parié (max. 30 euros)', min_value=5, max_value=30)
    message = st.text_input('Un message pour Lucas ?') 
else:
    temps, montant, message, h, mn, s = "","","","","","" 


if st.button(mode):
    if  ("Supprimer" in mode and any(i == '' for i in [username, pwd])) or ("Supprimer" not in mode  and any(i == '' or i == 0 for i in [username, pwd, h, mn, s, montant])):
        st.error('Remplis tous les champs puis réessaie !')
    elif "Nouveau" in mode and username in pd.read_csv('data/paris.csv')['Pseudo'].unique():
        st.error('Ce pseudo est déjà pris, choisis-en un autre...')
    else:
        out = bet(temps=temps, 
                montant=montant,
                pwd=pwd, 
                username=username, 
                message=message if message else '', 
                mode = mode)
        if out == 200:
            st.balloons()
            st.success('Merci ! Ton pari a bien été enregistré.')
        elif out == 401:
            st.error('Identifiants invalides !')
