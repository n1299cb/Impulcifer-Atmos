from typing import Dict

from constants import SPEAKER_NAMES
from utils import versus_distance


def interactive_speaker_delays(default_distance: float = 3.0,
                                default_angle: float = 0.0) -> Dict[str, float]:
    """Prompt for angle and distance per speaker and return delay table.

    The delay for the nearest speaker is normalised to zero.
    """
    print("Enter angle and distance for each speaker (press Enter for defaults).")
    delays = {}
    for sp in SPEAKER_NAMES:
        angle_str = input(f"{sp} angle [{default_angle} deg]: ")
        dist_str = input(f"{sp} distance [{default_distance} m]: ")
        angle = float(angle_str) if angle_str.strip() else default_angle
        distance = float(dist_str) if dist_str.strip() else default_distance
        _, delay, _ = versus_distance(angle=abs(angle), distance=distance, ear='primary')
        delays[sp] = delay

    min_delay = min(delays.values())
    for sp in delays:
        delays[sp] -= min_delay

    return delays