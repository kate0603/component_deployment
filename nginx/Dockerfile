FROM nginx:1.21.0

ENV TZ=Asia/Shanghai

# 日志分区配置
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y --no-install-recommends logrotate

COPY ./nginx /etc/logrotate.d/

# 反代理配置
#COPY ./nginx.conf /etc/nginx/nginx.conf
# 如果不删除默认文件default.conf, 则必须覆盖
COPY ./config /etc/nginx/conf.d

# 开启ngin 和 调度
RUN echo "0 1 * * * root /usr/sbin/logrotate -f /etc/logrotate.d/nginx > /var/log/cron.log 2>&1" >> /etc/crontab

COPY start_nginx.sh /start_nginx.sh
CMD ["/bin/bash", "/start_nginx.sh"]

