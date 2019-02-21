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

RUN apt-get -y update && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    apt-get upgrade -y  && \
    apt-get install -y locales gettext && \
    apt-get install -y build-essential git && \
    apt-get install -y python python-dev python-pip python-setuptools && \
    apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev postgresql-client-10 && \
    apt-get install -y python3 python3-dev python3-pip python3-venv python3-setuptools && \
    apt-get install -y python3.7 python3.7-dev python3.7-venv && \
    apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/supervisor

# Install test dependencies
RUN pip install wheel virtualenv

# Install test dependencies
RUN python3 -m pip install wheel virtualenv && \
    python3.7 -m pip install virtualenv wheel && \
    python3 -m virtualenv /venv

COPY . /opt/rtfd
COPY settings/* /opt/rtfd/readthedocs/settings/
COPY bin/* /opt/rtfd/bin/

RUN /bin/bash -c "source /venv/bin/activate; pip install -r /opt/rtfd/requirements.txt; pip install gunicorn psycopg2 psycopg2-binary elasticsearch-dsl "

COPY entrypoint.sh /opt/rtfd/bin/
RUN adduser --gecos 'py' --disabled-password py && \
    mkdir /opt/rtfd/static && \
    mkdir /opt/rtfd/user_builds && \
    mkdir /opt/rtfd/templates && \
    chmod +x /opt/rtfd/bin/* && \
    chown -R py /opt/rtfd/readthedocs

WORKDIR /opt/rtfd
ENTRYPOINT ["/bin/bash", "-c","/opt/rtfd/bin/entrypoint.sh"]
