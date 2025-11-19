from dataclasses import dataclass, field  # noqa: F401
from typing import List, Dict

#  Estructuras básicas


@dataclass
class Attribute:
    name: str  # nombre del atributo (ej: "sql", "ok")
    kind: str  # "synthesized" o "inherited"
    type: str  # tipo lógico del atributo (ej: "string", "bool")


@dataclass
class Production:
    head: str  # No terminal de la izquierda
    body: List[str]  # Símbolos de la derecha
    rules: List[str]  # Reglas semánticas en forma textual/documental


@dataclass
class AttributeGrammar:
    nonterminals: List[str]
    terminals: List[str]
    attributes: Dict[str, List[Attribute]]  # atributos por no terminal
    productions: List[Production]
    start_symbol: str


#  Construcción de la G. de Atributos


def build_sql_crud_attr_grammar() -> AttributeGrammar:
    """
    Genera un modelo de gramática de atributos para un mini-lenguaje
    de consultas tipo SQL (CRUD).
    """

    nonterminals = [
        "Program",
        "StmtList",
        "Stmt",
        "SelectStmt",
        "InsertStmt",
        "UpdateStmt",
        "DeleteStmt",
        "ColList",
        "TableName",
        "WhereOpt",
        "Cond",
    ]

    terminals = [
        "SELECT",
        "INSERT",
        "INTO",
        "UPDATE",
        "DELETE",
        "FROM",
        "SET",
        "VALUES",
        "WHERE",
        "ID",
        "NUM",
        "STRING",
        "COMMA",
        "EQ",
        "AND",
        "STAR",
        "LPAREN",
        "RPAREN",
        "SEMI",
    ]

    # Atributos: todos los no terminales tendrán un atributo sintetizado "sql"
    # que representa la cadena SQL reconstruida, y algunos pueden tener
    # atributos auxiliares como "ok" (bool para chequeos simples).
    attributes = {
        nt: [
            Attribute(name="sql", kind="synthesized", type="string"),
            Attribute(name="ok", kind="synthesized", type="bool"),
        ]
        for nt in nonterminals
    }

    prods: List[Production] = []

    # Program -> StmtList
    prods.append(
        Production(
            head="Program",
            body=["StmtList"],
            rules=[
                # Program.sql = StmtList.sql
                "Program.sql := StmtList.sql",
                "Program.ok := StmtList.ok",
            ],
        )
    )

    # StmtList -> StmtList Stmt
    prods.append(
        Production(
            head="StmtList",
            body=["StmtList", "Stmt"],
            rules=[
                "StmtList[1].ok := StmtList.ok and Stmt.ok",
                "StmtList[1].sql := StmtList.sql || '\\n' || Stmt.sql",
            ],
        )
    )

    # StmtList -> Stmt
    prods.append(
        Production(
            head="StmtList",
            body=["Stmt"],
            rules=["StmtList.sql := Stmt.sql", "StmtList.ok := Stmt.ok"],
        )
    )

    # Stmt -> SelectStmt SEMI
    prods.append(
        Production(
            head="Stmt",
            body=["SelectStmt", "SEMI"],
            rules=["Stmt.sql := SelectStmt.sql || ';'", "Stmt.ok := SelectStmt.ok"],
        )
    )

    # Stmt -> InsertStmt SEMI
    prods.append(
        Production(
            head="Stmt",
            body=["InsertStmt", "SEMI"],
            rules=["Stmt.sql := InsertStmt.sql || ';'", "Stmt.ok := InsertStmt.ok"],
        )
    )

    # Stmt -> UpdateStmt SEMI
    prods.append(
        Production(
            head="Stmt",
            body=["UpdateStmt", "SEMI"],
            rules=["Stmt.sql := UpdateStmt.sql || ';'", "Stmt.ok := UpdateStmt.ok"],
        )
    )

    # Stmt -> DeleteStmt SEMI
    prods.append(
        Production(
            head="Stmt",
            body=["DeleteStmt", "SEMI"],
            rules=["Stmt.sql := DeleteStmt.sql || ';'", "Stmt.ok := DeleteStmt.ok"],
        )
    )

    # SelectStmt -> SELECT ColList FROM TableName WhereOpt
    prods.append(
        Production(
            head="SelectStmt",
            body=["SELECT", "ColList", "FROM", "TableName", "WhereOpt"],
            rules=[
                "SelectStmt.sql := 'SELECT ' || ColList.sql || "
                "           ' FROM ' || TableName.sql || WhereOpt.sql",
                # ok sencillo: ok si ColList.ok y TableName.ok y WhereOpt.ok
                "SelectStmt.ok := ColList.ok and TableName.ok and WhereOpt.ok",
            ],
        )
    )

    # InsertStmt -> INSERT INTO TableName LPAREN ColList RPAREN VALUES LPAREN ColList RPAREN
    prods.append(
        Production(
            head="InsertStmt",
            body=[
                "INSERT",
                "INTO",
                "TableName",
                "LPAREN",
                "ColList",
                "RPAREN",
                "VALUES",
                "LPAREN",
                "ColList",
                "RPAREN",
            ],
            rules=[
                "InsertStmt.sql := 'INSERT INTO ' || TableName.sql || "
                "                  '(' || ColList[1].sql || ') VALUES (' || ColList[2].sql || ')'",
                # ok si el número de columnas coincide (control muy simple)
                "InsertStmt.ok := (ColList[1].count = ColList[2].count) "
                "                  and TableName.ok and ColList[1].ok and ColList[2].ok",
            ],
        )
    )

    # UpdateStmt -> UPDATE TableName SET ColList WhereOpt
    prods.append(
        Production(
            head="UpdateStmt",
            body=["UPDATE", "TableName", "SET", "ColList", "WhereOpt"],
            rules=[
                "UpdateStmt.sql := 'UPDATE ' || TableName.sql || "
                "                  ' SET ' || ColList.sql || WhereOpt.sql",
                "UpdateStmt.ok := TableName.ok and ColList.ok and WhereOpt.ok",
            ],
        )
    )

    # DeleteStmt -> DELETE FROM TableName WhereOpt
    prods.append(
        Production(
            head="DeleteStmt",
            body=["DELETE", "FROM", "TableName", "WhereOpt"],
            rules=[
                "DeleteStmt.sql := 'DELETE FROM ' || TableName.sql || WhereOpt.sql",
                "DeleteStmt.ok := TableName.ok and WhereOpt.ok",
            ],
        )
    )

    # ColList -> ID
    prods.append(
        Production(
            head="ColList",
            body=["ID"],
            rules=[
                "ColList.sql := ID.lexeme",
                "ColList.count := 1",
                "ColList.ok := true",
            ],
        )
    )

    # ColList -> ColList COMMA ID
    prods.append(
        Production(
            head="ColList",
            body=["ColList", "COMMA", "ID"],
            rules=[
                "ColList[1].sql := ColList.sql || ',' || ID.lexeme",
                "ColList[1].count := ColList.count + 1",
                "ColList[1].ok := ColList.ok",
            ],
        )
    )

    # TableName -> ID
    prods.append(
        Production(
            head="TableName",
            body=["ID"],
            rules=["TableName.sql := ID.lexeme", "TableName.ok := true"],
        )
    )

    # WhereOpt -> WHERE Cond
    prods.append(
        Production(
            head="WhereOpt",
            body=["WHERE", "Cond"],
            rules=["WhereOpt.sql := ' WHERE ' || Cond.sql", "WhereOpt.ok := Cond.ok"],
        )
    )

    # WhereOpt -> ε
    prods.append(
        Production(
            head="WhereOpt",
            body=[],
            rules=["WhereOpt.sql := ''", "WhereOpt.ok := true"],
        )
    )

    # Cond -> ID EQ (NUM | STRING)
    prods.append(
        Production(
            head="Cond",
            body=["ID", "EQ", "NUM"],
            rules=["Cond.sql := ID.lexeme || '=' || NUM.lexeme", "Cond.ok := true"],
        )
    )
    prods.append(
        Production(
            head="Cond",
            body=["ID", "EQ", "STRING"],
            rules=["Cond.sql := ID.lexeme || '=' || STRING.lexeme", "Cond.ok := true"],
        )
    )

    # Cond -> Cond AND Cond
    prods.append(
        Production(
            head="Cond",
            body=["Cond", "AND", "Cond"],
            rules=[
                "Cond[1].sql := Cond[0].sql || ' AND ' || Cond[2].sql",
                "Cond[1].ok := Cond[0].ok and Cond[2].ok",
            ],
        )
    )

    grammar = AttributeGrammar(
        nonterminals=nonterminals,
        terminals=terminals,
        attributes=attributes,
        productions=prods,
        start_symbol="Program",
    )

    return grammar


def main():
    g = build_sql_crud_attr_grammar()
    print("No terminales:", g.nonterminals)
    print("Terminales:", g.terminals)
    print("Producciones:")
    for p in g.productions:
        print(f"  {p.head} -> {' '.join(p.body) if p.body else 'ε'}")
        for r in p.rules:
            print("    {" + r + "}")


main()
