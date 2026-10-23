from collections import defaultdict


class CruzadorAsistencia:

    # ==========================================
    # INDEXAR MARCACIONES
    # ==========================================

    def indexar_marcaciones(self, marcaciones):

        indice = defaultdict(list)

        for marcacion in marcaciones:

            empleado_id = marcacion.get(
                "empleado_id"
            )

            fecha_hora = marcacion.get(
                "fecha_hora"
            )

            if empleado_id is None:
                continue

            if fecha_hora is None:
                continue

            fecha = fecha_hora.date()

            clave = (
                empleado_id,
                fecha
            )

            indice[clave].append(
                marcacion
            )

        return indice

    # ==========================================
    # CRUZAR DÍAS CON MARCACIONES
    # ==========================================

    def cruzar(
        self,
        dias_evaluables,
        marcaciones
    ):

        indice = self.indexar_marcaciones(
            marcaciones
        )

        resultado = []

        for dia in dias_evaluables:

            empleado_id = dia[
                "empleado_id"
            ]

            fecha = dia[
                "fecha"
            ]

            clave = (
                empleado_id,
                fecha
            )

            marcas = indice.get(
                clave,
                []
            )

            registro = {
                "empleado_id": empleado_id,
                "id_usuario": dia["id_usuario"],
                "nombre": dia["nombre"],
                "apellido": dia["apellido"],
                "fecha": fecha,
                "marcaciones": marcas
            }

            if marcas:

                registro["tiene_marcacion"] = True

            else:

                registro["tiene_marcacion"] = False

            resultado.append(
                registro
            )

        return resultado