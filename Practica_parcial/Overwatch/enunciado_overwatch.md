# Simulacro de Parcial — Diseño y Algoritmos Orientados a Objetos (Python)

**Temática:** Overwatch — *Registro de partidas de la Temporada*
**Modalidad:** individual, sin consultar material. Se valida con `pytest`.
**Duración sugerida:** 90 minutos

---

## 1. Descripción del problema

El servidor de Overwatch registra las partidas que juegan sus jugadores durante una **Temporada**. Cada partida la juega **un único jugador** y puede ser de dos clases:

- **Partida rápida**: modo casual, con eventos especiales y bono para los jugadores nuevos.
- **Partida competitiva**: modo clasificatorio, donde importan la victoria, la racha y el rol elegido.

Al terminar cada partida, el jugador recibe **puntos de experiencia (XP)**. La fórmula es distinta según el tipo de partida y, en ambos casos, interviene alguna característica del jugador (su **nivel** o su **rol**). La temporada debe poder registrar partidas y generar reportes.

Se pide modelar el sistema en Python aplicando **abstracción, herencia, polimorfismo y agregación**, y cargar los datos desde archivos CSV.

### Restricciones generales

- **No** se utilizan `@property`, `@setter`, getters ni setters. Todos los atributos son públicos y se asignan directamente en el `__init__`.
- **No** se requieren validaciones de negocio (no validar rangos, tipos ni valores negativos).
- Los nombres de clases, atributos y métodos deben respetar **exactamente** los indicados (los tests los usan).
- Los tests hacen `from main import ...`. Las clases pueden estar definidas en `main.py` o en archivos separados, siempre que `main.py` las importe. Las funciones de carga van en `main.py`.

---

## 2. Especificación de clases

### 2.1 `Jugador` (clase asociada 1 a 1 por agregación)

| Atributo    | Tipo  | Descripción                                                  |
|-------------|-------|--------------------------------------------------------------|
| `battletag` | `str` | Nombre único del jugador                                     |
| `nivel`     | `int` | Nivel de cuenta                                              |
| `rol`       | `str` | Uno de: `"Tanque"`, `"Danio"`, `"Apoyo"`                    |

Constructor: `Jugador(battletag, nivel, rol)`

### 2.2 `Partida` (clase base abstracta)

Debe heredar de `ABC`. **No** puede instanciarse directamente.

| Atributo          | Tipo      | Descripción                                           |
|-------------------|-----------|-------------------------------------------------------|
| `idPartida`       | `int`     | Identificador de la partida                           |
| `mapa`            | `str`     | Nombre del mapa                                       |
| `duracionMinutos` | `int`     | Duración de la partida en minutos                     |
| `eliminaciones`   | `int`     | Eliminaciones logradas por el jugador                 |
| `victoria`        | `bool`    | `True` si el jugador ganó                             |
| `jugador`         | `Jugador` | Jugador que disputó la partida (agregación)           |

Constructor: `Partida(idPartida, mapa, duracionMinutos, eliminaciones, victoria, jugador)`

Método abstracto (decorado con `@abstractmethod`):

```python
calcularExperiencia(self) -> float
```

### 2.3 `PartidaRapida(Partida)`

Atributo propio (además de los heredados):

| Atributo         | Tipo   | Descripción                                   |
|------------------|--------|-----------------------------------------------|
| `eventoEspecial` | `bool` | Si la partida se jugó durante un evento       |

Constructor: `PartidaRapida(idPartida, mapa, duracionMinutos, eliminaciones, victoria, jugador, eventoEspecial)`
Debe reutilizar el constructor de la clase base mediante `super().__init__(...)`.

**Fórmula de `calcularExperiencia()`** (aplicar los pasos en este orden):

1. `xp = duracionMinutos * 10 + eliminaciones * 5`
2. Si `victoria` es `True`: se suman **100** puntos fijos (`xp = xp + 100`).
3. Si `eventoEspecial` es `True`: `xp = xp * 1.25` (recargo del 25 %).
4. **Bono de novato:** si el `nivel` del jugador es **menor a 50**, `xp = xp * 1.5`. (El nivel 50 exacto no recibe bono.)

> Ejemplo: `duracionMinutos=15`, `eliminaciones=10`, victoria, evento especial, jugador nivel 60
> → `150 + 50 = 200` → `200 + 100 = 300` → `300 * 1.25 = 375` → nivel ≥ 50, sin bono → **375.0**

### 2.4 `PartidaCompetitiva(Partida)`

Atributo propio:

| Atributo | Tipo  | Descripción                                          |
|----------|-------|------------------------------------------------------|
| `racha`  | `int` | Victorias consecutivas previas del jugador           |

Constructor: `PartidaCompetitiva(idPartida, mapa, duracionMinutos, eliminaciones, victoria, jugador, racha)`
Debe reutilizar el constructor de la clase base mediante `super().__init__(...)`.

**Fórmula de `calcularExperiencia()`** (aplicar los pasos en este orden):

1. `xp = duracionMinutos * 15 + eliminaciones * 8`
2. Si `victoria` es `True`: `xp = xp * 1.5`. Si es `False` (derrota): `xp = xp * 0.5`.
3. **Bono de racha:** `xp = xp * (1 + 0.10 * racha)`, con la racha **limitada a un máximo de 5** (una racha de 8 se trata como 5).
4. **Bono de rol:** si el `rol` del jugador es `"Tanque"`, se suman **40** puntos fijos **al final** (esos 40 no se multiplican por nada).

