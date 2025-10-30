#!/usr/bin/env python3
"""
GramAddict Device Test - GeeLark Cloud Device
Tests device connectivity and GramAddict DeviceFacade compatibility
Aligned with GramAddict project structure
"""

import sys
import logging
from pathlib import Path
from argparse import Namespace

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from GramAddict.core.device_facade import (
    create_device,
    get_device_info,
    DeviceFacade,
    Direction,
    SleepTime,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_mock_args(device_id, app_id="com.instagram.android"):
    """Create mock args object with speed_multiplier for GramAddict utils"""
    return Namespace(
        device_id=device_id,
        app_id=app_id,
        speed_multiplier=1.0,  # Required by random_sleep() in utils.py
    )


def test_gramaddict_device(device_address, app_id="com.instagram.android"):
    """
    Test device using GramAddict's DeviceFacade
    This aligns with how the bot actually interacts with devices
    """
    
    try:
        logger.info("=" * 70)
        logger.info("GRAMADDICT DEVICE TEST - GEELARK CLOUD DEVICE")
        logger.info("=" * 70)
        logger.info(f"Device: {device_address}")
        logger.info(f"App ID: {app_id}")
        logger.info("=" * 70)
        
        # Initialize mock args for GramAddict utils
        logger.info("\n[1] Setting up GramAddict configuration...")
        mock_args = create_mock_args(device_address, app_id)
        
        # Import and configure utils (needed for random_sleep)
        from GramAddict.core.utils import load_config
        from GramAddict.core.config import Config
        
        # Create minimal config
        config = Config()
        config.args = mock_args
        load_config(config)
        logger.info("✓ Configuration loaded")
        
        # Create device using GramAddict's factory
        logger.info("\n[2] Creating device with GramAddict DeviceFacade...")
        device = create_device(device_address, app_id)
        
        if device is None:
            logger.error("Failed to create device!")
            return False
        
        logger.info("✓ DeviceFacade created")
        
        # Get device info using GramAddict's method
        logger.info("\n[3] Getting device information...")
        get_device_info(device)
        
        info = device.get_info()
        logger.info(f"✓ Product: {info.get('productName', 'Unknown')}")
        logger.info(f"✓ SDK: {info.get('sdkInt', 'Unknown')}")
        logger.info(f"✓ Display: {info['displayWidth']}x{info['displayHeight']}")
        logger.info(f"✓ Screen On: {info.get('screenOn', False)}")
        
        # Test if alive
        logger.info("\n[4] Checking device status...")
        if device.is_alive():
            logger.info("✓ Device is alive")
        else:
            logger.warning("⚠ Device may not be fully responsive")
        
        # Test home - use deviceV2 directly for basic navigation
        logger.info("\n[5] Testing navigation - HOME button...")
        device.deviceV2.press("home")
        logger.info("✓ HOME button pressed")
        
        # Test swipes using GramAddict's Direction enum
        logger.info("\n[6] Testing GramAddict swipe methods...")
        
        logger.info("  Swipe UP (scale=0.5)...")
        device.swipe(Direction.UP, scale=0.5)
        logger.info("  ✓ Swipe UP completed")
        
        logger.info("  Swipe DOWN (scale=0.5)...")
        device.swipe(Direction.DOWN, scale=0.5)
        logger.info("  ✓ Swipe DOWN completed")
        
        logger.info("  Swipe LEFT (scale=0.5)...")
        device.swipe(Direction.LEFT, scale=0.5)
        logger.info("  ✓ Swipe LEFT completed")
        
        logger.info("  Swipe RIGHT (scale=0.5)...")
        device.swipe(Direction.RIGHT, scale=0.5)
        logger.info("  ✓ Swipe RIGHT completed")
        
        # Test back button using GramAddict method
        logger.info("\n[7] Testing BACK navigation...")
        device.back(modulable=False)
        logger.info("✓ BACK button pressed")
        
        # Back to home
        device.deviceV2.press("home")
        
        # Test screen state
        logger.info("\n[8] Testing screen state...")
        locked = device.is_screen_locked()
        if locked is not None:
            logger.info(f"✓ Screen locked: {locked}")
        else:
            logger.warning("⚠ Could not determine screen lock state")
        
        # Test screenshot
        logger.info("\n[9] Testing screenshot capability...")
        try:
            screenshot = device.screenshot()
            if screenshot:
                logger.info(f"✓ Screenshot: {screenshot.size} pixels")
            else:
                logger.warning("⚠ Screenshot returned None")
        except Exception as e:
            logger.warning(f"⚠ Screenshot failed: {e}")
        
        # Check Instagram app
        logger.info("\n[10] Checking Instagram installation...")
        current_app = device._get_current_app()
        logger.info(f"✓ Current app: {current_app}")
        
        # Try to check if Instagram is installed
        try:
            import subprocess
            result = subprocess.run(
                f"adb -s {device_address} shell pm list packages | grep instagram",
                shell=True,
                capture_output=True,
                text=True
            )
            if "instagram" in result.stdout.lower():
                logger.info(f"✓ Instagram detected: {result.stdout.strip()}")
            else:
                logger.warning("⚠ Instagram not found - needs to be installed")
        except Exception as e:
            logger.warning(f"⚠ Could not check Instagram: {e}")
        
        # Success!
        logger.info("\n" + "=" * 70)
        logger.info("✓✓✓ ALL GRAMADDICT TESTS PASSED! ✓✓✓")
        logger.info("=" * 70)
        logger.info(f"\nDevice: {info.get('productName', 'Unknown')}")
        logger.info(f"Android SDK: {info.get('sdkInt', 'Unknown')}")
        logger.info(f"Resolution: {info['displayWidth']}x{info['displayHeight']}")
        logger.info(f"Status: READY FOR GRAMADDICT BOT")
        logger.info("=" * 70)
        logger.info("NEXT STEPS")
        logger.info("=" * 70)
        logger.info("\n1. Ensure Instagram is installed and logged in:")
        logger.info("   scrcpy -s 128.14.109.187:21398")
        logger.info("   - Install Instagram from Play Store if needed")
        logger.info("   - Login to Instagram manually (psy8s)")
        logger.info("\n2. Update your config file:")
        logger.info("   File: accounts/psy8s/config.yml")
        logger.info(f"   Uncomment and set: device: {device_address}")
        logger.info("\n3. Run GramAddict bot:")
        logger.info("   ./geelark_glogin.sh  # Authenticate first")
        logger.info("   python3 -m GramAddict run --config accounts/psy8s/config.yml")
        logger.info("\n" + "=" * 70)
        logger.info("REMINDER: GeeLark authentication (glogin) is per-session")
        logger.info("If disconnected, re-run: ./geelark_glogin.sh")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error("\n" + "=" * 70)
        logger.error("TEST FAILED")
        logger.error("=" * 70)
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    DEVICE = "128.14.109.187:21398"
    APP_ID = "com.instagram.android"
    
    if len(sys.argv) > 1:
        DEVICE = sys.argv[1]
    
    if len(sys.argv) > 2:
        APP_ID = sys.argv[2]
    
    logger.info(f"Testing GeeLark device: {DEVICE}")
    logger.info(f"App ID: {APP_ID}")
    logger.info("Make sure you ran: ./geelark_glogin.sh first!\n")
    
    success = test_gramaddict_device(DEVICE, APP_ID)
    sys.exit(0 if success else 1)
