import numpy as np
import soundfile as sf
from constants import HEXADECAGONAL_TRACK_ORDER
from viewmodel.crosstalk import CrosstalkViewModel


def test_crosstalk_vm_compute_and_save(tmp_path):
    data = np.zeros((1, len(HEXADECAGONAL_TRACK_ORDER)))
    data[0, 0] = 1.0   # FL-left
    data[0, 1] = 0.5   # FL-right
    data[0, 2] = 0.5   # FR-left
    data[0, 3] = 1.0   # FR-right
    wav_path = tmp_path / "hrir.wav"
    sf.write(wav_path, data, 48000, subtype="PCM_32")

    vm = CrosstalkViewModel()
    out_path = tmp_path / "filters.npz"
    filters = vm.compute_filters(str(wav_path), out_file=str(out_path), length=2, regularization=0.0)

    data = np.load(out_path)
    for key in ("LL", "LR", "RL", "RR"):
        assert key in data
        assert np.allclose(data[key], filters[key])

