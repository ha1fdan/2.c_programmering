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


def test_zero_scale_succeeds_when_scale_settles_at_zero(kiosk):
    kiosk.ser.lines = [b'5.0 g\r\n', b'0.0 g\r\n']
    assert kiosk.zero_scale(timeout=2)


def test_zero_scale_fails_when_weight_stays_on_scale(kiosk):
    kiosk.ser.lines = [b'250 g\r\n'] * 20
    assert not kiosk.zero_scale(timeout=1)
