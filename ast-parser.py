
from os import path

import argparse
import json

class AstParser:

    AUTHORIZED_FUNCTIONS = [
        "ArrayExpression",
        "ArrowFunctionExpression",
        "AssignmentExpression",
        "BinaryExpression",
        "BlockStatement",
        "BreakStatement",
        "CallExpression",
        "ExpressionStatement",
        "ForStatement",
        "FunctionDeclaration",
        "FunctionExpression",
        "Identifier",
        "IfStatement",
        "Literal",
        "MemberExpression",
        "NewExpression",
        "Program",
        "ReturnStatement",
        "TemplateElement",
        "TemplateLiteral",
        "UpdateExpression",
        "VariableDeclaration",
        "VariableDeclarator"
    ]

    NEW_LINE = "\n"
    OPEN_PARENTHESE = "("
    CLOSE_PARENTHESE = ")"
    SEMICOLON = ";"
    ARROW_EXPRESSION = "=>"
    OPEN_CBRACKET = "{"
    CLOSE_CBRACKET = "}"
    OPEN_SBRACKET = "["
    CLOSE_SBRACKET = "]"
    COMMA = ","
    EQUAL = "="


    def __init__(self, data: dict) -> None:
        self.data = data
        self.script = str()


    def parse(self) -> str:
        self._CallFunctionByType(self.data)
        
        return self.script

    def Program(self, data: dict) -> None:
        for line in data["body"]:
            self._CallFunctionByType(line)
            
            self.script += self.NEW_LINE


    def FunctionDeclaration(self, data: dict) -> None:
        self.script += "function "

        self._CallFunctionByType(data["id"])
        
        self.script += self.OPEN_PARENTHESE

        for param in data["params"]:
            raise NotImplementedError
        
        self.script += self.CLOSE_PARENTHESE

        self._CallFunctionByType(data["body"])


    def ExpressionStatement(self, data: dict) -> None:
        self._CallFunctionByType(data["expression"])
        
        self.script += self.SEMICOLON


    def AssignmentExpression(self, data: dict) -> None:
        self._CallFunctionByType(data["left"])

        self.script += data["operator"]

        self._CallFunctionByType(data["right"])


    def FunctionExpression(self, data: dict) -> None:
        self._CallFunctionByType(data["body"])


    def CallExpression(self, data: dict) -> None:
        self._CallFunctionByType(data["callee"])
        
        self.script += self.OPEN_PARENTHESE

        for k, arg in enumerate(data["arguments"]):
            self._CallFunctionByType(arg)

            if (k + 1) != len(data["arguments"]):
                self.script += ","

        self.script += self.CLOSE_PARENTHESE


    def BinaryExpression(self, data: dict) -> None:
        self.AssignmentExpression(data)


    def MemberExpression(self, data: dict) -> None:
        if "name" not in list(data["object"].keys()):
            self._CallFunctionByType(data["object"])

            self.script += f".{data['property']['name']}"
        else:
            self.script += f"{data['object']['name']}.{data['property']['name']}"


    def ArrowFunctionExpression(self, data: dict) -> None:
        self.script += self.OPEN_PARENTHESE

        for k, param in enumerate(data["params"]):
            self._CallFunctionByType(param)

            if (k + 1) != len(data["params"]):
                self.script += self.COMMA

        self.script += self.CLOSE_PARENTHESE + self.ARROW_EXPRESSION

        self._CallFunctionByType(data["body"])


    def BlockStatement(self, data: dict) -> None:
        self.script += self.OPEN_CBRACKET

        for line in data["body"]:
            self._CallFunctionByType(line)

        self.script += self.CLOSE_CBRACKET


    def ReturnStatement(self, data: dict) -> None:
        self.script += "return "

        self._CallFunctionByType(data["argument"])


    def IfStatement(self, data: dict) -> None:
        self.script += "if" + self.OPEN_PARENTHESE

        self._CallFunctionByType(data["test"])

        self.script += self.CLOSE_PARENTHESE

        self._CallFunctionByType(data["consequent"])

        # Check if else
        if not isinstance(data["alternate"], type(None)):
            self.script += "else"
            self._CallFunctionByType(data["alternate"])


    def ForStatement(self, data: dict) -> None:
        self.script += "for ("
        self._CallFunctionByType(data["init"])
        self.script += ";"

        self._CallFunctionByType(data["test"])
        self.script += ";"

        self._CallFunctionByType(data["update"])
        self.script += ")"

        self._CallFunctionByType(data["body"])


    def BreakStatement(self, data: dict) -> None:
        self.script += "break"


    def UpdateExpression(self, data: dict) -> None:
        self.script += data["argument"]["name"]
        self.script += data["operator"]


    def VariableDeclaration(self, data: dict) -> None:
        self.script += f"{data['kind']} "
        for line in data["declarations"]:
            self._CallFunctionByType(line)
        
        self.script += self.SEMICOLON


    def VariableDeclarator(self, data: dict) -> None:
        self._CallFunctionByType(data["id"])

        self.script += self.EQUAL

        self._CallFunctionByType(data["init"])


    def TemplateLiteral(self, data: dict) -> None:
        self.script += "`"

        expressions = data["expressions"]
        quasis = data["quasis"]

        array = sorted(expressions + quasis, key=lambda x: x["start"])

        for elem in array:
            if elem["type"] == "TemplateElement":
                self._CallFunctionByType(elem)
            else:
                self.script += "${"
                self._CallFunctionByType(elem)
                self.script += self.CLOSE_CBRACKET
        
        self.script += "`"


    def NewExpression(self, data: dict) -> None:
        self.script += self.OPEN_PARENTHESE

        for k, arg in enumerate(data["arguments"]):
            self._CallFunctionByType(arg)

            if (k + 1) != len(data["arguments"]):
                self.script += self.COMMA

        self.script += self.CLOSE_PARENTHESE


    def TemplateElement(self, data: dict) -> None:
        self.script += data["value"]["raw"]


    def Identifier(self, data: dict) -> None:
        self.script += data["name"]


    def ArrayExpression(self, data: dict) -> None:
        self.script += self.OPEN_SBRACKET

        for k, line in enumerate(data["elements"]):
            self._CallFunctionByType(line)
            if (k + 1) != len(data["elements"]):
                self.script += self.COMMA

        self.script += self.CLOSE_SBRACKET

    def Literal(self, data: dict) -> None:
        value = data["value"]

        if isinstance(value, str):
            self.script += f'"{value}"'
        else:
            self.script += str(value)


    def NotImplemented(self, data: dict) -> None:
        print(self.script)
        print(data)
        print(data["type"])
        raise NotImplementedError
    
    def _CallFunctionByType(self, data: dict) -> None:
        if data["type"] in self.AUTHORIZED_FUNCTIONS:
            func = getattr(self, data["type"], None)

            if func:
                func(data)
            else:
                self.NotImplemented(data)

        else:
            print(self.script)
            exit(f"Function {data['type']} not authorized")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert AST JSON file to Code.")
    parser.add_argument("-f", "--file", type=str, required=True, help="AST JSON file.")
    parser.add_argument("-o", "--output", type=str, required=False, help="Write to content to a file", default=None)
    args = parser.parse_args()

    if not path.exists(args.file):
        exit("File not found !")

    if not path.isfile(args.file):
        exit(f"{args.file} is not a file")


    with open(args.file, "r") as f:
        data = f.read()

    json_data: dict = json.loads(data)

    ast_parser = AstParser(json_data)
    script = ast_parser.parse()

    if args.output:
        with open(args.output, "w") as f:
            f.write(script)
    else:
        print(script)
