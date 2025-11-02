# pyproto — Statut et plan de développement

Librairie Python pour créer un client/serveur basé sur des paquets binaires (VarInt, strings, longs). Répo: https://github.com/Zalgo-Dev/pyproto

Objectif de ce document: avoir une vue claire de l’état actuel et de la suite à implémenter, dans l’ordre chronologique.

## Fichiers et symboles clés

- Racine
  - [exemples/client.py](exemples/client.py) — exemple/entrée cliente (à compléter).
  - [__init__.py](__init__.py)
- Réseau
  - [network/utils.py](network/utils.py)
    - [`network.utils.write_varint`](network/utils.py)
    - [`network.utils.read_varint`](network/utils.py)
    - [`network.utils.write_string`](network/utils.py)
    - [`network.utils.read_string`](network/utils.py)
    - [`network.utils.write_unsigned_short`](network/utils.py)
    - [`network.utils.read_long`](network/utils.py)
    - [`network.utils.write_long`](network/utils.py)
- Protocole
  - [protocol/__init__.py](protocol/__init__.py)
    - [`protocol.State`](protocol/__init__.py)
    - [`protocol.Direction`](protocol/__init__.py)
    - [`protocol.PacketRegistry`](protocol/__init__.py)
    - [`protocol.PacketRegistry.register`](protocol/__init__.py)
    - [`protocol.PacketRegistry.get`](protocol/__init__.py)
    - [`protocol.PacketRegistry.all`](protocol/__init__.py)
  - [protocol/base.py](protocol/base.py)
    - [`protocol.base.BasePacket`](protocol/base.py)
    - [`protocol.base.BasePacket.STATE`](protocol/base.py)
    - [`protocol.base.BasePacket.DIRECTION`](protocol/base.py)
  - [protocol/handshake.py](protocol/handshake.py)
    - [`protocol.handshake.Handshake`](protocol/handshake.py)
    - [`protocol.handshake.Handshake.STATE`](protocol/handshake.py)
    - [`protocol.handshake.Handshake.DIRECTION`](protocol/handshake.py)
  - [protocol/status.py](protocol/status.py)
    - [`protocol.status.StatusRequest`](protocol/status.py)
    - [`protocol.status.StatusRequest.STATE`](protocol/status.py)
    - [`protocol.status.StatusRequest.DIRECTION`](protocol/status.py)
- Tests
  - [test/](test/) — dossier tests (vide).

## État actuel

- Utils VarInt/String/Long implémentés dans [network/utils.py](network/utils.py).
- Enums [`protocol.State`](protocol/__init__.py) et [`protocol.Direction`](protocol/__init__.py) pour les états et directions de paquets.
- Registre de paquets [`protocol.PacketRegistry`](protocol/__init__.py) avec support état/direction pour éviter les collisions d'ID.
- Paquets sortants (sérialisation):
  - [`protocol.handshake.Handshake`](protocol/handshake.py) — sérialisation complète (ID + champs + longueur).
  - [`protocol.status.StatusRequest`](protocol/status.py) — sérialisation minimale (ID + longueur).

## Chronologie des étapes à introduire

1) Stabiliser la base et le registre
- [x] Retirer `@PacketRegistry.register` de [`protocol.base.BasePacket`](protocol/base.py) ou faire ignorer `PACKET_ID=None` dans [`protocol.PacketRegistry.register`](protocol/__init__.py). (Le décorateur n'est pas sur la base, et PACKET_ID=None est géré.)
- [] Documenter la convention d’ID de paquets par “état” pour éviter les collisions (Handshake 0x00 et Status 0x00 coexistent car états distincts). (Implémenté via clés (State, Direction, PACKET_ID).)

2) Définir l’API de désérialisation
- [ ] Ajouter une méthode `@classmethod deserialize(cls, data: bytes, offset=...) -> tuple[self, int]` sur [`protocol.base.BasePacket`](protocol/base.py).
- [ ] Implémenter `deserialize` pour [`protocol.handshake.Handshake`](protocol/handshake.py) et [`protocol.status.StatusRequest`](protocol/status.py).
- [ ] Créer un parseur générique: lire longueur via [`network.utils.read_varint`](network/utils.py), lire packet_id (VarInt), retrouver la classe via [`protocol.PacketRegistry.get`](protocol/__init__.py), puis déléguer à `deserialize`.

