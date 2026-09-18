"""How the application connects to the outside world.

Each port is a contract the application depends on and an adapter fulfils.
Ports face outward; ``domain`` contracts face inward.
"""

from model_architecture.ports.data_source import DataSource
from model_architecture.ports.output_renderer import OutputRenderer

__all__ = ["DataSource", "OutputRenderer"]
