import os
import sys
import numpy as np
import pytest

# Allow importing modules from repository root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from impulcifer import main
from hrir import HRIR
from impulse_response_estimator import ImpulseResponseEstimator

TEST_DIR = "data/test_capture"
SPEAKERS_916 = [
    "FL", "FR", "FC", "SL", "SR", "BL", "BR", "WL", "WR",
    "TFL", "TFR", "TSL", "TSR", "TBL", "TBR",
]

@pytest.mark.skipif(not os.path.isdir(TEST_DIR), reason="test data missing")
def test_impulcifer_916_pipeline(tmp_path):
    hrir_files = [f for f in os.listdir(TEST_DIR) if f.lower().endswith(".wav")]
    if not hrir_files:
        pytest.skip("No HRIR WAV files found")
    main(
        dir_path=TEST_DIR,
        plot=False,
        do_room_correction=False,
        do_headphone_compensation=True,
        do_equalization=False,
        test_signal=None,
        channel_balance="avg",
        fs=None,
    )
    output_path = os.path.join(TEST_DIR, "responses.wav")
    assert os.path.exists(output_path)
    estimator = ImpulseResponseEstimator(fs=48000)
    hrir = HRIR(estimator)
    hrir.open_recording(output_path, speakers=SPEAKERS_916[:len(hrir.irs)])
    for speaker, pair in hrir.irs.items():
        assert np.max(pair["left"].data) >= 0
        assert np.max(pair["right"].data) >= 0


@pytest.mark.skipif(not os.path.isdir(TEST_DIR), reason="test data missing")
def test_x_curve_options(tmp_path):
    hrir_files = [f for f in os.listdir(TEST_DIR) if f.lower().endswith(".wav")]
    if not hrir_files:
        pytest.skip("No HRIR WAV files found")
    main(
        dir_path=TEST_DIR,
        plot=False,
        do_room_correction=False,
        do_headphone_compensation=True,
        do_equalization=False,
        test_signal=None,
        channel_balance="avg",
        fs=None,
        apply_x_curve=True,
        x_curve_type="minus3db_oct",
    )
    main(
        dir_path=TEST_DIR,
        plot=False,
        do_room_correction=False,
        do_headphone_compensation=True,
        do_equalization=False,
        test_signal=None,
        channel_balance="avg",
        fs=None,
        remove_x_curve=True,
        x_curve_in_capture=True,
        x_curve_type="minus1p5db_oct",
    )
    assert os.path.exists(os.path.join(TEST_DIR, "responses.wav"))