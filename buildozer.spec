[app]
title = MeuApp
package.name = meuapp
package.domain = org.meuapp
version = 0.1
orientation = portrait
source.dir = .
source.include_exts = py,png,jpg,kv,json

requirements = python3,kivy,kivymd

# 👇 importante para KivyMD
android.permissions = INTERNET

# 👇 deixe padrão seguro
android.api = 31
android.minapi = 21

# 👇 isso ajuda no CI
log_level = 2
