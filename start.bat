#!/bin/bash

# Setze den Pfad zur Python-Umgebung
ENV_PATH="./env/"

# Überprüfe, ob das Verzeichnis existiert
if [ ! -d "$ENV_PATH" ]; then
    echo "Das Umgebungsverzeichnis existiert nicht: $ENV_PATH"
    exit 1
fi

# Starte main.py mit der angegebenen Umgebung
"$ENV_PATH/Scripts/python" main.py