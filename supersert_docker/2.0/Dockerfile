FROM apache/superset:2-0
# 启动时执行
ENTRYPOINT ["sh", "-c", "superset fab create-admin \
              --username admin \
              --firstname admin \
              --lastname admin \
              --email 1021907330@qq.com \
              --password admin &&\
              superset db upgrade && \
              superset init && \
              sh -c /usr/bin/run-server.sh"]
