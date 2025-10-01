import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from openpyxl import Workbook
from Authentification import *
from Fonction import *
import io

#import_users_from_excel()
# Configuration de la page 



def main():
   
    #st.markdown(tabs_css, unsafe_allow_html=True)
    is_authenticated = authentication_system("Enseignant")
    if is_authenticated:
        #st.set_page_config(
        #page_title="Enseignant - STATO-SPHERE PREPAS",
        #page_icon="👨‍🏫",
        #layout="wide",
        #initial_sidebar_state="expanded"
        #)
        user = st.session_state['username']
        
        etudiants_df=st.session_state.etudiants_df
        enseignants_df=st.session_state.enseignants_df
        seances_df=st.session_state.seances_df
        depenses_df=st.session_state.depenses_df
        versements_df=st.session_state.versements_df
        ventes_df=st.session_state.ventes_df
        presence_df=st.session_state.presence_df
        fiches_paie_df=st.session_state.fiches_paie_df
        Connect_df=st.session_state.Connect_df
        
        #boutton de mise à jour
        
        
                 
                
                
        
        df_ens=enseignants_df[["Nom","ID"]]
        dict_ens=df_ens.set_index("Nom").to_dict()
        teacher_id=dict_ens.get("ID")[user]
        #teacher_lesson=dict_ens.get("Matière")[user]
        teacher_info = get_teacher_info(user)
        
        #seances_df = read_from_google_sheet("Séances")
        teacher_seances = seances_df[seances_df['idEnseignant'] == teacher_id]
        
        
        # Sidebar configuration
        st.sidebar.title("Espace Enseignant")
        st.sidebar.write(f"Bienvenue, {user}!")
        
        # Menu de navigation dans la sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🧭 Navigation")
        st.sidebar.markdown("📝 **Pointer une séance** - Enregistrez vos cours")
        st.sidebar.markdown("📚 **Mes séances** - Consultez votre historique")
        st.sidebar.markdown("👥 **Ajouter étudiant** - Inscrivez de nouveaux étudiants")
        
        # Statistiques dans la sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Statistiques Rapides")
        
        
        if not seances_df.empty and 'idEnseignant' in seances_df.columns:
            
            st.sidebar.metric("📚 Séances totales", len(teacher_seances))
            
            if not teacher_seances.empty:
                # Séances ce mois
                current_month = datetime.now().month
                current_year = datetime.now().year
                seances_ce_mois = teacher_seances[
                    (pd.to_datetime(teacher_seances['Date']).dt.month == current_month) &
                    (pd.to_datetime(teacher_seances['Date']).dt.year == current_year)
                ]
                st.sidebar.metric("📅 Séances ce mois", len(seances_ce_mois))
                
                # Dernière séance
                if not teacher_seances.empty:
                    derniere_seance = pd.to_datetime(teacher_seances['Date']).max()
                    st.sidebar.metric("🕐 Dernière séance", derniere_seance.strftime('%d/%m/%Y'))
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 💡 Conseils")
        st.sidebar.info("💡 N'oubliez pas de pointer vos séances après chaque cours pour un suivi précis de votre activité.")
        
        #chargement des données
        
        #etudiants_df = read_from_google_sheet("Étudiants")
        
        
        # ============== INTERFACE PRINCIPALE ==============
        
        # En-tête avec informations enseignant
        st.markdown(f"""
        <div class="main-header">
            <h1>👨‍🏫 Espace Enseignant</h1>
            <h3>STATO-SPHERE PREPAS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="teacher-info">
            <h2>👨‍🏫 Mr. {teacher_info['nom']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Statistiques rapides de l'enseignant
        if not seances_df.empty and 'idEnseignant' in seances_df.columns:
            teacher_seances = seances_df[seances_df['idEnseignant'] == teacher_id]
        else:
            teacher_seances = pd.DataFrame()
        
        
        
        # Interface à onglets
        st.markdown('<div class="tabs-container">', unsafe_allow_html=True)
        tab = st.tabs(["📋 Faire l'appel","📝 Pointer une Séance", "📚 Mes Séances", "👥 Ajouter un Étudiant"])
        
        # ==================== ONGLET POUR FAIRE L'APPEL ====================
        with tab[0]:
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

                    cours_list = COURS_CHOICES
                    cours = st.selectbox("📚 Matière/Cours *", cours_list, key="cours_config")
                with col2:
                    # Liste des cours/matières
                    
                    
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
                                id_presence = len(presence_df) + success_count + 1
                                data = [
                                    id_presence, matricule, 
                                    f"{config['cours']} - {config['intitule']}", 
                                    statut, 
                                    config['date'].strftime('%Y-%m-%d'), 
                                    teacher_id  # idEnseignant par défaut (à améliorer)
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
       
        # ==================== ONGLET POINTER SÉANCE ====================
        with tab[1]:
            st.markdown("## 📝 Pointer une Nouvelle Séance")
            
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown("### ➕ Enregistrement de Séance")
            
            with st.form("form_seance"):
                col1, col2 = st.columns(2)
                
                with col1:
                    date_seance = st.date_input("📅 Date de la séance *", value=date.today())
                    
                    # L'enseignant est pré-sélectionné
                    nom_enseignant = st.text_input("👨‍🏫 Enseignant", value=teacher_info['nom'], disabled=True)
                    
                    cours_dispense = st.selectbox("📚 Cours dispensé *", teacher_info['matieres'])
                    
                    intitule_cours = st.text_input(
                        "📝 Intitulé du cours *", 
                        placeholder="Ex: Analyse mathématique - Chapitre 3 : Dérivées"
                    )
                
                with col2:
                    heure_arrivee = st.time_input("🕐 Heure d'arrivée *", value=time(15, 30))
                    
                    heure_depart = st.time_input("🕕 Heure de départ *", value=time(17, 30))
                    
                    nombre_etudiants = st.number_input(
                        "👥 Nombre d'étudiants présents *", 
                        min_value=0, 
                        max_value=100, 
                        value=0
                    )
                
                # Classe/Niveau (optionnel)
                classe = st.multiselect("🎓 Classes/Niveau", options=FILIERE_CHOICES)
                
                submitted_seance = st.form_submit_button("💾 Enregistrer la Séance", type="primary")
                
                if submitted_seance:
                    if (date_seance and cours_dispense and intitule_cours and 
                        heure_arrivee and heure_depart and nombre_etudiants >= 0):
                        
                        # Validation des heures
                        if heure_depart <= heure_arrivee:
                            st.markdown("""
                            <div class="error-box">
                                ⚠️ L'heure de départ doit être supérieure à l'heure d'arrivée
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Génération de l'ID
                            #seances_df = read_from_google_sheet("Séances")
                            id_seance = len(seances_df) + 1
                            Vclasse=", ".join(classe)
                            data = [
                                id_seance,
                                date_seance.strftime('%Y-%m-%d'),
                                cours_dispense,
                                heure_arrivee.strftime('%H:%M'),
                                heure_depart.strftime('%H:%M'),
                                Vclasse if Vclasse else "",
                                intitule_cours,
                                teacher_id,
                                nombre_etudiants
                            ]
                            
                            if save_to_google_sheet("Séances", data):
                                # Calcul de la durée
                                duree_minutes = (datetime.combine(date.today(), heure_depart) - 
                                               datetime.combine(date.today(), heure_arrivee)).seconds // 60
                                duree_heures = duree_minutes // 60
                                duree_min_restant = duree_minutes % 60
                                st.session_state.seances_df = read_from_google_sheet("Séances")
                                st.markdown(f"""
                                <div class="success-box">
                                    ✅ <strong>Séance enregistrée avec succès !</strong><br>
                                    📚 <strong>Cours :</strong> {cours_dispense}<br>
                                    ⏱️ <strong>Durée :</strong> {duree_heures}h{duree_min_restant:02d}<br>
                                    👥 <strong>Étudiants :</strong> {nombre_etudiants}
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
        
        # ==================== ONGLET MES SÉANCES ====================
        with tab[2]:
            st.markdown("## 📚 Historique de mes Séances")
            
            if not teacher_seances.empty:
                st.markdown(f"### 📊 {len(teacher_seances)} séance(s) enregistrée(s)")
                
                # Filtres
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if 'Matière' in teacher_seances.columns:
                        matieres_filter = st.multiselect(
                            "📚 Filtrer par matière",
                            options=teacher_seances['Matière'].unique(),
                            default=teacher_seances['Matière'].unique()
                        )
                    else:
                        matieres_filter = []
                
                with col2:
                    if 'Classe' in teacher_seances.columns:
                        classes_filter = st.multiselect(
                            "📍 Filtrer par Classe",
                            options=teacher_seances['Classe'].unique(),
                            default=teacher_seances['Classe'].unique()
                        )
                    else:
                        classes_filter = []
                
                with col3:
                    # Période
                    if 'Date' in teacher_seances.columns:
                        teacher_seances['Date'] = pd.to_datetime(teacher_seances['Date'])
                        date_min = teacher_seances['Date'].min().date()
                        date_max = teacher_seances['Date'].max().date()
                        
                        periode = st.date_input(
                            "📅 Période",
                            value=(date_min, date_max),
                            min_value=date_min,
                            max_value=date_max
                        )
                
                # Application des filtres
                filtered_seances = teacher_seances.copy()
                
                if matieres_filter:
                    filtered_seances = filtered_seances[filtered_seances['Matière'].isin(matieres_filter)]
                
                if classes_filter:
                    filtered_seances = filtered_seances[filtered_seances['Classe'].isin(classes_filter)]
                
                # Affichage des séances filtrées
                st.markdown("---")
                
                if not filtered_seances.empty:
                    # Tri par date décroissante
                    filtered_seances = filtered_seances.sort_values('Date', ascending=False)
                    
                    # Préparation des données pour l'affichage
                    display_df = filtered_seances.copy()
                    
                    # Calcul de la durée pour chaque séance
                    durees = []
                    for idx, seance in display_df.iterrows():
                        try:
                            heure_a = datetime.strptime(str(seance['HeureArrivée']), '%H:%M').time()
                            heure_d = datetime.strptime(str(seance['HeureDepart']), '%H:%M').time()
                            duree = (datetime.combine(date.today(), heure_d) - 
                                   datetime.combine(date.today(), heure_a)).seconds // 60
                            durees.append(f"{duree//60}h{duree%60:02d}")
                        except:
                            durees.append("")
                    
                    display_df['Durée'] = durees
                    display_df['Date'] = display_df['Date'].dt.strftime('%d/%m/%Y')
                    
                    # Sélection et renommage des colonnes pour l'affichage
                    columns_to_show = {
                        'Date': 'Date',
                        'Matière': 'Matière',
                        'IntituléCours': 'Intitulé du Cours',
                        'Centre': 'Centre',
                        'HeureArrivée': 'Arrivée',
                        'HeureDepart': 'Départ',
                        'Durée': 'Durée',
                        'NombreEtudiants': 'Étudiants',
                        'Classe': 'Classe'
                    }
                    
                    display_df = display_df[[col for col in columns_to_show.keys() if col in display_df.columns]]
                    display_df = display_df.rename(columns=columns_to_show)
                    
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                    
                    filtered_seances = filtered_seances.fillna("")
                    # Export des données
                    st.markdown("---")
                    # Préparation du fichier Excel en mémoire
                    output = io.BytesIO()
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "Séances"

                    # Ajout des en-têtes
                    ws.append(list(filtered_seances.columns))

                    # Ajout des données
                    for row in filtered_seances.itertuples(index=False):
                        ws.append(row)

                    wb.save(output)
                    output.seek(0)

                    st.download_button(
                        label="📥 Télécharger mes séances (Excel)",
                        data=output,
                        file_name=f"seances_{user}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.info("Aucune séance trouvée avec les filtres sélectionnés")
            else:
                st.markdown("""
                <div class="info-box">
                    ℹ️ <strong>Aucune séance enregistrée</strong><br>
                    Utilisez l'onglet "Pointer une Séance" pour enregistrer votre première séance.
                </div>
                """, unsafe_allow_html=True)
        
        # ==================== ONGLET AJOUTER ÉTUDIANT ====================
        with tab[3]:
            st.markdown("## 👥 Gestion des Étudiants")
            
            col1, col2 = st.columns([20, 2])
            
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
        #Enregistrement des données de connexion 
        data_connection=[user,'Enseignant', datetime.now().strftime('%Y-%m-%d %H:%M:%S')] 
        save_to_google_sheet("Connexion", data_connection)   
if __name__ == "__main__":
    main()     

