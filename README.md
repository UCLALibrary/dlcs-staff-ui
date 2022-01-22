# DLCS Staff UI

This is the new staff user interface to the Oral History project in the UCLA DLCS.  It may
be used with other DLCS projects.
It's a temporary application, intended for use until content can be migrated to a new backend.

This system is built using the Django framework.

## Developer Information

The development environment requires:
* git
* docker (current version recommended: 20.10.12)
* docker-compose (at least version 1.25.0; current recommended: 1.29.2)

The development database is Oracle XE 18.4.0, which is closest to UCLA ITS Oracle 19c.
The Oracle docker container comes from https://hub.docker.com/r/gvenzl/oracle-xe ; more info
via the [creator's blog](https://geraldonit.com/2021/08/15/oracle-xe-docker-images/).

#### Oracle container

This is large: 1.6 GB download, 2.9 GB uncompressed.  The database is persisted
to a docker volume, which requires another 2.6 GB.

#### Django container

This uses Django 4, which requires Python 3.8 or later; the container uses Python 3.9.
It shouldn't matter if Python 3.9 is used locally, as all code runs in the container.

The container runs via `docker_scripts/entrypoint.sh`, which
* Updates container with any new requirements, if the image hasn't been rebuilt (DEV environment only).
* Waits for the database to be completely available.  This can take 10-60 seconds, depending on your hardware and the Oracle gods.
* Applies any pending migrations (DEV environment only).
* Creates a generic Django superuser, if one does not already exist (DEV environment only).
* Starts the Django application server.

### Setup
1. Clone the repository.

   ```$ git clone git@github.com:UCLALibrary/dlcs-staff-ui.git```

2. Change directory into the project.

   ```$ cd dlcs-staff-ui```

3. Build using docker-compose.

   ```$ docker-compose build```

4. Bring the system up, with containers running in the background.

   ```$ docker-compose up -d```

5. Logs can be viewed, if needed (`-f` to tail logs).

   ```
   $ docker-compose logs -f db
   $ docker-compose logs -f django
   ```

6. Run commands in the containers, if needed.

   ```
   $ docker-compose exec db sqlplus
   $ docker-compose exec django bash
   # Django-aware Python shell
   $ docker-compose exec django python manage.py shell
   # Apply new migrations without a restart
   $ docker-compose exec django python manage.py migrate
   ```
7. Connect to the running application via browser

   [Application](http://127.0.0.1:8000) and [Admin](http://127.0.0.1:8000/admin)

8. Edit code locally.  All changes are immediately available in the running container, but if a restart is needed:

   ```$ docker-compose restart django```

9. Shut down the system when done.

   ```$ docker-compose down```
