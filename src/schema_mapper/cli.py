import typer
from pathlib import Path
from schema_mapper.csv_to_pydantic import csv_to_pydantic  # type: ignore

app = typer.Typer()

# Run with:
# python -m schema_mapper src/schema_mapper/example.csv --model-name UserModel --output user_model.py


@app.command()
def map_csv(
    csv_file: Path = typer.Argument(..., help="Path to the CSV file"),
    model_name: str = typer.Option(
        "AutoModel", "--model-name", "-m", help="Name of the Pydantic model"
    ),
    output: Path = typer.Option(
        None, "--output", "-o", help="Optional output .py file"
    ),
):
    """Convert a CSV file into a Pydantic model."""
    model_code = csv_to_pydantic(str(csv_file), model_name=model_name)

    if output:
        output.write_text(model_code)
        typer.echo(f"✅ Model written to {output}")
    else:
        typer.echo(model_code)


if __name__ == "__main__":
    app()
