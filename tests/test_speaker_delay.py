import builtins
from speaker_delay import interactive_speaker_delays
from constants import SPEAKER_NAMES


def test_interactive_speaker_delays(monkeypatch):
    inputs = [''] * (len(SPEAKER_NAMES) * 2)
    it = iter(inputs)
    monkeypatch.setattr(builtins, 'input', lambda _: next(it))
    monkeypatch.setattr(builtins, 'print', lambda *a, **k: None)

    delays = interactive_speaker_delays()

    assert set(delays.keys()) == set(SPEAKER_NAMES)
    assert min(delays.values()) == 0
    assert all(v == 0 for v in delays.values())