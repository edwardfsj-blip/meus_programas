[app]

# Nome do app
title = MeuApp

# Identificação do pacote
package.name = meuapp
package.domain = org.meuapp

# Versão do app
version = 0.1

# Orientação
orientation = portrait

# Pasta do código
source.dir = .

# Tipos de arquivos incluídos
source.include_exts = py,png,jpg,kv,json

# Dependências (VERSÕES ESTÁVEIS)
requirements = python3==3.10.11,kivy==2.1.0,kivymd==1.1.1,cython==0.29.33,pyjnius==1.3.0

# Permissões Android
android.permissions = INTERNET

# Configuração Android
android.api = 31
android.minapi = 21

# Aceitar licença automaticamente
android.accept_sdk_license = True

# 🔥 IMPORTANTE (corrige bug de build/cache)
android.allow_backup = False


[buildozer]

log_level = 2
