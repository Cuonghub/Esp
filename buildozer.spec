[app]
title = Enemy Detector
package.name = enemydetector
package.domain = com.enemy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,opencv-python,numpy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.gradle_dependencies = 'org.tensorflow:tensorflow-lite:2.14.0'
