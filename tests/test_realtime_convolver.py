import numpy as np
from realtime_convolution import RealTimeConvolver


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
