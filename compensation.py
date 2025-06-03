# -*- coding: utf-8 -*-

from autoeq.frequency_response import FrequencyResponse
from constants import APPLY_DIFFUSE_FIELD_COMPENSATION

def diffuse_field_compensation(hrir):
    """
    Apply diffuse-field compensation to HRIR.

    This modifies each impulse response in-place using the AutoEQ diffuse-field target.

    Args:
        hrir: HRIR instance containing impulse responses to be compensated.
    """
    if not APPLY_DIFFUSE_FIELD_COMPENSATION:
        return

    for speaker, pair in hrir.irs.items():
        for side, ir in pair.items():
            fr = ir.frequency_response()
            fr.diffuse_field_compensation()
            fir = fr.minimum_phase_impulse_response(fs=hrir.fs)
            ir.equalize(fir)