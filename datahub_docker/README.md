# component_deployment
组件部署
cd /opt/datahub_docker/zookeeper/
docker-compose build
docker-compose -f docker-compose-dev.yml up

查看log
docker-compose logs zookeeper

docker inspect  elasticsearch


some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres:latest tail -f /dev/null
此命令将在后台运行 Postgres 容器，并使用  tail -f /dev/null  命令启动容器。这将防止容器在完成启动任务后退出。这种方法适用于在容器中运行常驻服务（如数据库）的情况。

command: tail -f /dev/null

zk访问需在同一个网络下
同一主机：
networks:
  default:
    name: datahub_network_new

## zookeeper
创建挂载路径
mkdir

1. 使用 telnet 命令测试：
   在命令行窗口中输入以下命令以测试 ZooKeeper 是否成功连接：
telnet localhost 21811
如果成功连接则会返回以下输出：
Trying 127.0.0.1...
   Connected to localhost.
   Escape character is '^]'.
如果连接失败则会返回以下输出：
Trying 127.0.0.1...
   telnet: Unable to connect to remote host: Connection refused


## broker
1. 创建一个主题：
docker-compose exec broker kafka-topics --bootstrap-server localhost:29092 --create --topic my-topic --partitions 1 --replication-factor 1
2. 启动一个消费者：
docker-compose exec broker kafka-console-consumer --bootstrap-server localhost:29092 --topic my-topic --from-beginning
3. 启动一个生产者并发送消息：
docker-compose exec broker bash -c "echo 'hello world' | kafka-console-producer --broker-list localhost:29092 --topic my-topic > /dev/null"
4. 在消费者终端查看是否收到了消息。
   如果提示消费者已经订阅了主题并且能够收到消息，那么 DataHub Broker 部署成功并且能够正常工作。

常见问题
service "broker" is not running container #1
检查zk是否连接成功 docker-compose logs broker
```
Attaching to kafka-setup
kafka-setup  | DATAHUB_PRECREATE_TOPICS=false
kafka-setup  | Pre-creation of topics has been turned off, exiting
kafka-setup exited with code 0
```

## schema-registry
要测试 Schema-Registry 是否已经成功部署，您可以执行以下步骤：
1. 确定 Docker 容器已启动：
   docker ps
这将显示在 Docker 中启动的所有容器的列表。
2. 确定 Schema-Registry 容器的 IP 地址：
docker inspect <schema-registry-container-name>
在输出中找到  IPAddress  字段，这是 Schema-Registry 容器的 IP 地址。
3. 使用 curl 命令测试 Schema-Registry：
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
     --data '{"schema": "{\"type\":\"string\"}"}' \
     http://<schema-registry-ip-address>:8081/subjects/test/versions
这将向 Schema-Registry 发送一个简单的测试请求。
4. 检查响应是否返回200 OK：
curl -s -o /dev/null -w "%{http_code}" \
     http://<schema-registry-ip-address>:8081/subjects/test/versions
如果成功部署了 Schema-Registry，则应返回200 OK。
如果以上步骤都已成功执行，则可以确认您已成功在 Docker 中部署了 Schema-Registry。

## mariadb
测试：客户端工具连接数据库查看
常见问题
init.sql可不执行，因为在setup中会执行


/docker-entrypoint-initdb.d/init.sql: Permission denied
改为在容器内执行

init.sql未执行：docker-entrypoint-initdb.d 文件夹只会在创建(实例化)容器时运行一次，因此您实际上必须执行 docker-compose up -d --force-recreate

