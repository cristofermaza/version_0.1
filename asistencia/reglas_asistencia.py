from datetime import date


class ReglasAsistencia:

    def empleado_pertenencia_en_fecha(
        self,
        fecha,
        fecha_ingreso=None,
        fecha_cese=None
    ):
        if not isinstance(fecha, date):
            raise ValueError(
                "La fecha debe ser de tipo date."
            )

        if fecha_ingreso is not None:
            if fecha < fecha_ingreso:
                return False

        if fecha_cese is not None:
            if fecha > fecha_cese:
                return False

        return True

    def es_fin_de_semana(self, fecha):
        return fecha.weekday() >= 5

    def es_dia_laborable(self, fecha):
        if self.es_fin_de_semana(fecha):
            return False

        return True

    def debe_evaluarse_asistencia(
        self,
        fecha,
        fecha_ingreso=None,
        fecha_cese=None
    ):
        if not self.empleado_pertenencia_en_fecha(
            fecha,
            fecha_ingreso,
            fecha_cese
        ):
            return False

        if not self.es_dia_laborable(fecha):
            return False

        return True