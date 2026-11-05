"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Relaciona cada criterio de aceptación con un identificador de prueba y su resultado esperado, en una tabla criterio -> test_id -> resultado.
Incluye casos positivos, negativos, de borde e integración.
Detalla preparación, datos de prueba, comandos con su entorno de ejecución y limpieza o rollback, incluida la reversión de migraciones de Datos cuando la prueba las haya ejercitado.
Comprueba los contratos de API y persistencia, incluidas restricciones de integridad (claves únicas, foráneas) y las correcciones propuestas.
Marca cada caso como EJECUTADO o NO EJECUTADO según tengas o no una salida real. No inventes resultados.
Entrega testing_report.md, pruebas y comandos reproducibles por cualquier integrante sin contexto adicional."""
agent = Agent(role='Ingeniero de pruebas',
              goal="Diseñar y documentar pruebas reproducibles para el Issue del equipo, verificando sus criterios de aceptación y los contratos aprobados de API y persistencia.",
              backstory="Eres especialista en QA. Evalúas el feature asignado mediante sus interfaces y contratos aprobados; separas claramente los casos propuestos de los realmente ejecutados y nunca inventas resultados ni detalles técnicos que no estén especificados.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='testing_report.md con tabla criterio -> test_id -> resultado, pruebas y comandos reproducibles. Marca cada caso EJECUTADO o NO EJECUTADO y no afirmes resultados no comprobados.', agent=agent)
