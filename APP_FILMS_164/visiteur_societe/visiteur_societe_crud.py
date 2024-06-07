"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les genres.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *




@app.route("/visiteurs_societes_afficher/<int:id_visiteur_sel>", methods=['GET', 'POST'])
def visiteurs_societes_afficher(id_visiteur_sel):
    print(" visiteurs_societes_afficher id_visiteur_sel ", id_visiteur_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_visiteurs_societes_afficher_data = """
                    SELECT 
                        t_visiteur.ID_Visiteur, 
                        t_visiteur.Nom, 
                        t_visiteur.Prenom, 
                        t_visiteur.Adresse, 
                        t_visiteur.Date_de_Naissance, 
                        t_visiteur.Numero_de_Telephone, 
                        t_visiteur.Le_Visiteur_se_deplace_en_Vehicule_Personnel,
                        GROUP_CONCAT(t_societe.Nom_de_la_Societe) as Societes
                    FROM t_visiteur_societe
                    RIGHT JOIN t_visiteur ON t_visiteur.ID_Visiteur = t_visiteur_societe.FK_visiteur
                    LEFT JOIN t_societe ON t_societe.ID_Societe = t_visiteur_societe.FK_societe
                    GROUP BY t_visiteur.ID_Visiteur
                """
                if id_visiteur_sel == 0:
                    # le paramètre 0 permet d'afficher tous les visiteurs
                    # Sinon le paramètre représente la valeur de l'id du visiteur
                    mc_afficher.execute(strsql_visiteurs_societes_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du visiteur sélectionné avec un nom de variable
                    valeur_id_visiteur_selected_dictionnaire = {"value_id_visiteur_selected": id_visiteur_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    strsql_visiteurs_societes_afficher_data += """ HAVING t_visiteur.ID_Visiteur= %(value_id_visiteur_selected)s"""

                    mc_afficher.execute(strsql_visiteurs_societes_afficher_data, valeur_id_visiteur_selected_dictionnaire)

                # Récupère les données de la requête.
                data_visiteurs_societes_afficher = mc_afficher.fetchall()
                print("data_visiteurs_societes_afficher ", data_visiteurs_societes_afficher, " Type : ", type(data_visiteurs_societes_afficher))

                # Différencier les messages.
                if not data_visiteurs_societes_afficher and id_visiteur_sel == 0:
                    flash("""La table "t_visiteur" est vide. !""", "warning")
                elif not data_visiteurs_societes_afficher and id_visiteur_sel > 0:
                    # Si l'utilisateur change l'id_visiteur dans l'URL et qu'il ne correspond à aucun visiteur
                    flash(f"Le visiteur {id_visiteur_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données visiteurs et sociétés affichées !!", "success")

        except Exception as Exception_visiteurs_societes_afficher:
            raise ExceptionVisiteursSocietesAfficher(f"fichier : {Path(__file__).name}  ;  {visiteurs_societes_afficher.__name__} ;"
                                               f"{Exception_visiteurs_societes_afficher}")

    print("visiteurs_societes_afficher  ", data_visiteurs_societes_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("visiteur_societe/visiteur_societe_afficher.html", data=data_visiteurs_societes_afficher)





"""Fonction pour afficher les données des visiteurs et leurs sociétés associées"""

def visiteurs_societes_afficher_data(valeur_id_visiteur_selected_dict):
    print("valeur_id_visiteur_selected_dict...", valeur_id_visiteur_selected_dict)
    try:
        strsql_visiteur_selected = """SELECT ID_Visiteur, Nom, Prenom, Adresse, Date_de_Naissance, Numero_de_Telephone, Le_Visiteur_se_deplace_en_Vehicule_Personnel, 
                                      GROUP_CONCAT(ID_Societe) as Societes 
                                      FROM t_visiteur_societe
                                      INNER JOIN t_visiteur ON t_visiteur.ID_Visiteur = t_visiteur_societe.FK_visiteur
                                      INNER JOIN t_societe ON t_societe.ID_Societe = t_visiteur_societe.FK_societe
                                      WHERE ID_Visiteur = %(value_id_visiteur_selected)s"""

        strsql_societes_visiteurs_non_attribues = """SELECT ID_Societe, Nom_de_la_Societe FROM t_societe WHERE ID_Societe NOT IN (SELECT ID_Societe FROM t_visiteur_societe
                                      INNER JOIN t_visiteur ON t_visiteur.ID_Visiteur = t_visiteur_societe.FK_visiteur
                                      INNER JOIN t_societe ON t_societe.ID_Societe = t_visiteur_societe.FK_societe
                                      WHERE ID_Visiteur = %(value_id_visiteur_selected)s)"""

        strsql_societes_visiteurs_attribues = """SELECT ID_Visiteur, ID_Societe, Nom_de_la_Societe FROM t_visiteur_societe
                                      INNER JOIN t_visiteur ON t_visiteur.ID_Visiteur = t_visiteur_societe.FK_visiteur
                                      INNER JOIN t_societe ON t_societe.ID_Societe = t_visiteur_societe.FK_societe
                                      WHERE ID_Visiteur = %(value_id_visiteur_selected)s"""

        with DBconnection() as mc_afficher:
            mc_afficher.execute(strsql_societes_visiteurs_non_attribues, valeur_id_visiteur_selected_dict)
            data_societes_visiteurs_non_attribues = mc_afficher.fetchall()
            print("visiteurs_societes_afficher_data ----> data_societes_visiteurs_non_attribues ", data_societes_visiteurs_non_attribues,
                  " Type : ", type(data_societes_visiteurs_non_attribues))

            mc_afficher.execute(strsql_visiteur_selected, valeur_id_visiteur_selected_dict)
            data_visiteur_selected = mc_afficher.fetchall()
            print("data_visiteur_selected  ", data_visiteur_selected, " Type : ", type(data_visiteur_selected))

            mc_afficher.execute(strsql_societes_visiteurs_attribues, valeur_id_visiteur_selected_dict)
            data_societes_visiteurs_attribues = mc_afficher.fetchall()
            print("data_societes_visiteurs_attribues ", data_societes_visiteurs_attribues, " Type : ",
                  type(data_societes_visiteurs_attribues))

            return data_visiteur_selected, data_societes_visiteurs_non_attribues, data_societes_visiteurs_attribues

    except Exception as Exception_visiteurs_societes_afficher_data:
        raise ExceptionVisiteursSocietesAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{visiteurs_societes_afficher_data.__name__} ; "
                                               f"{Exception_visiteurs_societes_afficher_data}")


"""
   GET ET POST
   POUR MODIFIER

"""


@app.route("/edit_visiteur_societe_selected", methods=['GET', 'POST'])
def edit_visiteur_societe_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_societes_afficher = """SELECT ID_Societe, Nom_de_la_Societe FROM t_societe ORDER BY ID_Societe ASC"""
                mc_afficher.execute(strsql_societes_afficher)
            data_societes_all = mc_afficher.fetchall()
            print("dans edit_visiteur_societe_selected ---> data_societes_all", data_societes_all)

            id_visiteur_societes_edit = request.values['id_visiteur_societes_edit_html']
            session['session_id_visiteur_societes_edit'] = id_visiteur_societes_edit

            valeur_id_visiteur_selected_dictionnaire = {"value_id_visiteur_selected": id_visiteur_societes_edit}

            data_visiteur_societe_selected, data_societes_visiteurs_non_attribues, data_societes_visiteurs_attribues = \
                visiteurs_societes_afficher_data(valeur_id_visiteur_selected_dictionnaire)

            lst_data_visiteur_selected = [item['ID_Visiteur'] for item in data_visiteur_societe_selected]
            lst_data_societes_visiteurs_non_attribues = [item['ID_Societe'] for item in data_societes_visiteurs_non_attribues]
            session['session_lst_data_societes_visiteurs_non_attribues'] = lst_data_societes_visiteurs_non_attribues

            lst_data_societes_visiteurs_old_attribues = [item['ID_Societe'] for item in data_societes_visiteurs_attribues]
            session['session_lst_data_societes_visiteurs_old_attribues'] = lst_data_societes_visiteurs_old_attribues

        except Exception as Exception_edit_visiteur_societe_selected:
            raise ExceptionEditVisiteurSocieteSelected(f"fichier : {Path(__file__).name}  ;  "
                                                       f"{edit_visiteur_societe_selected.__name__} ; "
                                                       f"{Exception_edit_visiteur_societe_selected}")

    return render_template("visiteur_societe/visiteur_societe_modifier_tags_dropbox.html",
                           data_societes=data_societes_all,
                           data_visiteur_selected=data_visiteur_societe_selected,
                           data_societes_attribues=data_societes_visiteurs_attribues,
                           data_societes_non_attribues=data_societes_visiteurs_non_attribues)

@app.route("/update_visiteur_societe_selected", methods=['GET', 'POST'])
def update_visiteur_societe_selected():
    if request.method == "POST":
        try:
            id_visiteur_selected = session['session_id_visiteur_societes_edit']
            old_lst_data_societes_visiteurs_non_attribues = session['session_lst_data_societes_visiteurs_non_attribues']
            old_lst_data_societes_visiteurs_attribues = session['session_lst_data_societes_visiteurs_old_attribues']

            session.clear()

            new_lst_str_societes_visiteurs = request.form.getlist('name_select_tags')
            new_lst_int_societes_visiteurs = list(map(int, new_lst_str_societes_visiteurs))

            lst_diff_societes_delete_b = list(set(old_lst_data_societes_visiteurs_attribues) - set(new_lst_int_societes_visiteurs))
            lst_diff_societes_insert_a = list(set(new_lst_int_societes_visiteurs) - set(old_lst_data_societes_visiteurs_attribues))

            strsql_insert_societe_visiteur = """INSERT INTO t_visiteur_societe (ID_visiteur_societe, FK_societe, FK_visiteur)
                                                VALUES (NULL, %(value_fk_societe)s, %(value_fk_visiteur)s)"""

            strsql_delete_societe_visiteur = """DELETE FROM t_visiteur_societe WHERE FK_societe = %(value_fk_societe)s AND FK_visiteur = %(value_fk_visiteur)s"""

            with DBconnection() as mconn_bd:
                for id_societe_ins in lst_diff_societes_insert_a:
                    valeurs_visiteur_sel_societe_sel_dictionnaire = {"value_fk_visiteur": id_visiteur_selected,
                                                                     "value_fk_societe": id_societe_ins}

                    mconn_bd.execute(strsql_insert_societe_visiteur, valeurs_visiteur_sel_societe_sel_dictionnaire)

                for id_societe_del in lst_diff_societes_delete_b:
                    valeurs_visiteur_sel_societe_sel_dictionnaire = {"value_fk_visiteur": id_visiteur_selected,
                                                                     "value_fk_societe": id_societe_del}

                    mconn_bd.execute(strsql_delete_societe_visiteur, valeurs_visiteur_sel_societe_sel_dictionnaire)

        except Exception as Exception_update_visiteur_societe_selected:
            raise ExceptionUpdateVisiteurSocieteSelected(f"fichier : {Path(__file__).name}  ;  "
                                                         f"{update_visiteur_societe_selected.__name__} ; "
                                                         f"{Exception_update_visiteur_societe_selected}")

    return redirect(url_for('visiteurs_societes_afficher', id_visiteur_sel=id_visiteur_selected))




