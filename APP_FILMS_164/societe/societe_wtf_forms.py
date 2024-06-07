"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp

class FormWTFAjouterSociete(FlaskForm):
    """
        Formulaire pour ajouter une société.
    """
    nom_societe_regexp = r"^[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'\- ]*$"
    nom_societe_wtf = StringField("Nom de la société ", validators=[
        Length(min=2, max=255, message="min 2 max 255"),
        Regexp(nom_societe_regexp,
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait d'union")
    ])

    submit = SubmitField("Enregistrer la société")

class FormWTFUpdateSociete(FlaskForm):
    """
        Dans le formulaire "societe_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_societe_regexp = r"^[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'\- ]*$"
    nom_societe_update_wtf = StringField("Nom de la société ", validators=[
        Length(min=2, max=20, message="min 2 max 20"),
        Regexp(nom_societe_regexp,
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait d'union")
    ])
    submit = SubmitField("Update société")

class FormWTFDeleteSociete(FlaskForm):
    """
        Dans le formulaire "societe_delete_wtf.html"

        nom_societe_delete_wtf : Champ qui reçoit la valeur du nom de la société, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer une société.
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_societe".
    """
    nom_societe_delete_wtf = StringField("Effacer cette société")
    submit_btn_del = SubmitField("Effacer société")
    submit_btn_conf_del = SubmitField("Etes-vous sûr d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
