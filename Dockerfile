FROM python:3.9-slim-bullseye

# Debian repository management
RUN apt-get update && apt-get install -y software-properties-common \
    && apt-add-repository non-free && apt-get update

# Set correct timezone
RUN ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

# Install Oracle client; thanks to https://stackoverflow.com/a/59869379
WORKDIR /opt/oracle
RUN apt-get install -y libaio1 wget unzip \
    && wget -q https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
    && unzip instantclient-basiclite-linuxx64.zip \
    && rm -f instantclient-basiclite-linuxx64.zip \
    && cd /opt/oracle/instantclient* \
    && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci \
    && echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig

# Install derivative processing programs from repo,
# along with java, which jhove requires but the package doesn't install?
RUN apt-get install -y default-jdk ffmpeg imagemagick jhove

# Create django user and switch context to that user
RUN useradd -c "django app user" -d /home/django -s /bin/bash -m django
USER django

# Switch to application directory
WORKDIR /home/django/dlcs-staff-ui

# Copy application files to image, and ensure django user owns everything
COPY --chown=django:django . .

# Include local python bin into django user's path, mostly for pip
ENV PATH /home/django/.local/bin:${PATH}

# Make sure pip is up to date, and don't complain if it isn't yet
RUN pip install --upgrade pip --disable-pip-version-check

# Install requirements for this application
RUN pip install --no-cache-dir -r requirements.txt --user --no-warn-script-location

# Expose the typical Django port
EXPOSE 8000

# For now, use the built-in Django application server when the container starts
#CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
CMD [ "sh", "docker_scripts/entrypoint.sh" ]
