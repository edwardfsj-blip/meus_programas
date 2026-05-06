[app]

title = MeuApp

package.name = meuapp
package.domain = org.meuapp

version = 0.1

orientation = portrait

source.dir = .

source.include_exts = py,png,jpg,kv,json

fullscreen = 0

requirements = python3==3.10.11,kivy==2.1.0,kivymd==1.1.1,cython==0.29.33,pyjnius==1.4.2

android.permissions = INTERNET

android.api = 30
android.minapi = 21

android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = False

android.accept_sdk_license = True

log_level = 2


[buildozer]

log_level = 2
