# Auth Demo — Flask + Argon2

Implementación sencilla de **autenticación** con **hashing de contraseñas (Argon2)**.
Incluye **registro**, **login**, sesiones y **SQLite**.

## Requisitos
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar
```bash
export APP_SECRET="cambia-esto"  # Windows PowerShell: $env:APP_SECRET="cambia-esto"
python app.py
# Abre http://127.0.0.1:5000
```

## Guion para el video
1. Mostrar instalación de dependencias con `pip`.
2. Ejecutar `python app.py`.
3. Registrar un usuario y luego iniciar sesión (éxito).
4. Intentar login con contraseña incorrecta (falla).
5. (Opcional) Abrir `auth.db`/`auth.sqlite` con un visor y evidenciar que se almacenan **hashes** Argon2, no texto plano.

## Estructura
```
auth-flask-argon2/
  app.py
  auth.py
  db.py
  requirements.txt
  templates/
    base.html
    home.html
    login.html
    register.html
```

## Notas de seguridad
- No guardes contraseñas en texto plano ni uses cifrado reversible.
- Argon2 genera **salt** aleatoria por usuario y permite rehash (endurecimiento).
- En producción: usa HTTPS, rate limiting, bloqueo por intentos, validación de complejidad, y opcionalmente un **pepper** en el servidor.
