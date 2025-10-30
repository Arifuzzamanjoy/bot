#!/bin/bash
#
# Instagram Downgrade Helper for GramAddict
# Helps you downgrade Instagram to a compatible version
#

set -e

DEVICE="128.14.109.187:21398"
RECOMMENDED_VERSION="260.0.0.23.115"
CURRENT_VERSION="404.0.0.48.76"

echo "================================================================"
echo "INSTAGRAM DOWNGRADE HELPER"
echo "================================================================"
echo ""
echo "Current Instagram: $CURRENT_VERSION (TOO NEW)"
echo "Recommended: $RECOMMENDED_VERSION (TESTED & WORKING)"
echo "Device: $DEVICE"
echo ""
echo "================================================================"
echo ""

# Check if APK file exists
APK_FILE=""
for file in instagram-*.apk Instagram-*.apk; do
    if [ -f "$file" ]; then
        APK_FILE="$file"
        break
    fi
done

if [ -z "$APK_FILE" ]; then
    echo "❌ No Instagram APK found in current directory"
    echo ""
    echo "STEP 1: Download Instagram APK"
    echo "================================"
    echo ""
    echo "Option A: APKMirror (Recommended)"
    echo "  1. Visit: https://www.apkmirror.com/apk/instagram/instagram-instagram/"
    echo "  2. Find version: $RECOMMENDED_VERSION"
    echo "  3. Download the APK"
    echo "  4. Transfer to this directory: $(pwd)"
    echo ""
    echo "Option B: APKPure"
    echo "  1. Visit: https://apkpure.com/instagram/com.instagram.android/versions"
    echo "  2. Find version: $RECOMMENDED_VERSION"
    echo "  3. Download the APK"
    echo "  4. Transfer to this directory: $(pwd)"
    echo ""
    echo "Option C: Direct download (if available)"
    echo "  wget 'https://www.apkmirror.com/...' -O instagram-$RECOMMENDED_VERSION.apk"
    echo ""
    echo "After downloading, run this script again."
    echo ""
    exit 1
fi

echo "✓ Found APK: $APK_FILE"
echo ""
echo "================================================================"
echo "INSTALLATION STEPS"
echo "================================================================"
echo ""

# Step 1: Authenticate
echo "STEP 1: Authenticate with GeeLark"
echo "----------------------------------"
read -p "Press ENTER to authenticate with GeeLark device..." 
./geelark_glogin.sh || {
    echo "❌ Authentication failed"
    exit 1
}

echo ""
echo "✓ Device authenticated"
echo ""

# Step 2: Backup (optional)
echo "STEP 2: Backup current Instagram data (OPTIONAL)"
echo "------------------------------------------------"
echo "This will backup your Instagram app data (login session, etc.)"
echo ""
read -p "Do you want to backup? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating backup..."
    adb -s $DEVICE backup -f instagram_backup_$(date +%Y%m%d).ab com.instagram.android
    echo "✓ Backup saved as instagram_backup_$(date +%Y%m%d).ab"
    echo ""
else
    echo "Skipping backup"
    echo ""
fi

# Step 3: Uninstall current version
echo "STEP 3: Uninstall current Instagram"
echo "------------------------------------"
echo "⚠️  WARNING: This will remove Instagram $CURRENT_VERSION"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled"
    exit 0
fi

echo "Uninstalling Instagram..."
adb -s $DEVICE uninstall com.instagram.android || {
    echo "❌ Failed to uninstall. Instagram may not be installed."
}

echo "✓ Instagram uninstalled"
echo ""

# Step 4: Install old version
echo "STEP 4: Install Instagram $RECOMMENDED_VERSION"
echo "-----------------------------------------------"
echo "Installing APK: $APK_FILE"
echo ""

adb -s $DEVICE install "$APK_FILE" || {
    echo "❌ Installation failed"
    echo ""
    echo "Common issues:"
    echo "  - APK is corrupted"
    echo "  - Wrong Android version compatibility"
    echo "  - Insufficient storage on device"
    echo ""
    exit 1
}

echo ""
echo "✓ Instagram $RECOMMENDED_VERSION installed successfully!"
echo ""

# Step 5: Verify installation
echo "STEP 5: Verify installation"
echo "----------------------------"
NEW_VERSION=$(adb -s $DEVICE shell dumpsys package com.instagram.android | grep versionName | head -1 | awk '{print $1}' | cut -d= -f2)
echo "Installed version: $NEW_VERSION"
echo ""

if [ -z "$NEW_VERSION" ]; then
    echo "❌ Could not verify installation"
    exit 1
fi

echo "✓ Instagram installed and verified"
echo ""

# Final instructions
echo "================================================================"
echo "✅ INSTALLATION COMPLETE!"
echo "================================================================"
echo ""
echo "Instagram has been downgraded to: $NEW_VERSION"
echo ""
echo "NEXT STEPS:"
echo "================================================================"
echo ""
echo "1. Open Instagram on device:"
echo "   - Use: scrcpy -s $DEVICE"
echo "   - Or open via GeeLark interface"
echo ""
echo "2. Login to Instagram:"
echo "   - Username: psy8s"
echo "   - Password: (your password)"
echo "   - Complete any 2FA/verification"
echo ""
echo "3. IMPORTANT: Disable auto-updates"
echo "   - Open Play Store on device"
echo "   - Search 'Instagram'"
echo "   - Tap 3 dots (⋮)"
echo "   - Uncheck 'Enable auto-update'"
echo "   - This prevents Instagram from updating automatically"
echo ""
echo "4. Update GramAddict config:"
echo "   nano accounts/psy8s/config.yml"
echo "   Set: allow-untested-ig-version: true"
echo ""
echo "5. Test the bot:"
echo "   ./geelark_glogin.sh"
echo "   source .venv/bin/activate"
echo "   python3 -m GramAddict run --config accounts/psy8s/config.yml"
echo ""
echo "================================================================"
echo ""
echo "If you need to restore your backup later:"
echo "  adb -s $DEVICE restore instagram_backup_YYYYMMDD.ab"
echo ""
echo "================================================================"
