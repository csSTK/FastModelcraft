from typing import List
from datamodel_viz.model_parser import ParsedModel


def generate_mermaid(models: List[ParsedModel]) -> str:
    lines = ["classDiagram"]

    for model in models:
        lines.append(f"    class {model.name} {{")
        for field in model.fields:
            lines.append(f"        {field.type_hint} {field.name}")
        lines.append("    }")

    return "\n".join(lines)


if __name__ == "__main__":
    from datamodel_viz.model_parser import parse_pydantic_models
    from pathlib import Path

    models = parse_pydantic_models(Path(__file__).parent / "example_models.py")
    mermaid_code = generate_mermaid(models)
    print(mermaid_code)
