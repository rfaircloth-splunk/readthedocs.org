FROM ubuntu:latest
LABEL maintainer='\
Ryan Faircloth <rfaircloth@splunk.com>'

ENV DEBIAN_FRONTEND=noninteractive \
    APPDIR=/opt/rtfd \
    DJANGO_SETTINGS_MODULE=readthedocs.settings.container \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    RTD_REF=2.5.0

#    apt-get upgrade -y  && \
RUN apt-get -y update && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    apt-get install -y locales gettext build-essential git \
      python python-dev python-pip python-setuptools \
      libxml2-dev libxslt1-dev zlib1g-dev postgresql-client-10 \
      python3 python3-dev python3-pip python3-venv python3-setuptools \
      python3.7 python3.7-dev python3.7-venv \
      texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

COPY ["./readthedocs", "./media", "./requirements", "./django-rtd-create-users.py",  "./manage.py", "requirements.txt","./entrypoint.sh" , "/opt/rtfd/"]

# Install test dependencies
RUN pip install wheel virtualenv && \
    python3 -m pip install wheel virtualenv && \
    python3.7 -m pip install virtualenv wheel && \
    python3 -m virtualenv /venv && \
    /bin/bash -c "source /venv/bin/activate; pip install -r /opt/rtfd/requirements.txt; pip install uwsgi psycopg2 psycopg2-binary elasticsearch-dsl "

RUN adduser --gecos 'py' -u 2000 --disabled-password py && \
    mkdir /opt/rtfd/static || true && \
    mkdir /opt/rtfd/user_builds || true && \
    mkdir /opt/rtfd/logs || true && \
    touch /opt/rtfd/logs/debug.log && \
    mkdir /opt/rtfd/readthedocs/templates_custom || true && \
    chmod +x /opt/rtfd/entrypoint.sh && \
    chown -R py:py /opt/rtfd

WORKDIR /opt/rtfd
ENTRYPOINT ["/bin/bash", "-c","/opt/rtfd/entrypoint.sh"]
