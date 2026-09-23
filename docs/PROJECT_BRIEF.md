# Prompt de arranque — proyecto `feynlag-anomalies`

> Pega todo este texto como primer mensaje en Claude Code, abierto en una carpeta vacía que será el nuevo repositorio (con `feynlag` y `feynlag-models` clonados como carpetas hermanas o instalados en el entorno). Guarda también una copia como `docs/PROJECT_BRIEF.md` dentro del repo.

---

## 0. Rol y modo de trabajo

Eres mi colaborador de investigación y desarrollo para un nuevo repositorio, `feynlag-anomalies` (nombre provisional). Soy físico teórico (fenomenología BSM, sector escalar extendido, neutrinos, LFV) y autor de `feynlag` (pipeline Python/SymPy: invariancia gauge, EWSB, matrices de masa, vértices, export UFO/LaTeX, round-trip con MadGraph) y de `feynlag-models` (biblioteca verificada de extensiones mínimas del SM con escala de madurez L0–L4).

**Antes de escribir código:** explora los repos, lee la documentación indicada en §2 y preséntame un plan (usa plan mode). No empieces a construir hasta que yo lo apruebe. Si algo de este prompt contradice lo que encuentres en los repos, detente y pregúntame.

## 1. Objetivo del proyecto

Construir una biblioteca, verificable y pedagógica, que para cada anomalía o medición que sugiere física más allá del SM:

1. **Explique la anomalía**: qué se mide, quién la mide, cuál es su significancia y cuál es su estatus actual.
2. **Explique, calculando, por qué el SM no la describe**, e identifique *qué protección del SM* la bloquea.
3. **Construya la escalera de extensiones mínimas** que podría describirla: estimación → EFT → completación UV → modelo en `feynlag-models` → confrontación con restricciones.

**Audiencia:** colegas y estudiantes de posgrado. Principio pedagógico: *un físico teórico aprende calculando, y el cálculo genera el criterio para las decisiones posteriores*. Cada paso de la escalera debe ser un cálculo que el lector ejecuta y que motiva el siguiente paso.

**Usos posteriores:** fuente para artículos (revisiones, estudios fenomenológicos) y para divulgación. Diseña pensando en que el contenido se pueda reutilizar, no solo leer.

**Alcance temático:** colisionador (Higgs y resonancias), sabor, precisión electrodébil, neutrinos (incluidas las anomalías de corta distancia: LSND/MiniBooNE/MicroBooNE, galio, reactores), materia oscura (directa, reliquia), cosmología (H₀, ΔN_eff, etc.) y X17 (ATOMKI/PADME/MEG II).

## 2. Relación con `feynlag-models`: regla de no duplicación

Lee primero, en `feynlag-models`: `README.md`, `CLAUDE.md`, `CONVENTIONS.md`, `GENEALOGY.md`, `FEYNLAG_GAPS.md` y `REPORT.md`. Revisa también la documentación y la API pública de `feynlag`.

| Vive en `feynlag-anomalies` | Vive en `feynlag-models` |
|---|---|
| Fichas de anomalías: datos, fuentes, estatus | Declaración del modelo y `Model.validate()` |
| Tests de "por qué el SM no puede" | Espectro, vértices, UFO, round-trip |
| Candidatos mínimos (referenciados por `model_id`) | Tests contra literatura (L2) |
| Puntos de benchmark, escaneos, ajustes, χ² | `GENEALOGY.md` |
| Notebooks pedagógicos (escaleras) | — |

Reglas:
- **Este repo nunca declara un Lagrangiano.** Importa modelos de `feynlag-models` por `model_id`.
- Si una anomalía necesita un modelo inexistente, o una variante (por ejemplo, más generaciones), escribe una **petición de modelo** en `model_requests/<id>.md`: campos, números cuánticos, simetrías, motivación, qué cálculo la exige y nivel mínimo requerido. **No modifiques `feynlag-models` sin mi aprobación explícita.**
- Solo se ajustan o escanean modelos con madurez **≥ L2**.
- Las carencias de `feynlag` que descubras (por ejemplo, loops o matching a coeficientes de Wilson) se documentan como propuesta para `FEYNLAG_GAPS.md`, no se parchean aquí.

## 3. Conceptos que estructuran todo el repo

### 3.1 Tres tipos de "el SM no puede explicarlo" (campo `sm_failure_type`)
- `structural`: faltan campos o términos (masa de ν, candidato a DM, bariogénesis). Se **demuestra** con feynlag: enumeración de invariantes, conteo de estados.
- `resonance`: estado nuevo a una masa donde el SM no tiene nada (95 GeV, 146 GeV eμ). El trabajo está en la significancia (local frente a global, look-elsewhere) y la coherencia entre canales.
- `quantitative`: el SM contribuye, pero la predicción difiere de la medición (R(D*), b→sℓℓ, CAA, M_W, g−2). La predicción del SM suele requerir QCD o loops que feynlag no calcula, y debe **citarse y etiquetarse**.

