[app]
title = MeuApp
package.name = meuapp
package.domain = org.meuapp
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 0.1
orientation = portrait
fullscreen = 0

# Ajustado para maior compatibilidade
requirements = python3,kivy==2.1.0,kivymd==1.1.1,cython==0.29.36,pyjnius==1.4.2

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
