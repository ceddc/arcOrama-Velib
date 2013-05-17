# -*- coding: cp1252 -*-
# modules Python : requests pour les requ�tes HTTP et json pour l'encodage Json
#
import requests, json

# On r�cup�re l'�tat courant des stations v�lib sous forme JSON
# remplacer les "xxx" par votre API Key JC Decaux
#
etat = requests.get('https://api.jcdecaux.com/vls/v1/stations?apiKey=xxxxxxxx&contract=Paris').json()

# d'abord on r�cup�re un Token sur ArcGIS Online qui permettra de s'authentifier sur la plateforme
# Substituer vos propres nom d'utilisateur et mot de passe
#
agol_url = 'https://www.arcgis.com/sharing/rest/generateToken'
agol_user = 'votre_nom_d_utilisateur'
agol_password = 'votre_mot_de_passe'

# Le referer n'a pas d'importance pour ce type de requ�te � partir d'un script
#
params = {'username': agol_user,'password': agol_password, 'f': 'pjson', 'client': 'referer','referer':'arcgis.com'}
token_reponse = requests.post(agol_url,data=params)
token = token_reponse.json()['token']

# On r�cup�re toutes les stations � partir du service d'entit�s ArcGIS Online
# en passant le token en param�tre. Notez le referer pass� dans le Header de la requ�te,
# n�c�ssaire par rapport � l'encodage du token.
# La requ�te 1=1 permet de r�cup�rer toutes les stations
# Vous devez changer l'URL d'acc�s au service d'entit� pour pointer vers votre propre service
#
query_url = 'https://services.arcgis.com/xxxxxxxxxxx/ArcGIS/rest/services/xxxxxxx/FeatureServer/0/query'
params = {'where': '1=1','outfields': '*','f': 'json','token': token}
headers = {'referer': 'www.arcgis.com'}
query_reponse = requests.get(query_url,data=params,headers=headers)
features = query_reponse.json()['features']

nb_updated_features=0
nb_unchanged_features=0


updatedFeatures = []

# On it�re station par station dans le jeux de donn�es ArcGIS
#
for feature in features:
    number = feature['attributes']['number']
    # On lance la recherche de la station courante dans les donn�es issues de l'API Velib
    #
    for etat_station in etat:
        if etat_station['number'] == number:
            # On a trouv� la station courante,
            # a-t-elle �t� mise � jour par rapport � son �tat dans ArcGIS Online ?
            #
            if etat_station['last_update'] > feature['attributes']['last_update']:
                # On met � jour la station (dans les objets Python)
                #
                feature['attributes']['status'] = etat_station['status']
                feature['attributes']['available_bike_stands'] = etat_station['available_bike_stands']
                feature['attributes']['available_bikes'] = etat_station['available_bikes']
                feature['attributes']['last_update'] = etat_station['last_update']
                # On copie la version mise � jour dans une liste des objets mis � jour
                #
                updatedFeatures.append(feature)
                nb_updated_features=nb_updated_features+1
            else:
                nb_unchanged_features=nb_unchanged_features+1
            break

# On va poster via HTTP la liste des objets mis � jour sur le Endpoint REST ArcGIS permettant
# la mise � jour de la couche carto des stations
# Ces objets sont "dump�s" en Json avant d'�tre post�s en HTTP
# Vous devez changer l'URL d'acc�s au service d'entit� pour pointer vers votre propre service
#
update_url = 'http://services.arcgis.com/xxxxxxxxxxxxxx/ArcGIS/rest/services/xxxxxxx/FeatureServer/0/updateFeatures'
params = {'features': json.dumps(updatedFeatures),'f': 'json','token': token}
update_reponse = requests.post(update_url,data=params,headers=headers)

print str(nb_updated_features) + " stations mises � jour et " + str(nb_unchanged_features) + ' stations inchang�es'