3) Encapsulation trame (framing) et helpers
- [ ] Centraliser l’encodage longueur+ID dans un helper commun (éviter duplication dans les `serialize`).
- [ ] Ajouter un helper de parsing de trame unique (retourne paquet et offset restant).

4) I/O réseau minimal (MVP)
- [ ] Client TCP synchrone (socket) capable d’envoyer un paquet (Handshake) puis [`protocol.status.StatusRequest`](protocol/status.py).
- [ ] Lecture bloquante d’une réponse “StatusResponse” (à créer).
- [ ] Exemple filaire dans [client.py](client.py).

5) Implémenter les paquets essentiels pour “status”
- [ ] `StatusResponse` (JSON ou binaire selon cible).
- [ ] `Ping` / `Pong` (aller-retour temps de latence).
- [ ] Enregistrer ces paquets via [`protocol.PacketRegistry.register`](protocol/__init__.py).

6) Validation et erreurs
- [ ] Vérifier les bornes en lecture dans [`network.utils.read_varint`](network/utils.py) et [`network.utils.read_string`](network/utils.py) (offset/longueur).
- [ ] Définir exceptions dédiées (ex: `PacketDecodeError`, `UnknownPacketError`).
- [ ] Logs/trace minimal en cas de paquet inconnu (`get` retourne `None`).

7) Tests unitaires
- [ ] Tests sur utils: [`network.utils.write_varint`](network/utils.py)/[`network.utils.read_varint`](network/utils.py), [`network.utils.write_string`](network/utils.py)/[`network.utils.read_string`](network/utils.py), [`network.utils.write_long`](network/utils.py)/[`network.utils.read_long`](network/utils.py).
- [ ] Tests de sérialisation/désérialisation des paquets existants.
- [ ] Tests du parseur générique + registre.
- [ ] Placer dans [test/](test/).

8) Exemple(s) complet(s)
- [ ] Exemple client minimal dans [client.py](client.py) (Handshake -> StatusRequest -> lecture StatusResponse).
- [ ] Exemple serveur “echo” basique (répertoire `examples/` futur).

9) Documentation, packaging et CI
- [ ] Docstrings pour toutes classes et méthodes publiques.
- [ ] README utilisateur (installation, usage) distinct de ce fichier de statut.
- [ ] pyproject.toml / setup.cfg, classifiers, versioning sémantique.
- [ ] CI (lint + tests).

## Checklist rapide (où j’en suis)

- [x] Utils VarInt/String/Long — voir [network/utils.py](network/utils.py).
- [x] Enums State et Direction — voir [protocol/__init__.py](protocol/__init__.py).
- [x] Registre de paquets avec support état/direction — voir [`protocol.PacketRegistry`](protocol/__init__.py).
- [x] Paquets sortants: [`protocol.handshake.Handshake`](protocol/handshake.py), [`protocol.status.StatusRequest`](protocol/status.py).
- [ ] Désérialisation et parseur de paquets.
- [ ] I/O réseau (client/serveur) MVP.
- [ ] Paquets StatusResponse/Ping/Pong.
- [ ] Validation/erreurs robustes.
- [ ] Tests unitaires.
- [ ] Exemples complets.
- [ ] Packaging + CI.

## Prochaines actions immédiates

- Ajouter `deserialize` + parseur générique basé sur [`network.utils.read_varint`](network/utils.py) et [`protocol.PacketRegistry.get`](protocol/__init__.py).
- Écrire tests unitaires de base dans [test/](test/).
- Mettre un exemple minimal dans [client.py](client.py).