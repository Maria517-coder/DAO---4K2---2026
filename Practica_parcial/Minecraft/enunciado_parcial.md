# Simulacro de Parcial — Diseño y Algoritmos Orientados a Objetos (Python)

**Temática:** Minecraft — *El Taller de Crafteo del servidor*
**Modalidad:** individual, sin consultar material. Se valida con `pytest`.
**Duración sugerida:** 90 minutos

---

## 1. Descripción del problema

Un servidor de Minecraft cuenta con un **Taller de Crafteo** donde los jugadores encargan objetos y pagan por ellos en esmeraldas. Cada encargo (un *crafteo*) pertenece a **un único jugador** y puede ser de dos clases:

- **Crafteo de arma** (espadas, hachas, arcos, etc.).
- **Crafteo de poción** (curación, fuerza, velocidad, etc.).

El costo final de cada encargo se calcula de forma distinta según su tipo, y en ambos casos interviene alguna característica del jugador que lo pidió (su **rango** o su **nivel**). El taller debe poder registrar encargos y generar reportes.

Se pide modelar el sistema en Python aplicando **abstracción, herencia, polimorfismo y agregación**, y cargar los datos desde archivos CSV.

### Restricciones generales

- **No** se utilizan `@property`, `@setter`, getters ni setters. Todos los atributos son públicos y se asignan directamente en el `__init__`.
- **No** se requieren validaciones de negocio (no validar rangos, tipos ni valores negativos).
- Los nombres de clases, atributos y métodos deben respetar **exactamente** los indicados (los tests los usan).
- Todo el código (clases y funciones de carga) se escribe en un único módulo: **`main.py`**.

---

## 2. Especificación de clases

### 2.1 `Jugador` (clase asociada 1 a 1 por agregación)

| Atributo   | Tipo  | Descripción                                             |
|------------|-------|---------------------------------------------------------|
| `nickname` | `str` | Nombre único del jugador                                |
| `nivel`    | `int` | Nivel de experiencia                                    |
| `rango`    | `str` | Uno de: `"Novato"`, `"Aventurero"`, `"Veterano"`, `"Leyenda"` |

Constructor: `Jugador(nickname, nivel, rango)`

### 2.2 `Crafteo` (clase base abstracta)

Debe heredar de `ABC`. **No** puede instanciarse directamente.

| Atributo      | Tipo      | Descripción                                        |
|---------------|-----------|----------------------------------------------------|
| `idCrafteo`   | `int`     | Identificador del encargo                          |
| `item`        | `str`     | Nombre del objeto crafteado                        |
| `costoBase`   | `float`   | Costo base **por unidad**, en esmeraldas           |
| `cantidad`    | `int`     | Unidades encargadas                                |
| `jugador`     | `Jugador` | Jugador que realizó el encargo (agregación)        |

Constructor: `Crafteo(idCrafteo, item, costoBase, cantidad, jugador)`

Método abstracto (decorado con `@abstractmethod`):

```python
calcularCostoFinal(self) -> float
```

### 2.3 `CrafteoArma(Crafteo)`

Atributos propios (además de los heredados):

| Atributo    | Tipo   | Descripción                              |
|-------------|--------|------------------------------------------|
| `danio`     | `int`  | Puntos de daño del arma                  |
| `encantada` | `bool` | Si el arma lleva encantamiento           |

Constructor: `CrafteoArma(idCrafteo, item, costoBase, cantidad, jugador, danio, encantada)`
Debe reutilizar el constructor de la clase base mediante `super().__init__(...)`.

**Fórmula de `calcularCostoFinal()`:**

1. `subtotal = (costoBase + danio * 1.5) * cantidad`
2. Si `encantada` es `True`: `subtotal = subtotal * 1.25` (recargo del 25 %).
3. Descuento según el **rango** del jugador:

   | Rango       | Descuento |
   |-------------|-----------|
   | `Leyenda`   | 20 %      |
   | `Veterano`  | 10 %      |
   | cualquier otro | 0 %    |

4. `costoFinal = subtotal * (1 - descuento)`

> Ejemplo: Hacha de netherita, `costoBase=90.0`, `cantidad=1`, `danio=10`, encantada, jugador *Leyenda*
> → `(90 + 15) * 1 = 105` → `105 * 1.25 = 131.25` → `131.25 * 0.80 = 105.0`

### 2.4 `CrafteoPocion(Crafteo)`

Atributos propios:

| Atributo   | Tipo   | Descripción                                   |
|------------|--------|-----------------------------------------------|
| `potencia` | `int`  | Nivel de potencia de la poción (1 a 3)        |
| `splash`   | `bool` | Si es poción arrojadiza                       |

Constructor: `CrafteoPocion(idCrafteo, item, costoBase, cantidad, jugador, potencia, splash)`
Debe reutilizar el constructor de la clase base mediante `super().__init__(...)`.

**Fórmula de `calcularCostoFinal()`:**

