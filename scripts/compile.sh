rm -rf app/
rm app.zip

mkdir app


cp main.py app/__main__.py
cp discover.py modify.py remote.py app/

cd app/

zip -r ../app.zip *

cd ..

rm -rf app/
