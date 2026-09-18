"""Interfaces between the application and external adapters."""

from model_architecture.ports.data_repo import DataRepo
from model_architecture.ports.output import Output

__all__ = ["DataRepo", "Output"]
