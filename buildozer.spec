[app]
title = Betting PRO
package.name = bettingpro
package.domain = com.bettingpro.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,ttc,json,csv
source.include_patterns = static/fonts/*.ttf,static/*.png
version = 18.0

# ✅ Только необходимое, чтобы не перегружать память сервера
requirements = python3,kivy,certifi

p4a.branch = master

orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/static/icon.png
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# ✅ Правильная связка: NDK 25b + ndk_api 21
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
