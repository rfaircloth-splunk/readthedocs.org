FROM python:3.7-stretch
LABEL maintainer='\
Ryan Faircloth <rfaircloth@splunk.com>'

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8

RUN apt-get update && \
    apt-get install -y && \
    pip3 install uwsgi && \
    apt-get install -y locales gettext build-essential git \
            libxml2-dev libxslt1-dev zlib1g-dev postgresql-client \
            texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra && \
   rm -rf /var/lib/apt/lists/*


COPY ./requirements/ /opt/app/readthedocs/requirements
RUN pip3 install -r /opt/app/readthedocs/requirements/pip.txt && \
    pip3 install -r /opt/app/readthedocs/requirements/local-docs-build.txt && \
    pip3 install -r /opt/app/readthedocs/requirements/deploy.txt
COPY ./readthedocs/ /opt/app/readthedocs/
COPY ./media/ /opt/app/media/

ENV DEBIAN_FRONTEND=noninteractive \
     APPDIR=/opt/app/readthedocs \
     DJANGO_SETTINGS_MODULE=readthedocs.settings.container

COPY ["entrypoint.sh","uwsgi.ini","setup.py","setup.cfg","manage.py","tasks.py","django-rtd-create-users.py","/opt/app/"]
RUN cd /opt/app/ && \
    mkdir -p /opt/app/logs && \
    mkdir -p /opt/app/user_builds && \
    mkdir -p /opt/app/templates_custom && \
    python manage.py makemessages --all && \
    python manage.py compilemessages && \
    python manage.py collectstatic --no-input

RUN adduser --gecos 'py' -u 2000 --disabled-password py && \
  chown -R py:py /opt/app

EXPOSE 8000
USER py
ENTRYPOINT ["/bin/bash", "-c","/opt/app/entrypoint.sh"]
