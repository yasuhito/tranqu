from tranqu.device_type_manager import DeviceTypeManager


class DummyDevice:
    """Dummy device class for testing"""


class TestDeviceTypeManager:
    def setup_method(self):
        self.manager = DeviceTypeManager()

    def test_register_type(self):
        self.manager.register_type("dummy", DummyDevice)
        device = DummyDevice()

        result = self.manager.detect_lib(device)

        assert result == "dummy"

    def test_detect_lib_returns_none_for_unregistered_type(self):
        device = DummyDevice()

        result = self.manager.detect_lib(device)

        assert result is None

    def test_detect_lib_with_multiple_registrations(self):
        class AnotherDummyDevice:
            pass

        self.manager.register_type("dummy1", DummyDevice)
        self.manager.register_type("dummy2", AnotherDummyDevice)

        device1 = DummyDevice()
        device2 = AnotherDummyDevice()

        assert self.manager.detect_lib(device1) == "dummy1"
        assert self.manager.detect_lib(device2) == "dummy2"

    def test_register_type_multiple_times(self):
        self.manager.register_type("dummy", DummyDevice)
        self.manager.register_type("another_dummy", DummyDevice)

        device = DummyDevice()

        # The last registered library identifier is returned
        assert self.manager.detect_lib(device) == "another_dummy"
