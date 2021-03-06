#!/bin/bash
set -e

#source /venv/bin/activate
cd /opt/app

until PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "$DB_USER" --port=$DB_PORT --dbname $DB_NAME -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing commands"

echo "Migrating (provisioning) the database..."
python manage.py migrate

if [ ! -e /opt/rtfd/readthedocs/rtd-provisioned ]; then

    # echo "Building RTD's locale files..."
    # python manage.py makemessages --all
    # python manage.py compilemessages

    echo "Creating users..."
    python manage.py shell < /opt/app/django-rtd-create-users.py || true

#    echo "Generating static assets..."
#    python manage.py collectstatic --no-input


    #if [ "$RTD_HAS_ELASTICSEARCH" == "true" ]; then
    #    echo "Provisioning Elasticsearch..."
    #    python manage.py provision_elasticsearch
    #fi

    touch /opt/app/readthedocs/rtd-provisioned
fi

if [ "$RTD_HAS_ELASTICSEARCH" == "true" ]; then
    echo "Reindexing Elasticsearch..."


    until curl http://elasticsearch:9200/_cat/health; do
      >&2 echo "elasticsearch is unavailable - sleeping"
      sleep 1
    done

    python manage.py reindex_elasticsearch
fi

>&2 echo "Starting server"
uwsgi --ini /opt/app/uwsgi.ini
