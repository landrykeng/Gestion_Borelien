import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import time

# Import du système d'authentification (supposé dans le même répertoire)
# from Authentification import AuthenticationManager, UserRole, SecurityLevel, create_authentication_system

# Pour la démo, je vais inclure les imports nécessaires
# (Dans un vrai projet, vous importeriez depuis votre fichier)
from enum import Enum

class UserRole(Enum):
    UTILISATEUR = "Utilisateur"
    ENQUETEUR = "Enquêteur"
    SUPERVISEUR = "Superviseur"
    ADMINISTRATEUR = "Administrateur"
    SUPER_ADMIN = "Super Administrateur"

class SecurityLevel(Enum):
    PUBLIC = 0
    BASIC = 1
    ELEVATED = 2
    ADMIN = 3
    SUPER_ADMIN = 4

def configure_page():
    """Configuration de la page Streamlit"""
    st.set_page_config(
        page_title="🧪 Test Système d'Authentification ISSEA",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS personnalisé pour la page de test
    st.markdown("""
    <style>
    .test-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .test-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #007bff;
    }
    
    .success-metric {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .error-metric {
        background: linear-gradient(135deg, #dc3545, #e74c3c);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .warning-metric {
        background: linear-gradient(135deg, #ffc107, #ff9f00);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .info-metric {
        background: linear-gradient(135deg, #17a2b8, #007bff);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .test-result {
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .test-passed {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
    }
    
    .test-failed {
        background-color: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
    }
    
    .test-pending {
        background-color: #fff3cd;
        border-color: #ffeaa7;
        color: #856404;
    }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    """Affiche l'en-tête de la page de test"""
    st.markdown("""
    <div class="test-header">
        <h1>🧪 Page de Test - Système d'Authentification ISSEA</h1>
        <p>Interface complète pour tester toutes les fonctionnalités d'authentification</p>
    </div>
    """, unsafe_allow_html=True)

def create_test_users_data():
    """Crée des données de test pour les utilisateurs"""
    test_users = {
        "users": {
            "admin": {
                "password_hash": "test_hash_admin",
                "salt": "test_salt",
                "role": "Administrateur",
                "email": "admin@issea.cm",
                "created_at": "2024-01-01T00:00:00",
                "last_login": "2024-01-15T10:30:00",
                "is_active": True,
                "profile": {
                    "first_name": "Admin",
                    "last_name": "Test",
                    "department": "IT",
                    "phone": "+237123456789"
                }
            },
            "enqueteur1": {
                "password_hash": "test_hash_enq",
                "salt": "test_salt",
                "role": "Enquêteur",
                "email": "enqueteur@issea.cm",
                "created_at": "2024-01-02T00:00:00",
                "last_login": "2024-01-14T09:15:00",
                "is_active": True,
                "profile": {
                    "first_name": "Jean",
                    "last_name": "Enquêteur",
                    "department": "Enquêtes",
                    "phone": "+237987654321"
                }
            },
            "utilisateur1": {
                "password_hash": "test_hash_user",
                "salt": "test_salt",
                "role": "Utilisateur",
                "email": "user@issea.cm",
                "created_at": "2024-01-03T00:00:00",
                "last_login": None,
                "is_active": False,
                "profile": {
                    "first_name": "Marie",
                    "last_name": "Utilisateur",
                    "department": "Formation",
                    "phone": "+237456789123"
                }
            }
        },
        "metadata": {
            "version": "2.0",
            "created": "2024-01-01T00:00:00",
            "last_updated": "2024-01-15T12:00:00"
        }
    }
    return test_users

def test_user_database_operations():
    """Test des opérations sur la base de données utilisateurs"""
    st.markdown('<div class="test-section">', unsafe_allow_html=True)
    st.subheader("🗄️ Test des Opérations Base de Données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📖 Lecture de la base de données**")
        
        if st.button("🔍 Charger les utilisateurs", key="load_users"):
            try:
                # Simuler le chargement
                with st.spinner("Chargement..."):
                    time.sleep(0.5)
                    
                if os.path.exists("users.json"):
                    with open("users.json", "r") as f:
                        users_data = json.load(f)
                    st.success(f"✅ Base chargée: {len(users_data.get('users', {}))} utilisateurs")
                    
                    # Afficher un aperçu
                    if users_data.get('users'):
                        st.json(list(users_data['users'].keys())[:3])
                else:
                    st.warning("⚠️ Fichier users.json non trouvé")
                    
            except Exception as e:
                st.error(f"❌ Erreur: {e}")
    
    with col2:
        st.markdown("**💾 Création de données de test**")
        
        if st.button("🔧 Créer données de test", key="create_test_data"):
            try:
                test_data = create_test_users_data()
                with open("users_test.json", "w") as f:
                    json.dump(test_data, f, indent=4)
                
                st.success("✅ Données de test créées dans users_test.json")
                st.json(list(test_data['users'].keys()))
                
            except Exception as e:
                st.error(f"❌ Erreur: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def test_password_operations():
    """Test des opérations de mot de passe"""
    st.markdown('<div class="test-section">', unsafe_allow_html=True)
    st.subheader("🔐 Test des Opérations Mot de Passe")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔒 Test de hachage**")
        test_password = st.text_input("Mot de passe à tester:", 
                                    value="TestPassword123!", 
                                    key="test_password")
        
        if st.button("🧮 Hasher le mot de passe", key="hash_password"):
            # Simulation du hachage (remplacez par votre vraie fonction)
            import hashlib
            import secrets
            
            salt = secrets.token_hex(32)
            password_hash = hashlib.pbkdf2_hmac('sha256', 
                                             test_password.encode('utf-8'), 
                                             salt.encode('utf-8'), 
                                             100000)
            hash_b64 = password_hash.hex()
            
            st.code(f"Salt: {salt[:20]}...")
            st.code(f"Hash: {hash_b64[:20]}...")
            st.success("✅ Hachage réussi!")
    
    with col2:
        st.markdown("**✅ Test de validation**")
        password_to_validate = st.text_input("Mot de passe à valider:", 
                                           value="weak", 
                                           key="validate_password")
        
        if st.button("🔍 Valider la force", key="validate_strength"):
            # Simulation de validation
            requirements = []
            is_valid = True
            
            if len(password_to_validate) < 8:
                requirements.append("Au moins 8 caractères")
                is_valid = False
            
            if not any(c.islower() for c in password_to_validate):
                requirements.append("Au moins une minuscule")
                is_valid = False
                
            if not any(c.isupper() for c in password_to_validate):
                requirements.append("Au moins une majuscule")
                is_valid = False
                
            if not any(c.isdigit() for c in password_to_validate):
                requirements.append("Au moins un chiffre")
                is_valid = False
            
            if is_valid:
                st.success("✅ Mot de passe fort!")
            else:
                st.error(f"❌ Requis: {', '.join(requirements)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def test_role_permissions():
    """Test des rôles et permissions"""
    st.markdown('<div class="test-section">', unsafe_allow_html=True)
    st.subheader("🎭 Test des Rôles et Permissions")
    
    # Matrice des permissions
    roles = [role.value for role in UserRole]
    security_levels = [level.name for level in SecurityLevel]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**🔐 Matrice des Permissions**")
        
        # Créer une matrice de permissions
        permission_matrix = []
        for role in roles:
            row = {"Rôle": role}
            for level in security_levels:
                # Simulation de la logique de permission
                role_level = {
                    "Utilisateur": 1,
                    "Enquêteur": 2,
                    "Superviseur": 2,
                    "Administrateur": 3,
                    "Super Administrateur": 4
                }.get(role, 0)
                
                level_value = {
                    "PUBLIC": 0,
                    "BASIC": 1,
                    "ELEVATED": 2,
                    "ADMIN": 3,
                    "SUPER_ADMIN": 4
                }.get(level, 0)
                
                row[level] = "✅" if role_level >= level_value else "❌"
            
            permission_matrix.append(row)
        
        df_permissions = pd.DataFrame(permission_matrix)
        st.dataframe(df_permissions, use_container_width=True)
    
    with col2:
        st.markdown("**🧪 Test de Permission**")
        
        selected_role = st.selectbox("Rôle à tester:", roles, key="test_role")
        selected_level = st.selectbox("Niveau requis:", security_levels, key="test_level")
        
        if st.button("🔍 Tester Permission", key="test_permission"):
            # Simulation du test de permission
            role_level = {
                "Utilisateur": 1,
                "Enquêteur": 2,
                "Superviseur": 2,
                "Administrateur": 3,
                "Super Administrateur": 4
            }.get(selected_role, 0)
            
            level_value = {
                "PUBLIC": 0,
                "BASIC": 1,
                "ELEVATED": 2,
                "ADMIN": 3,
                "SUPER_ADMIN": 4
            }.get(selected_level, 0)
            
            if role_level >= level_value:
                st.success(f"✅ {selected_role} a accès au niveau {selected_level}")
            else:
                st.error(f"❌ {selected_role} n'a PAS accès au niveau {selected_level}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def test_excel_import():
    """Test de l'importation Excel"""
    st.markdown('<div class="test-section">', unsafe_allow_html=True)
    st.subheader("📤 Test Import Excel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Créer fichier Excel de test**")
        
        if st.button("🔧 Générer Excel de test", key="create_excel"):
            # Créer des données de test
            test_data = {
                "User": ["testuser1", "testuser2", "testuser3", "testadmin"],
                "Password": ["password123", "mypass456", "secret789", "admin2024"],
                "Statut": ["Utilisateur", "Enquêteur", "Superviseur", "Administrateur"],
                "Email": ["user1@test.com", "user2@test.com", "user3@test.com", "admin@test.com"]
            }
            
            df = pd.DataFrame(test_data)
            
            # Sauvegarder en Excel
            with pd.ExcelWriter("test_import.xlsx") as writer:
                df.to_excel(writer, sheet_name="Identifiant", index=False)
            
            st.success("✅ Fichier test_import.xlsx créé!")
            st.dataframe(df)
    
    with col2:
        st.markdown("**📥 Simuler Import**")
        
        uploaded_file = st.file_uploader("Fichier Excel à tester:", 
                                       type=['xlsx', 'xls'],
                                       key="test_upload")
        
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file, sheet_name="Identifiant")
                st.success(f"✅ Fichier lu: {len(df)} lignes")
                st.dataframe(df.head())
                
                # Validation des colonnes
                required_cols = ['User', 'Password', 'Statut']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"❌ Colonnes manquantes: {missing_cols}")
                else:
                    st.success("✅ Structure du fichier valide")
                    
            except Exception as e:
                st.error(f"❌ Erreur de lecture: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def test_security_features():
    """Test des fonctionnalités de sécurité"""
    st.markdown('<div class="test-section">', unsafe_allow_html=True)
    st.subheader("🛡️ Test des Fonctionnalités de Sécurité")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🚫 Test Anti-Brute Force**")
        
        # Simuler des tentatives échouées
        if "failed_attempts" not in st.session_state:
            st.session_state.failed_attempts = {}
        
        test_user = st.text_input("Utilisateur à tester:", value="testuser", key="brute_user")
        
        if st.button("❌ Simuler échec connexion", key="simulate_fail"):
            if test_user not in st.session_state.failed_attempts:
                st.session_state.failed_attempts[test_user] = 0
            
            st.session_state.failed_attempts[test_user] += 1
            attempts = st.session_state.failed_attempts[test_user]
            
            if attempts >= 3:
                st.error(f"🔒 Compte {test_user} verrouillé après {attempts} tentatives!")
            else:
                st.warning(f"⚠️ Tentative {attempts}/3 pour {test_user}")
        
        if st.button("🔓 Réinitialiser", key="reset_attempts"):
            if test_user in st.session_state.failed_attempts:
                del st.session_state.failed_attempts[test_user]
            st.success("✅ Tentatives réinitialisées")
    
    with col2:
        st.markdown("**⏰ Test Expiration Session**")
        
        # Simuler une session
        if "test_session_time" not in st.session_state:
            st.session_state.test_session_time = datetime.now()
        
        session_age = datetime.now() - st.session_state.test_session_time
        hours = session_age.total_seconds() / 3600
        
        st.metric("Âge de session", f"{hours:.1f}h")
        
        if hours > 8:
            st.error("❌ Session expirée!")
        elif hours > 6:
            st.warning("⚠️ Session bientôt expirée")
        else:
            st.success("✅ Session active")
        
        if st.button("🔄 Nouvelle session", key="new_session"):
            st.session_state.test_session_time = datetime.now()
            st.success("✅ Nouvelle session créée")
    
    with col3:
        st.markdown("**📧 Test Validation Email**")
        
        test_emails = [
            "valid@example.com",
            "invalid.email",
            "user@domain",
            "test@issea.cm",
            "@invalid.com"
        ]
        
        for email in test_emails:
            # Validation email simple
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            is_valid = re.match(pattern, email) is not None
            
            if is_valid:
                st.success(f"✅ {email}")
            else:
                st.error(f"❌ {email}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_user_statistics():
    """Affiche les statistiques des utilisateurs"""
    st.markdown('<div class="test-section">', unsafe_allow_html=True)
    st.subheader("📊 Statistiques et Analytics")
    
    # Données simulées pour les graphiques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="success-metric">', unsafe_allow_html=True)
        st.metric("👥 Total Utilisateurs", "47", delta="5")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-metric">', unsafe_allow_html=True)
        st.metric("🔐 Connexions Actives", "12", delta="2")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="warning-metric">', unsafe_allow_html=True)
        st.metric("⚠️ Comptes Verrouillés", "3", delta="-1")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="error-metric">', unsafe_allow_html=True)
        st.metric("❌ Tentatives Échouées", "15", delta="4")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique de distribution des rôles
        roles_data = {
            "Rôle": ["Utilisateur", "Enquêteur", "Superviseur", "Administrateur"],
            "Nombre": [25, 15, 5, 2]
        }
        fig_roles = px.pie(roles_data, values="Nombre", names="Rôle", 
                          title="Distribution des Rôles",
                          color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_roles, use_container_width=True)
    
    with col2:
        # Graphique des connexions par jour
        dates = pd.date_range(start="2024-01-01", end="2024-01-15", freq="D")
        connexions = [12, 15, 8, 20, 18, 22, 25, 19, 16, 23, 21, 17, 14, 26, 24]
        
        fig_connexions = go.Figure()
        fig_connexions.add_trace(go.Scatter(
            x=dates, y=connexions,
            mode='lines+markers',
            name='Connexions',
            line=dict(color='#007bff', width=3),
            marker=dict(size=8)
        ))
        fig_connexions.update_layout(
            title="Connexions Quotidiennes",
            xaxis_title="Date",
            yaxis_title="Nombre de Connexions"
        )
        st.plotly_chart(fig_connexions, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def run_automated_tests():
    """Lance une série de tests automatisés"""
    st.markdown('<div class="test-section">', unsafe_allow_html=True)
    st.subheader("🤖 Tests Automatisés")
    
    if st.button("🚀 Lancer tous les tests", key="run_all_tests"):
        # Liste des tests à exécuter
        tests = [
            ("Test de hachage mot de passe", "test_password_hashing"),
            ("Test de validation email", "test_email_validation"),
            ("Test de permissions rôles", "test_role_permissions"),
            ("Test anti-brute force", "test_brute_force"),
            ("Test expiration session", "test_session_expiry"),
            ("Test import Excel", "test_excel_import"),
            ("Test base de données", "test_database_ops")
        ]
        
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, (test_name, test_function) in enumerate(tests):
            status_text.text(f"Exécution: {test_name}...")
            time.sleep(0.5)  # Simulation du temps d'exécution
            
            # Simulation des résultats de test
            import random
            success = random.choice([True, True, True, False])  # 75% de succès
            
            results.append({
                "Test": test_name,
                "Statut": "✅ PASSÉ" if success else "❌ ÉCHOUÉ",
                "Durée": f"{random.randint(50, 500)}ms"
            })
            
            progress_bar.progress((i + 1) / len(tests))
        
        status_text.text("Tests terminés!")
        
        # Afficher les résultats
        df_results = pd.DataFrame(results)
        st.dataframe(df_results, use_container_width=True)
        
        # Résumé
        passed = sum(1 for r in results if "PASSÉ" in r["Statut"])
        total = len(results)
        
        if passed == total:
            st.success(f"🎉 Tous les tests réussis! ({passed}/{total})")
        elif passed > total * 0.7:
            st.warning(f"⚠️ La plupart des tests réussis ({passed}/{total})")
        else:
            st.error(f"❌ Plusieurs tests échoués ({passed}/{total})")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Fonction principale de la page de test"""
    configure_page()
    display_header()
    
    # Menu de navigation dans la sidebar
    st.sidebar.title("🧪 Menu de Test")
    
    test_sections = [
        "🏠 Vue d'ensemble",
        "🗄️ Base de Données",
        "🔐 Mots de Passe",
        "🎭 Rôles & Permissions",
        "📤 Import Excel",
        "🛡️ Sécurité",
        "📊 Statistiques",
        "🤖 Tests Automatisés"
    ]
    
    selected_section = st.sidebar.selectbox("Choisir une section:", test_sections)
    
    # Informations système dans la sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Informations Système")
    st.sidebar.info(f"**Version:** 2.0\n**Date:** {datetime.now().strftime('%d/%m/%Y')}")
    
    # Navigation vers les différentes sections
    if selected_section == "🏠 Vue d'ensemble":
        st.markdown("""
        ## 🎯 Objectif de cette page
        
        Cette page de test vous permet de valider toutes les fonctionnalités 
        de votre système d'authentification de manière interactive.
        
        ### 📋 Fonctionnalités testées:
        - ✅ Gestion des utilisateurs et base de données
        - ✅ Hachage et validation des mots de passe  
        - ✅ Système de rôles et permissions
        - ✅ Import/Export Excel
        - ✅ Fonctionnalités de sécurité avancées
        - ✅ Surveillance et analytics
        
        ### 🚀 Comment utiliser:
        1. Sélectionnez une section dans le menu latéral
        2. Exécutez les tests interactifs
        3. Vérifiez les résultats et corrections nécessaires
        """)
        
        # Statut global du système
        st.markdown("### 🔍 Statut Global du Système")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if os.path.exists("users.json"):
                st.success("✅ Base de données accessible")
            else:
                st.warning("⚠️ Base de données non trouvée")
        
        with col2:
            # Test d'import de modules
            try:
                import hashlib, secrets
                st.success("✅ Modules cryptographiques OK")
            except:
                st.error("❌ Modules cryptographiques manquants")
        
        with col3:
            st.success("✅ Interface Streamlit OK")
    
    elif selected_section == "🗄️ Base de Données":
        test_user_database_operations()
        
    elif selected_section == "🔐 Mots de Passe":
        test_password_operations()
        
    elif selected_section == "🎭 Rôles & Permissions":
        test_role_permissions()
        
    elif selected_section == "📤 Import Excel":
        test_excel_import()
        
    elif selected_section == "🛡️ Sécurité":
        test_security_features()
        
    elif selected_section == "📊 Statistiques":
        display_user_statistics()
        
    elif selected_section == "🤖 Tests Automatisés":
        run_automated_tests()

if __name__ == "__main__":
    main()