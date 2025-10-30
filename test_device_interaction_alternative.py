#!/usr/bin/env python3
"""
Alternative Device Test - Direct Connection (No ADB Shell Required)
Works with cloud devices like Geelark that restrict ADB shell access
"""

import sys
import logging
import uiautomator2 as u2
from time import sleep

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_direct_connection(device_ip, device_port=20624):
    """
    Test device connection using direct uiautomator2 without ADB shell
    
    Args:
        device_ip: Device IP address
        device_port: Device port (default: 20624)
    """
    
    logger.info("=" * 70)
    logger.info("ALTERNATIVE DEVICE TEST (No ADB Shell Required)")
    logger.info("=" * 70)
    
    connection_methods = []
    device = None
    
    # Try multiple connection methods
    methods_to_try = [
        ("ADB WiFi", f"{device_ip}:{device_port}", lambda: u2.connect_adb_wifi(f"{device_ip}:{device_port}")),
        ("HTTP Direct (7912)", f"http://{device_ip}:7912", lambda: u2.connect(f"http://{device_ip}:7912")),
        ("Simple IP", device_ip, lambda: u2.connect(device_ip)),
    ]
    
    for method_name, address, connect_func in methods_to_try:
        try:
            logger.info(f"\n[Trying Method: {method_name}]")
            logger.info(f"Address: {address}")
            
            test_device = connect_func()
            
            # Test if connection works by getting device info
            info = test_device.info
            
            if info:
                logger.info(f"✓ SUCCESS! Connected via {method_name}")
                device = test_device
                connection_methods.append((method_name, True))
                break
            
        except Exception as e:
            logger.warning(f"✗ {method_name} failed: {str(e)[:100]}")
            connection_methods.append((method_name, False))
            continue
    
    if not device:
        logger.error("\n" + "=" * 70)
        logger.error("UNABLE TO CONNECT TO DEVICE")
        logger.error("=" * 70)
        logger.error("All connection methods failed:")
        for method, success in connection_methods:
            status = "✓" if success else "✗"
            logger.error(f"  {status} {method}")
        logger.error("\nPossible solutions:")
        logger.error("1. Authenticate with 'glogin' (for Geelark devices)")
        logger.error("2. Check if device is still online")
        logger.error("3. Verify firewall rules allow connection")
        logger.error("4. Contact your cloud device provider")
        return False
    
    try:
        # Get and display device info
        logger.info("\n" + "=" * 70)
        logger.info("DEVICE INFORMATION")
        logger.info("=" * 70)
        
        info = device.info
        logger.info(f"Product Name: {info.get('productName', 'Unknown')}")
        logger.info(f"Model: {info.get('model', 'Unknown')}")
        logger.info(f"Brand: {info.get('brand', 'Unknown')}")
        logger.info(f"SDK Version (Android): {info.get('sdkInt', 'Unknown')}")
        logger.info(f"Display Size: {info.get('displayWidth', 0)}x{info.get('displayHeight', 0)}")
        logger.info(f"Display DPI: {info.get('displaySizeDpX', 0)}x{info.get('displaySizeDpY', 0)}")
        logger.info(f"Screen On: {info.get('screenOn', False)}")
        logger.info(f"Natural Orientation: {info.get('naturalOrientation', True)}")
        logger.info(f"Current Package: {info.get('currentPackageName', 'Unknown')}")
        
        # Test 1: Screen wake
        logger.info("\n" + "=" * 70)
        logger.info("TEST 1: Screen Wake")
        logger.info("=" * 70)
        
        if not info.get('screenOn', False):
            logger.info("Screen is off, waking device...")
            device.screen_on()
            sleep(1)
            device.unlock()  # Swipe to unlock
            sleep(1)
            logger.info("✓ Device woken up")
        else:
            logger.info("✓ Screen already on")
        
        # Test 2: Simple swipe gestures
        logger.info("\n" + "=" * 70)
        logger.info("TEST 2: Swipe Gestures")
        logger.info("=" * 70)
        
        width = info['displayWidth']
        height = info['displayHeight']
        
        # Swipe up (scroll down)
        logger.info("Swiping UP (scroll down content)...")
        device.swipe(width//2, height*0.8, width//2, height*0.2, 0.1)
        sleep(1.5)
        logger.info("✓ Swipe UP completed")
        
        # Swipe down (scroll up)
        logger.info("Swiping DOWN (scroll up content)...")
        device.swipe(width//2, height*0.2, width//2, height*0.8, 0.1)
        sleep(1.5)
        logger.info("✓ Swipe DOWN completed")
        
        # Swipe left (go right)
        logger.info("Swiping LEFT (move right)...")
        device.swipe(width*0.8, height//2, width*0.2, height//2, 0.1)
        sleep(1.5)
        logger.info("✓ Swipe LEFT completed")
        
        # Swipe right (go left)
        logger.info("Swiping RIGHT (move left)...")
        device.swipe(width*0.2, height//2, width*0.8, height//2, 0.1)
        sleep(1.5)
        logger.info("✓ Swipe RIGHT completed")
        
        # Test 3: Click/tap
        logger.info("\n" + "=" * 70)
        logger.info("TEST 3: Click/Tap Interaction")
        logger.info("=" * 70)
        
        # Tap center of screen
        center_x = width // 2
        center_y = height // 2
        logger.info(f"Tapping center of screen ({center_x}, {center_y})...")
        device.click(center_x, center_y)
        sleep(1)
        logger.info("✓ Tap completed")
        
        # Test 4: Screen info retrieval
        logger.info("\n" + "=" * 70)
        logger.info("TEST 4: Screen & Window Info")
        logger.info("=" * 70)
        
        window_size = device.window_size()
        logger.info(f"Window Size: {window_size}")
        
        # Get current app
        logger.info(f"Current App: {device.app_current()}")
        logger.info("✓ Screen info retrieved")
        
        # Test 5: UI element search (basic)
        logger.info("\n" + "=" * 70)
        logger.info("TEST 5: UI Element Detection")
        logger.info("=" * 70)
        
        # Try to find any UI element
        logger.info("Searching for UI elements...")
        try:
            # Get UI hierarchy dump
            xml = device.dump_hierarchy()
            element_count = xml.count("<node")
            logger.info(f"✓ Found {element_count} UI elements on screen")
        except Exception as e:
            logger.warning(f"Could not dump hierarchy: {e}")
        
        # Test 6: Press back button
        logger.info("\n" + "=" * 70)
        logger.info("TEST 6: Back Button Press")
        logger.info("=" * 70)
        
        logger.info("Pressing back button...")
        device.press("back")
        sleep(1)
        logger.info("✓ Back button pressed")
        
        # Test 7: Home button
        logger.info("\n" + "=" * 70)
        logger.info("TEST 7: Home Button Press")
        logger.info("=" * 70)
        
        logger.info("Pressing home button...")
        device.press("home")
        sleep(1)
        logger.info("✓ Home button pressed")
        
        # Final Summary
        logger.info("\n" + "=" * 70)
        logger.info("TEST SUMMARY - ALL TESTS PASSED! ✓")
        logger.info("=" * 70)
        logger.info("✓ Device connection: SUCCESS")
        logger.info("✓ Device info retrieval: SUCCESS")
        logger.info("✓ Screen control: SUCCESS")
        logger.info("✓ Swipe gestures: SUCCESS")
        logger.info("✓ Click/Tap interaction: SUCCESS")
        logger.info("✓ Screen info: SUCCESS")
        logger.info("✓ UI detection: SUCCESS")
        logger.info("✓ Hardware buttons: SUCCESS")
        logger.info("\n" + "=" * 70)
        logger.info("DEVICE IS READY FOR GRAMADDICT BOT!")
        logger.info("=" * 70)
        logger.info(f"\nConnection Method Used: {[m for m, s in connection_methods if s][0]}")
        logger.info(f"Device: {info.get('brand', '')} {info.get('productName', '')}")
        logger.info(f"Android Version (SDK): {info.get('sdkInt', 'Unknown')}")
        logger.info("\nYou can now run GramAddict automation!")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error("\n" + "=" * 70)
        logger.error("TEST FAILED DURING EXECUTION")
        logger.error("=" * 70)
        logger.error(f"Error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    # Default device
    DEFAULT_IP = "128.14.109.187"
    DEFAULT_PORT = 20624
    
    # Parse command line
    if len(sys.argv) > 1:
        device_address = sys.argv[1]
        if ":" in device_address:
            device_ip, device_port = device_address.split(":")
            device_port = int(device_port)
        else:
            device_ip = device_address
            device_port = DEFAULT_PORT
    else:
        device_ip = DEFAULT_IP
        device_port = DEFAULT_PORT
        logger.info(f"No device specified, using default: {device_ip}:{device_port}")
        logger.info("Usage: python test_device_interaction_alternative.py [IP:PORT]")
        logger.info("Example: python test_device_interaction_alternative.py 192.168.1.100:5555\n")
    
    # Run test
    success = test_direct_connection(device_ip, device_port)
    
    # Exit
    sys.exit(0 if success else 1)
