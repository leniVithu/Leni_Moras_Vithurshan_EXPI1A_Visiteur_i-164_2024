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

class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_regexp = "^[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'\- ]*$"
    nom_genre_wtf = StringField("Nom du visiteur ", validators=[
        Length(min=2, max=20, message="min 2 max 20"),
        Regexp(nom_genre_regexp,
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait d'union")
    ])

    prenom_genre_regexp = "^[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'\- ]*$"
    prenom_genre_wtf = StringField("Prénom du visiteur ", validators=[
        Length(min=2, max=20, message="min 2 max 20"),
        Regexp(prenom_genre_regexp,
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait d'union")
    ])

    adresse_genre_wtf = StringField("Adresse du visiteur ", validators=[
        Length(min=2, max=50, message="min 2 max 50")
    ])

    datenaiss_genre_wtf = DateField("Date de naissance du visiteur ", format='%Y-%m-%d', validators=[
        DataRequired(message="Veuillez entrer une date valide au format AAAA-MM-JJ")
    ])

    telephone_genre_wtf = StringField("Numéro de téléphone du visiteur ", validators=[
        Length(min=2, max=30, message="min 2 max 30")
    ])

    vehicule_genre_wtf = StringField("Est-ce que le visiteur vient en véhicule? ", validators=[
        Length(min=2, max=20, message="min 2 max 20")
    ])

    submit = SubmitField("Enregistrer le visiteur")

class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_regexp = "^[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'\- ]*$"
    nom_genre_updatewtf = StringField("Nom du visiteur ", validators=[
        Length(min=2, max=20, message="min 2 max 20"),
        Regexp(nom_genre_regexp,
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait d'union")
    ])

    prenom_genre_regexp = "^[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'\- ]*$"
    prenom_genre_updatewtf = StringField("Prénom du visiteur ", validators=[
        Length(min=2, max=20, message="min 2 max 20"),
        Regexp(prenom_genre_regexp,
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait d'union")
    ])

    adresse_genre_updatewtf = StringField("Adresse du visiteur ", validators=[
        Length(min=2, max=50, message="min 2 max 50")
    ])

    datenaiss_genre_updatewtf = DateField("Date de naissance du visiteur ", format='%Y-%m-%d', validators=[
        DataRequired(message="Veuillez entrer une date valide au format AAAA-MM-JJ")
    ])

    telephone_genre_updatewtf = StringField("Numéro de téléphone du visiteur ", validators=[
        Length(min=2, max=30, message="min 2 max 30")
    ])

    vehicule_genre_updatewtf = StringField("Est-ce que le visiteur vient en véhicule? ", validators=[
        Length(min=2, max=20, message="min 2 max 20")
    ])
    submit = SubmitField("Update visiteur")


class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_genre_delete_wtf = StringField("Effacer ce genre")
    submit_btn_del = SubmitField("Effacer genre")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")