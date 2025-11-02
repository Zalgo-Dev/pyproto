# pyproto 🚀

Librairie Python pour créer des clients/serveurs binaires basés sur des paquets (VarInt, String, Long).

## 🔧 Installation

```bash
git clone https://github.com/Zalgo-Dev/pyproto.git
cd pyproto
pip install -e .
```

## 🧪 Exemple rapide

```python
from pyproto.protocol.handshake import Handshake

packet = Handshake(
    protocol_version=47,
    host="localhost",
    port=25565,
    next_state=1
)
data = packet.serialize()
print(data)
```

## 🎯 Objectifs

- Gérer la sérialisation et la désérialisation de paquets binaires.
- Fournir un registre de paquets (via `PacketRegistry`) pour mapping ID ↔ classe.
- Support minimal client/serveur avec framing, envoi/lecture de paquets.
- Inclure tests unitaires, documentation et CI pour garantir fiabilité et maintenabilité.

## 📂 Structure du projet

```
pyproto/
├─ client.py                # Exemple client
├─ network/                 # Outils bas niveau (VarInt, String, Long, etc.)
├─ protocol/                # Définition des paquets et registre
├─ test/                    # Tests unitaires
└─ README.md                # (Vous êtes ici)
```

## ✅ Statut de développement

Ce projet est en **phase de développement actif**. Certaines fonctionnalités sont déjà implémentées :
- Utils VarInt/String/Long ✅
- PacketRegistry et classes de base ✅
- Paquets de sortie (Handshake, StatusRequest) ✅

Fonctionnalités à venir :
- Désérialisation générique des paquets  
- Framing et API réseau synchrones  
- Serveur minimal + paquets StatusResponse, Ping/Pong  
- Tests unitaires couvrant l’ensemble  
- Packaging, versioning sémantique et CI  

## 🧭 Contribution

Les contributions sont les bienvenues !  
Merci de :
- Forker ce dépôt  
- Créer une branche dédiée pour votre feature/fix  
- Documenter vos modifications (docstrings, README)  
- Ajouter des tests pour toute nouvelle fonctionnalité  

## 📄 Licence

Ce projet est soumis à la licence MIT. Voir le fichier `LICENSE` pour plus de détails.

