# Aventuras del Sur - EV3 Programación Backend

Sistema de reservas para un ecoparque con tres roles: Administrador, Guía y Turista. Hecho con Django, MySQL y Bootstrap 5.

## Cómo ejecutarlo

1. Tener el servidor MySQL encendido.
2. Crear la base de datos: CREATE DATABASE inventarioaventura_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
3. Importar los datos: en Workbench, Server > Data Import > Import from Self-Contained File, elegir respaldo_inventarioaventura.sql y, en Default Target Schema, inventarioaventura_db.
4. En inventarioAventura/settings.py, dentro de DATABASES, revisar USER y PASSWORD. El proyecto usa el usuario admin con clave 2026: se puede crear ese usuario en MySQL con permisos sobre la base, o cambiar los datos por los de tu usuario.
5. python -m venv env
6. .\env\Scripts\Activate.ps1
7. python -m pip install -r requirements.txt
8. python manage.py runserver
9. Abrir http://127.0.0.1:8000/

Nota: los estilos y scripts (Bootstrap, AdminLTE, DataTables) se cargan desde internet, por lo que se necesita conexión.

## Usuarios de prueba

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | admin_parque | Aventura2026! |
| Guía | guia_pedro | Aventura2026! |
| Guía | guia_ana | Aventura2026! |
| Turista | turista_luis | Aventura2026! |
| Turista | turista_sofia | Aventura2026! |

## Qué puede hacer cada rol

- Administrador: gestiona categorías, experiencias, usuarios y reservas (puede confirmar pagos y eliminar).
- Guía: crea, ve y edita solo las experiencias que él creó. No puede eliminar.
- Turista: ve el catálogo de experiencias activas, se inscribe y gestiona sus propias reservas.