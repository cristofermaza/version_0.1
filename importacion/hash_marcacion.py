import hashlib


def generar_hash_marcacion(
    id_usuario,
    fecha_hora,
    numero_tarjeta,
    dispositivo,
    evento
):

    texto = (
        f"{id_usuario}|"
        f"{fecha_hora}|"
        f"{numero_tarjeta}|"
        f"{dispositivo}|"
        f"{evento}"
    )

    hash_marcacion = hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()

    return hash_marcacion