### 3.2 Taxonomía de protecciones del SM (`docs/protections.md` y campo `sm_protection`)
Simetrías accidentales (B, L_e, L_μ, L_τ); contenido de campos; GIM; supresión quiral/helicidad; simetría custodial (ρ = 1); supresión por loop; jerarquía CKM; otras que encuentres. Cada anomalía se mapea a la(s) protección(es) que hay que romper, y eso orienta la familia de extensiones.

### 3.3 Escala de madurez de anomalías (paralela a L0–L4)
- **A0**: ficha con datos y fuentes primarias verificadas.
- **A1**: argumento del SM (test estructural ejecutable o predicción citada y etiquetada) y protección identificada.
- **A2**: operador EFT de menor dimensión y candidato(s) mínimo(s) con `model_id` (o petición de modelo).
- **A3**: escaneo o ajuste de etapa 1 (χ² gaussiano con restricciones).
- **A4**: ajuste con verosimilitudes reales (etapas 2–3).

### 3.4 Vocabulario cerrado de estatus
`established` · `live` · `weakened` · `resolved` (caso cerrado, se conserva como material pedagógico) · `hint` (preliminar, pendiente de confirmación). Siempre con fecha y justificación. Campo obligatorio `tensions_with_other_data` (por ejemplo, ATOMKI frente a MEG II/PADME, LSND/MiniBooNE frente a MicroBooNE, CDF frente a ATLAS/CMS en M_W).

## 4. La ficha (esquema de datos)

Una carpeta por anomalía: `anomalies/<anomaly_id>/` con:
- `anomaly.yaml`, validado por un esquema (pydantic o jsonschema) con al menos: `id`, `title`, `sector`, `observables[]` (nombre, valor medido, incertidumbres estadística y sistemática, unidades), `sm_prediction` (valor, incertidumbre, `provenance: computed|cited`, referencia), `significance` (local, global, método), `experiments[]`, `sources[]` (arXiv / DOI / HEPData / PDG, **fecha de consulta**), `status`, `status_date`, `status_rationale`, `tensions_with_other_data`, `sm_failure_type`, `sm_protection[]`, `eft_operators[]`, `candidate_models[]` (model_id o model_request), `maturity` (A0–A4), `falsifiers[]` (qué medición futura descartaría cada candidato), `changelog[]`.
- `ladder.ipynb`: la escalera pedagógica (§5).
- `solutions/`: soluciones de los checkpoints (separadas de los ejercicios).
- `decisions.md`: registro de decisiones, una línea por peldaño ("elegí X porque el cálculo Y dio Z").
- `tests/`: tests de la ficha.

**Ningún número vive solo en la prosa**: todo valor numérico usado en notebooks o docs se lee de `anomaly.yaml`.

## 5. Escalera pedagógica (plantilla de `ladder.ipynb`)

Cada peldaño termina con un **checkpoint** `check_<peldaño>(respuesta)` que valida lo que calcula el lector, y ofrece **pistas escalonadas** (1 → 2 → 3).

0. **Estimación a mano**: análisis dimensional de la escala o el acoplamiento necesario.
1. **Intentarlo con el SM**: enumerar invariantes con feynlag o reproducir y citar la predicción. Nombrar la protección que actúa.
2. **EFT antes que modelo**: operador SMEFT/WET de menor dimensión y estimación de Λ.
3. **Del operador a los campos**: completaciones UV a nivel árbol (referencia: de Blas, Criado, Pérez-Victoria, Santiago, arXiv:1711.10391). Elegir la mínima con un criterio explícito (menos campos → representaciones más pequeñas → menos parámetros → sin simetrías ad hoc) e importarla de `feynlag-models`.
4. **Predecir antes de correr**: el lector anota lo que espera (número de escalares físicos, Goldstones, vértices nuevos, mezclas) y luego compara con feynlag.
5. **Romperlo a propósito**: probar una elección no mínima o incorrecta y mostrar, calculando, por qué falla.
6. **Confrontar con restricciones**: χ² de etapa 1. Si hay tensión, eso motiva el siguiente peldaño de la genealogía.

Orden curricular previsto, donde cada anomalía añade una habilidad nueva: neutrinos → 95 GeV → 146 GeV eμ → g−2 (caso cerrado) → sabor → cosmología.

## 6. Ajustes a datos (de lo simple a lo completo)

- **Etapa 1 (implementar ahora):** χ² gaussiano con valores resumidos y cortes duros (perturbatividad, unitariedad, estabilidad del vacío). Solo con `lambdify` + NumPy/SciPy. Módulo común `fit/stage1.py`, reutilizable por todas las fichas.
- **Etapa 2 (solo diseñar interfaces, no implementar):** HiggsTools (colisionador), flavio/smelli (sabor, vía matching a WCxf, lo que sería una carencia nueva de feynlag), micrOMEGAs (reliquia y detección directa vía UFO/CalcHEP).
- **Etapa 3 (futuro):** HEPData, pyhf y CLASS para cosmología.
- No instales herramientas pesadas (micrOMEGAs, CLASS, HiggsTools) sin preguntarme.

