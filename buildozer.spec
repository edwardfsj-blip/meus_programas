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

# Dependências

requirements = python3,kivy,kivymd

# Permissões Android

android.permissions = INTERNET

# Configuração Android (ESTÁVEL)

android.api = 30
android.minapi = 21
android.build_tools = 30.0.3

# Aceitar licença automaticamente

android.accept_sdk_license = True

# Evita problemas no CI

log_level = 2

[buildozer]

# Nível de log

log_level = 2
