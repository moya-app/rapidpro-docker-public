Easy RapidPro environment spin-up

Based on the official docs and https://riseuplabs.com/rapidpro-installation-guide/

# Install

Look over rapidpro.env, docker-compose/rapidpro/conf/settings.py and docker-compose.yml to handle any setup.

To start the stack, just run:

    docker-compose up -d --build

Browse to port 80 and if you see an nginx 'Bad Gateway' page just wait a bit
and hit refresh - database configuration is being set up. You can see progress with:

    docker-compose logs -f rapidpro

Then create a superuser:

    docker-compose exec rapidpro poetry run python manage.py createsuperuser

Navigate to http://<server>/users/user/ to manage users

# Updating theme styling

    docker-compose stop redis; docker-compose rm -f redis; docker-compose up -d redis
    docker-compose exec rapidpro poetry run python manage.py collectstatic --no-input

# DB access

    docker-compose exec db psql rapidpro rapidpro

# TODO

- Abstract out standard configuration variables (such as `example.com` as the server name)
