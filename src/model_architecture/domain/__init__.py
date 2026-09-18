"""What the application computes.

Domain objects hold business meaning and never touch the outside world.
Anything that reaches a database, filesystem, network, or screen belongs
in ``ports`` instead.
"""

from model_architecture.domain.data_processor import DataProcessor
from model_architecture.domain.errors import DataValidationError, ModelArchitectureError
from model_architecture.domain.model import Model

__all__ = ["DataProcessor", "DataValidationError", "Model", "ModelArchitectureError"]
