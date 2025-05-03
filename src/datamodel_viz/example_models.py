from pydantic import BaseModel


class Person(BaseModel):
    id: int
    name: str
    email: str


class Company(BaseModel):
    id: int
    name: str
    employees: list[Person]
