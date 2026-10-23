from asistencia.procesador import ProcesadorAsistencia
from asistencia.reglas_asistencia import ReglasAsistencia
from asistencia.evaluador_asistencia import EvaluadorAsistencia
from asistencia.cruzador_asistencia import CruzadorAsistencia
from asistencia.clasificador_asistencia import ClasificadorAsistencia


class ServicioAsistencia:

    def __init__(
        self,
        gestor_fuentes,
        configuracion
    ):
        self.gestor_fuentes = gestor_fuentes
        self.configuracion = configuracion

        # -------------------------------------------------
        # COMPONENTES DEL SERVICIO
        # -------------------------------------------------

        self.reglas = ReglasAsistencia()

        self.evaluador = EvaluadorAsistencia()

        self.cruzador = CruzadorAsistencia()

        # -------------------------------------------------
        # CONFIGURACIÓN
        # -------------------------------------------------

        self.cargar_configuracion(
            configuracion
        )

        # -------------------------------------------------
        # CLASIFICADOR
        # -------------------------------------------------

        self.clasificador = ClasificadorAsistencia(
            procesador=self.procesador
        )

    # =====================================================
    # CONFIGURACIÓN
    # =====================================================

    def cargar_configuracion(
        self,
        configuracion
    ):

        self.configuracion = configuracion

        asistencia = configuracion.get(
            "asistencia",
            {}
        )

        horario = asistencia.get(
            "horario",
            {}
        )

        tolerancia = asistencia.get(
            "tolerancia",
            {}
        )

        reglas = asistencia.get(
            "reglas",
            {}
        )

        # -------------------------------------------------
        # HORARIOS
        # -------------------------------------------------

        hora_entrada = horario.get(
            "hora_entrada",
            "08:00"
        )

        hora_salida = horario.get(
            "hora_salida",
            "17:00"
        )

        # -------------------------------------------------
        # TOLERANCIA
        # -------------------------------------------------

        minutos_tolerancia = tolerancia.get(
            "minutos_entrada",
            0
        )

        # -------------------------------------------------
        # REGLAS
        # -------------------------------------------------

        primera_marcacion = reglas.get(
            "primera_marcacion_es_entrada",
            True
        )

        ultima_marcacion = reglas.get(
            "ultima_marcacion_es_salida",
            True
        )

        generar_salida = reglas.get(
            "generar_salida_si_solo_hay_una_marcacion",
            False
        )

        # -------------------------------------------------
        # CREAR PROCESADOR
        # -------------------------------------------------

        self.procesador = ProcesadorAsistencia(
            hora_entrada=hora_entrada,
            hora_salida=hora_salida,
            tolerancia_entrada=minutos_tolerancia,
            primera_marcacion_es_entrada=primera_marcacion,
            ultima_marcacion_es_salida=ultima_marcacion,
            generar_salida_si_solo_hay_una_marcacion=generar_salida
        )

        # -------------------------------------------------
        # ACTUALIZAR CLASIFICADOR
        # -------------------------------------------------

        if hasattr(
            self,
            "clasificador"
        ):
            self.clasificador.procesador = (
                self.procesador
            )

    # =====================================================
    # PROCESAMIENTO GENERAL
    # =====================================================

    def procesar_asistencia(
        self,
        fecha_inicio,
        fecha_fin
    ):

        if not self.gestor_fuentes.esta_disponible():

            raise Exception(
                "La fuente de datos no está disponible."
            )

        marcaciones = (
            self.gestor_fuentes.obtener_marcaciones(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
        )

        resultados = self.procesador.procesar(
            marcaciones
        )

        cantidad = 0

        if resultados:

            cantidad = (
                self.gestor_fuentes
                .guardar_asistencia_diaria(
                    resultados
                )
            )

        return cantidad

    # =====================================================
    # DÍAS EVALUABLES
    # =====================================================

    def obtener_dias_evaluables(
        self,
        fecha_inicio,
        fecha_fin
    ):

        if not self.gestor_fuentes.esta_disponible():

            raise Exception(
                "La fuente de datos no está disponible."
            )

        empleados = (
            self.gestor_fuentes.obtener_empleados()
        )

        calendario = (
            self.gestor_fuentes
            .obtener_calendario_laboral(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
        )

        return self.evaluador.generar_para_empleados(
            empleados=empleados,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            registros_calendario=calendario
        )

    # =====================================================
    # EVALUACIÓN DEL PERÍODO
    # =====================================================

    def obtener_evaluacion_periodo(
        self,
        fecha_inicio,
        fecha_fin
    ):

        if not self.gestor_fuentes.esta_disponible():

            raise Exception(
                "La fuente de datos no está disponible."
            )

        # -------------------------------------------------
        # 1. DÍAS QUE DEBEN SER EVALUADOS
        # -------------------------------------------------

        dias_evaluables = (
            self.obtener_dias_evaluables(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
        )

        # -------------------------------------------------
        # 2. OBTENER MARCACIONES
        # -------------------------------------------------

        marcaciones = (
            self.gestor_fuentes.obtener_marcaciones(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
        )

        # -------------------------------------------------
        # 3. CRUZAR DÍAS CON MARCACIONES
        # -------------------------------------------------

        registros_cruzados = (
            self.cruzador.cruzar(
                dias_evaluables=dias_evaluables,
                marcaciones=marcaciones
            )
        )

        # -------------------------------------------------
        # 4. CLASIFICAR
        # -------------------------------------------------

        return self.clasificador.clasificar_todos(
            registros_cruzados
        )