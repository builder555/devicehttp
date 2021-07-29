### HTTP Wrapper around an I/O device


_Usage - reading_


```python
from piinput import SensorAdaptor
from devicehttp import DeviceHTTPWrapper
sensor = SensorAdaptor(pin=3)
http_server = DeviceHTTPWrapper(device=sensor, http_port=8000)
http_server.start()
```

```bash
$ curl http://localhost:8000
{"output": false}
```

_Usage - writing_

```python
from pioutput import MotorAdaptor
from devicehttp import DeviceHTTPWrapper
motor = MotorAdaptor(pin=3)
http_server = DeviceHTTPWrapper(device=motor, http_port=8000)
http_server.start()
```

```bash
$ curl -X POST http://localhost:8000 -h 'Content-Type: application/json' -d '{"on": true}'
```