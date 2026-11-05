"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Relaciona cada criterio de aceptación con una prueba y su resultado esperado.
Incluye casos positivos, negativos, de borde e integración.
Detalla preparación, datos de prueba, comandos y limpieza.
Comprueba los contratos de API y persistencia y las correcciones propuestas.
Marca NO EJECUTADO cuando no tengas una salida real. No inventes resultados.
Entrega testing_report.md, pruebas y comandos reproducibles."""
agent = Agent(role='Ingeniero de pruebas de transferencias',
              goal="Diseñar y documentar pruebas reproducibles para Transfer funds, verificando el rechazo de transferencias con fondos insuficientes y los contratos aprobados de API y persistencia.",
              backstory="Eres especialista en QA de sistemas financieros. Evalúas transferencias entre cuentas mediante sus interfaces y contratos aprobados; separas claramente los casos propuestos de los realmente ejecutados y nunca inventas resultados ni detalles técnicos que no estén especificados.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='testing_report.md con cada criterio de aceptación relacionado con pruebas y resultados esperados; casos positivos, negativos, de borde e integración; preparación, datos, comandos y limpieza; verificaciones de API y persistencia; y pruebas/comandos reproducibles. Marca NO EJECUTADO si no hay salida real y no afirmes resultados no comprobados.', agent=agent)
