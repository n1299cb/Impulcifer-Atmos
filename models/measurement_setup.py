from dataclasses import dataclass


@dataclass
class MeasurementSetup:
    """Data model representing measurement setup configuration."""

    test_signal: str = ""
    measurement_dir: str = ""