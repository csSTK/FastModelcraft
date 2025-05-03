import re
from typing import (
    Dict,
    List,
    Type,
    TypeVar,
    Iterable,
    Any,
)

from sqlalchemy import Column, inspect as sa_inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql.sqltypes import (
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Float,
    Text,
    BigInteger,
    SmallInteger,
    Numeric,
    JSON,
    ARRAY,
    TypeEngine,
)

# Type variable for SQLAlchemy models
SQLAlchemyModel = TypeVar("SQLAlchemyModel")


def get_type_hint(column_type: TypeEngine[Any]) -> str:
    """
    Convert SQLAlchemy column type to Python type hint.

    Args:
        column_type: SQLAlchemy type engine instance

    Returns:
        str: Corresponding Python type hint as a string
    """
    type_map: Dict[Type[TypeEngine[Any]], str] = {
        Integer: "int",
        SmallInteger: "int",
        BigInteger: "int",
        Float: "float",
        Numeric: "float",
        String: "str",
        Text: "str",
        Boolean: "bool",
        Date: "date",
        DateTime: "datetime",
        JSON: "Dict[str, Any]",
    }

    # Check for array types
    if isinstance(column_type, ARRAY):
        inner_type: str = get_type_hint(column_type.item_type)
        return f"List[{inner_type}]"

    for sa_type, py_type in type_map.items():
        if isinstance(column_type, sa_type):
            return py_type

    # Default to Any for unknown types
    return "Any"


def sqlalchemy_to_pydantic(model: Type[SQLAlchemyModel]) -> str:
    """
    Convert a SQLAlchemy model to Pydantic model code.

    Args:
        model: SQLAlchemy model class

    Returns:
        str: Python code for the equivalent Pydantic model
    """
    try:
        model_name: str = model.__name__
        pydantic_model_name: str = f"{model_name}Model"

        # Get table columns
        inspector: Inspector = sa_inspect(model)
        columns: Iterable[Column] = inspector.columns

        lines: List[str] = [f"class {pydantic_model_name}(BaseModel):"]

        # Add docstring
        if model.__doc__:
            doc: str = re.sub(r"\s+", " ", model.__doc__.strip())
            lines.append(f'    """{doc}"""')

        # Add fields
        for column in columns:
            type_hint: str = get_type_hint(column.type)

            # Handle nullable columns
            if column.nullable:
                type_hint = f"Optional[{type_hint}]"

            field_kwargs: List[str] = []

            # Add Field constraints
            if column.default is not None:
                field_kwargs.append(f"default={repr(column.default.arg)}")
            elif column.nullable:
                field_kwargs.append("default=None")

            if getattr(column, "comment", None):
                field_kwargs.append(f"description={repr(column.comment)}")

            field_str: str = f"{column.name}: {type_hint}"
            if field_kwargs:
                field_str += f" = Field({', '.join(field_kwargs)})"

            lines.append(f"    {field_str}")

        # Add Config class for ORM mode
        lines.extend(["", "    class Config:", "        from_attributes = True"])

        return "\n".join(lines)
    except Exception as e:
        return f"# Error converting {model.__name__}: {str(e)}\n"


def alembic_to_pydantic(models: List[Type[SQLAlchemyModel]]) -> str:
    """
    Convert multiple SQLAlchemy models to Pydantic models.

    Args:
        models: List of SQLAlchemy model classes

    Returns:
        str: Python code containing all the Pydantic model definitions
    """

    result: str = ""

    for model in models:
        result += sqlalchemy_to_pydantic(model) + "\n\n\n"

    return result


if __name__ == "__main__":
    # Example usage:
    # from src.schema_mapper.example_models import User

    # pydantic_code: str = alembic_to_pydantic([User])
    # with open("pydantic_models.py", "w") as f:
    #     f.write(pydantic_code)
    pass
