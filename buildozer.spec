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

# Tela cheia (opcional)
fullscreen = 0

# Dependências (VERSÕES COMPATÍVEIS)
requirements = python3==3.10.11,kivy==2.1.0,kivymd==1.1.1,cython==0.29.33,pyjnius==1.5.0

# Permissões Android
android.permissions = INTERNET

# Configuração Android (estável)
android.api = 30
android.minapi = 21
android.build_tools = 30.0.3

# Força versão estável do python-for-android (CRÍTICO)
p4a.branch = stable

# NDK compatível
android.ndk = 25b

# Evita backup automático
android.allow_backup = False

# Aceitar licença automaticamente
android.accept_sdk_license = True

# Log mais detalhado (ajuda debug)
log_level = 2


[buildozer]

# Log do buildozer
log_level = 2
