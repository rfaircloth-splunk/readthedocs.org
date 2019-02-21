#!/bin/bash
set -e

source /venv/bin/activate
cd /opt/rtfd

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "database" -U "$POSTGRES_USER" --dbname $POSTGRES_DB -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing commands"

echo "Migrating (provisioning) the database..."
python manage.py migrate

if [ ! -e /opt/rtfd/readthedocs/rtd-provisioned ]; then

    echo "Building RTD's locale files..."
    python manage.py makemessages --all
    python manage.py compilemessages

    echo "Creating users..."
    python manage.py shell < /opt/rtfd/bin/django-rtd-create-users.py || true

    echo "Generating static assets..."
    python manage.py collectstatic --no-input


    #if [ "$RTD_HAS_ELASTICSEARCH" == "true" ]; then
    #    echo "Provisioning Elasticsearch..."
    #    python manage.py provision_elasticsearch
    #fi

    touch /opt/rtfd/readthedocs/rtd-provisioned
fi

if [ "$RTD_HAS_ELASTICSEARCH" == "true" ]; then
    echo "Reindexing Elasticsearch..."


    until curl http://elasticsearch:9200/_cat/health; do
      >&2 echo "elasticsearch is unavailable - sleeping"
      sleep 1
    done

    python manage.py reindex_elasticsearch
fi

>&2 echo "Starting runserver"
#python manage.py runserver 0.0.0.0:8000
gunicorn -w 3 --forwarded-allow-ips="*" -b "0.0.0.0:8000" readthedocs.wsgi 
