#!/bin/bash
# Geelark Device Authentication and Test Script
# 
# This script helps you authenticate with Geelark and test your device
# Device: 128.14.109.187:20624:2226cd

echo "============================================================"
echo "GEELARK DEVICE SETUP & AUTHENTICATION"
echo "============================================================"
echo ""
echo "Device Details:"
echo "  IP: 128.14.109.187"
echo "  Port: 20624"
echo "  Credential: 2226cd"
echo ""
echo "============================================================"
echo ""

# Check if glogin is installed
if ! command -v glogin &> /dev/null; then
    echo "❌ glogin is NOT installed"
    echo ""
    echo "STEP 1: Install glogin (Geelark's authentication tool)"
    echo "----------------------------------------"
    echo ""
    echo "Option A: Download from Geelark"
    echo "  Visit: https://www.geelark.com/download or your Geelark dashboard"
    echo "  Look for: 'glogin' or 'Geelark CLI tools'"
    echo ""
    echo "Option B: Request from Support"
    echo "  Contact: Geelark support"
    echo "  Request: 'glogin authentication tool for Linux'"
    echo ""
    echo "Option C: Common installation (if available)"
    echo "  wget https://geelark.com/tools/glogin-linux -O /usr/local/bin/glogin"
    echo "  chmod +x /usr/local/bin/glogin"
    echo ""
    echo "After installation, run this script again."
    echo ""
    exit 1
else
    echo "✓ glogin is installed at: $(which glogin)"
    echo ""
fi

# Check if already logged in
echo "STEP 2: Checking authentication status..."
echo "----------------------------------------"
echo ""

if glogin status &> /dev/null; then
    echo "✓ Already authenticated with Geelark"
    echo ""
else
    echo "❌ Not authenticated. Starting login process..."
    echo ""
    echo "Please enter your Geelark credentials when prompted:"
    echo ""
    
    # Run glogin (interactive)
    glogin
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Successfully authenticated!"
        echo ""
    else
        echo ""
        echo "❌ Authentication failed"
        echo ""
        echo "Troubleshooting:"
        echo "  1. Verify your Geelark account credentials"
        echo "  2. Check if your account has device access"
        echo "  3. Contact Geelark support if issues persist"
        echo ""
        exit 1
    fi
fi

# Test ADB connection
echo "STEP 3: Testing ADB connection..."
echo "----------------------------------------"
echo ""

# Ensure device is connected
adb connect 128.14.109.187:20624 &> /dev/null

# Test basic ADB command
if adb -s 128.14.109.187:20624 shell getprop ro.product.model &> /dev/null; then
    MODEL=$(adb -s 128.14.109.187:20624 shell getprop ro.product.model 2>/dev/null | tr -d '\r')
    echo "✓ ADB connection successful!"
    echo "  Device model: $MODEL"
    echo ""
else
    echo "❌ ADB connection failed"
    echo ""
    echo "Try:"
    echo "  adb disconnect 128.14.109.187:20624"
    echo "  adb connect 128.14.109.187:20624"
    echo ""
    exit 1
fi

# Test Python uiautomator2
echo "STEP 4: Testing uiautomator2 connection..."
echo "----------------------------------------"
echo ""

cd /root/bot/bot
source .venv/bin/activate

python3 << 'PYEOF'
import uiautomator2 as u2
import sys

try:
    device = u2.connect_adb_wifi("128.14.109.187:20624")
    info = device.info
    print(f"✓ uiautomator2 connected successfully!")
    print(f"  Brand: {info.get('brand', 'Unknown')}")
    print(f"  Model: {info.get('productName', 'Unknown')}")
    print(f"  Android SDK: {info.get('sdkInt', 'Unknown')}")
    print(f"  Display: {info['displayWidth']}x{info['displayHeight']}")
    print("")
    sys.exit(0)
except Exception as e:
    print(f"❌ uiautomator2 connection failed: {e}")
    print("")
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo "============================================================"
    echo "✓ ALL TESTS PASSED!"
    echo "============================================================"
    echo ""
    echo "Your Geelark device is ready for GramAddict bot!"
    echo ""
    echo "Next steps:"
    echo "  1. Ensure Instagram is installed on device"
    echo "  2. Login to Instagram manually (bot doesn't handle login)"
    echo "  3. Run: gramaddict run --config accounts/satosa1x/config.yml"
    echo ""
    echo "============================================================"
else
    echo "============================================================"
    echo "❌ SETUP INCOMPLETE"
    echo "============================================================"
    echo ""
    echo "Please resolve the errors above and try again."
    echo ""
fi
