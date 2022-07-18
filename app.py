import gspread
import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def authenticate(creds_path=None):
    """gc
    Refreshes the Sheets API credentials using the service account credentials stored in a json.
    """
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    if creds_path == None:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            str(path) + '/service_account_credentials.json', scope)
    else:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            creds_path, scope)
    gc = gspread.authorize(credentials)
    return gc

gc = authenticate('lucas-semi-1319e524581c.json')

def read_sheet(gc):    
    wks = gc.open_by_key('1iPYvh65Y_rLWE_wyCcWh3LNWs2spzT_CO65rUfCHCys')
    sheet = wks.worksheet('data')
    data = sheet.get_all_values()
    data = pd.DataFrame(data[1:], columns=data[0])
    return data


def write_df(df, gc):
    wks = gc.open_by_key('1iPYvh65Y_rLWE_wyCcWh3LNWs2spzT_CO65rUfCHCys')
    sheet = wks.worksheet('data')
    wks.values_clear(sheet.title)
    sheet.update('A1', [df.columns.values.tolist()] +
                 df.values.tolist(), value_input_option='USER_ENTERED')


def bet(temps, montant, pwd, username, mode, message=None):
    df = read_sheet(gc)
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
    write_df(df.dropna(), gc)
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
df = read_sheet(gc)
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
st.write('Enregistrez votre pari ici, puis payez sur la cagnotte Lydia : https://lydia-app.com/collect/91003-lucas-semi-2023/fr')

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
    if  ("Supprimer" in mode and any(i == '' for i in [username, pwd])) or ("Supprimer" not in mode  and any(i == '' for i in [username, pwd, montant])):
        st.error('Remplis tous les champs puis réessaie !')
    elif "Nouveau" in mode and username in read_sheet(gc)['Pseudo'].unique():
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
