[app]
title = MeuApp
package.name = meuapp
package.domain = org.meuapp
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 0.1
orientation = portrait
fullscreen = 0

requirements = python3==3.10.11,kivy==2.2.1,kivymd==1.1.1,cython==0.29.33,pyjnius==1.5.0

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
