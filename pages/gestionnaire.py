import streamlit as st
import pandas as pd
from datetime import datetime, date
from pathlib import Path
import openpyxl
from openpyxl import Workbook
from Authentification import *
from Fonction import *
import base64
from io import BytesIO





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
    
    is_authenticated = authentication_system("Gestionnaire")
    
    if is_authenticated:
        #st.set_page_config(
            #page_title="Gestionnaire - LE BORELIEN",
           # page_icon="🧑‍💻",
           # layout="wide",
           # initial_sidebar_state="expanded"
       # )
        
        #from Home import etudiants_df, enseignants_df, depenses_df, versements_df, ventes_df, presences_df
        user = st.session_state['username']
        st.sidebar.title("Interface Gestionnaire")
        st.sidebar.write(f"Bienvenue, {user}!")

        etudiants_df=st.session_state.etudiants_df
        enseignants_df=st.session_state.enseignants_df
        seances_df=st.session_state.seances_df
        depenses_df=st.session_state.depenses_df
        versements_df=st.session_state.versements_df
        ventes_df=st.session_state.ventes_df
        presences_df=st.session_state.presences_df
        fiches_paie_df=st.session_state.fiches_paie_df
        Connect_df=st.session_state.Connect_df

        

        #etudiants_df, enseignants_df, seances_df, depenses_df, versements_df, ventes_df, presence_df, presences_df, fiches_paie_df, Connect_df=load_all_data()   

        
        # ============== INTERFACE PRINCIPALE ==============
        
        # En-tête principal
        st.markdown("""
        <div class="main-header">
            <h1>📊 Gestion - LE BORELIEN</h1>
            <h3>Interface d'Administration</h3>
            <p>Gestion des étudiants, finances et opérations</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Statistiques rapides
        col1, col2, col3, col4 = st.columns(4)
        


        # Interface à onglets
        tab1, tab2, tab3, tab4, tab5, tab6,tab7 = st.tabs([
            "👥 Étudiants", "💸 Dépenses", "💰 Versements", 
            "📚 Ventes Bords", "📋 Présences", 
            "📊 Absentéisme","Contrôle"
        ])
        
        # ==================== ONGLET ÉTUDIANTS ====================
        with tab1:
            st.markdown("## 👥 Gestion des Étudiants")
            
            col1, col2 = st.columns([2, 2])
            
            with col1:
                st.markdown("### ➕ Enregistrer un Nouvel Étudiant")
                
                with st.form("form_etudiant"):
                    col_a, col_b = st.columns([1,2])
                    
                    with col_a:
                        nom = st.text_input("Nom *", placeholder="Ex: DUPONT")
                        prenom = st.text_input("Prénom *", placeholder="Ex: Jean")
                        sexe = st.selectbox("Sexe *", SEXE_CHOICES)
                        filiere = st.selectbox("Filière *", FILIERE_CHOICES)
                        
                    
                    with col_b:
                        date_arrivee = st.date_input("Date d'arrivée *", value=date.today())
                        telephone = st.text_input("Téléphone", placeholder="Ex: +237670123456")
                        telephone_parent = st.text_input("Téléphone Parent", placeholder="Ex: +237670123456")
                        montant_a_payer = st.number_input("Montant à payer (FCFA)", min_value=0, step=1000)
                        echeance_paiement = st.date_input("Échéance de paiement", value=date.today() + timedelta(days=10))
                        
                    submitted = st.form_submit_button("🎓 Enregistrer l'Étudiant", type="primary")
                    
                    if submitted:
                        if nom and prenom and sexe and filiere:
                            matricule = generate_matricule()
                            
                            data = [
                                matricule, nom, prenom, sexe, filiere, 
                                telephone, telephone_parent, date_arrivee.strftime('%Y-%m-%d'), montant_a_payer,echeance_paiement
                            ]
                            
                            if save_to_google_sheet("Étudiants", data):
                                st.session_state.etudiants_df = read_from_google_sheet("Étudiants")
                                st.markdown(f"""
                                <div class="success-box">
                                    ✅ <strong>Étudiant enregistré avec succès !</strong><br>
                                    Matricule généré: <strong>{matricule}</strong>
                                </div>
                                """, unsafe_allow_html=True)
                                st.balloons()
                            else:
                                st.markdown("""
                                <div class="error-box">
                                    ❌ Erreur lors de l'enregistrement. Veuillez réessayer.
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="error-box">
                                ⚠️ Veuillez remplir tous les champs obligatoires (*)
                            </div>
                            """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("## 🔍 Recherche et Profil Étudiant")
            
                st.markdown('<div class="search-container">', unsafe_allow_html=True)
                st.markdown("### 🔍 Rechercher un Étudiant")
                
                # Barre de recherche
                search_query = st.text_input(
                    "🔍 Tapez le nom, prénom ou matricule de l'étudiant",
                    placeholder="Ex: DUPONT ou Jean ou STAT20250101ABCD",
                    key="student_search"
                )
                
                if search_query:
                    # Effectuer la recherche
                    search_results = search_student(search_query, etudiants_df)
                    
                    if not search_results.empty:
                        st.markdown(f"### 📋 Résultats de la recherche ({len(search_results)} trouvé(s))")
                        
                        # Afficher les résultats sous forme de sélection
                        for idx, student in search_results.iterrows():
                            if st.button(f"👤 {student['Nom']} {student['Prénom']} - {student['Matricule']}", key=f"select_{idx}"):
                                st.session_state['selected_student'] = student
                                st.rerun()
                    else:
                        st.warning("🚫 Aucun étudiant trouvé avec cette recherche")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            # Affichage du profil de l'étudiant sélectionné
            if 'selected_student' in st.session_state:
                    student = st.session_state['selected_student']
                    
                    # Calcul des statistiques de l'étudiant
                    #presences_df = read_from_google_sheet("Présences")
                    stats = calculate_student_stats(student['Matricule'], versements_df, presences_df, seances_df)
                    
                    st.markdown("---")
                    st.markdown(f"""
                    <div class="student-profile">
                        <h2>👤 Profil de {student['Nom']} {student['Prénom']}</h2>
                        <p><strong>Matricule:</strong> {student['Matricule']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Informations personnelles
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 📋 Informations Personnelles")
                        st.write(f"**Nom:** {student['Nom']}")
                        st.write(f"**Prénom:** {student['Prénom']}")
                        st.write(f"**Sexe:** {student['Sexe']}")
                        st.write(f"**Téléphone:** {student.get('Téléphone', 'Non renseigné')}")
                        st.write(f"**Téléphone Parent:** {student.get('Téléphone Parent', 'Non renseigné')}")
                        st.write(f"**Date d'arrivée:** {student['DateArrivée']}")
                        st.write(f"**Montant à payer:** {student.get('Montant a Payer', 0):,.0f} FCFA")
                    
                    with col2:
                        st.markdown("#### Filière")
                        st.write(f"**Filière:** {student['Filière']}")
                        st.markdown("#### 💰 Finances")
                        st.write(f"**Total versé:** {stats['total_verse']:,.0f} FCFA")
                        st.write(f"**Nombre de versements:** {stats['nombre_versements']}")
                    
                    with col3:
                        st.markdown("#### 📊 Assiduité")
                        st.write(f"**Total séances:** {stats['total_seances']}")
                        st.write(f"**Présences:** {stats['seances_presentes']}")
                        st.write(f"**Absences:** {stats['seances_absentes']}")
                        st.write(f"**Retards:** {stats['seances_retard']}")
                        
                        if stats['total_seances'] > 0:
                            if stats['taux_absenteisme'] <= 10:
                                st.success(f"**Taux d'absentéisme:** {stats['taux_absenteisme']:.1f}% 🟢")
                            elif stats['taux_absenteisme'] <= 25:
                                st.warning(f"**Taux d'absentéisme:** {stats['taux_absenteisme']:.1f}% 🟡")
                            else:
                                st.error(f"**Taux d'absentéisme:** {stats['taux_absenteisme']:.1f}% 🔴")
                        else:
                            st.info("**Taux d'absentéisme:** Aucune séance enregistrée")
                    
                    # Bouton pour effacer la sélection
                    if st.button("🗑️ Effacer la sélection"):
                        del st.session_state['selected_student']
                        st.rerun()
        
        # ==================== ONGLET DÉPENSES ====================
        with tab2:
            st.markdown("## 💸 Gestion des Dépenses")
            
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown("### ➕ Enregistrer une Nouvelle Dépense")
            
            with st.form("form_depense"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    motif_depense = st.text_input("Motif de la dépense *", placeholder="Ex: Achat de matériel")
                    type_depense = st.selectbox("Type de dépense *", TYPE_DEPENSE_CHOICES)
                
                with col_b:
                    date_depense = st.date_input("Date *", value=date.today())
                    montant = st.number_input("Montant (FCFA) *", min_value=0, step=1000)
                
                submitted_depense = st.form_submit_button("💳 Enregistrer", type="primary")
                if submitted_depense:
                    if motif_depense and type_depense and montant > 0:
                        id_depense = len(depenses_df) + 1
                        data = [
                            id_depense, motif_depense, type_depense, date_depense.strftime('%Y-%m-%d'), montant
                        ]
                        
                        if save_to_google_sheet("Dépenses", data):
                            st.session_state.depenses_df = read_from_google_sheet("Dépenses")
                            st.success(f"✅ Dépense de {montant:,} FCFA enregistrée")
                        else:
                            st.error("❌ Erreur lors de l'enregistrement")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ==================== ONGLET VERSEMENTS ====================
        with tab3:
            st.markdown('## <div class="form-container"> 💰 Gestion des Versements', unsafe_allow_html=True)
            col1, col2 = st.columns([2, 1])
            
            with col1:
                
                st.markdown("### ➕ Enregistrer un Nouveau Versement")
                
                with st.form("form_versement"):
                    col_a, col_b = st.columns(2)
                
                    with col_a:
                        if not etudiants_df.empty:
                            etudiants_list = [f"{row['Matricule']} - {row['Nom']} {row['Prénom']}" 
                                            for _, row in etudiants_df.iterrows()]
                            etudiant_selectionne = st.selectbox("Étudiant *", etudiants_list)
                            matricule_etudiant = etudiant_selectionne.split(" - ")[0] if etudiant_selectionne else ""
                        else:
                            matricule_etudiant = ""
                        montant_versement = st.number_input("Montant (FCFA) *", min_value=0, step=1000)
                        
                    
                    with col_b:
                        date_versement = st.date_input("Date *", value=date.today())
                        motif_versement = st.text_input("Motif", placeholder="Ex: Frais d'inscription")
                        moyen_paiment = st.selectbox("Moyen de paiement", MOYEN_PAIEMENT_CHOICES)
                    
                    submitted_versement = st.form_submit_button("💵 Enregistrer le Versement", type="primary")
                    
                    if submitted_versement:
                        if date_versement and montant_versement > 0 and matricule_etudiant:
                            id_versement = len(versements_df) + 1
                            
                            data = [
                                id_versement, date_versement.strftime('%Y-%m-%d'), motif_versement,
                                montant_versement, matricule_etudiant, moyen_paiment
                            ]
                            
                            if save_to_google_sheet("Versements", data):
                                st.session_state.versements_df = read_from_google_sheet("Versements")
                                st.markdown(f"""
                                <div class="success-box">
                                    ✅ <strong>Versement enregistré avec succès !</strong><br>
                                    Montant: <strong>{montant_versement:,.0f} FCFA</strong>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Générer le reçu
                                student_info = etudiants_df[etudiants_df['Matricule'] == matricule_etudiant].iloc[0]
                                versement_info = {
                                    'date': date_versement.strftime('%d/%m/%Y'),
                                    'montant': montant_versement,
                                    'motif': motif_versement
                                }
                                
                                receipt_html = generate_receipt_html(student_info, versement_info)
                                
                                st.markdown("---")
                                st.markdown("### 📄 Reçu de Paiement")
                                
                                col_receipt1, col_receipt2 = st.columns([3, 1])
                                
                                with col_receipt1:
                                    st.markdown(f"""
                                    <div class="receipt-container">
                                        <h4>🎓 Reçu généré automatiquement</h4>
                                        <p><strong>Étudiant:</strong> {student_info['Nom']} {student_info['Prénom']}</p>
                                        <p><strong>Matricule:</strong> {student_info['Matricule']}</p>
                                        <p><strong>Montant:</strong> {montant_versement:,.0f} FCFA</p>
                                        <p><strong>Date:</strong> {date_versement.strftime('%d/%m/%Y')}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with col_receipt2:
                                    # Bouton de téléchargement du reçu
                                    b64 = base64.b64encode(receipt_html.encode()).decode()
                                    href = f'data:text/html;base64,{b64}'
                                    st.markdown(f'<a href="{href}" download="recu_{matricule_etudiant}_{date_versement.strftime("%Y%m%d")}.html"><button style="background-color: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">📥 Télécharger le Reçu</button></a>', unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div class="error-box">
                                    ❌ Erreur lors de l'enregistrement.
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="error-box">
                                ⚠️ Veuillez remplir tous les champs obligatoires
                            </div>
                            """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                pass
        
        # ==================== ONGLET VENTES ====================
        
        with tab4:
            st.markdown("## 📚 Gestion des Ventes de Bords")
            
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            
            with st.form("form_vente"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    date_vente = st.date_input("Date *", value=date.today())
                    bord_vendu = st.selectbox("Bords vendus *", [f"Bords de {c}" for c in FILIERE_CHOICES])
                    nom_acheteur = st.text_input("Nom de l'acheteur *")
                
                with col_b:
                    nombre_bords = st.number_input("Nombre d'exemplaires *", min_value=1, value=1)
                    montant_vente = st.number_input("Montant total (FCFA) *", min_value=0, step=500)
                    contact_acheteur = st.text_input("Contact acheteur")
                
                
                submitted_vente = st.form_submit_button("📖 Enregistrer", type="primary")
                
                if submitted_vente:
                    if date_vente and bord_vendu and nom_acheteur and montant_vente > 0:
                        id_vente = len(ventes_df) + 1
                        data = [
                            id_vente, bord_vendu, nom_acheteur, contact_acheteur,
                            nombre_bords, montant_vente, date_vente.strftime('%Y-%m-%d')
                        ]
                        
                        if save_to_google_sheet("Ventes_Bords", data):
                            st.session_state.ventes_df = read_from_google_sheet("Ventes_Bords")
                            st.success(f"✅ Vente de {montant_vente:,} FCFA enregistrée")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ==================== ONGLET PRÉSENCES ====================
        with tab5:
            st.markdown("## 📋 Gestion des Présences - Appel Interactif")
            
            # Initialisation des variables de session pour l'appel
            if "appel_started" not in st.session_state:
                st.session_state.appel_started = False
            if "current_student_index" not in st.session_state:
                st.session_state.current_student_index = 0
            if "presences_data" not in st.session_state:
                st.session_state.presences_data = {}
            if "etudiants_appel" not in st.session_state:
                st.session_state.etudiants_appel = []
            
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            
            if not st.session_state.appel_started:
                # === PHASE 1: Configuration de l'appel ===
                st.markdown("### ⚙️ Configuration de l'Appel")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    #centre_appel = st.selectbox("📍 Centre *", CENTRES_CHOICES, key="centre_config")
                    
                    # Sélection multiple des concours
                    concours_appel = st.multiselect(
                        "🎓 Concours *", 
                        FILIERE_CHOICES, 
                        default=[FILIERE_CHOICES[0]],
                        key="concours_config"
                    )
                    
                    # Liste des enseignants (ici on peut lire depuis Excel ou avoir une liste prédéfinie)
                    enseignants_list = [
                        "Dr. MBANG Pierre", "Prof. NJOYA Marie", "M. FOMBA Jean",
                        "Mme. KAMGA Sylvie", "Dr. TCHOUMI Paul", "Prof. NANA Claire"
                    ]
                    enseignant = st.selectbox("👨‍🏫 Enseignant *", enseignants_df['Nom'].tolist() if not enseignants_df.empty else ["Enseignant Test"], key="enseignant_config")
                
                with col2:
                    # Liste des cours/matières
                    cours_list = COURS_CHOICES
                    cours = st.selectbox("📚 Matière/Cours *", cours_list, key="cours_config")
                    
                    intitule_cours = st.text_input(
                        "📝 Intitulé du cours *", 
                        placeholder="Ex: Analyse mathématique - Chapitre 3",
                        key="intitule_config"
                    )
                    
                    date_appel = st.date_input("📅 Date", value=date.today(), key="date_config")
                    heure_debut = st.time_input("🕐 Heure de début", key="heure_config")
                
                # Filtrage des étudiants selon les critères
                if not etudiants_df.empty and concours_appel:
                    etudiants_filtres = etudiants_df
                    
                    # Filtrer par concours (OR entre les concours sélectionnés)
                    etudiants_filtres = etudiants_filtres[(etudiants_filtres['Filière'].isin(concours_appel)) ]
                    etudiants_filtres=etudiants_filtres.sort_values(by=["Nom","Prénom"])
                    # Affichage du résumé
                    st.markdown("---")
                    st.markdown("### 📊 Résumé de l'Appel")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("👥 Étudiants à appeler", len(etudiants_filtres))
                    with col_b:
                        pass #st.metric("📍 Centre", centre_appel)
                    with col_c:
                        st.metric("🎓 Concours", len(concours_appel))
                    
                    if len(etudiants_filtres) > 0:
                        st.markdown("**Aperçu des étudiants :**")
                        preview_df = etudiants_filtres[['Nom', 'Prénom', 'Filière']].head(5)
                        st.dataframe(preview_df, use_container_width=True)
                        
                        if len(etudiants_filtres) > 5:
                            st.caption(f"... et {len(etudiants_filtres) - 5} autres étudiants")
                        
                        # Bouton pour démarrer l'appel
                        if st.button("🚀 Démarrer l'Appel", type="primary", use_container_width=True):
                            if enseignant and cours and intitule_cours:
                                # Sauvegarder les paramètres dans la session
                                st.session_state.appel_config = {
                                    "concours": concours_appel,
                                    "enseignant": enseignant,
                                    "cours": cours,
                                    "intitule": intitule_cours,
                                    "date": date_appel,
                                    "heure_debut": heure_debut
                                }
                                st.session_state.etudiants_appel = etudiants_filtres.to_dict('records')
                                st.session_state.appel_started = True
                                st.session_state.current_student_index = 0
                                st.session_state.presences_data = {}
                                st.rerun()
                            else:
                                st.error("⚠️ Veuillez remplir tous les champs obligatoires")
                    else:
                        st.warning("Aucun étudiant trouvé pour les critères sélectionnés")
                else:
                    if etudiants_df.empty:
                        st.warning("Aucun étudiant enregistré dans le système")
            
            else:
                # === PHASE 2: Appel en cours ===
                config = st.session_state.appel_config
                etudiants = st.session_state.etudiants_appel
                current_index = st.session_state.current_student_index
                total_students = len(etudiants)
                
                # En-tête de l'appel
                st.markdown(f"""
                ### 📋 Appel en Cours
                **📚 {config['cours']}** - {config['intitule']}  
                **👨‍🏫 Enseignant:** {config['enseignant']} |**📅 Date:** {config['date']}
                """)
                
                # Barre de progression
                progress = current_index / total_students if total_students > 0 else 0
                st.progress(progress, text=f"Étudiant {current_index} sur {total_students}")
                
                if current_index < total_students:
                    # Affichage des 3 étudiants (précédent, actuel, suivant)
                    st.markdown("---")

                    col1, col2 = st.columns(2) 

                    with col1:
                        # Étudiant précédent
                        if current_index > 0:
                            prev_student = etudiants[current_index - 1]
                            prev_status = st.session_state.presences_data.get(prev_student['Matricule'], "")
                            status_icon = "✅" if prev_status == "Présent" else "❌" if prev_status == "Absent" else ""
                            
                            if prev_status == "Présent":
                                st.success(f"{prev_student['Nom']} {prev_student['Prénom']} : {status_icon} {prev_status}") 
                            else:
                                st.error(f"{prev_student['Nom']} {prev_student['Prénom']} : {status_icon} {prev_status}")
                            
                        else:
                            st.markdown("""
                            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; text-align: center;">
                                <h5>👤 Précédent</h5>
                                <p><em>Premier étudiant</em></p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Étudiant en cours
                        current_student = etudiants[current_index]
                        st.warning(f"{current_student['Nom']} {current_student['Prénom']}")
                        # Étudiant suivant
                        if current_index + 1 < total_students:
                            next_student = etudiants[current_index + 1]
                            st.info(f"👤 Suivant: {next_student['Nom']} {next_student['Prénom']} (En attente...)")
                            
                    # Étudiant actuel
                    with col2:
                        pass
                    
                    # Boutons de présence
                    st.markdown("---")
                    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                    
                    with col_btn1:
                        if st.button("❌ ABSENT", use_container_width=True, type="secondary"):
                            matricule = current_student['Matricule']
                            st.session_state.presences_data[matricule] = "Absent"
                            st.session_state.current_student_index += 1
                            st.rerun()
                    
                    with col_btn2:
                        if st.button("✅ PRÉSENT", use_container_width=True, type="primary"):
                            matricule = current_student['Matricule']
                            st.session_state.presences_data[matricule] = "Présent"
                            st.session_state.current_student_index += 1
                            st.rerun()
                    
                    with col_btn3:
                        if st.button("⚠️ RETARD", use_container_width=True):
                            matricule = current_student['Matricule']
                            st.session_state.presences_data[matricule] = "Retard"
                            st.session_state.current_student_index += 1
                            st.rerun()
                    
                    # Bouton d'abandon
                    st.markdown("---")
                    if st.button("🔙 Abandonner l'appel", type="secondary"):
                        # Reset de l'appel
                        st.session_state.appel_started = False
                        st.session_state.current_student_index = 0
                        st.session_state.presences_data = {}
                        st.session_state.etudiants_appel = []
                        st.rerun()
                
                else:
                    # === PHASE 3: Appel terminé ===
                    st.markdown("### 🎉 Appel Terminé !")
                    
                    # Résumé des présences
                    presents = sum(1 for status in st.session_state.presences_data.values() if status == "Présent")
                    absents = sum(1 for status in st.session_state.presences_data.values() if status == "Absent")
                    retards = sum(1 for status in st.session_state.presences_data.values() if status == "Retard")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("👥 Total", total_students)
                    with col2:
                        st.metric("✅ Présents", presents)
                    with col3:
                        st.metric("❌ Absents", absents)
                    with col4:
                        st.metric("⚠️ Retards", retards)
                    
                    # Tableau récapitulatif
                    st.markdown("### 📊 Récapitulatif des Présences")
                    recap_data = []
                    for etudiant in etudiants:
                        matricule = etudiant['Matricule']
                        status = st.session_state.presences_data.get(matricule, "Non pointé")
                        recap_data.append({
                            "Matricule": matricule,
                            "Nom": etudiant['Nom'],
                            "Prénom": etudiant['Prénom'],
                            "Statut": status
                        })
                    
                    recap_df = pd.DataFrame(recap_data)
                    st.dataframe(recap_df, use_container_width=True)
                    
                    # Boutons d'action
                    col_save, col_restart = st.columns(2)
                    
                    with col_save:
                        if st.button("💾 Enregistrer les Présences", type="primary", use_container_width=True):
                            #presences_df = read_from_google_sheet("Présences")
                            success_count = 0
                            
                            for matricule, statut in st.session_state.presences_data.items():
                                id_presence = len(presences_df) + success_count + 1
                                data = [
                                    id_presence, matricule, 
                                    f"{config['cours']} - {config['intitule']}", 
                                    statut, 
                                    config['date'].strftime('%Y-%m-%d'), 
                                    1  # idEnseignant par défaut (à améliorer)
                                ]
                                
                                if save_to_google_sheet("Présences", data):
                                    success_count += 1
                            
                            if success_count > 0:
                                st.session_state.presence_df = read_from_google_sheet("Présences")
                                st.success(f"✅ {success_count} présences enregistrées avec succès !")
                                # Reset après sauvegarde
                                st.session_state.appel_started = False
                                st.session_state.current_student_index = 0
                                st.session_state.presences_data = {}
                                st.session_state.etudiants_appel = []
                                st.balloons()
                            else:
                                st.error("❌ Erreur lors de l'enregistrement des présences")
                    
                    with col_restart:
                        if st.button("🔄 Nouvel Appel", use_container_width=True):
                            # Reset pour un nouvel appel
                            st.session_state.appel_started = False
                            st.session_state.current_student_index = 0
                            st.session_state.presences_data = {}
                            st.session_state.etudiants_appel = []
                            st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
       
        # ====================== ONGLET ABSENTÉISME ======================
        with tab6:
            st.markdown("## <div class=\"form-container\"> 📊 Analyse de l'Absentéisme</div>", unsafe_allow_html=True)
            st.markdown("### ⚙️ Paramètres d'Analyse")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                start_date_abs = st.date_input("📅 Date de début", value=date.today().replace(day=1), key="abs_start")
            
            with col2:
                end_date_abs = st.date_input("📅 Date de fin", value=date.today(), key="abs_end")
            
            with col3:
                min_absences = st.number_input("🎯 Minimum d'absences", min_value=1, max_value=10, value=2, key="min_abs")
            
            if st.button("📊 Analyser l'Absentéisme", type="primary"):
                #presences_df = read_from_google_sheet("Présences")
                absent_students = get_absent_students(start_date_abs, end_date_abs, min_absences, presences_df, etudiants_df)
                
                if not absent_students.empty:
                    st.markdown(f"### 📋 Étudiants Absentéistes ({len(absent_students)} trouvé(s))")
                    st.markdown(f"**Période:** {start_date_abs.strftime('%d/%m/%Y')} - {end_date_abs.strftime('%d/%m/%Y')}")
                    st.markdown(f"**Critère:** Au moins {min_absences} absence(s)")
                    
                    # Affichage en cartes
                    for idx, student in absent_students.iterrows():
                        st.markdown(f"""
                        <div class="absent-student-card">
                            <h4>⚠️ {student['Nom']} {student['Prénom']}</h4>
                            <p><strong>🎓 Filière:</strong> {student['Filière']} | 
                            <strong>📞 Tel parent:</strong> {student.get('Téléphone Parent', 'Non renseigné')} | 
                            <strong>📞 Tel:</strong> {student.get('Téléphone', 'Non renseigné')}</p>
                            <p><strong>❌ Nombre d'absences:</strong> <span style="color: #dc3545; font-weight: bold;">{student['NombreAbsences']}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Export des données
                    st.markdown("---")
                    csv = absent_students.to_csv(index=False)
                    st.download_button(
                        label="📥 Télécharger la liste des absentéistes (CSV)",
                        data=csv,
                        file_name=f"absenteistes_{start_date_abs.strftime('%Y%m%d')}_{end_date_abs.strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.success("🎉 Aucun étudiant ne correspond aux critères d'absentéisme définis !")
                    st.info("Tous les étudiants ont une assiduité correcte sur cette période.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ====================== ONGLET CONTROLE ======================
        with tab7:
            c_col=st.columns([4,2]) 
            with c_col[0]:
                st.markdown("## 🔎 Contrôle des Étudiants en Retard de Paiement")

                # Choix du montant seuil
                montant_seuil = st.number_input(
                    "Montant minimum payé (FCFA)", min_value=0, value=25000, step=1000
                )

                # Date du jour pour comparer l'échéance
                #date_aujourdhui = pd.to_datetime(date.today())
                date_choix = st.date_input("Choisir une date", value=date.today())
                # Filtrer les étudiants dont l'échéance est passée et le total payé < seuil
                etudiants_retard = etudiants_df[
                    (pd.to_datetime(etudiants_df["Echeance"]) < pd.to_datetime(date_choix)) &
                    (etudiants_df["Total_Paye"] < montant_seuil)
                ]

                st.markdown(f"### 📋 Étudiants ayant payé moins de {montant_seuil:,} FCFA et dont l'échéance est dépassée")
                filiere_choisie = st.selectbox("Choisir une classe", options=etudiants_df["Filière"].unique())
                etudiants_retard = etudiants_retard[etudiants_retard["Filière"] == filiere_choisie]
                if not etudiants_retard.empty:
                    st.dataframe(
                        etudiants_retard[
                            ["Matricule", "Nom", "Prénom", "Filière", "Total_Paye", "Echeance"]
                        ],
                        use_container_width=True,
                        hide_index=True
                    )
                    st.info(f"{len(etudiants_retard)} étudiant(s) trouvé(s).")
                else:
                    st.success("Aucun étudiant en retard de paiement selon ce critère.")
            
            with c_col[1]:
                st.markdown("## Définir une nouvelle echéance pour un étudiant")
                etudiant_to_prolong = [f"{row['Matricule']} - {row['Nom']} {row['Prénom']}" 
                                            for _, row in etudiants_df.iterrows()]
                etudiant_selectionne = st.selectbox("Étudiant *", etudiant_to_prolong)
                matricule_etudiant = etudiant_selectionne.split(" - ")[0] if etudiant_selectionne else ""
                new_echeance=st.date_input("Choisir une nouvelle date", value=date.today())
                if st.button("Mettre à jour l'échéance"):
                    update_value_in_google_sheet2(sheet_name="Étudiants",column_to_update="Echeance",identifier_value=matricule_etudiant, new_value=new_echeance)
                    #st.rerun()
        
        #Enregistrement des données de connexion 
        data_connection=[user,'Gestionnaire', datetime.now().strftime('%Y-%m-%d %H:%M:%S')] 
        save_to_google_sheet("Connexion", data_connection)
if __name__ == "__main__":
    main()