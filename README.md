# FPGA_Securise
Repo du projet de 2A FPGA sécurisé

## Contexte

- Récupération de la donnée issue de l'instrument
- Chiffrement
- Transmission par UART à un ordinateur
- Lecture, déchiffrement, affichage en python sur l'ordinateur

Input:
- Taille ECG: 161 samples
- UART

Output:
- 181 octets chiffrés 
- UART

ASCON:
- DA ou data sur 64 bits (21 paquets de 64 bits pour les 161 octets d'ECG. Le 21e a un padding de x 0)

Liste tâches:
- Comprendre ASCON
- Faire un test-bench: machine d'etat qui fait tourner le ascon fourni
- Inclure la machine d'etat et ascon dans un bloc plus grand
- Ajouter a ce bloc l'émission et la réception UART des données

On chiffre à chaque fois un ECG complet


Modules à écrire:
- FSM pour ASCON
- FSM pour piloter bloc ASCON et Initialisation


## Liens

https://ascon.isec.tugraz.at/specification.html

