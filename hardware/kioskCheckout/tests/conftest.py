import sys
import types
from pathlib import Path

import pytest
import serial
from serial.tools import list_ports

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


class FakeSerial:
    """Stands in for the scale: readline() returns queued lines, then b''."""

    def __init__(self, **kwargs):
        self.lines = []

    def readline(self):
        return self.lines.pop(0) if self.lines else b''


@pytest.fixture
def kiosk(tmp_path, monkeypatch):
    """Import main with a fake scale and run inside an empty temp dir (so kiosk.db is a fresh file)."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(list_ports, 'comports',
                        lambda: [types.SimpleNamespace(device='/dev/fake', description='FT230X Basic UART')])
    monkeypatch.setattr(serial, 'Serial', FakeSerial)
    monkeypatch.setattr('add_item.DB_PATH', 'kiosk.db')
    monkeypatch.delenv('KIOSK_ADMIN_PASSWORD', raising=False)
    sys.modules.pop('main', None)
    import main
    main.app.config['TESTING'] = True
    main.ADMIN_PASSWORD = None
    yield main
    sys.modules.pop('main', None)


@pytest.fixture
def client(kiosk):
    return kiosk.app.test_client()


@pytest.fixture
def cola():
    return {'name': 'Cola', 'category': 'drinks', 'price': 15, 'weight_g': 532, 'tolerance_g': 5, 'stock': 10}