```
Attaching to mysql-setup
mysql-setup  | 2023/05/17 07:04:28 Waiting for: tcp://mariadb:3306
mysql-setup  | 2023/05/17 07:04:28 Connected to tcp://mariadb:3306
mysql-setup  | -- create datahub database
mysql-setup  | CREATE DATABASE IF NOT EXISTS datahub CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
mysql-setup  | USE datahub;
mysql-setup  |
mysql-setup  | -- create metadata aspect table
mysql-setup  | create table if not exists metadata_aspect_v2 (
mysql-setup  |   urn                           varchar(500) not null,
mysql-setup  |   aspect                        varchar(200) not null,
mysql-setup  |   version                       bigint(20) not null,
mysql-setup  |   metadata                      longtext not null,
mysql-setup  |   systemmetadata                longtext,
mysql-setup  |   createdon                     datetime(6) not null,
mysql-setup  |   createdby                     varchar(255) not null,
mysql-setup  |   createdfor                    varchar(255),
mysql-setup  |   constraint pk_metadata_aspect_v2 primary key (urn,aspect,version),
mysql-setup  |   INDEX timeIndex (createdon)
mysql-setup  | );
mysql-setup  |
mysql-setup  | -- create default records for datahub user if not exists
mysql-setup  | DROP TABLE if exists temp_metadata_aspect_v2;
mysql-setup  | CREATE TABLE temp_metadata_aspect_v2 LIKE metadata_aspect_v2;
mysql-setup  | INSERT INTO temp_metadata_aspect_v2 (urn, aspect, version, metadata, createdon, createdby) VALUES(
mysql-setup  |   'urn:li:corpuser:datahub',
mysql-setup  |   'corpUserInfo',
mysql-setup  |   0,
mysql-setup  |   '{"displayName":"Data Hub","active":true,"fullName":"Data Hub","email":"datahub@linkedin.com"}',
mysql-setup  |   now(),
mysql-setup  |   'urn:li:corpuser:__datahub_system'
mysql-setup  | ), (
mysql-setup  |   'urn:li:corpuser:datahub',
mysql-setup  |   'corpUserEditableInfo',
mysql-setup  |   0,
mysql-setup  |   '{"skills":[],"teams":[],"pictureLink":"https://raw.githubusercontent.com/datahub-project/datahub/master/datahub-web-react/src/images/default_avatar.png"}',
mysql-setup  |   now(),
mysql-setup  |   'urn:li:corpuser:__datahub_system'
mysql-setup  | );
mysql-setup  | -- only add default records if metadata_aspect is empty
mysql-setup  | INSERT INTO metadata_aspect_v2
mysql-setup  | SELECT * FROM temp_metadata_aspect_v2
mysql-setup  | WHERE NOT EXISTS (SELECT * from metadata_aspect_v2);
mysql-setup  | DROP TABLE temp_metadata_aspect_v2;
mysql-setup  |
mysql-setup  | -- create metadata index table
mysql-setup  | CREATE TABLE IF NOT EXISTS metadata_index (
mysql-setup  |  `id` BIGINT NOT NULL AUTO_INCREMENT,
mysql-setup  |  `urn` VARCHAR(200) NOT NULL,
mysql-setup  |  `aspect` VARCHAR(150) NOT NULL,
mysql-setup  |  `path` VARCHAR(150) NOT NULL,
mysql-setup  |  `longVal` BIGINT,
mysql-setup  |  `stringVal` VARCHAR(200),
mysql-setup  |  `doubleVal` DOUBLE,
mysql-setup  |  CONSTRAINT id_pk PRIMARY KEY (id),
mysql-setup  |  INDEX longIndex (`urn`,`aspect`,`path`,`longVal`),
mysql-setup  |  INDEX stringIndex (`urn`,`aspect`,`path`,`stringVal`),
mysql-setup  |  INDEX doubleIndex (`urn`,`aspect`,`path`,`doubleVal`)
mysql-setup  | );
mysql-setup  | 2023/05/17 07:04:28 Command finished successfully.
mysql-setup exited with code 0
```

## postgres
测试是否成功：客户端连接工具连接


默认初始化数据库少了 【analytics】【ingestion】【govern-domain】等
登出再登录即可。手动加入数据库 【fixdb.xlsx】

