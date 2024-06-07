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
from APP_FILMS_164.societe.societe_wtf_forms import FormWTFAjouterSociete,FormWTFUpdateSociete,FormWTFDeleteSociete


"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher

    Test : ex : http://127.0.0.1:5575/genres_afficher

    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/societes_afficher/<string:order_by>/<int:id_societe_sel>", methods=['GET', 'POST'])
def societes_afficher(order_by, id_societe_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_societe_sel == 0:
                    strsql_societes_afficher = """SELECT * FROM t_societe"""
                    mc_afficher.execute(strsql_societes_afficher)
                elif order_by == "ASC":
                    valeur_id_societe_selected_dictionnaire = {"value_id_societe_selected": id_societe_sel}
                    strsql_societes_afficher = """SELECT * FROM t_societe WHERE ID_Societe = %(value_id_societe_selected)s"""
                    mc_afficher.execute(strsql_societes_afficher, valeur_id_societe_selected_dictionnaire)
                else:
                    strsql_societes_afficher = """SELECT * FROM t_societe ORDER BY ID_Societe DESC"""
                    mc_afficher.execute(strsql_societes_afficher)

                data_societes = mc_afficher.fetchall()

                print("data_societes ", data_societes, " Type : ", type(data_societes))

                if not data_societes and id_societe_sel == 0:
                    flash("""La table "t_societe" est vide. !!""", "warning")
                elif not data_societes and id_societe_sel > 0:
                    flash(f"La société demandée n'existe pas !!", "warning")
                else:
                    flash(f"Données sociétés affichées !!", "success")

        except Exception as Exception_societes_afficher:
            raise ExceptionSocietesAfficher(f"fichier : {Path(__file__).name}  ;  "
                                            f"{societes_afficher.__name__} ; "
                                            f"{Exception_societes_afficher}")

    return render_template("societes/societes_afficher.html", data=data_societes)


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


@app.route("/societes_ajouter", methods=['GET', 'POST'])
def societes_ajouter_wtf():
    form = FormWTFAjouterSociete()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_societe_wtf = form.nom_societe_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_nom_societe": nom_societe_wtf
                }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_societe = """
                    INSERT INTO t_societe (Nom_de_la_Societe)
                    VALUES (%(value_nom_societe)s)
                """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_societe, valeurs_insertion_dictionnaire)

                flash("Données insérées !!", "success")
                print("Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('societes_afficher', order_by='DESC', id_societe_sel=0))

        except Exception as Exception_societes_ajouter_wtf:
            raise ExceptionSocietesAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                              f"{societes_ajouter_wtf.__name__} ; "
                                              f"{Exception_societes_ajouter_wtf}")

    return render_template("societes/societes_ajouter_wtf.html", form=form)


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


@app.route("/societe_update", methods=['GET', 'POST'])
def societe_update_wtf():
    id_societe_update = request.values['id_societe_btn_edit_html']
    form_update = FormWTFUpdateSociete()

    try:
        if request.method == "POST" and form_update.submit.data:
            nom_societe_update = form_update.nom_societe_update_wtf.data

            valeur_update_dictionnaire = {
                "value_nom_societe": nom_societe_update,
                "value_id_societe": id_societe_update
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_societe = """
                UPDATE t_societe
                SET Nom_de_la_Societe = %(value_nom_societe)s
                WHERE ID_Societe = %(value_id_societe)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_societe, valeur_update_dictionnaire)

            flash("Donnée mise à jour !!", "success")
            print("Donnée mise à jour !!")

            return redirect(url_for('societes_afficher', order_by="ASC", id_societe_sel=id_societe_update))

        elif request.method == "GET":
            str_sql_id_societe = """
                SELECT ID_Societe, Nom_de_la_Societe
                FROM t_societe
                WHERE ID_Societe = %(value_id_societe)s
            """
            valeur_select_dictionnaire = {"value_id_societe": id_societe_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_societe, valeur_select_dictionnaire)
                data_nom_societe = mybd_conn.fetchone()

            if data_nom_societe:
                print("data_nom_societe ", data_nom_societe, " type ", type(data_nom_societe), " societe ",
                      data_nom_societe["Nom_de_la_Societe"])

                form_update.nom_societe_update_wtf.data = data_nom_societe["Nom_de_la_Societe"]
            else:
                flash("Société non trouvée", "warning")
                return redirect(url_for('societes_afficher', order_by="ASC", id_societe_sel=0))
    except Exception as Exception_societe_update_wtf:
        raise ExceptionSocieteUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                        f"{societe_update_wtf.__name__} ; "
                                        f"{Exception_societe_update_wtf}")

    return render_template("societes/societe_update_wtf.html", form_update=form_update)




