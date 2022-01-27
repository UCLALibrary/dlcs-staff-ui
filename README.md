# DLCS Staff UI

## Purpose

This is the new staff user interface to the Oral History project in the UCLA DLCS.  It may
be used with other DLCS projects.
It's a temporary application, intended for use until content can be migrated to a new backend.

## Developer Information

### Overview of environment

The development environment requires:
* git
* docker (current version recommended: 20.10.12)
* docker-compose (at least version 1.25.0; current recommended: 1.29.2)

#### Oracle container

The development database is Oracle XE 18.4.0, which is closest to UCLA ITS Oracle 19c.
The Oracle docker container comes from https://hub.docker.com/r/gvenzl/oracle-xe ; more info
via the [creator's blog](https://geraldonit.com/2021/08/15/oracle-xe-docker-images/).

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

### Working with remote databases

Development uses the Oracle docker container mentioned above, running locally.  However, there are times
when developers may need to connect to the real test / production Oracle databases, in the context of the 
running Django container.

This is currently a somewhat manual process, to be improved once secure secret management is in place.

**WARNING: FOR NOW, DO THIS ONLY FOR DATABASE INTROSPECTION**

#### Via allowed host

If running the system on a host which is on the "allowed IP" list to access the remote databases:
```
# Bring the system up, if not already
$ docker-compose up -d

# Open a shell in the Django container
$ docker-compose exec django bash

# Either source a file with these variables, or directly set them via the command line,
# using appropriate values.
# If using a file, keep it out of the git repo by including "secret" or "password" in the filename.
DJANGO_DB_DSN=remote_database_domain:1521/remote_oracle_service_name
DJANGO_DB_USER=remote_username
DJANGO_DB_PASS=remote_password

# Inspect the remote database using Django's management command
# Full schema
$ python manage.py inspectdb > dump_models.py
# Selected tables
$ python manage.py inspectdb table1 table2 table3 etc > dump_models.py

# When done, if the system will remain up, point Django back at the local development database
$ source .docker-compose_django.env
```

#### Via ssh tunnel

If running the system on a host not on the "allowed IP" list, first set up a tunnel through the jump server,
which does have an allowed IP address.

This opens a tunnel through the jump server, passing connections to host port 1599 via jump to remote_database_domain port 1521.
Run this in a separate terminal window; it remains active until killed with `ctrl-c`.
* `-NT` tells ssh not to create a TTY or to run any commands on connection
* `-L` defines this as a local port forwarding
* `0.0.0.0:1599` tells ssh to forward **all** interfaces - needed for docker container to access the tunnel
* `remote_database_domain` is the domain name of the remote database server
* `1521` is the port the remote database server is listening on for Oracle db connections
* `jump` is from local `.ssh/config` file.  If not using that, replace it with the appropriate `user@jump_domain:jump_port`
```
$ ssh -NT -L 0.0.0.0:1599:remote_database_domain:1521 jump
```

Once the ssh tunnel is established, follow the same steps as in the `Via allowed host` section above, except tunneling
requires a different DSN for database connection (remote user and password are the same with both methods):
```
# host.docker.internal is a "magic" docker domain which allows docker to connect to host network resources
DJANGO_DB_DSN=host.docker.internal:1599/remote_oracle_service_name
DJANGO_DB_USER=remote_username
DJANGO_DB_PASS=remote_password
```
