# Parcial_3

Gramática de Atributos + Lenguaje Matricial + ANTLR (Python)**

Este proyecto implementa los tres puntos solicitados en el trabajo:

1. **Modelar una función que genere una gramática de atributos** para un lenguaje con operaciones CRUD tipo SQL.
2. **Diseñar la gramática** para un lenguaje capaz de realizar **producto punto entre matrices**.
3. **Implementar en ANTLR**, con destino Python, el lenguaje diseñado en el punto 2.


# **1. Estructura del proyecto**

```
- sql_attr_grammar.py       ← Punto 1: gramática de atributos SQL-CRUD
- matlang_grammar.txt       ← Punto 2: gramática formal en BNF/EBNF
- MatLang.g4                ← Punto 3: gramática ANTLR del lenguaje MatLang
- matlang_semantics.py      ← Semántica: visitor que ejecuta el lenguaje
- matlang_main.py           ← Main para ejecutar programas MatLang

- (Archivos generados por ANTLR)
    - MatLangLexer.py
    - MatLangParser.py
    - MatLangVisitor.py
    - MatLangListener.py
```

# **2. Punto 1 – Gramática de Atributos (SQL-CRUD)**

Archivo: **`sql_attr_grammar.py`**

Este archivo contiene una función en Python llamada:

```python
build_sql_crud_attr_grammar()
```

La función construye un **modelo completo de gramática de atributos** para un lenguaje con operaciones SQL:

* SELECT
* INSERT
* UPDATE
* DELETE

La gramática incluye:

* No terminales
* Terminales
* Producciones
* Atributos sintetizados:

  * `sql` (representación reconstruida de la sentencia)
  * `ok` (validación simple)
* Reglas semánticas formales

### **Ejecución**

```bash
python3 sql_attr_grammar.py
```

La salida mostrará:

* Lista de no terminales
* Lista de terminales
* Producciones
* Reglas semánticas asociadas

Este archivo NO ejecuta SQL real — es un **modelo formal** de una gramática de atributos.

# **3. Punto 2 – Gramática para Lenguaje de Matrices**

Archivo: **`matlang_grammar.txt`**

Define una gramática en BNF/EBNF para un lenguaje `MatLang` que permite:

* Declarar matrices con dimensiones
* Asignar matrices
* Evaluar expresiones con producto de matrices mediante `*`
* Imprimir matrices

Ejemplo válido:

```
mat A[2,3] = [[1,2,3],[4,5,6]];
mat B[3,2] = [[1,2],[3,4],[5,6]];
C = A * B;
print C;
```

Este archivo **no se ejecuta**.
Es una **especificación formal** para entregar.

# **4. Punto 3 – Implementación en ANTLR (Python)**

## **4.1. Archivo principal ANTLR**

Archivo: **`MatLang.g4`**

Define la gramática para ANTLR con destino Python:

* Declaraciones (`mat ID[...] = literal`)
* Asignaciones (`ID = expr`)
* Expresiones (`A * B`)
* Literales de matrices
* Impresión (`print ID`)

## **4.2. Generar el parser (lexer + parser + visitor)**

Desde consola:

```bash
java -jar antlr-4.jar -Dlanguage=Python3 -visitor MatLang.g4
```

Esto genera:

```
MatLangLexer.py
MatLangParser.py
MatLangVisitor.py
MatLangListener.py
```

Todos quedan en la misma carpeta.

# **5. Semántica del Lenguaje**

Archivo: **`matlang_semantics.py`**

Implementa un **visitor** que ejecuta las instrucciones del lenguaje:

* Manejo de un entorno de matrices (`env`)
* Validación de dimensiones
* Producto de matrices con método clásico
* Interpretación de literales
* Ejecución de `print`

La clase principal es:

```python
class EvalVisitor(MatLangVisitor):
```

# **6. Ejecución del Lenguaje MatLang**

Archivo: **`matlang_main.py`**

Este archivo:

* Lee un archivo fuente `.mt`
* Llama al lexer y parser generados por ANTLR
* Ejecuta el visitor semántico

### **Crear un programa de prueba**

Archivo: `program.mt`

```
mat A[2,3] = [[1,2,3],[4,5,6]];
mat B[3,2] = [[1,2],[3,4],[5,6]];
C = A * B;
print C;
```

### **Ejecutar**

```bash
python3 matlang_main.py program.mt
```

Si todo es correcto, se imprimirá la matriz resultante del producto.

# **7. Requisitos previos**

* Runtime de ANTLR en Python:

  ```bash
  pip install antlr4-python3-runtime
  ```

# **9. Ejemplo de flujo completo**

```bash
# Compilar ANTLR
java -jar antlr-4.jar -Dlanguage=Python3 -visitor MatLang.g4

# Ejecutar el programa del lenguaje MatLang
python3 matlang_main.py program.mt
```
