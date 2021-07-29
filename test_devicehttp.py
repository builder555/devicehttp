import requests
import threading
import pytest
from unittest.mock import MagicMock
from devicehttp import DeviceHTTPWrapper
from time import sleep

class TestHTTPDeviceAdaptor:

    def test_can_read_pin_state(self, fake_device, port):
        fake_device.is_on = True
        resp = requests.get(f'http://localhost:{port}')
        assert resp.status_code == 200
        assert resp.json().get('output') == True
        fake_device.is_on = False
        resp = requests.get(f'http://localhost:{port}')
        assert resp.json().get('output') == False

    def test_writing_TRUE_turns_the_device_ON(self, fake_device, port):
        resp = requests.post(f'http://localhost:{port}/', json={'on': True})
        assert resp.status_code == 200
        assert fake_device.start.called

    def test_writing_FALSE_turns_the_device_OFF(self, fake_device, port):
        resp = requests.post(f'http://localhost:{port}/', json={'on': False})
        assert resp.status_code == 200
        assert fake_device.stop.called

    def test_writing_NO_DATA_results_in_error_400(self, fake_device, port):
        resp = requests.post(f'http://localhost:{port}/')
        assert resp.status_code == 400
        assert not fake_device.start.called

    def test_writing_WRONG_DATA_results_in_error_400(self, fake_device, port):
        resp = requests.post(f'http://localhost:{port}/', json={'maybe': True})
        assert resp.status_code == 400
        assert not fake_device.start.called

@pytest.fixture(autouse=True, scope='module')
def start_server(port, fake_device):
    server = DeviceHTTPWrapper(device=fake_device, http_port=port)
    thread = threading.Thread(target=server.start)
    thread.start()
    yield
    server.shutdown()

@pytest.fixture(scope='module')
def port():
    return 8800

@pytest.fixture(scope='module')
def fake_device():
    fake_device = MagicMock()
    fake_device.is_on = False
    fake_device.start = MagicMock()
    fake_device.stop = MagicMock()
    yield fake_device

@pytest.fixture(autouse=True)
def reset_fake_device(fake_device):
    fake_device.is_on = False
    fake_device.start = MagicMock()
    fake_device.stop = MagicMock()
