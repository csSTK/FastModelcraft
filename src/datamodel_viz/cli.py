import typer
from pathlib import Path
from src.datamodel_viz.model_parser import parse_pydantic_models
from src.datamodel_viz.diagram_generator import generate_mermaid

app = typer.Typer()

# Run with:
# python -m datamodel_viz src/datamodel_viz/example_models.py --output diagram.mmd


@app.command("render")
def render(
    file: Path = typer.Argument(..., help="Path to the Python file with models"),
    output: Path = typer.Option(None, "--output", "-o", help="Optional output file"),
):
    """Render Pydantic models as a Mermaid diagram."""
    models = parse_pydantic_models(file)
    mermaid_code = generate_mermaid(models)

    if output:
        output.write_text(mermaid_code)
        typer.echo(f"✅ Diagram written to {output}")
    else:
        typer.echo(mermaid_code)
