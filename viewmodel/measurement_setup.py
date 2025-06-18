import os
from dataclasses import dataclass, field
from typing import List, Optional

from models.measurement_setup import MeasurementSetup

@dataclass
class MeasurementSetupViewModel:
    """ViewModel for managing measurement setup state and validation."""

    setup: MeasurementSetup = field(default_factory=MeasurementSetup)

    def update(self, test_signal: Optional[str] = None, measurement_dir: Optional[str] = None) -> None:
        """Update underlying setup model with new values."""
        if test_signal is not None:
            self.setup.test_signal = test_signal
        if measurement_dir is not None:
            self.setup.measurement_dir = measurement_dir

    def validate_paths(self, test_signal: Optional[str] = None, measurement_dir: Optional[str] = None) -> List[str]:
        """Validate the provided paths or current model state and return invalid field names."""
        if test_signal is not None or measurement_dir is not None:
            self.update(test_signal, measurement_dir)

        errors = []
        if not os.path.isfile(self.setup.test_signal):
            errors.append("test_signal")
        if not os.path.isdir(self.setup.measurement_dir):
            errors.append("measurement_dir")
        return errors