[app]
title = Betting PRO
package.name = bettingpro
package.domain = com.bettingpro.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,ttc,json,csv
source.include_patterns = static/fonts/*.ttf,static/*.png
version = 18.0

# ✅ Чистый Python, без проблемных библиотек
requirements = python3,kivy,plyer,pillow,certifi

p4a.branch = master

orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/static/icon.png
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# ✅ ВОЗВРАЩАЕМ NDK 25b (он нужен p4a) + явно указываем ndk_api
android.api = 28
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
