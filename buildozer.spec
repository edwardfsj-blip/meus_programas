[app]
title = MeuApp
package.name = meuapp
package.domain = org.meuapp

source.dir = .
source.include_exts = py,png,jpg,kv,json

version = 0.1
orientation = portrait
fullscreen = 0

# Dependências estáveis (compatível com Xiaomi)
requirements = python3==3.10.11,kivy==2.1.0,kivymd==1.1.1,cython==0.29.33,pyjnius==1.4.2

# Permissões mínimas
android.permissions = INTERNET

# Config Android
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Arquiteturas
android.archs = arm64-v8a, armeabi-v7a

# CORREÇÃO CRÍTICA PARA CRASH (GPU / Xiaomi)
android.opengl_es_version = 2


[buildozer]
log_level = 2
warn_on_root = 1