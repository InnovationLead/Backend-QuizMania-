FROM python:3.11 as base
# set enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# create user to avoid containers as root in production
RUN addgroup --system web \
    && adduser --system --ingroup web web
# install os-level dependency as root
RUN apt-get update && apt-get install -y -q --no-install-recommends \
    # dependencies for building python packages 
    build-essential \
    # postgres client (psycopg2) dependencies
    libpq-dev \
    # cleaning up unused file to reduce image size
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*
# switch to non-root user
USER web
# Create a directory for the source code and use it as base path
WORKDIR /home/web/code
# copy python dependencies list for pip
COPY --chown=web:web ./requirements/base.txt requirements/base.txt
# switch to root user temporary, to grant execution permission
USER root
# Install python packages at system level
RUN pip install --no-cache-dir -r requirements/base.txt
# copy entrypoint script which waits for the db to be ready
COPY --chown=web:web ./docker/app/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

USER web

# This script will run before every command executed in the container
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

# RUN if [ -f "./app/docker/app/entrypoint.sh" ]; then \
#         echo "Source path exists"; \
#     else \
#         echo "Source path does not exist"; \
#         echo $(pwd); \
#         echo $(ls /usr/local/bin); \
#         echo $(ls -l /usr/local/bin/entrypoint.sh); \
#         exit 1; \
#     fi

# Define image for the local development. Inherits common packages from the base stage
FROM base as dev
# copy the scripts that starts development server (runserver) 
COPY --chown=web:web ./docker/app/start-dev-server.sh /usr/local/bin/start-dev-server.sh
USER root
RUN chmod +x /usr/local/bin/start-dev-server.sh
USER web
# dev server starts by default when container starts
CMD ["start-dev-server.sh"]

# define the base image for production. Inherits common packages from the base stage.
FROM base as prod
# Install extra packages required at production
USER root
COPY --chown=web:web ./requirements/prod.txt requirements/prod.txt
RUN pip install --no-cache-dir -r requirements/prod.txt
# Copy the script that starts the production application server (gunicorn)
COPY --chown=web:web ./docker/app/start-prod-server.sh /usr/local/bin/start-prod-server.sh
RUN chmod +x /usr/local/bin/start-prod-server.sh
USER web
# Copy the source code of our django app to the working directoy
COPY --chown=web:web . ./
# The production server starts by default when the container starts
CMD ["start-prod-server.sh"]