"""
    Fichier : gestion_visite_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, IntegerField, StringField, SubmitField
from wtforms.validators import Length, Optional, ValidationError
import datetime

def valid_time(form, field):
    if field.data:
        try:
            if isinstance(field.data, datetime.time):
                return  # La valeur est déjà un objet datetime.time valide
            elif isinstance(field.data, datetime.timedelta):
                raise ValidationError("Not a valid time value.")
            datetime.time.fromisoformat(str(field.data))
        except ValueError:
            raise ValidationError("Not a valid time value.")


class FormWTFAjouterVisite(FlaskForm):
    date_de_visite_wtf = DateField("Date de la visite", format='%Y-%m-%d', validators=[Optional()])
    heure_d_arrivee_prevue_wtf = TimeField("Heure d'arrivée prévue", validators=[valid_time])
    heure_d_arrivee_reelle_wtf = TimeField("Heure d'arrivée réelle", validators=[valid_time])
    heure_de_depart_wtf = TimeField("Heure de départ", validators=[valid_time])
    duree_wtf = IntegerField("Durée de la visite (en minutes)", validators=[Optional()])
    motif_de_visite_wtf = StringField("Motif de la visite", validators=[
        Length(min=0, max=255, message="Max 255 caractères"),
        Optional()
    ])
    frequence_de_visites_wtf = StringField("Fréquence des visites", validators=[
        Length(min=0, max=50, message="Max 50 caractères"),
        Optional()
    ])
    nom_du_batiment_wtf = StringField("Nom du bâtiment", validators=[
        Length(min=0, max=255, message="Max 255 caractères"),
        Optional()
    ])
    submit = SubmitField("Enregistrer la visite")

class FormWTFUpdateVisite(FlaskForm):
    date_visite_update_wtf = DateField("Date de la visite", format='%Y-%m-%d', validators=[Optional()])
    heure_arrivee_prevue_update_wtf = TimeField("Heure d'arrivée prévue", validators=[valid_time])
    heure_arrivee_reelle_update_wtf = TimeField("Heure d'arrivée réelle", validators=[valid_time])
    heure_depart_update_wtf = TimeField("Heure de départ", validators=[valid_time])
    duree_update_wtf = IntegerField("Durée de la visite (en minutes)", validators=[Optional()])
    motif_visite_update_wtf = StringField("Motif de la visite", validators=[
        Length(min=0, max=255, message="Max 255 caractères"),
        Optional()
    ])
    frequence_visites_update_wtf = StringField("Fréquence des visites", validators=[
        Length(min=0, max=50, message="Max 50 caractères"),
        Optional()
    ])
    nom_batiment_update_wtf = StringField("Nom du bâtiment", validators=[
        Length(min=0, max=255, message="Max 255 caractères"),
        Optional()
    ])
    submit = SubmitField("Enregistrer la visite")

class FormWTFDeleteVisite(FlaskForm):
    """
        Dans le formulaire "visite_delete_wtf.html"

        nom_visite_delete_wtf : Champ qui reçoit la valeur du visite, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "visite".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_visite".
    """
    nom_visite_delete_wtf = StringField("Effacer ce visiteur")
    submit_btn_del = SubmitField("Effacer Visiteur")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")