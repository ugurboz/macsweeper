#!/bin/bash
set -e

APP_NAME="MacSweeper Pro"
DMG_NAME="MacSweeper_Pro_Installer.dmg"

echo "🧹 Eski derleme dosyaları temizleniyor..."
rm -rf build dist "$DMG_NAME"

echo "📦 Uygulama (Release Mode) paketleniyor. Bu biraz zaman alabilir..."
python3 setup.py py2app

echo "🔐 Apple Silicon uyumluluğu için kütüphaneler (Framework/so/dylib) imzalanıyor..."
xattr -cr "dist/$APP_NAME.app"
find "dist/$APP_NAME.app" -type f \( -name "*.dylib" -o -name "*.so" -o -name "Python" -o -name "*.framework" \) -exec codesign --force -s - {} +
codesign --force --deep --options runtime --entitlements entitlements.plist -s - "dist/$APP_NAME.app"

echo "📋 Applications kısayolu dist klasörüne ekleniyor..."
ln -s /Applications dist/Applications

echo "💿 DMG dosyası oluşturuluyor..."
hdiutil create -volname "$APP_NAME Installer" -srcfolder dist -ov -format UDZO "$DMG_NAME"

echo "🧹 Applications kısayolu dist içerisinden kaldırılıyor..."
rm dist/Applications

echo "✅ Tamamlandı! $DMG_NAME dosyası proje klasörünüzde hazır."
