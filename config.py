# This file is part of Earprint, a modified version of Impulcifer.
# Original code © 2018 Jaakko Pasanen — licensed under the MIT License.
# Modifications © 2025 Blaring Sound LLC — also licensed under the MIT License unless otherwise stated.
#
# This file may include integrated or rewritten components from the original project.
# For details on changes and authorship, see the project README or CHANGELOG.

from dataclasses import dataclass


@dataclass
class ProcessingConfig:
    """Feature flags controlling processing behaviour."""

    apply_diffuse_field_compensation: bool = False
    apply_headphone_eq: bool = True
    apply_x_curve_compensation: bool = False
    x_curve_type: str = "minus3db_oct"
    apply_room_correction: bool = False
    preserve_room_response: bool = True

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


settings = ProcessingConfig()
