#!/bin/bash
#
# GEELARK GLOGIN - ACTUAL WORKING METHOD
# =======================================
# Based on your discovery: adb shell glogin <credential>
#

set -e

DEVICE_IP="128.14.109.187"
DEVICE_PORT="21398"
CREDENTIAL="526020"
DEVICE_ADDRESS="${DEVICE_IP}:${DEVICE_PORT}"

echo "============================================================"
echo "GEELARK AUTHENTICATION - GLOGIN METHOD"
echo "============================================================"
echo ""
echo "Device: $DEVICE_ADDRESS"
echo "Credential: $CREDENTIAL"
echo ""
echo "Using method: adb -s <device> shell glogin <credential>"
echo ""
echo "============================================================"
echo ""

# Step 1: Connect via ADB
echo "[Step 1] Connecting to device via ADB..."
adb connect $DEVICE_ADDRESS

if [ $? -ne 0 ]; then
    echo "✗ Failed to connect"
    exit 1
fi

echo "✓ Connected to $DEVICE_ADDRESS"
echo ""

# Step 2: Run glogin via ADB shell
echo "[Step 2] Authenticating with glogin..."
echo "Running: adb -s $DEVICE_ADDRESS shell glogin $CREDENTIAL"
echo ""

adb -s $DEVICE_ADDRESS shell glogin $CREDENTIAL

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "✓ AUTHENTICATION SUCCESSFUL!"
    echo "============================================================"
    echo ""
    echo "Device is now authenticated and ready to use."
    echo ""
    
    # Test the connection
    echo "[Step 3] Testing device access..."
    echo ""
    
    MODEL=$(adb -s $DEVICE_ADDRESS shell getprop ro.product.model 2>&1)
    
    if echo "$MODEL" | grep -q "error.*glogin"; then
        echo "✗ Still getting glogin error"
        echo "  The credential might be incorrect or expired"
        echo ""
        exit 1
    else
        echo "✓ Device model: $MODEL"
        echo "✓ ADB shell access is working!"
        echo ""
        
        # Get more device info
        echo "[Step 4] Getting device information..."
        echo ""
        BRAND=$(adb -s $DEVICE_ADDRESS shell getprop ro.product.brand 2>&1 | tr -d '\r')
        ANDROID=$(adb -s $DEVICE_ADDRESS shell getprop ro.build.version.release 2>&1 | tr -d '\r')
        
        echo "Device Information:"
        echo "  Brand: $BRAND"
        echo "  Model: $MODEL"
        echo "  Android: $ANDROID"
        echo "  Address: $DEVICE_ADDRESS"
        echo ""
        
        echo "============================================================"
        echo "✓✓✓ SUCCESS! DEVICE IS READY! ✓✓✓"
        echo "============================================================"
        echo ""
        echo "Now you can:"
        echo "  1. Run the device test script:"
        echo "     python3 test_device_simple.py $DEVICE_ADDRESS"
        echo ""
        echo "  2. Or test with Python directly:"
        echo "     cd /root/bot/bot"
        echo "     source .venv/bin/activate"
        echo "     python3 -c 'import uiautomator2 as u2; d=u2.connect_adb_wifi(\"$DEVICE_ADDRESS\"); print(d.info)'"
        echo ""
        echo "  3. Run GramAddict bot:"
        echo "     python3 -m GramAddict run --config accounts/psy8s/config.yml"
        echo ""
        echo "============================================================"
        echo ""
        
        # Save authentication info
        echo "$DEVICE_ADDRESS authenticated at $(date)" > /root/bot/bot/.geelark_authenticated
        echo "✓ Authentication status saved"
        echo ""
        
        exit 0
    fi
else
    echo ""
    echo "============================================================"
    echo "✗ AUTHENTICATION FAILED"
    echo "============================================================"
    echo ""
    echo "Possible issues:"
    echo "  1. Credential '$CREDENTIAL' is incorrect"
    echo "  2. Credential has expired"
    echo "  3. Device is offline or unavailable"
    echo "  4. Different authentication method required"
    echo ""
    echo "Try:"
    echo "  - Check credential in GeeLark dashboard"
    echo "  - Verify device is online"
    echo "  - Contact GeeLark support"
    echo ""
    exit 1
fi
