import ast
from pathlib import Path
from typing import List


class ModelField:
    def __init__(self, name: str, type_hint: str):
        self.name = name
        self.type_hint = type_hint


class ParsedModel:
    def __init__(self, name: str, fields: List[ModelField]):
        self.name = name
        self.fields = fields


def parse_pydantic_models(file_path: Path) -> List[ParsedModel]:
    source = file_path.read_text()
    tree = ast.parse(source)

    models: List[ParsedModel] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
            if "BaseModel" in bases:
                fields: List[ModelField] = []
                for stmt in node.body:
                    if isinstance(stmt, ast.AnnAssign) and isinstance(
                        stmt.target, ast.Name
                    ):
                        field_name = stmt.target.id
                        field_type = ast.unparse(stmt.annotation)
                        fields.append(ModelField(field_name, field_type))
                models.append(ParsedModel(node.name, fields))

    return models


if __name__ == "__main__":
    models = parse_pydantic_models(Path(__file__).parent / "example_models.py")
    for model in models:
        print(f"Model: {model.name}")
        for field in model.fields:
            print(f"  - {field.name}: {field.type_hint}")
