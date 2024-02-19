# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 19:40:32 2024

@author: jean-jonathan
"""

from PIL import Image, ImageDraw
import math
from PIL import Image, ImageDraw, ImageStat
import colorsys

"Fonction de Validation d'Avatar"
'''
But: Vérifie la taille, la forme circulaire et les couleurs. 
Retourne un résultat de validation.'''

def valider_avatar(chemin_image):
    try:
        # On charge l'image
        with Image.open(chemin_image) as img:
            # On vérifie la taille de l'image
            if img.size != (512, 512):
                return "La taille de l'image doit être de 512x512 pixels."

            # Préparation d'un masque pour le cercle
            masque = Image.new('L', (512, 512), 0) # On crée une nouvelle image en mode L (niveaux de gris) avec une couleur de fond noire (0 cad noir en niveaux de gris).
            dessin = ImageDraw.Draw(masque)
            dessin.ellipse((0, 0, 512, 512), fill=255) # On dessine une ellipse qui remplit toute l'image masque. fill=255 remplit le cercle en blanc

            # On vérifie si tous les pixels non transparents sont uniquement à l'intérieur du cercle
            for x in range(512):
                for y in range(512):
                    if masque.getpixel((x, y)) == 0 and img.getpixel((x, y))[3] != 0: # Si Le pixel correspondant dans le masque est noir, donc il se trouve à l'extérieur du cercle blanc et on verifie si le quatrième composant (ind 3) du pixel dans image originale (img) n est pas égal à 0 
                        return "Des pixels non transparents se trouvent en dehors du cercle."

            return "L'image est valide."
    except IOError:
        return "Erreur lors de la lecture de l'image."

print(valider_avatar('C:\\Users\\HP\\Downloads\\School\\BUT3\\Semestre5\\R5A11MéthodesOptimisationpourAideALadécision\\AbreDeDecision\\projetSaid\\android-chrome-512x512.png'))

"Fonction de Conversion d'Image"
'''
But: Convertir une image de n'importe quel format en un avatar circulaire de 512x512 pixels.
Cette fonction devra ajuster la taille de l'image, la découper en forme circulaire et
éventuellement ajuster les couleurs.
'''
def convertir_en_avatar(chemin_image):
    # On charge l'image et la redimensionner
    with Image.open(chemin_image) as img: # Image.open gere tout les formats
        img = img.resize((512, 512))

        # Création d'un masque circulaire
        masque = Image.new('L', (512, 512), 0)
        dessin = ImageDraw.Draw(masque)
        dessin.ellipse((0, 0, 512, 512), fill=255)

        # On applique le masque à l'image
        img.putalpha(masque)

        # Enregistrement de l'image
        img.save('avatar_circulaire.png')  
        return img  # Ou on retourne sous forme objet image

convertir_en_avatar('C:\\Users\\HP\\Downloads\\School\\BUT3\\Semestre5\\R5A11MéthodesOptimisationpourAideALadécision\\AbreDeDecision\\projetSaid\\android-chrome-512x512.png')



'''fonction d'analyse des couleurs pour déterminer si elles évoquent une sensation
 de bonheur '''
def est_proche(couleur, cible, seuil=30):
    """ On vérifie si une couleur est proche d'une cible avec un certain seuil """
    return all(abs(c - t) <= seuil for c, t in zip(couleur, cible))

def saturation_et_luminosite(rgb):
    """ On convertit RGB en HLS et renvoie la saturation et la luminosité """
    return colorsys.rgb_to_hls(*rgb)[1:3]

def analyser_couleurs(chemin_image):
    # Définition des couleurs de bonheur avec des plages de tolérance
    couleurs_bonheur = [
        (255, 255, 0),  # Jaune
        (0, 255, 0),    # Vert
        (0, 255, 255)   # Cyan
    ]

    # On charge l'image et on la convertir en RGB
    with Image.open(chemin_image) as img:
        img = img.convert('RGB')

        # On obtient les données de couleur
        pixels = list(img.getdata())

        # Analyse des pixels
        compteur_bonheur, compteur_total = 0, 0
        for pixel in pixels:
            # Vérification de la proximité avec les couleurs de bonheur
            if any(est_proche(pixel, couleur_bonheur) for couleur_bonheur in couleurs_bonheur):
                compteur_bonheur += 1
            
            # Analyse de la saturation et de la luminosité
            saturation, luminosite = saturation_et_luminosite(pixel)
            if saturation > 0.5 and luminosite > 0.5:  # Seuil de saturation et luminosité
                compteur_total += 1

        # Calcul du pourcentage
        pourcentage_bonheur = (compteur_bonheur / len(pixels)) * 100
        pourcentage_sat_lum = (compteur_total / len(pixels)) * 100

        return f"Pourcentage de couleurs de bonheur: {pourcentage_bonheur:.2f}%, Pourcentage de couleurs vives: {pourcentage_sat_lum:.2f}%"

print(analyser_couleurs('C:\\Users\\HP\\Downloads\\School\\BUT3\\Semestre5\\R5A11MéthodesOptimisationpourAideALadécision\\AbreDeDecision\\projetSaid\\android-chrome-512x512.png'))
