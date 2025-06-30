import numpy as np
from realtime_convolution import RealTimeConvolver
from impulse_response import ImpulseResponse
from hrir import HRIR
from crosstalk import compute_crosstalk_filters


def test_convolver_interpolates_between_angles():
    brirs = {
        (0.0, 0.0, 0.0): (np.array([1.0]), np.array([0.0])),
        (90.0, 0.0, 0.0): (np.array([0.0]), np.array([1.0])),
    }
    engine = RealTimeConvolver(brirs, samplerate=48000, block_size=2)
    engine.set_orientation(45.0)
    block = np.zeros((2, 2))
    block[0, 0] = 1.0
    block[1, 0] = 1.0
    out = engine.process_block(block)
    assert out.shape == (2, 2)
    assert abs(out[0, 0] - 0.5) < 1e-6
    assert abs(out[1, 0] - 0.5) < 1e-6


def test_convolver_uses_all_angles():
    brirs = {
        0.0: (np.array([1.0]), np.array([0.0])),
        90.0: (np.array([0.0]), np.array([1.0])),
        180.0: (np.array([0.5]), np.array([0.5])),
    }
    engine = RealTimeConvolver(brirs, samplerate=48000, block_size=2)
    engine.set_orientation(45.0)
    block = np.zeros((2, 2))
    block[0, 0] = 1.0
    block[1, 0] = 1.0
    out = engine.process_block(block)

    dists = np.array([45.0, 45.0, 135.0])
    inv = 1 / dists
    weights = inv / inv.sum()
    expected_left = weights[0] * 1.0 + weights[2] * 0.5
    expected_right = weights[1] * 1.0 + weights[2] * 0.5

    assert abs(out[0, 0] - expected_left) < 1e-6
    assert abs(out[1, 0] - expected_right) < 1e-6


def test_convolver_wraps_yaw_angles():
    brirs = {
        0.0: (np.array([1.0]), np.array([0.0])),
        90.0: (np.array([0.0]), np.array([1.0])),
    }
    engine = RealTimeConvolver(brirs, samplerate=48000, block_size=2)
    engine.set_orientation(350.0)
    block = np.zeros((2, 2))
    block[0, 0] = 1.0
    block[1, 0] = 1.0
    out = engine.process_block(block)

    d0 = engine._angular_distance(0.0, 350.0)
    d1 = engine._angular_distance(90.0, 350.0)
    inv = np.array([1 / d0, 1 / d1])
    weights = inv / inv.sum()

    assert abs(out[0, 0] - weights[0]) < 1e-6
    assert abs(out[1, 0] - weights[1]) < 1e-6


def test_crosstalk_cancellation():
    estimator = type("_e", (), {"fs": 48000})()
    hrir = HRIR(estimator)
    hrir.irs["FL"] = {
        "left": ImpulseResponse(np.array([1.0]), 48000),
        "right": ImpulseResponse(np.array([0.5]), 48000),
    }
    hrir.irs["FR"] = {
        "left": ImpulseResponse(np.array([0.5]), 48000),
        "right": ImpulseResponse(np.array([1.0]), 48000),
    }
    filters = compute_crosstalk_filters(hrir, "FL", "FR", length=2, regularization=0.0)
    engine = RealTimeConvolver(hrir, block_size=2, cross_talk_filters=filters)
    block = np.zeros((2, 2))
    block[0, 0] = 1.0
    out = engine.process_block(block)
    # Physical loudspeaker crosstalk matrix
    H = np.array([[1.0, 0.5], [0.5, 1.0]])
    final_ears = H @ out[:, 0]
    # Should reproduce the binaural signal produced by the virtualizer
    assert np.allclose(final_ears, [1.0, 0.5], atol=1e-6)