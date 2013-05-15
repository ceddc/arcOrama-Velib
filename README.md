arcOrama-Velib
==============

Scripts, code et apps d'intégration des opendata Velib dans ArcGIS

Ce script Python permet l'intégration du flux de données temps réel de l'API Velib Opendata dans une classe d'entités stockée sur ArcGIS Online.

La classe d'entités doit déjà contenir 1227 points (à la date de création du script) décrivant les stations avec les champs suivants qui seront mis à jour à chaque exécution :

number (type: esriFieldTypeInteger, alias: number, SQL Type: sqlTypeOther, nullable: true, editable: true)
status (type: esriFieldTypeString, alias: status, SQL Type: sqlTypeOther, length: 50, nullable: true, editable: true)
bike_stands (type: esriFieldTypeSmallInteger, alias: bike_stands, SQL Type: sqlTypeOther, nullable: true, editable: true)
available_bike_stands (type: esriFieldTypeSmallInteger, alias: available_bike_stands, SQL Type: sqlTypeOther, nullable: true, editable: true)
available_bikes (type: esriFieldTypeSmallInteger, alias: available_bikes, SQL Type: sqlTypeOther, nullable: true, editable: true)
last_update (type: esriFieldTypeDate, alias: last_update, SQL Type: sqlTypeOther, length: 8, nullable: true, editable: true)

Dans ce script, doivent être modifiés pour correspondre à votre environnement :
- Username/Password ArcGIS Online utilisé pour l'exécution
- URL REST d'accès Query et Update à la classe d'entité des stations





