import streamlit as st
from Fonction import *
from Authentification import *





# Configuration de la page


# CSS personnalisé pour l'interface admin
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #8b0000 0%, #dc143c 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .admin-info {
        background: linear-gradient(135deg, #2f13d8 0%, #ff6b6b 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-left: 4px solid #dc143c;
    }
    
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #dc143c 0%, #ff6b6b 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
    }
    
    .login-container {
        background: white;
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        max-width: 500px;
        margin: 2rem auto;
        border-top: 5px solid #dc143c;
    }
    
    .teacher-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc143c;
        margin-bottom: 1rem;
    }
    
    .payroll-card {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    
    .danger-zone {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #dc3545;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# CSS personnalisé
management_css = """
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-left: 4px solid #1e3c72;
    }
    
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
    }
    
    .data-table {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .student-profile {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .search-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 2px solid #1e3c72;
    }
    
    .receipt-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        border: 2px solid #28a745;
    }
    
    .absent-student-card {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin-bottom: 1rem;
    }
</style>
"""

table_css = """
<style>
/* Style général des tableaux */
.stDataFrame {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border-radius: 10px;
    overflow: hidden;
}

/* En-tête du tableau */
.stDataFrame thead {
    background-color: #1e3c72;
    color: white;
    font-weight: bold;
}

/* Lignes du tableau */
.stDataFrame tbody tr:nth-child(even) {
    background-color: #f8f9fa;
}

.stDataFrame tbody tr:nth-child(odd) {
    background-color: #ffffff;
}

/* Effet de survol */
.stDataFrame tbody tr:hover {
    background-color: #e9ecef;
    transition: background-color 0.3s ease;
}

/* Cellules */
.stDataFrame th, .stDataFrame td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #dee2e6;
}

/* Style des colonnes */
.stDataFrame th {
    text-transform: uppercase;
    font-size: 0.9em;
    letter-spacing: 1px;
}
</style>
"""

  

def main():
    st.markdown(table_css, unsafe_allow_html=True)
    st.markdown(management_css, unsafe_allow_html=True)
    
    is_authenticated = authentication_system("Administrateur")
    
    if is_authenticated:
        
        #st.set_page_config(
            #page_title="Admin - STATO-SPHERE PREPAS",
            #page_icon="⚡",
            #layout="wide",
            #initial_sidebar_state="expanded"
        #)
        
        user = st.session_state['username']
        #from Home import etudiants_df, enseignants_df, depenses_df, versements_df, ventes_df, Connect_df,seances_df, presence_df
        
        etudiants_df=st.session_state.etudiants_df
        enseignants_df=st.session_state.enseignants_df
        seances_df=st.session_state.seances_df
        depenses_df=st.session_state.depenses_df
        versements_df=st.session_state.versements_df
        ventes_df=st.session_state.ventes_df
        presence_df=st.session_state.presence_df
        presences_df=st.session_state.presences_df
        fiches_paie_df=st.session_state.fiches_paie_df
        Connect_df=st.session_state.Connect_df

        st.markdown(f"""
            <div class="admin-info">
                <h2>⚡ Tableau de Bord </h2>
                <p><strong>Connecté en tant que :</strong> {user.upper()}</p>
                <p><strong>Droits :</strong> Accès complet à toutes les fonctionnalités</p>
            </div>
            """, unsafe_allow_html=True)
        
        
        refresh=st.sidebar.button("Actualiser")
        if refresh:
            with st.spinner("Chargement des données...",show_time=True):
                st.session_state.etudiants_df = read_from_google_sheet("Étudiants")
                st.session_state.enseignants_df = read_from_google_sheet("Enseignants")
                st.session_state.seances_df = read_from_google_sheet("Séances")
                st.session_state.depenses_df = read_from_google_sheet("Dépenses")
                st.session_state.versements_df = read_from_google_sheet("Versements")
                st.session_state.ventes_df = read_from_google_sheet("Ventes_Bords")
                st.session_state.presence_df = read_from_google_sheet("Présences")
                st.session_state.presences_df = read_from_google_sheet("Présences")
                st.session_state.fiches_paie_df = read_from_google_sheet("Fiches_Paie")
                st.session_state.Connect_df = read_from_google_sheet("Connexion")
            #st.rerun()  # relance la page et recharge les données

        #etudiants_df, enseignants_df, seances_df, depenses_df, versements_df, ventes_df, presence_df, presences_df, fiches_paie_df, Connect_df=load_all_data()
        tab= st.tabs([
                "🏠 Accueil",
                "💰 Gestion Financière",
                "📚 Gestion des Étudiants",
                "👨‍🏫 Gestion des Enseignants",
                "📋 Gestion des Présences",
            ])
        
            # ====================== ONGLET ACCUEIL ======================
        with tab[0]:
            # Calcul de l'aire de chaque table (nombre de lignes * nombre de colonnes)
            tables = [etudiants_df, enseignants_df, seances_df, depenses_df, versements_df, ventes_df, presence_df, fiches_paie_df, Connect_df]
            aires = [df.shape[0] * df.shape[1] for df in tables]
            space_used = round(sum(aires)/100000,2)
            st.markdown(f"Stockage utilisé : {space_used} %")
            
            st.markdown("## <div class=\"form-container\"> 🏠 Bienvenue sur le Tableau de Bord Administrateur</div>", unsafe_allow_html=True)
            Connect_df
        with tab[1]:
            st.markdown("## <div class=\"form-container\"> 💰 Gestion Financière</div>", unsafe_allow_html=True)
            st.dataframe(versements_df)
            depenses_df
            ventes_df
        with tab[2]:
            st.markdown("## <div class=\"form-container\"> 📚 Gestion des Étudiants</div>", unsafe_allow_html=True)
            etudiants_df
        with tab[3]:
            st.markdown("## <div class=\"form-container\"> 👨‍🏫 Gestion des Enseignants</div>", unsafe_allow_html=True)
            st.dataframe(enseignants_df)
            st.dataframe(seances_df)
        with tab[4]:
            st.markdown("## <div class=\"form-container\"> 📋 Gestion des Présences</div>", unsafe_allow_html=True)
            st.dataframe(presence_df)
    
        #Enregistrement des données de connexion 
        data_connection=[user,'Administrateur', datetime.now().strftime('%Y-%m-%d %H:%M:%S')] 
        save_to_google_sheet("Connexion", data_connection)  
if __name__ == "__main__":
    main()