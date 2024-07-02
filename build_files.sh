pip install -r requirements.txt
python3.x manage.py collectstatic --no-input --clear
chmod +x build_files.sh
python manage.py migrate