README:

Install dependencies on Kali:

pip install pycryptodome

Setup environment:

  - Download and unzip .zip file with source code

  - Open main.py and change Global Variables.

  - Run "scripts/compile.sh"

  - Run "scripts/setup.sh"

  - Run code with "python app.zip" (note: at the end of the execution a popup will be displayed and script deleted)

Program Usage:

To encrypt:

  - root@kali# python app.zip

To decrypt:

  - root@kali# python app.zip -d [key]
