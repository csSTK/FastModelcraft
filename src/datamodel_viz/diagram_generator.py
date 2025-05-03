from typing import List
import re
from src.datamodel_viz.model_parser import ParsedModel


def generate_mermaid(models: List[ParsedModel]) -> str:
    top = ["classDiagram"]
    head = [""]
    lines = [""]

    for model in models:
        lines.append(f"    class {model.name} {{")
        for field in model.fields:
            if re.match(r"(?:List|list)\[(.*?)\]", field.type_hint):
                head.append("        Person <|-- Company")
            lines.append(f"        {field.type_hint} {field.name}")
        lines.append("    }")

    return "\n".join(top + head + lines)


if __name__ == "__main__":
    from src.datamodel_viz.model_parser import parse_pydantic_models
    from pathlib import Path

    models = parse_pydantic_models(Path(__file__).parent / "example_models.py")
    mermaid_code = generate_mermaid(models)
    print(mermaid_code)
