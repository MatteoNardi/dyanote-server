# Server update istructions

Backup database:

  heroku pgbackups:capture

Update:

  git push heroku

Check at http://dyanote.herokuapp.com/admin/

Migrate db:

  heroku run python manage.py migrate api