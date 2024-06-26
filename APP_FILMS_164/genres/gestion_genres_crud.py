"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""

"""ceci t_genre pour mon table : T_visiteur"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFAjouterGenres
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFDeleteGenre
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFUpdateGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher

    Test : ex : http://127.0.0.1:5575/genres_afficher

    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/genres_afficher/<string:order_by>/<int:id_genre_sel>", methods=['GET', 'POST'])
def genres_afficher(order_by, id_genre_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_genre_sel == 0:
                    strsql_genres_afficher = """SELECT * from t_visiteur"""
                    mc_afficher.execute(strsql_genres_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_genre_selected": id_genre_sel}
                    strsql_genres_afficher = """SELECT * from t_visiteur WHERE ID_Visiteur = %(value_id_genre_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_genres_afficher = """SELECT * from t_visiteur WHERE ID_Visiteur ORDER BY ID_Visiteur DESC"""

                    mc_afficher.execute(strsql_genres_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_genre_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_genres and id_genre_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données visiteurs affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{genres_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("genres/genres_afficher.html", data=data_genres)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter

    Test : ex : http://127.0.0.1:5575/genres_ajouter

    Paramètres : sans

    But : Ajouter un genre pour un film

    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_genre_wtf = form.nom_genre_wtf.data
                prenom_genre_wtf = form.prenom_genre_wtf.data
                adresse_genre_wtf = form.adresse_genre_wtf.data
                datenaiss_genre_wtf = form.datenaiss_genre_wtf.data
                telephone_genre_wtf = form.telephone_genre_wtf.data
                vehicule_genre_wtf = form.vehicule_genre_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_intitule_genre": name_genre_wtf,
                    "value_prenom_genre": prenom_genre_wtf,
                    "value_adresse_genre": adresse_genre_wtf,
                    "value_datenaiss_genre": datenaiss_genre_wtf,
                    "value_telephone_genre": telephone_genre_wtf,
                    "value_vehicule_genre": vehicule_genre_wtf
                }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_genre = """
                    INSERT INTO t_visiteur (
                        Nom, Prenom, Adresse, Date_de_Naissance, Numero_de_Telephone, Le_Visiteur_se_deplace_en_Vehicule_Personnel
                    ) VALUES (
                        %(value_intitule_genre)s,
                        %(value_prenom_genre)s,
                        %(value_adresse_genre)s,
                        %(value_datenaiss_genre)s,
                        %(value_telephone_genre)s,
                        %(value_vehicule_genre)s
                    )
                """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash("Données insérées !!", "success")
                print("Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('genres_afficher', order_by='DESC', id_genre_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{genres_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("genres/genres_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update

    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"

    Paramètres : sans

    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genre_update", methods=['GET', 'POST'])
def genre_update_wtf():
    id_genre_update = request.values['id_genre_btn_edit_html']
    form_update = FormWTFUpdateGenre()

    try:
        if request.method == "POST" and form_update.submit.data:
            name_genre_update = form_update.nom_genre_updatewtf.data
            prenom_genre_update = form_update.prenom_genre_updatewtf.data
            adresse_genre_update = form_update.adresse_genre_updatewtf.data
            datenaiss_genre_update = form_update.datenaiss_genre_updatewtf.data
            telephone_genre_update = form_update.telephone_genre_updatewtf.data
            vehicule_genre_update = form_update.vehicule_genre_updatewtf.data

            valeur_update_dictionnaire = {
                "value_intitule_genre": name_genre_update,
                "value_prenom_genre": prenom_genre_update,
                "value_adresse_genre": adresse_genre_update,
                "value_datenaiss_genre": datenaiss_genre_update,
                "value_telephone_genre": telephone_genre_update,
                "value_vehicule_genre": vehicule_genre_update,
                "value_id_genre": id_genre_update
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """
                UPDATE t_visiteur 
                SET Nom = %(value_intitule_genre)s, 
                    Prenom = %(value_prenom_genre)s,
                    Adresse = %(value_adresse_genre)s,
                    Date_de_Naissance = %(value_datenaiss_genre)s,
                    Numero_de_Telephone = %(value_telephone_genre)s,
                    Le_Visiteur_se_deplace_en_Vehicule_Personnel= %(value_vehicule_genre)s 
                WHERE ID_Visiteur = %(value_id_genre)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash("Donnée mise à jour !!", "success")
            print("Donnée mise à jour !!")

            return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=id_genre_update))

        elif request.method == "GET":
            str_sql_id_genre = """
                SELECT ID_Visiteur, Nom, Prenom, Adresse, Date_de_Naissance, Numero_de_Telephone, Le_Visiteur_se_deplace_en_Vehicule_Personnel 
                FROM t_visiteur 
                WHERE ID_Visiteur = %(value_id_genre)s
            """
            valeur_select_dictionnaire = {"value_id_genre": id_genre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                data_nom_genre = mybd_conn.fetchone()

            if data_nom_genre:
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["Nom"])

                form_update.nom_genre_updatewtf.data = data_nom_genre["Nom"]
                form_update.prenom_genre_updatewtf.data = data_nom_genre["Prenom"]
                form_update.adresse_genre_updatewtf.data = data_nom_genre["Adresse"]
                form_update.datenaiss_genre_updatewtf.data = data_nom_genre["Date_de_Naissance"]
                form_update.telephone_genre_updatewtf.data = data_nom_genre["Numero_de_Telephone"]
                form_update.vehicule_genre_updatewtf.data = data_nom_genre[
                    "Le_Visiteur_se_deplace_en_Vehicule_Personnel"]
            else:
                flash("Visiteur non trouvé", "warning")
                return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=0))
    except Exception as Exception_genre_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_update_wtf.__name__} ; "
                                      f"{Exception_genre_update_wtf}")

    return render_template("genres/genre_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete

    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"

    Paramètres : sans

    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/genre_delete", methods=['GET', 'POST'])
def genre_delete_wtf():
    data_societe_attribue_visiteur_delete = None
    data_visite_attribue_visiteur_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_visiteur_delete = request.values['id_genre_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteGenre()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("genres_afficher", order_by="ASC", id_genre_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_societe_attribue_visiteur_delete = session['data_societe_attribue_visiteur_delete']
                data_visite_attribue_visiteur_delete = session['data_visite_attribue_visiteur_delete']
                print("data_societe_attribue_visiteur_delete ", data_societe_attribue_visiteur_delete)
                print("data_visite_attribue_visiteur_delete ", data_visite_attribue_visiteur_delete)

                flash(f"Effacer le visiteur de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer visiteur" qui va irrémédiablement EFFACER le visiteur
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_visiteur": id_visiteur_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_visiteur_societe = """DELETE FROM t_visiteur_societe WHERE FK_visiteur = %(value_id_visiteur)s"""
                str_sql_delete_visiteur_visite = """DELETE FROM t_visiteur_visite WHERE FK_visiteur = %(value_id_visiteur)s"""
                str_sql_delete_idvisiteur = """DELETE FROM t_visiteur WHERE ID_Visiteur = %(value_id_visiteur)s"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_visiteur_societe, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_visiteur_visite, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idvisiteur, valeur_delete_dictionnaire)

                flash(f"Visiteur définitivement effacé !!", "success")
                print(f"Visiteur définitivement effacé !!")

                # afficher les données
                return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_visiteur": id_visiteur_delete}
            print(id_visiteur_delete, type(id_visiteur_delete))

            # Requête qui affiche toutes les sociétés attribuées au visiteur que l'utilisateur veut effacer
            str_sql_visiteur_societe_delete = """SELECT t_visiteur_societe.ID_visiteur_societe, t_visiteur.Nom, t_visiteur.Prenom, t_visiteur.ID_Visiteur, t_visiteur.Adresse, t_societe.Nom_de_la_Societe 
                                                FROM t_visiteur_societe 
                                                INNER JOIN t_visiteur ON t_visiteur_societe.FK_visiteur = t_visiteur.ID_Visiteur
                                                INNER JOIN t_societe ON t_visiteur_societe.FK_societe = t_societe.ID_Societe
                                                WHERE FK_visiteur = %(value_id_visiteur)s"""
            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_visiteur_societe_delete, valeur_select_dictionnaire)
                data_societe_attribue_visiteur_delete = mydb_conn.fetchall()
                print("data_societe_attribue_visiteur_delete...", data_societe_attribue_visiteur_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_societe_attribue_visiteur_delete'] = data_societe_attribue_visiteur_delete

                # Requête qui affiche toutes les visites attribuées au visiteur que l'utilisateur veut effacer
                str_sql_visiteur_visite_delete = """SELECT t_visiteur_visite.ID_visiteur_visite, t_visiteur.Nom, t_visiteur.Prenom, t_visiteur.ID_Visiteur, t_visiteur.Adresse, t_visite.Date_de_Visite, t_visite.Motif_de_Visite, t_visite.Nom_du_Batiment 
                                                    FROM t_visiteur_visite 
                                                    INNER JOIN t_visiteur ON t_visiteur_visite.FK_visiteur = t_visiteur.ID_Visiteur
                                                    INNER JOIN t_visite ON t_visiteur_visite.FK_visite = t_visite.ID_Visite
                                                    WHERE FK_visiteur = %(value_id_visiteur)s"""
                mydb_conn.execute(str_sql_visiteur_visite_delete, valeur_select_dictionnaire)
                data_visite_attribue_visiteur_delete = mydb_conn.fetchall()
                print("data_visite_attribue_visiteur_delete...", data_visite_attribue_visiteur_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_visite_attribue_visiteur_delete'] = data_visite_attribue_visiteur_delete

                # Opération sur la BD pour récupérer "ID_Visiteur" et "Nom" de la "t_visiteur"
                str_sql_id_visiteur = "SELECT ID_Visiteur, Nom FROM t_visiteur WHERE ID_Visiteur = %(value_id_visiteur)s"

                mydb_conn.execute(str_sql_id_visiteur, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom visiteur" pour l'action DELETE
                data_nom_visiteur = mydb_conn.fetchone()
                print("data_nom_visiteur ", data_nom_visiteur, " type ", type(data_nom_visiteur), " visiteur ",
                      data_nom_visiteur["Nom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_delete_wtf.html"
            form_delete.nom_genre_delete_wtf.data = data_nom_visiteur["Nom"]

            # Le bouton pour l'action "DELETE" dans le form. "genre_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")

    return render_template("genres/genre_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_societe_associes=data_societe_attribue_visiteur_delete,
                           data_visite_associes=data_visite_attribue_visiteur_delete)
