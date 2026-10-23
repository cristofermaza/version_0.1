from datetime import timedelta

from asistencia.reglas_asistencia import ReglasAsistencia


class EvaluadorAsistencia:

    def __init__(self):
        self.reglas = ReglasAsistencia()

    # ==========================================
    # PREPARAR CALENDARIO
    # ==========================================

    def preparar_calendario(
        self,
        registros_calendario
    ):
        """
        Convierte los registros del calendario
        en un diccionario indexado por fecha.
        """

        calendario = {}

        for registro in registros_calendario:

            fecha = registro.get("fecha")

            if fecha is None:
                continue

            calendario[fecha] = registro

        return calendario

    # ==========================================
    # COMPROBAR SI EL DÍA ES LABORABLE
    # ==========================================

    def es_dia_laborable(
        self,
        fecha,
        calendario
    ):
        """
        Si existe una configuración específica
        en el calendario, se utiliza.

        Si no existe, se aplica la regla
        predeterminada de lunes a viernes.
        """

        registro = calendario.get(fecha)

        if registro is not None:

            return bool(
                registro.get(
                    "es_laborable",
                    False
                )
            )

        return self.reglas.es_dia_laborable(
            fecha
        )

    # ==========================================
    # GENERAR DÍAS EVALUABLES
    # ==========================================

    def generar_dias_evaluables(
        self,
        empleado,
        fecha_inicio,
        fecha_fin,
        calendario=None
    ):

        if calendario is None:
            calendario = {}

        dias = []

        fecha_actual = fecha_inicio

        while fecha_actual < fecha_fin:

            fecha_ingreso = empleado.get(
                "fecha_ingreso"
            )

            fecha_cese = empleado.get(
                "fecha_cese"
            )

            pertenece = (
               self.reglas.empleado_pertenencia_en_fecha(
                    fecha=fecha_actual,
                    fecha_ingreso=fecha_ingreso,
                    fecha_cese=fecha_cese
                )
            )

            if pertenece:

                if self.es_dia_laborable(
                    fecha_actual,
                    calendario
                ):

                    dias.append({
                        "empleado_id": empleado["id"],
                        "id_usuario": empleado["id_usuario"],
                        "nombre": empleado["nombre"],
                        "apellido": empleado["apellido"],
                        "fecha": fecha_actual
                    })

            fecha_actual += timedelta(
                days=1
            )

        return dias

    # ==========================================
    # GENERAR PARA TODOS LOS EMPLEADOS
    # ==========================================

    def generar_para_empleados(
        self,
        empleados,
        fecha_inicio,
        fecha_fin,
        registros_calendario=None
    ):

        if registros_calendario is None:
            registros_calendario = []

        calendario = self.preparar_calendario(
            registros_calendario
        )

        resultado = []

        for empleado in empleados:

            dias = self.generar_dias_evaluables(
                empleado=empleado,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                calendario=calendario
            )

            resultado.extend(
                dias
            )

        return resultado