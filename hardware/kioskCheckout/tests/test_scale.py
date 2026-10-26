import pytest


@pytest.mark.parametrize('line, expected', [
    (b'  541 g  \r\n', 541.0),
    (b'541.5 g\r\n', 541.5),
    (b'0.0 g\r\n', 0.0),
    (b'-3.0 g\r\n', -3.0),
    (b'1.25 kg\r\n', 1250.0),
    (b'\x00  12 g\r\n', 12.0),
])
def test_valid_readings_are_returned_in_grams(kiosk, line, expected):
    kiosk.ser.lines = [line]
    assert kiosk.read_weight() == expected


@pytest.mark.parametrize('line', [
    b'',            # timeout
    b'\r\n',
    b'   \r\n',
    b'g   \r\n',    # fragment
    b'541\r\n',     # no unit
    b'g ? \r\n',    # unstable marker
    b'541 g ?\r\n',
    b'ES\r\n',      # scale error
    b'\x00\n',
])
def test_garbage_is_ignored(kiosk, line):
    kiosk.ser.lines = [line]
    assert kiosk.read_weight() is None