1. `subtotal = costoBase * potencia * cantidad`
2. Si `splash` es `True`: se suma un recargo fijo de **15 esmeraldas por unidad** → `subtotal = subtotal + 15 * cantidad`
3. Descuento según el **nivel** del jugador: si `nivel >= 30` se aplica un **10 %** de descuento; en caso contrario, ninguno. (El descuento no se acumula: un nivel 100 también recibe solo 10 %.)
4. `costoFinal = subtotal * (1 - descuento)`

> Ejemplo: Poción de regeneración, `costoBase=18.0`, `cantidad=2`, `potencia=3`, splash, jugador nivel 30
> → `18*3*2 = 108` → `108 + 15*2 = 138` → `138 * 0.90 = 124.2`

### 2.5 `TallerCrafteo` (contenedor principal)

| Atributo   | Tipo             | Descripción                                         |
|------------|------------------|-----------------------------------------------------|
| `nombre`   | `str`            | Nombre del taller                                   |
| `crafteos` | `list[Crafteo]`  | Lista de encargos, **inicializada vacía** en el `__init__` |

Constructor: `TallerCrafteo(nombre)`

> ⚠️ Cada instancia debe tener **su propia** lista (no compartida entre talleres).

**Métodos a implementar:**

| Método | Descripción | Retorno si no hay datos / coincidencias |
|--------|-------------|------------------------------------------|
| `addCrafteo(crafteo)` | Agrega el encargo al final de la lista. | — |
| `totalRecaudado()` | Suma de `calcularCostoFinal()` de **todos** los encargos. | `0.0` |
| `totalPorJugador(nickname)` | Suma de los costos finales de los encargos cuyo `jugador.nickname` coincide. | `0.0` |
| `promedioEnRango(minimo, maximo)` | Promedio de los costos finales que cumplan `minimo <= costo <= maximo` (**ambos extremos inclusivos**). | `0.0` |
| `buscarPrimeroDeJugador(nickname)` | Devuelve el **primer** encargo (en orden de inserción) del jugador indicado. Debe cortar apenas lo encuentra. | `None` |
| `buscarPrimeroMayorA(umbral)` | Devuelve el **primer** encargo cuyo costo final sea **estrictamente mayor** que `umbral`. Debe cortar apenas lo encuentra (no recorrer ni calcular el resto). | `None` |
| `contarPorTipo(tipo)` | Cantidad de encargos que son instancia de la clase `tipo` (por ejemplo `CrafteoArma`, `CrafteoPocion` o incluso `Crafteo`). | `0` |
| `crafteoMasCaro()` | Devuelve el encargo con mayor costo final. | `None` |

---

## 3. Carga de datos desde CSV

Se entregan tres archivos (codificación UTF-8, separador coma, con encabezado):

- `jugadores.csv` → `nickname,nivel,rango`
- `crafteos_armas.csv` → `idCrafteo,item,costoBase,cantidad,nickname,danio,encantada`
- `crafteos_pociones.csv` → `idCrafteo,item,costoBase,cantidad,nickname,potencia,splash`

En los campos booleanos (`encantada`, `splash`) el valor es `si` o `no`.
En los CSV de crafteos, la columna `nickname` referencia a un jugador de `jugadores.csv`.

Implementar en `main.py` las siguientes funciones (pueden usar el módulo `csv`):

| Función | Retorno |
|---------|---------|
| `cargarJugadores(ruta)` | `dict` con clave `nickname` y valor el objeto `Jugador`. |
| `cargarArmas(ruta, jugadores)` | `list` de `CrafteoArma`, en el orden del archivo. Cada arma referencia el **mismo objeto** `Jugador` del diccionario. |
| `cargarPociones(ruta, jugadores)` | `list` de `CrafteoPocion`, en el orden del archivo. Idem. |
| `cargarTaller(rutaJugadores, rutaArmas, rutaPociones)` | Un `TallerCrafteo` de nombre `"Taller Central"` con **primero todas las armas y luego todas las pociones**. |

Recordar convertir los tipos: `int` para `nivel`, `idCrafteo`, `cantidad`, `danio`, `potencia`; `float` para `costoBase`; `bool` para `encantada` y `splash`.

---

## 4. Estructura de archivos y ejecución

```
parcial/
├── main.py                 # (lo escribís vos)
├── jugadores.csv
├── crafteos_armas.csv
├── crafteos_pociones.csv
└── test_parcial.py
```

```bash
pip install pytest
pytest test_parcial.py -v
```

## 5. Criterios de evaluación

| Aspecto | Peso |
|---------|------|
| Clase base abstracta correcta (`ABC`, `@abstractmethod`, no instanciable) | 15 % |
| Herencia con `super().__init__` y atributos propios | 15 % |
| Cálculo polimórfico en cada subclase | 25 % |
| Contenedor: lista propia, `addCrafteo`, totales y promedio con filtro | 25 % |
| Búsquedas con corte temprano y conteo por tipo | 10 % |
| Carga desde CSV con conversión de tipos | 10 % |

**Aprobación:** todos los tests de las secciones de abstracción, herencia y polimorfismo deben pasar, y al menos el 70 % del total.
