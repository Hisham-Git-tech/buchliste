# Buchliste

Webanwendung zur Verwaltung persönlicher Bücher.

## Funktionen

- Benutzerregistrierung
- Login / Logout
- Bücher hinzufügen
- Bücher bearbeiten
- Bücher löschen
- Lesestatus verwalten
- Bewertungen vergeben
- Notizen speichern

## API

Token erstellen:

```
curl -u USERNAME:PASSWORD -X POST /api/tokens
```

Bücher abrufen:

```
curl -H "Authorization: Bearer TOKEN" /api/books
```

## Technologien

- Python
- Flask
- SQLAlchemy
- MariaDB
- Gunicorn
- Nginx