> Ejemplo: `duracionMinutos=20`, `eliminaciones=10`, victoria, `racha=2`, jugador `"Tanque"`
> → `300 + 80 = 380` → `380 * 1.5 = 570` → `570 * 1.2 = 684` → `684 + 40 = 724` → **724.0**

### 2.5 `Temporada` (contenedor principal)

| Atributo   | Tipo             | Descripción                                                  |
|------------|------------------|--------------------------------------------------------------|
| `nombre`   | `str`            | Nombre de la temporada                                       |
| `partidas` | `list[Partida]`  | Lista de partidas, **inicializada vacía** en el `__init__`   |

Constructor: `Temporada(nombre)`

> ⚠️ Cada instancia debe tener **su propia** lista (no compartida entre temporadas).

**Métodos a implementar:**

| Método | Descripción | Retorno si no hay datos / coincidencias |
|--------|-------------|------------------------------------------|
| `addPartida(partida)` | Agrega la partida al final de la lista. | — |
| `experienciaTotal()` | Suma de `calcularExperiencia()` de **todas** las partidas. | `0.0` |
| `experienciaPorJugador(battletag)` | Suma de la experiencia de las partidas cuyo `jugador.battletag` coincide. | `0.0` |
| `promedioEnRango(minimo, maximo)` | Promedio de la experiencia de las partidas que cumplan `minimo <= xp <= maximo` (**ambos extremos inclusivos**). | `0.0` |
| `buscarPrimeraDeJugador(battletag)` | Devuelve la **primera** partida (en orden de inserción) del jugador indicado. Debe cortar apenas la encuentra. | `None` |
| `buscarPrimeraMayorA(umbral)` | Devuelve la **primera** partida cuya experiencia sea **estrictamente mayor** que `umbral`. Debe cortar apenas la encuentra (no recorrer ni calcular el resto). | `None` |
| `contarPorTipo(tipo)` | Cantidad de partidas que son instancia de la clase `tipo` (por ejemplo `PartidaRapida`, `PartidaCompetitiva` o incluso `Partida`). | `0` |
| `partidaMasLarga()` | Devuelve la partida con mayor `duracionMinutos` (se compara la **duración**, no la experiencia). Si hay empate, la primera. | `None` |

---

## 3. Carga de datos desde CSV

Se entregan dos archivos (codificación UTF-8, separador coma, con encabezado):

- `jugadores_ow.csv` → `battletag,nivel,rol`
- `partidas_ow.csv` → `tipo,idPartida,mapa,duracionMinutos,eliminaciones,victoria,battletag,eventoORacha`

`partidas_ow.csv` es **un único archivo** que mezcla los dos tipos de partida. La columna `tipo` es el código que indica qué clase instanciar, y la última columna cambia de significado (y de tipo de dato) según ese código:

| `tipo` | Clase a instanciar   | `eventoORacha` es…                    | Se convierte a… |
|--------|----------------------|---------------------------------------|-----------------|
| `1`    | `PartidaRapida`      | `eventoEspecial` (`si` / `no`)        | `bool`          |
| `2`    | `PartidaCompetitiva` | `racha` (un número entero)            | `int`           |

- La columna `victoria` también vale `si` o `no`.
- La columna `battletag` referencia a un jugador de `jugadores_ow.csv`.

Implementar en `main.py` las siguientes funciones (pueden usar el módulo `csv`):

| Función | Retorno |
|---------|---------|
| `cargarJugadores(ruta)` | `dict` con clave `battletag` y valor el objeto `Jugador`. |
| `cargarPartidas(ruta, jugadores)` | `list` de `PartidaRapida` y `PartidaCompetitiva` (según la columna `tipo`), en el orden del archivo. Cada partida referencia el **mismo objeto** `Jugador` del diccionario. |
| `cargarTemporada(rutaJugadores, rutaPartidas)` | Una `Temporada` de nombre `"Temporada Actual"` con las partidas en el orden del archivo. |

Recordar convertir los tipos: `int` para `nivel`, `idPartida`, `duracionMinutos`, `eliminaciones`; `bool` para `victoria` (y para `eventoORacha` cuando el tipo es 1); `int` para `eventoORacha` cuando el tipo es 2.

---

## 4. Estructura de archivos y ejecución

Usar una **carpeta nueva** para este examen (con su propio `main.py`):

```
parcial_overwatch/
├── main.py                 # (lo escribís vos)
├── jugadores_ow.csv
├── partidas_ow.csv
└── test_parcial_ow.py
```

```bash
pip install pytest
pytest test_parcial_ow.py -v
```

## 5. Criterios de evaluación

| Aspecto | Peso |
|---------|------|
| Clase base abstracta correcta (`ABC`, `@abstractmethod`, no instanciable) | 15 % |
| Herencia con `super().__init__` y atributos propios | 15 % |
| Cálculo polimórfico en cada subclase | 25 % |
| Contenedor: lista propia, `addPartida`, totales y promedio con filtro | 25 % |
| Búsquedas con corte temprano, conteo por tipo y máximo | 10 % |
| Carga desde CSV único, distinguiendo la clase por `tipo` | 10 % |

**Aprobación:** todos los tests de las secciones de abstracción, herencia y polimorfismo deben pasar, y al menos el 70 % del total.
