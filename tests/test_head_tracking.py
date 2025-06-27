import time
from pythonosc.udp_client import SimpleUDPClient

from tracking import HeadTracker


def test_head_tracker_updates_orientation():
    tracker = HeadTracker(port=10000)
    tracker.start()

    client = SimpleUDPClient("127.0.0.1", 10000)
    client.send_message("/yaw", 42.0)
    time.sleep(0.1)

    assert abs(tracker.yaw() - 42.0) < 1e-3
    tracker.stop()