```
Attaching to postgres-setup
postgres-setup  | 2023/05/18 07:41:26 Waiting for: tcp://postgres:5432
postgres-setup  | 2023/05/18 07:41:26 Connected to tcp://postgres:5432
postgres-setup  | -- create metadata aspect table
postgres-setup  | CREATE TABLE IF NOT EXISTS metadata_aspect_v2 (
postgres-setup  |   urn                           varchar(500) not null,
postgres-setup  |   aspect                        varchar(200) not null,
postgres-setup  |   version                       bigint not null,
postgres-setup  |   metadata                      text not null,
postgres-setup  |   systemmetadata                text,
postgres-setup  |   createdon                     timestamp not null,
postgres-setup  |   createdby                     varchar(255) not null,
postgres-setup  |   createdfor                    varchar(255),
postgres-setup  |   CONSTRAINT pk_metadata_aspect_v2 PRIMARY KEY (urn, aspect, version)
postgres-setup  | );
postgres-setup  |
postgres-setup  | create index timeIndex ON metadata_aspect_v2 (createdon);
postgres-setup  |
postgres-setup  | -- create default records for datahub user if not exists
postgres-setup  | CREATE TEMP TABLE temp_metadata_aspect_v2 AS TABLE metadata_aspect_v2;
postgres-setup  | INSERT INTO temp_metadata_aspect_v2 (urn, aspect, version, metadata, createdon, createdby) VALUES(
postgres-setup  |   'urn:li:corpuser:datahub',
postgres-setup  |   'corpUserInfo',
postgres-setup  |   0,
postgres-setup  |   '{"displayName":"Data Hub","active":true,"fullName":"Data Hub","email":"datahub@linkedin.com"}',
postgres-setup  |   now(),
postgres-setup  |   'urn:li:corpuser:__datahub_system'
postgres-setup  | ), (
postgres-setup  |   'urn:li:corpuser:datahub',
postgres-setup  |   'corpUserEditableInfo',
postgres-setup  |   0,
postgres-setup  |   '{"skills":[],"teams":[],"pictureLink":"https://raw.githubusercontent.com/datahub-project/datahub/master/datahub-web-react/src/images/default_avatar.png"}',
postgres-setup  |   now(),
postgres-setup  |   'urn:li:corpuser:__datahub_system'
postgres-setup  | );
postgres-setup  | -- only add default records if metadata_aspect is empty
postgres-setup  | INSERT INTO metadata_aspect_v2
postgres-setup  | SELECT * FROM temp_metadata_aspect_v2
postgres-setup  | WHERE NOT EXISTS (SELECT * from metadata_aspect_v2);
postgres-setup  | DROP TABLE temp_metadata_aspect_v2;
postgres-setup  | CREATE TABLE
postgres-setup  | CREATE INDEX
postgres-setup  | SELECT 0
postgres-setup  | INSERT 0 2
postgres-setup  | INSERT 0 2
postgres-setup  | DROP TABLE
postgres-setup  | NOTICE:  relation "metadata_aspect_v2" already exists, skipping
postgres-setup  | ERROR:  relation "timeindex" already exists
postgres-setup  | CREATE TABLE
postgres-setup  | SELECT 2
postgres-setup  | INSERT 0 2
postgres-setup  | INSERT 0 0
postgres-setup  | DROP TABLE
postgres-setup  | CREATE TABLE
postgres-setup  | NOTICE:  relation "metadata_aspect_v2" already exists, skipping
postgres-setup  | ERROR:  relation "timeindex" already exists
postgres-setup  | SELECT 2
postgres-setup  | INSERT 0 2
postgres-setup  | INSERT 0 0
postgres-setup  | DROP TABLE
postgres-setup  | NOTICE:  relation "metadata_aspect_v2" already exists, skipping
postgres-setup  | CREATE TABLE
postgres-setup  | ERROR:  relation "timeindex" already exists
postgres-setup  | SELECT 2
postgres-setup  | INSERT 0 2
postgres-setup  | INSERT 0 0
postgres-setup  | DROP TABLE
postgres-setup  | 2023/05/18 07:41:26 Command finished successfully.
postgres-setup exited with code 0
```

