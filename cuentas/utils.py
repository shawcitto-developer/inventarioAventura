def rol_de(user):
    """Devuelve 'admin', 'guia', 'turista' o None si no hay sesión."""
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return 'admin'
    perfil = getattr(user, 'perfil', None)
    return perfil.rol if perfil else 'turista'
