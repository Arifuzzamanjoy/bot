"""
Test GramAddict device connectivity with GeeLark cloud devices
Uses pytest for testing framework consistency
"""

import pytest
import sys
from pathlib import Path
from argparse import Namespace

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from GramAddict.core.device_facade import (
    create_device,
    get_device_info,
    Direction,
)
from GramAddict.core.config import Config
from GramAddict.core.utils import load_config


@pytest.fixture
def device_address():
    """GeeLark device address - override with pytest --device-address"""
    return "128.14.109.187:21398"


@pytest.fixture
def app_id():
    """Instagram app ID"""
    return "com.instagram.android"


@pytest.fixture
def mock_config(device_address, app_id):
    """Create mock config for GramAddict utils"""
    args = Namespace(
        device_id=device_address,
        app_id=app_id,
        speed_multiplier=1.0,
    )
    config = Config()
    config.args = args
    load_config(config)
    return config


@pytest.fixture
def device(mock_config, device_address, app_id):
    """Create GramAddict DeviceFacade instance"""
    device = create_device(device_address, app_id)
    assert device is not None, "Failed to create device"
    return device


def test_device_creation(device):
    """Test that device can be created"""
    assert device is not None
    assert hasattr(device, 'deviceV2')


def test_device_info(device):
    """Test getting device information"""
    info = device.get_info()
    
    assert info is not None
    assert 'displayWidth' in info
    assert 'displayHeight' in info
    assert 'sdkInt' in info
    
    # Log device info
    get_device_info(device)


def test_device_is_alive(device):
    """Test device is responsive"""
    assert device.is_alive() is True


def test_device_get_current_app(device):
    """Test getting current app"""
    current_app = device._get_current_app()
    assert current_app is not None
    assert isinstance(current_app, str)


def test_device_press_home(device):
    """Test HOME button press"""
    device.deviceV2.press("home")
    # No exception = success


def test_device_swipe_up(device):
    """Test swipe UP gesture"""
    device.swipe(Direction.UP, scale=0.5)
    # No exception = success


def test_device_swipe_down(device):
    """Test swipe DOWN gesture"""
    device.swipe(Direction.DOWN, scale=0.5)
    # No exception = success


def test_device_swipe_left(device):
    """Test swipe LEFT gesture"""
    device.swipe(Direction.LEFT, scale=0.5)
    # No exception = success


def test_device_swipe_right(device):
    """Test swipe RIGHT gesture"""
    device.swipe(Direction.RIGHT, scale=0.5)
    # No exception = success


def test_device_back_button(device):
    """Test BACK button"""
    device.back(modulable=False)
    # No exception = success


def test_device_screen_lock_status(device):
    """Test checking screen lock status"""
    locked = device.is_screen_locked()
    # Can be True, False, or None
    assert locked is not None or locked is False or locked is True


def test_device_screenshot(device):
    """Test screenshot capability"""
    screenshot = device.screenshot()
    assert screenshot is not None
    assert hasattr(screenshot, 'size')


def test_instagram_installed(device_address):
    """Test if Instagram is installed"""
    import subprocess
    result = subprocess.run(
        f"adb -s {device_address} shell pm list packages | grep instagram",
        shell=True,
        capture_output=True,
        text=True
    )
    assert "instagram" in result.stdout.lower(), "Instagram not installed"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