## elasticsearch
可以使用以下 curl 命令测试 DataHub Elasticsearch 是否已成功部署：
curl http://localhost:9200/
如果您看到类似以下内容的输出，那么 DataHub Elasticsearch 已成功部署：
"name" : "MY_NODE_NAME",
  "cluster_name" : "datahub-cluster",
  "cluster_uuid" : "MY_CLUSTER_UUID",
  "version" : {
    "number" : "7.10.1",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "1c34507e66d7db1211f66f3513706fdf548736aa",
    "build_date" : "2020-12-05T01:00:33.671820Z",
    "build_snapshot" : false,
    "lucene_version" : "8.7.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
如果出现错误或其他输出，请检查 Elasticsearch 的配置和日志，以查找问题。

```
Attaching to elasticsearch-setup
elasticsearch-setup  | 2023/05/17 08:00:50 Waiting for: http://elasticsearch:9200
elasticsearch-setup  | 2023/05/17 08:00:50 Received 200 from http://elasticsearch:9200
elasticsearch-setup  | going to use protocol: http
elasticsearch-setup  | going to use default elastic headers
elasticsearch-setup  | not using any prefix
elasticsearch-setup  |
elasticsearch-setup  |  datahub_analytics_enabled: true
elasticsearch-setup  |
elasticsearch-setup  | >>> GET _ilm/policy/datahub_usage_event_policy response code is 404
elasticsearch-setup  | >>> creating _ilm/policy/datahub_usage_event_policy because it doesn't exist ...
elasticsearch-setup  | {
elasticsearch-setup  |   "policy": {
elasticsearch-setup  |     "phases": {
elasticsearch-setup  |       "hot": {
elasticsearch-setup  |         "actions": {
elasticsearch-setup  |           "rollover": {
elasticsearch-setup  |             "max_age": "7d"
elasticsearch-setup  |           }
elasticsearch-setup  |         }
elasticsearch-setup  |       },
elasticsearch-setup  |       "delete": {
elasticsearch-setup  |         "min_age": "60d",
elasticsearch-setup  |         "actions": {
elasticsearch-setup  |           "delete": {}
elasticsearch-setup  |         }
elasticsearch-setup  |       }
elasticsearch-setup  |     }
elasticsearch-setup  |   }
elasticsearch-setup  | }{"acknowledged":true}
elasticsearch-setup  | >>> GET _index_template/datahub_usage_event_index_template response code is 404
elasticsearch-setup  | >>> creating _index_template/datahub_usage_event_index_template because it doesn't exist ...
elasticsearch-setup  | {
elasticsearch-setup  |   "index_patterns": ["*datahub_usage_event*"],
elasticsearch-setup  |   "data_stream": { },
elasticsearch-setup  |   "priority": 500,
elasticsearch-setup  |   "template": {
elasticsearch-setup  |     "mappings": {
elasticsearch-setup  |       "properties": {
elasticsearch-setup  |         "@timestamp": {
elasticsearch-setup  |           "type": "date"
elasticsearch-setup  |         },
elasticsearch-setup  |         "type": {
elasticsearch-setup  |           "type": "keyword"
elasticsearch-setup  |         },
elasticsearch-setup  |         "timestamp": {
elasticsearch-setup  |           "type": "date"
elasticsearch-setup  |         },
elasticsearch-setup  |         "userAgent": {
elasticsearch-setup  |           "type": "keyword"
elasticsearch-setup  |         },
elasticsearch-setup  |         "browserId": {
elasticsearch-setup  |           "type": "keyword"
elasticsearch-setup  |         }
elasticsearch-setup  |       }
elasticsearch-setup  |     },
elasticsearch-setup  |     "settings": {
elasticsearch-setup  |       "index.lifecycle.name": "datahub_usage_event_policy"
elasticsearch-setup  |     }
elasticsearch-setup  |   }
elasticsearch-setup  | }{"acknowledged":true}
elasticsearch-setup  | >>> GET _data_stream/datahub_usage_event response code is 404
elasticsearch-setup  | >>> creating _data_stream/datahub_usage_event because it doesn't exist ...
elasticsearch-setup  | sed: /index/usage-event/datahub_usage_event: No such file or directory
elasticsearch-setup  | {"acknowledged":true}2023/05/17 08:00:51 Command finished successfully.
elasticsearch-setup exited with code 0
```

curl -X DELETE "http://192.168.5.115:9200/datahubpolicyindex_v2?pretty"
curl -X GET "http://localhost:9200/my_index/_search?q=my_field:my_value&pretty"

curl -X POST "http://192.168.5.115:9200/_aliases?pretty" -H 'Content-Type: application/json' -d'{"actions" : [{ "add" : { "index" : "datahub-policy-index_v2", "alias" : "datahubpolicyindex_v2" } }]}'

curl -X PUT "http://192.168.5.115:9200/datahub-policy-index_v2/_mapping" -H 'Content-Type: application/json' -d'{"properties": {"lastUpdatedTimestamp": {"type": "date"}}}'

下面是 DataHub Elasticsearch 中存储的所有索引的列表：

1.  datahub-frontend** ：DataHub 前端 Web 应用程序使用的存储索引；通常包含用户和团队信息。

2.  datahub-gmsauditlog** ：DataHub GMS 使用的审核日志记录的索引；用于记录所有提交到 DataHub 的操作。

3.  datahub-**lineage** ：DataHub 程序的血缘数据索引，用于跟踪数据资产之间的关系。

4.  datahub-mce** ：DataHub GMS 使用的 MCE（Metadata Change Event）索引，用于记录 DataHub 中发生的所有元数据更改。

5.  datahub-metadata** ：DataHub 中存储元数据的索引，包括数据集、数据源和其他相关对象的信息。

6.  datahub-**policyindex** ：DataHub 中存储策略配置的索引，用于记录策略配置信息。

7.  datahub-**search** ：DataHub 中存储搜索相关信息的索引，包括搜索结果、过滤器和其他相关信息。

8.  datahub-tag** ：DataHub 中存储标签的索引，用于标识数据集、数据源和其他相关对象。

注意：索引名称中带有 "**" 的部分是通配符，表示该索引名称可能包含额外的标识符，例如日期或时间戳。这通常是由于索引自动滚动或分割导致的。


## gms
测试 DataHub GMS 是否已成功部署，您可以使用以下 CURL 命令进行检查（请确保 GMS 容器正在运行）：
curl http://localhost:8080/healthcheck
如果一切正常，您将看到如下响应：
json
{"status":"OK"}
如果出现错误或其他输出，请检查 DataHub GMS 的配置和日志，以查找问题


"reason":"no such index [datahubpolicyindex_v2]
执行 update 的镜像，es索引已修改





Error response from daemon: error parsing HTTP 408 response body: invalid character '<' looking for beginning of value: "<html><body><h1>408 Request Time-out</h1>\nYour browser didn't send a complete request in time.\n</body></html>\n"
修改docker数据源

docker-volumes 挂载在数据的数据并没有存下，容器内的路径需要写到具体的数据目录下，eg： /var/lib/postgres/data 而不是/var/lib/postgres