import streamlit as st
import pandas as pd
import numpy as np
import json
import hashlib
import os
from datetime import datetime, timedelta
from PIL import Image
import base64


def hash_password(password):
    """Hash un mot de passe pour un stockage sécurisé"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Charge la base de données des utilisateurs depuis un fichier JSON"""
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {"users": {}}

def save_users(users):
    """Sauvegarde la base de données des utilisateurs dans un fichier JSON"""
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def import_users_from_excel(excel_path="Connexion.xlsx"):
    """Importe les utilisateurs depuis un fichier Excel vers la base de données JSON"""
    try:
        # Charger le fichier Excel
        df = pd.read_excel(excel_path, sheet_name="Identifiant")
        
        # Charger la base d'utilisateurs existante
        users = load_users()
        
        # Parcourir les lignes du DataFrame
        for _, row in df.iterrows():
            username = row['User'].strip() if isinstance(row['User'], str) else str(row['User'])
            status = row['Statut'].strip() if isinstance(row['Statut'], str) else str(row['Statut'])
            password = row['Password'].strip() if isinstance(row['Password'], str) else str(row['Password'])
            
            # Si l'utilisateur n'existe pas déjà, l'ajouter
            if username not in users["users"]:
                users["users"][username] = {
                    "password": hash_password(password),
                    "status": status,
                    "email": f"{username}@example.com",  # Email par défaut
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        
        # Sauvegarder la base d'utilisateurs mise à jour
        save_users(users)
        #return True, f"{len(df)} utilisateurs importés avec succès"
    except Exception as e:
        return False, f"Erreur lors de l'importation: {str(e)}"

def check_credentials(username, password):
    """Vérifie si les identifiants sont corrects et renvoie également le statut"""
    users = load_users()
    if username in users["users"]:
        if users["users"][username]["password"] == hash_password(password):
            return True, users["users"][username].get("status", "Utilisateur")
    return False, None

def register_user(username, password, email, status="Utilisateur"):
    """Enregistre un nouvel utilisateur avec un statut"""
    users = load_users()
    if username in users["users"]:
        return False, "Ce nom d'utilisateur existe déjà"
    
    users["users"][username] = {
        "password": hash_password(password),
        "email": email,
        "status": status,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_users(users)
    return True, "Compte créé avec succès"

def authentication_system(required_status=None):
    """
    Système d'authentification complet pour Streamlit
    
    Args:
        required_status (str, optional): Statut requis pour accéder à l'application
                                         Si None, tous les utilisateurs peuvent accéder
    """
    # Initialisation des variables de session
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "status" not in st.session_state:
        st.session_state["status"] = None
    if "login_time" not in st.session_state:
        st.session_state["login_time"] = None
        
    # Si l'utilisateur est déjà authentifié
    if st.session_state["authenticated"]:
        # Vérifier si la session n'a pas expiré (8 heures)
        if st.session_state["login_time"] and datetime.now() - st.session_state["login_time"] > timedelta(hours=8):
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.session_state["status"] = None
            st.session_state["login_time"] = None
            st.warning("Votre session a expiré. Veuillez vous reconnecter.")
        else:
            # Vérifier si l'utilisateur a le statut requis
            if required_status and st.session_state["status"] != required_status:
                st.error(f"Accès refusé. Vous avez besoin du statut '{required_status}' pour accéder à cette page.")
                if st.sidebar.button("🚪 Déconnexion"):
                    st.session_state["authenticated"] = False
                    st.session_state["username"] = None
                    st.session_state["status"] = None
                    st.session_state["login_time"] = None
                    st.rerun()
                return False
            
            # Afficher un message de bienvenue et un bouton de déconnexion
            st.sidebar.success(f"Connecté en tant que {st.session_state['username']} ({st.session_state['status']})")
            if st.sidebar.button("Déconnexion"):
                st.session_state["authenticated"] = False
                st.session_state["username"] = None
                st.session_state["status"] = None
                st.session_state["login_time"] = None
                st.rerun()
            return True
        
    def add_bg_local(image_file):
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
            background: linear-gradient(
                rgba(255,255,255,0.85), 
                rgba(255,255,255,0.85)
            ), url("data:image/png;base64,{encoded}");
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center center;
            background-size: 1500px 700px; /* Ajustez la taille ici */
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    add_bg_local("logo.jpg")

    col=st.columns([4,2])
    
    with col[0]:
        logo=Image.open("logo.jpg")
        st.image(logo,caption="",width=280)
        # Si l'utilisateur n'est pas authentifié, afficher les formulaires de connexion/inscription
        tab1, tab2, tab3 = st.tabs(["Connexion", " ", " "])
        
        with tab1:
            username = st.text_input("Nom d'utilisateur", key="login_username")
            password = st.text_input("Mot de passe", type="password", key="login_password")
            
            if st.button("Se connecter"):
                success, status = check_credentials(username, password)
                if success:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.session_state["status"] = status
                    st.session_state["login_time"] = datetime.now()
                    
                    # Vérifier si l'utilisateur a le statut requis
                    if required_status and status != required_status:
                        st.error(f"Accès refusé. Vous avez besoin du statut '{required_status}' pour accéder à cette page.")
                        st.session_state["authenticated"] = False
                        st.session_state["username"] = None
                        st.session_state["status"] = None
                        st.session_state["login_time"] = None
                    else:
                        st.success("Connexion réussie!")
                        st.rerun()
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect")


    #with tab2:
        """
        st.header("Créer un compte")
        new_username = st.text_input("Choisir un nom d'utilisateur", key="register_username")
        new_email = st.text_input("Email", key="register_email")
        new_password = st.text_input("Choisir un mot de passe", type="password", key="register_password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="confirm_password")
        
        # Option pour les administrateurs d'attribuer un statut
        #if st.session_state.get("authenticated") and st.session_state.get("status") == "Administrateur":
        status_options = ["Utilisateur", "Enquêteur", "Administrateur"]
        new_status = st.selectbox("Statut", options=status_options)
        #else:
        new_status = "Utilisateur"  # Statut par défaut
        
        if st.button("S'inscrire"):
            if not new_username or not new_email or not new_password:
                st.error("Tous les champs sont obligatoires")
            elif new_password != confirm_password:
                st.error("Les mots de passe ne correspondent pas")
            else:
                success, message = register_user(new_username, new_password, new_email, new_status)
                if success:
                    st.success(message)
                    st.info("Vous pouvez maintenant vous connecter")
                else:
                    st.error(message)
        """
    
    #with tab3:
        """
        st.header("Importer des utilisateurs depuis Excel")
        # Cette fonctionnalité ne devrait être accessible qu'aux administrateurs
        #if st.session_state.get("authenticated") and st.session_state.get("status") == "Administrateur":
        uploaded_file = st.file_uploader("Choisir un fichier Excel", type=['xlsx', 'xls'])
            
        if uploaded_file is not None:
                # Sauvegarder temporairement le fichier
            with open("temp_upload.xlsx", "wb") as f:
                f.write(uploaded_file.getbuffer())
                
                if st.button("Importer les utilisateurs"):
                    success, message = import_users_from_excel("temp_upload.xlsx")
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            # Option pour utiliser le fichier par défaut
        if st.button("Importer depuis Connexion.xlsx"):
            success, message = import_users_from_excel()
            if success:
                st.success(message)
            else:
                st.error(message)
        #else:
            #st.info("Vous devez être administrateur pour importer des utilisateurs.")
    
    return False
    """

    with col[1]:
        logo2=Image.open("logo2.png")
        #st.image(logo2,width=200)
# Exemple d'utilisation
