import os
from dataclasses import dataclass
from typing import List

@dataclass
class MeasurementSetupViewModel:
    """ViewModel for validating measurement setup paths."""

    def validate_paths(self, test_signal: str, measurement_dir: str) -> List[str]:
        """Return list of field names that failed validation."""
        errors = []
        if not os.path.isfile(test_signal):
            errors.append("test_signal")
        if not os.path.isdir(measurement_dir):
            errors.append("measurement_dir")
        return errors