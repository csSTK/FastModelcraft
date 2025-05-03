# FastModelcraft - Tools for visualising and modelling data structures

## Overview

This repository contains tools for visualising data models and converting CSV files into Pydantic models. It offers two main functions:

1. **Schema Mapper** - Converts CSV files to Pydantic models.
2. **DataModel Viz** - Visualises Pydantic models and SQLAlchemy database models. -- SQLAlchemy will be added in a future version

## Installation

### Dependencies

To use the tools, make sure you have Python 3.x and pdm installed. The following packages are also required:

- `typer` for CLI
- `pydantic` for modelling
- `sqlalchemy` for SQLAlchemy integration

Install the required packages with:

```bash
pdm install --frozen-lock
```

The `pdm.lock` file contains all the necessary dependencies:

```
typer==0.7.0
pydantic==1.8.2
sqlalchemy==1.4.23
```

## Usage

### Schema Mapper (CSV to Pydantic-Modell)

The **Schema Mapper** converts a CSV file into a Pydantic model. You can use the following command:

```bash
python -m schema_mapper <CSV_FILE> --model-name <MODEL_NAME> --output <OUTPUT_FILE>
```

#### Optionen:

- `<CSV_FILE>`: The path to the CSV file to be converted.
- `--model-name` or `-m`: The name of the Pydantic model to be generated (optional, default: `AutoModel`).
- `--output` or `-o`: The path under which the generated model is to be saved (optional).

Example:

```bash
python -m schema_mapper src/schema_mapper/example.csv --model-name UserModel --output data/user_model.py
```

### DataModel Viz (Visualisation of data models)

The **DataModel Viz** command creates a visualisation of Pydantic and SQLAlchemy data models as a diagram. You can create the diagram with the following command:

```bash
python -m datamodel_viz <MODEL_FILE> --output <OUTPUT_PATH>
```

#### Optionen:

- `<MODEL_FILE>`: The path to the file containing the model (e.g. `person_model.py`).
- `--output` oder `-o`: The path under which the output file is to be saved (optional, default: `datamodel.svg`).

Beispiel:

```bash
python -m datamodel_viz src/datamodel_viz/example_models.py --output diagram.mmd
```

### Generate mermaid diagram

Once you have created the mermaid diagram, you can convert it into an SVG or PNG image format using the `mermaid-cli` library.

### Container-based (recommended)

Problems may occur when using `mermaid-cli`. Therefore, I recommend running it in a Docker container. Make sure Docker is installed on your system and run the following command:

```bash
sudo chmod -R 777 $(pwd)
sudo docker run --rm -v $(pwd):/data minlag/mermaid-cli -i diagram.mmd -o diagram.svg
```

This creates the diagram directly from the `.mmd` file and saves it as `.svg`.

### Alternative with `mermaid-cli`:

#### Installation of the Mermaid CLI:

```bash
npm install -g @mermaid-js/mermaid-cli
```

#### Generate diagram:

```bash
mmdc -i diagram.mmd -o diagram.svg
```

## LICENSE

This project is licensed under the MIT licence. Further details can be found in the [LICENSE](LICENSE) file.
