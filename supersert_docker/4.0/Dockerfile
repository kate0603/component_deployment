FROM apache/superset:4.0.0

USER root

COPY superset_config.py /app/pythonpath/superset_config.py
RUN chown superset:superset /app/pythonpath/superset_config.py
RUN chmod +x /app/pythonpath/superset_config.py

COPY --chown=superset ./docker-bootstrap.sh /app/docker/
COPY --chown=superset ./docker-init.sh /app/docker/
COPY --chown=superset ./docker-ci.sh /app/docker/
COPY --chown=superset ./docker-ci.sh /app/docker/
RUN chmod a+x /app/docker/*.sh

USER superset:superset

CMD /app/docker/docker-ci.sh