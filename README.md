# turbodose

Script python pour surveiller les rendez-vous disponnibles pour la vaccination Covid19 sur Doctolib.

**Important**: les notifications turbodose fonctionnent grâce à notify.run. Les notifications fontionnent sur Chrome (desktop et android) et firefox (desktop et android), mais a priori pas sur iOS.

**Important 2**: Lorsque vous recevrez une notification, **si vous vous êtes abbonés depuis chrome** vous pouvez cliquer sur la notification qui vous ammènera directement à la page doctolib du 1er rdv dispo !

## Instances déjà existantes 

Vous pouvez vous abonner aux notifications de certaines villes au lieu d'héberger votre propre instance :

| Ville  | Adresse                               |
|--------|---------------------------------------|
| Paris  | https://notify.run/c/q66HliivDiCIjfkP |
| Nantes | https://notify.run/c/EbfTl4vGdkENQgqF |
| Lyon   | https://notify.run/c/iNRV2oXZaDNBwv7V |

Il faut ensuite décendre sur la page et cliquer sur `subscribe on this device`

## Utiliser sa propre instance

### Installation

Il faut commencer par cloner le repo git :
```
git clone https://github.com/N0ciple/turbodose.git
```

ensuite installer les paquets python necessaires (`notify-run` et `selenium`):
```
cd turbodose
pip install -r requirements.txt
```
on peut ensuite lancer le script de la manière suivante :
```
python turbodose.py
```

### Ajouter une nouvelle ville :
Le service utilise notify-run. Pour ajouter une nouvelle ville il faut créer un nouveau channel en allant sur [notify.run](https://notify.run) puis cliquer sur `create a channel`.  Vous pouvez ensuite cliquer sur `subscribe on this device` pour vous abonner aux futures notifications. Copiez l'id du channel ( `Your new channel is called <id du channel>.`) et ajoutez le dans le fichier `city_config.txt` de la manière suivante :
```json
{  
    "paris": "clx4mqxyeNWob3yO",
    "lyon": "eFgdpvxFSnF1qCkb",
    "nantes": "T3wYueIHIKYvqLUg",
    "nouvelle-ville": "<id du channel>"
}
```

⚠️ Ne pas oublier la virgule après chaque id, **sauf** pour la dernière ville !

### Retrouver l'url via l'id

Si vous avez perdu l'url pour obtenir les notification, celle ci est : `https://notify.run/c/<id du channel>`
