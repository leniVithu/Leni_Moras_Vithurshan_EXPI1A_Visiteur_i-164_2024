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
    nom_genre_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_genre_update_wtf = StringField("Le nom de le visiteur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_genre_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    prenom_genre_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_genre_update_wtf = StringField("Prénom du visiteur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                      Regexp(prenom_genre_update_regexp,
                                                                             message="Pas de chiffres, de caractères "
                                                                                     "spéciaux, "
                                                                                     "d'espace à double, de double "
                                                                                     "apostrophe, de double trait union")
                                                                      ])

    adresse_genre_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    adresse_genre_update_wtf = StringField("Adresse du visiteur ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                        Regexp(adresse_genre_update_regexp,
                                                                               message="Pas de chiffres, de caractères "
                                                                                       "spéciaux, "
                                                                                       "d'espace à double, de double "
                                                                                       "apostrophe, de double trait union")
                                                                        ])
    datenaiss_genre_regexp = "^[\d-]+$"
    datenaiss_genre_update_wtf = StringField("Date de naissance du visiteur ",
                                      validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                  Regexp(nom_genre_update_regexp,
                                                         message="Pas de lettres, caractères "
                                                                 "spéciaux, "
                                                                 "d'espace à double, de double "
                                                                 "apostrophe, de double trait union")
                                                  ])
    telephone_genre_regexp = "^[\d-]+$"
    telephone_genre_update_wtf = StringField("Numéro de téléphone du visiteur ",
                                      validators=[Length(min=2, max=30, message="min 2 max 30"),
                                                  Regexp(nom_genre_update_regexp,
                                                         message="Pas de lettres, de caractères "
                                                                 "spéciaux, "
                                                                 "d'espace à double, de double "
                                                                 "apostrophe, de double trait union")
                                                  ])
    idsociete_genre_regexp = "^[1-9]|10$"
    idsociete_genre_update_wtf = StringField("Société du visiteur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_genre_update_regexp,
                                                                                 message="Choisir la bonne ID dans la liste suivante (1 ABC Company, 2 XYZ Corporation, 3 LMN Enterprises, 4 123 Industries, 5 PQR Ltd, 6 EFG Group, 7 UVW Inc, 8 RST Co, 9 GHI Ltd, 10 JKL Enterprise)")
                                                                          ])
    vehicule_genre_regexp = "^(oui|non)$"
    vehicule_genre_update_wtf = StringField("Est-ce que le visiteur vient en véhicule? ",
                                     validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                 Regexp(nom_genre_update_regexp,
                                                        message="Seulement oui ou non")
                                                 ])

    date_genre_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update genre")


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