## 7. Reglas de verificabilidad (no negociables)

1. **No uses valores experimentales de memoria.** Cada número se obtiene de la fuente primaria (arXiv, HEPData, PDG, nota oficial de la colaboración) y se registra con su referencia y fecha de consulta. Si no puedes verificarlo, marca `TODO_VERIFY` y no lo uses en cálculos.
2. **Estatus con fecha.** Tu conocimiento puede estar desactualizado. Verifica en la literatura el estatus actual de cada anomalía antes de escribirlo. Ejemplos que requieren verificación explícita: g−2 del muón (resultado final de Fermilab 2025 frente al White Paper 2025 basado en lattice), M_W (CDF frente a ATLAS/CMS), exceso a 95 GeV (CMS/ATLAS γγ, ττ, LEP bb̄), exceso a 146 GeV en eμ (CMS), evento anómalo de LZ (septiembre de 2026; toma los detalles del preprint, no de la prensa), X17 (PADME, MEG II), MicroBooNE.
3. **Etiqueta `computed` frente a `cited`** en cada predicción y en cada afirmación de los notebooks.
4. **Tests automáticos (pytest):** validación de esquema de todas las fichas; tests estructurales del SM (por ejemplo, "no existe término de masa de ν de dimensión ≤ 4 con el contenido del SM"); checkpoints contra soluciones; ejecución de notebooks en CI (nbmake o nbval).
5. **Test de regresión contra literatura** antes de cualquier resultado propio: reproducir un benchmark publicado del modelo usado.
6. **"Explica la anomalía"** solo se afirma con una métrica calculada por código (Δχ² o pull) y la lista de restricciones satisfechas.
7. **Reproducibilidad:** entorno fijado (`pyproject.toml`), CI, versiones congeladas pensadas para DOI de Zenodo, `CHANGELOG`.
8. Sigue las convenciones de `feynlag-models/CONVENTIONS.md` (métrica, potencial, signos). Si hay ambigüedad, pregunta.

## 8. Tareas de esta primera sesión

1. **Exploración y plan** (esperar mi aprobación): resumen de la API de feynlag relevante, estado de los modelos en `feynlag-models` y plan de estructura del repo.
2. **Esqueleto del repo:** `pyproject.toml`, estructura de carpetas, `README.md`, `CLAUDE.md` (reglas operativas de este repo, derivadas de este prompt), `docs/PROJECT_BRIEF.md` (copia de este prompt), `docs/protections.md`, `docs/maturity.md`, CI básico.
3. **Esquema de la ficha + validador + tests de esquema.**
4. **Módulo `checkpoints`** (helpers para ejercicios con pistas escalonadas) y **módulo `fit/stage1.py`**.
5. **Piloto completo: `neutrino_mass`, hasta A2** (y A3 si es sencillo):
   - Peldaño 0: m_ν ~ y²v²/M.
   - Peldaño 1: test con feynlag de ausencia de término de masa en dimensión ≤ 4; protección = sin ν_R + L accidental.
   - Peldaño 2: operador de Weinberg (dimensión 5).
   - Peldaño 3: completaciones a árbol (seesaw tipo I, II, III); la mínima es tipo I → `seesaw_type1`.
   - Peldaño 4: el lector predice cuántos ν ligeros masivos hay con 1 N y lo verifica con el rango de la matriz de masa.
   - Peldaño 5: dos Δm² medidas exigen al menos 2 N. Redactar `model_requests/seesaw_type1_nN.md` (o la variante que corresponda según `feynlag-models`).
   - Peldaño 6: si es viable, χ² de etapa 1 con datos de oscilación (valores de un ajuste global verificado, p. ej. NuFIT, con versión y fecha).
6. **Stubs en A0** para `higgs_95gev` y `emu_146gev`, con fuentes primarias verificadas; y un `anomalies/INDEX.md` con el catálogo candidato completo (todos los sectores de §1), indicando sector, tipo, estatus preliminar y fuentes a verificar.

## 9. Qué no hacer

- No declarar modelos ni Lagrangianos en este repo.
- No modificar `feynlag` ni `feynlag-models` sin aprobación.
- No inventar ni recordar de memoria valores experimentales, significancias o referencias.
- No eliminar anomalías resueltas: pasan a `status: resolved` como casos pedagógicos.
- No avanzar a etapas 2–3 de ajuste en esta sesión.

## 10. Al terminar la sesión, repórtame

- Qué quedó hecho y en qué nivel A0–A4 está cada ficha.
- Tests que pasan o fallan.
- Peticiones de modelo generadas y carencias de feynlag detectadas.
- Valores marcados `TODO_VERIFY` y decisiones que necesitan mi criterio.
- Propuesta concreta para la siguiente sesión.
