"""Errors that callers can handle without depending on an adapter."""


class ModelArchitectureError(Exception):
    """Base error for expected pipeline failures."""


class DataValidationError(ModelArchitectureError):
    """Raised when raw data cannot be converted into valid model input."""
