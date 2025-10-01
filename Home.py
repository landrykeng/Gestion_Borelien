import streamlit as st
from Fonction import *
from PIL import Image
from Authentification import *


# Configuration de la page
st.set_page_config(
    page_title="Le Borelien",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

#import_users_from_excel()

load_all_data()
etudiants_df=st.session_state.etudiants_df
enseignants_df=st.session_state.enseignants_df
seances_df=st.session_state.seances_df
depenses_df=st.session_state.depenses_df
versements_df=st.session_state.versements_df
ventes_df=st.session_state.ventes_df
presence_df=st.session_state.presence_df
fiches_paie_df=st.session_state.fiches_paie_df
Connect_df=st.session_state.Connect_df



versements_df["Montant"]=versements_df["Montant"].astype(int)


# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .concours-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #2a5298;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
    }
    
    .info-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .center-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .chat-message-user {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        margin-left: 2rem;
        border-left: 4px solid #2196f3;
    }
    
    .chat-message-assistant {
        background: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        margin-right: 2rem;
        border-left: 4px solid #9c27b0;
    }
    
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # En-tête principal
    logo2=Image.open("logo2.png")
    logo1=Image.open("logo.jpg")
    st.image(logo1,width=1000)
    st.markdown('<div class="main-header"><h1>Bienvenue au Borelien</h1><p>Gestion des étudiants, enseignants et finances</p></div>', unsafe_allow_html=True)
    st.image(logo2,width=1000)

if __name__ == "__main__":
    main()