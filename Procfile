# Create a Procfile
echo "web: gunicorn app:server" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy to Heroku
heroku create your-app-name
git push heroku main
