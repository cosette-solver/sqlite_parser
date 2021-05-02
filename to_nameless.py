from sql_ast import *
import os
import json
from pprint import pprint
import copy
import sys
import re
from antlr4 import *
from grammar.SQLiteLexer import SQLiteLexer
from grammar.SQLiteParser import SQLiteParser
from grammar.SQLiteListener import SQLiteListener
from readlisp import readlisp, LispSymbol


def get_parsed_tree(filename):
    with open(filename, "r+") as f:
        query = f.read()
    cleaned_query = pre_process_tree(query)
    with open(filename, "w+") as f:
        f.write(cleaned_query)
    input_stream = FileStream(filename)
    lexer = SQLiteLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SQLiteParser(stream)
    tree = parser.parse()   
    tree = remove_lisp_symbol(readlisp(tree.toStringTree(recog=parser)))
    return tree

def pre_process_tree(query):
    query += "\n"
    query = re.sub("""(?!\()([^\s]+?\s+?(?:not\s)?like\s+?["'][^\s]+?["'])\s+?(?!\))""", r' (\1) ', query, flags = re.IGNORECASE)
    query = re.sub("""(?!\()([^\s]+?\s+?(?:not\s)?like\s*?["'][^\s]+?["'])\s*?(?!\))""", r' (\1) ', query, flags = re.IGNORECASE)
    query = re.sub("""(?!\()([^\s]+?\s+?(?:not\s)?like\s*?["']%?[\w\d\s]+?%?["'])\s*?(?!\))""", r' (\1) ', query, flags = re.IGNORECASE)
    query = query.replace(";", "")
    return query

        
def remove_lisp_symbol(l):
    if type(l) in [LispSymbol, int, float]:
        if type(l) == LispSymbol:
            return l.name.lower()
        else:
            return str(l)
    elif type(l) == list:
        return [remove_lisp_symbol(ls) for ls in l]
    else:
        print("Uhoh", type(l), l)

def to_nameless(input_sql, output_json):
    schema_tree = get_parsed_tree(input_sql)
    schema = {}
    queries = []
    for stmt in schema_tree[1:]:
        if stmt == '<eof>':
            break
        if stmt[1][1][0] == "create_table_stmt":
            create_tbl_stmt = stmt[1][1]
            table_name = create_tbl_stmt[3][1][1] if create_tbl_stmt[3][0] == 'table_name' else ""
            schema[table_name] = {}
            for col in create_tbl_stmt[4]:
                if col == ',':
                    continue
                elif col[0] == 'column_def':
                    col_name = col[1][1][1]
                    col_type = col[2][1][1][1]
                    if len(col) > 3:
                        col_constraint = col[3][1:-1]
                    else:
                        col_constraint = None
                    schema[table_name][col_name] = [col_type, col_constraint]
                else:
                    pass
        elif stmt[1][1][0] == "factored_select_stmt":
            query = SelectStatement(stmt[1][1])
            query_tree = query.rename_to_index(schema)[0]
            query_result = query_tree.to_nameless(schema)
            queries.append(query_result)

    output = {"schema": schema, "queries": queries}
    with open(output_json, "w+") as f:
        json.dump(output,f)

if __name__ == '__main__':
    args = sys.argv
    input_sql = args[1]
    output_json = args[2]
    to_nameless(input_sql, output_json)