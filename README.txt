# Prototipo de sistema de remuneraciones

Este proyecto simula el escenario real:
- 200 ingenieros.
- 30 días de registros del biométrico.
- Más de 6,000 registros de asistencia.
- Pandas para cargar, unir, agrupar y resumir datos.
- NumPy para operaciones numéricas.
- Streamlit para la interfaz.

## Ejecutar

1. Abrir esta carpeta en VS Code.
2. Abrir la terminal.
3. Instalar:

pip install streamlit pandas numpy

4. Ejecutar:

streamlit run app.py

## Importante

Las reglas salariales son INVENTADAS para practicar:
- valor hora = sueldo / 240
- hora extra = valor hora * 1.25
- tardanza = descuento por minuto
- falta = sueldo / 30

Cuando la empresa entregue sus reglas reales, estas fórmulas deben reemplazarse.
