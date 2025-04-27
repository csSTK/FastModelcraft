import csv
from datetime import datetime
from typing import List


def infer_type(values: List[str]) -> str:
    for value in values:
        value = value.strip()
        if value == "":
            continue
        if value.isdigit():
            return "int"
        try:
            float(value)
            return "float"
        except ValueError:
            pass
        try:
            datetime.fromisoformat(value)
            return "datetime"
        except ValueError:
            pass
    return "str"


def csv_to_pydantic(csv_path: str, model_name: str = "AutoModel") -> str:
    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        rows = list(reader)

    if not headers:
        raise ValueError("CSV file has no headers")

    inferred = {h: infer_type([row[h] for row in rows[:10]]) for h in headers}

    lines = [
        f"class {model_name}(BaseModel):",
    ]
    for field, field_type in inferred.items():
        lines.append(f"    {field}: {field_type}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(csv_to_pydantic("src/schema_mapper/example.csv", "ExampleModel"))
