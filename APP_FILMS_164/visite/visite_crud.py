"""Gestion des "routes" FLASK et des données pour les visite.
Fichier : gestion_visite_crud.py
Auteur : OM 2021.03.16
"""

"""ceci t_visite pour mon table : T_visiteur"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.visite.visite_wtf_forms import FormWTFAjouterVisite,FormWTFDeleteVisite,FormWTFUpdateVisite


"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /visite_afficher

    Test : ex : http://127.0.0.1:5575/visite_afficher

    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_visite_sel = 0 >> tous les visite.
                id_visite_sel = "n" affiche le visite dont l'id est "n"
"""


@app.route("/visite_afficher/<string:order_by>/<int:id_visite_sel>", methods=['GET', 'POST'])
def visite_afficher(order_by, id_visite_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_visite_sel == 0:
                    strsql_visite_afficher = """SELECT * from t_visite"""
                    mc_afficher.execute(strsql_visite_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_visite"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du visite sélectionné avec un nom de variable
                    valeur_id_visite_selected_dictionnaire = {"value_id_visite_selected": id_visite_sel}
                    strsql_visite_afficher = """SELECT * from t_visite WHERE ID_Visite = %(value_id_visite_selected)s"""

                    mc_afficher.execute(strsql_visite_afficher, valeur_id_visite_selected_dictionnaire)
                else:
                    strsql_visite_afficher = """SELECT * from t_visite WHERE ID_Visite ORDER BY ID_Visite DESC"""

                    mc_afficher.execute(strsql_visite_afficher)

                data_visite = mc_afficher.fetchall()

                print("data_visite ", data_visite, " Type : ", type(data_visite))

                # Différencier les messages si la table est vide.
                if not data_visite and id_visite_sel == 0:
                    flash("""La table "t_visite" est vide. !!""", "warning")
                elif not data_visite and id_visite_sel > 0:
                    # Si l'utilisateur change l'id_visite dans l'URL et que le visite n'existe pas,
                    flash(f"Le visite demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_visite" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données visiteurs affichés !!", "success")

        except Exception as Exception_visite_afficher:
            raise ExceptionvisiteAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{visite_afficher.__name__} ; "
                                          f"{Exception_visite_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("visite/visite_afficher.html", data=data_visite)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /visite_ajouter

    Test : ex : http://127.0.0.1:5575/visite_ajouter

    Paramètres : sans

    But : Ajouter un visite pour un film

    Remarque :  Dans le champ "name_visite_html" du formulaire "visite/visite_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""





@app.route("/visite_ajouter", methods=['GET', 'POST'])
def visite_ajouter_wtf():
    form = FormWTFAjouterVisite()
    if form.validate_on_submit():
        date_visite_wtf = form.date_de_visite_wtf.data
        prevue_visite_wtf = form.heure_d_arrivee_prevue_wtf.data
        reelle_visite_wtf = form.heure_d_arrivee_reelle_wtf.data
        dure_visite_wtf = form.duree_wtf.data
        depart_visite_wtf = form.heure_de_depart_wtf.data
        motif_visite_wtf = form.motif_de_visite_wtf.data
        frequence_visite_wtf = form.frequence_de_visites_wtf.data
        batiment_visite_wtf = form.nom_du_batiment_wtf.data

        valeurs_insertion_dictionnaire = {
            "value_date_visite": date_visite_wtf,
            "value_prevue_visite": prevue_visite_wtf,
            "value_reelle_visite": reelle_visite_wtf,
            "value_dure_visite": dure_visite_wtf,
            "value_depart_visite": depart_visite_wtf,
            "value_motif_visite": motif_visite_wtf,
            "value_frequence_visite": frequence_visite_wtf,
            "value_batiment_visite": batiment_visite_wtf
        }

        print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

        strsql_insert_visite = """
            INSERT INTO t_visite (
                Date_de_Visite, Heure_d_Arrivee_Prevue, Heure_d_Arrivee_Reelle, Duree, Heure_de_Depart, Motif_de_Visite, Frequence_de_visites, Nom_du_Batiment
            ) VALUES (
                %(value_date_visite)s,
                %(value_prevue_visite)s,
                %(value_reelle_visite)s,
                %(value_dure_visite)s,
                %(value_depart_visite)s,
                %(value_motif_visite)s,
                %(value_frequence_visite)s,
                %(value_batiment_visite)s
            )
        """
        with DBconnection() as mconn_bd:
            mconn_bd.execute(strsql_insert_visite, valeurs_insertion_dictionnaire)

        flash("Données insérées !!", "success")
        print("Données insérées !!")

        return redirect(url_for('visite_afficher', order_by='DESC', id_visite_sel=0))

    return render_template("visite/visite_ajouter_wtf.html", form=form)

"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /visite_update

    Test : ex cliquer sur le menu "visite" puis cliquer sur le bouton "EDIT" d'un "visite"

    Paramètres : sans

    But : Editer(update) un visite qui a été sélectionné dans le formulaire "visite_afficher.html"

    Remarque :  Dans le champ "nom_visite_update_wtf" du formulaire "visite/visite_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/visite_update", methods=['GET', 'POST'])
def visite_update_wtf():
    id_visite_update = request.values.get('id_visite_btn_edit_html')
    form_update = FormWTFUpdateVisite()

    try:
        if request.method == "POST" and form_update.submit.data:
            date_visite_update = form_update.date_visite_update_wtf.data
            prevue_visite_update = form_update.heure_arrivee_prevue_update_wtf.data
            reelle_visite_update = form_update.heure_arrivee_reelle_update_wtf.data
            duree_visite_update = form_update.duree_update_wtf.data
            depart_visite_update = form_update.heure_depart_update_wtf.data
            motif_visite_update = form_update.motif_visite_update_wtf.data
            frequence_visite_update = form_update.frequence_visites_update_wtf.data
            batiment_visite_update = form_update.nom_batiment_update_wtf.data

            # Debugging information
            print(f"prevue_visite_update: {type(prevue_visite_update)}, {prevue_visite_update}")
            print(f"reelle_visite_update: {type(reelle_visite_update)}, {reelle_visite_update}")
            print(f"depart_visite_update: {type(depart_visite_update)}, {depart_visite_update}")

            # Conversion des objets datetime.time en chaînes de caractères
            if isinstance(prevue_visite_update, datetime.time):
                prevue_visite_update = prevue_visite_update.isoformat()
            elif isinstance(prevue_visite_update, str):
                prevue_visite_update = prevue_visite_update
            else:
                prevue_visite_update = None

            if isinstance(reelle_visite_update, datetime.time):
                reelle_visite_update = reelle_visite_update.isoformat()
            elif isinstance(reelle_visite_update, str):
                reelle_visite_update = reelle_visite_update
            else:
                reelle_visite_update = None

            if isinstance(depart_visite_update, datetime.time):
                depart_visite_update = depart_visite_update.isoformat()
            elif isinstance(depart_visite_update, str):
                depart_visite_update = depart_visite_update
            else:
                depart_visite_update = None

            valeur_update_dictionnaire = {
                "value_date_visite": date_visite_update,
                "value_prevue_visite": prevue_visite_update,
                "value_reelle_visite": reelle_visite_update,
                "value_dure_visite": duree_visite_update,
                "value_depart_visite": depart_visite_update,
                "value_motif_visite": motif_visite_update,
                "value_frequence_visite": frequence_visite_update,
                "value_batiment_visite": batiment_visite_update,
                "value_id_visite": id_visite_update
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_visite = """
                UPDATE t_visite
                SET Date_de_Visite = %(value_date_visite)s, 
                    Heure_d_Arrivee_Prevue = %(value_prevue_visite)s,
                    Heure_d_Arrivee_Reelle = %(value_reelle_visite)s,
                    Duree = %(value_dure_visite)s,
                    Heure_de_Depart = %(value_depart_visite)s,
                    Motif_de_Visite = %(value_motif_visite)s,
                    Frequence_de_visites = %(value_frequence_visite)s,
                    Nom_du_Batiment = %(value_batiment_visite)s
                WHERE ID_Visite = %(value_id_visite)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_visite, valeur_update_dictionnaire)

            flash("Donnée mise à jour !!", "success")
            print("Donnée mise à jour !!")

            return redirect(url_for('visite_afficher', order_by="ASC", id_visite_sel=id_visite_update))

        elif request.method == "GET":
            valeur_select_dictionnaire = {"value_id_visite": id_visite_update}

            str_sql_id_visite = """
                SELECT ID_Visite, Date_de_Visite, Heure_d_Arrivee_Prevue, Heure_d_Arrivee_Reelle, Duree, Heure_de_Depart, Motif_de_Visite, Frequence_de_visites, Nom_du_Batiment
                FROM t_visite
                WHERE ID_Visite = %(value_id_visite)s
            """
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_visite, valeur_select_dictionnaire)
                data_visite = mybd_conn.fetchone()

            if data_visite:
                form_update.date_visite_update_wtf.data = data_visite["Date_de_Visite"]
                form_update.heure_arrivee_prevue_update_wtf.data = data_visite["Heure_d_Arrivee_Prevue"]
                form_update.heure_arrivee_reelle_update_wtf.data = data_visite["Heure_d_Arrivee_Reelle"]
                form_update.duree_update_wtf.data = data_visite["Duree"]
                form_update.heure_depart_update_wtf.data = data_visite["Heure_de_Depart"]
                form_update.motif_visite_update_wtf.data = data_visite["Motif_de_Visite"]
                form_update.frequence_visites_update_wtf.data = data_visite["Frequence_de_visites"]
                form_update.nom_batiment_update_wtf.data = data_visite["Nom_du_Batiment"]
            else:
                flash("Visite non trouvée", "warning")
                return redirect(url_for('visite_afficher', order_by="ASC", id_visite_sel=0))

    except Exception as Exception_visite_update_wtf:
        raise ExceptionvisiteUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{visite_update_wtf.__name__} ; "
                                      f"{Exception_visite_update_wtf}")

    return render_template("visite/visite_update_wtf.html", form_update=form_update)

"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /visite_delete

    Test : ex. cliquer sur le menu "visite" puis cliquer sur le bouton "DELETE" d'un "visite"

    Paramètres : sans

    But : Effacer(delete) un visite qui a été sélectionné dans le formulaire "visite_afficher.html"

    Remarque :  Dans le champ "nom_visite_delete_wtf" du formulaire "visite/visite_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/visite_delete", methods=['GET', 'POST'])
def visite_delete_wtf():
    data_societe_attribue_visiteur_delete = None
    data_visite_attribue_visiteur_delete = None
    btn_submit_del = None
    id_visiteur_delete = request.values.get('id_visite_btn_delete_html')

    form_delete = FormWTFDeleteVisite()
    try:
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("visite_afficher", order_by="ASC", id_visite_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_societe_attribue_visiteur_delete = session.get('data_societe_attribue_visiteur_delete')
                data_visite_attribue_visiteur_delete = session.get('data_visite_attribue_visiteur_delete')

                flash("Effacer le visiteur de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_visiteur": id_visiteur_delete}

                str_sql_delete_annulation_visite = """DELETE FROM t_annulation_visite WHERE FK_visite IN 
                                                     (SELECT ID_Visite FROM t_visite WHERE ID_Visite IN 
                                                     (SELECT FK_visite FROM t_visiteur_visite WHERE FK_visiteur = %(value_id_visiteur)s))"""
                str_sql_delete_visiteur_visite = """DELETE FROM t_visiteur_visite WHERE FK_visiteur = %(value_id_visiteur)s"""
                str_sql_delete_visite_contact = """DELETE FROM t_visite_contact WHERE FK_visite IN 
                                                  (SELECT ID_Visite FROM t_visite WHERE ID_Visite IN 
                                                  (SELECT FK_visite FROM t_visiteur_visite WHERE FK_visiteur = %(value_id_visiteur)s))"""
                str_sql_delete_idvisiteur = """DELETE FROM t_visiteur WHERE ID_Visiteur = %(value_id_visiteur)s"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_annulation_visite, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_visiteur_visite, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_visite_contact, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idvisiteur, valeur_delete_dictionnaire)

                flash("Visiteur définitivement effacé !!", "success")

                return redirect(url_for('visite_afficher', order_by="ASC", id_visite_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_visiteur": id_visiteur_delete}

            str_sql_visiteur_societe_delete = """SELECT t_visiteur_societe.ID_visiteur_societe, t_visiteur.Nom, t_visiteur.Prenom, t_visiteur.ID_Visiteur, t_visiteur.Adresse, t_societe.Nom_de_la_Societe 
                                                FROM t_visiteur_societe 
                                                INNER JOIN t_visiteur ON t_visiteur_societe.FK_visiteur = t_visiteur.ID_Visiteur
                                                INNER JOIN t_societe ON t_visiteur_societe.FK_societe = t_societe.ID_Societe
                                                WHERE FK_visiteur = %(value_id_visiteur)s"""
            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_visiteur_societe_delete, valeur_select_dictionnaire)
                data_societe_attribue_visiteur_delete = mydb_conn.fetchall()
                session['data_societe_attribue_visiteur_delete'] = data_societe_attribue_visiteur_delete

                str_sql_visiteur_visite_delete = """SELECT t_visiteur_visite.ID_visiteur_visite, t_visiteur.Nom, t_visiteur.Prenom, t_visiteur.ID_Visiteur, t_visiteur.Adresse, t_visite.Date_de_Visite, t_visite.Motif_de_Visite, t_visite.Nom_du_Batiment 
                                                    FROM t_visiteur_visite 
                                                    INNER JOIN t_visiteur ON t_visiteur_visite.FK_visiteur = t_visiteur.ID_Visiteur
                                                    INNER JOIN t_visite ON t_visiteur_visite.FK_visite = t_visite.ID_Visite
                                                    WHERE FK_visiteur = %(value_id_visiteur)s"""
                mydb_conn.execute(str_sql_visiteur_visite_delete, valeur_select_dictionnaire)
                data_visite_attribue_visiteur_delete = mydb_conn.fetchall()
                session['data_visite_attribue_visiteur_delete'] = data_visite_attribue_visiteur_delete

                str_sql_id_visiteur = "SELECT ID_Visiteur, Nom FROM t_visiteur WHERE ID_Visiteur = %(value_id_visiteur)s"
                mydb_conn.execute(str_sql_id_visiteur, valeur_select_dictionnaire)
                data_nom_visiteur = mydb_conn.fetchone()

            form_delete.nom_visite_delete_wtf.data = data_nom_visiteur["Nom"]
            btn_submit_del = False

    except Exception as Exception_visite_delete_wtf:
        raise ExceptionvisiteDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                       f"{visite_delete_wtf.__name__} ; "
                                       f"{Exception_visite_delete_wtf}")

    return render_template("visite/visite_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_societe_associes=data_societe_attribue_visiteur_delete,
                           data_visite_associes=data_visite_attribue_visiteur_delete)
