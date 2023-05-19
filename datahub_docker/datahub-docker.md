# 简介
- Datahub 由 4 个主要组件组成：
   - GMS
   - Frontend
   - MAE Consumer（可选）
   - MCE Consumer（可选）
- 主要组件由 4 个外部依赖项提供支持：
   - Kafka
   - Local db（MySQL、Postgres、MariaDB）
   - 搜索索引（Elasticsearch）
   - 图索引（支持 Neo4j 或 Elasticsearch）
# Docker Images

- [linkedin/datahub-ingestion](https://hub.docker.com/r/linkedin/datahub-ingestion/) - This contains the Python CLI. If you are looking for docker image for every minor CLI release you can find them under [acryldata/datahub-ingestion](https://hub.docker.com/r/acryldata/datahub-ingestion/).
- [linkedin/datahub-gms](https://hub.docker.com/repository/docker/linkedin/datahub-gms/).
- [linkedin/datahub-frontend-react](https://hub.docker.com/repository/docker/linkedin/datahub-frontend-react/)
- [linkedin/datahub-mae-consumer](https://hub.docker.com/repository/docker/linkedin/datahub-mae-consumer/)
- [linkedin/datahub-mce-consumer](https://hub.docker.com/repository/docker/linkedin/datahub-mce-consumer/)
- [acryldata/datahub-upgrade](https://hub.docker.com/r/acryldata/datahub-upgrade/)
- [linkedin/datahub-kafka-setup](https://hub.docker.com/r/acryldata/datahub-kafka-setup/)
- [linkedin/datahub-elasticsearch-setup](https://hub.docker.com/r/linkedin/datahub-elasticsearch-setup/)
- [acryldata/datahub-mysql-setup](https://hub.docker.com/r/acryldata/datahub-mysql-setup/)
- [acryldata/datahub-postgres-setup](https://hub.docker.com/r/acryldata/datahub-postgres-setup/)
- [acryldata/datahub-actions](https://hub.docker.com/r/acryldata/datahub-actions). Do not use acryldata/acryl-datahub-actions as that is deprecated and no longer used.

Dependencies:

- [Kafka, Zookeeper, and Schema Registry](https://github.com/datahub-project/datahub/blob/master/docker/kafka-setup)
- [Elasticsearch](https://github.com/datahub-project/datahub/blob/master/docker/elasticsearch-setup)
- [MySQL](https://github.com/datahub-project/datahub/blob/master/docker/mysql)/[MARIADB](https://github.com/datahub-project/datahub/tree/master/docker/mariadb)/[POSTGRES](https://github.com/datahub-project/datahub/tree/master/docker/postgres)
- [(Optional) Neo4j](https://github.com/datahub-project/datahub/blob/master/docker/neo4j)
# 部署以及升级
## 快捷部署
确保为 Docker 引擎分配足够的硬件资源。
测试和确认的配置：2个CPU，8GB RAM，2GB交换区域和10GB磁盘空间。
![image.png](https://cdn.nlark.com/yuque/0/2023/png/745518/1683258883797-10ec00d1-22a5-46a5-9b28-4f86795c7073.png#averageHue=%23252423&clientId=uaf3c715a-8bbc-4&from=paste&height=287&id=u2b4a8a36&originHeight=359&originWidth=1468&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=94979&status=done&style=none&taskId=ua56c90b8-488c-467b-bd83-eb54a110417&title=&width=1174.4)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/745518/1683257620333-6b655443-3ab5-4270-97c7-84d9c0babc78.png#averageHue=%23222222&clientId=ue27b0dba-401a-4&from=paste&height=234&id=u9a5611db&originHeight=371&originWidth=443&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=62444&status=done&style=none&taskId=u97373919-aa7a-4978-9791-80322ab66c2&title=&width=279.3999938964844)![image.png](https://cdn.nlark.com/yuque/0/2023/png/745518/1683257726910-2fe5ab83-7524-4df1-a31e-52ab0358f6d1.png#averageHue=%23242321&clientId=ue27b0dba-401a-4&from=paste&height=57&id=u2eda1cc8&originHeight=109&originWidth=969&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=22845&status=done&style=none&taskId=u354fab03-41a3-4d3d-850a-94bee042367&title=&width=504.4000244140625)
[docker-compose.quickstart.yml](https://github.com/datahub-project/datahub/blob/master/docker/quickstart/docker-compose.quickstart.yml)
```shell
# （可选）修改版本 建议不使用特定于版本的标签head
vim /root/.datahub/quickstart/quickstart_version_mapping.yaml
# 开启容器
python3.7 -m datahub docker quickstart --quickstart-compose-file /opt/datahub/docker-compose.quickstart.yml
```
## 多容器部署

- 将Datahub部署到多个容器中需要管理容器之间的通信和协作，以确保整个系统的正确性和可靠性。
- [github代码](https://github.com/kate0603/component_deployment/tree/main/datahub_docker)
### 数据存储层容器
Datahub需要一个持久化的存储层来存储元数据。因此，可以使用一个独立的容器来运行数据库，如MySQL或PostgreSQL。
#### mariadb

- 流程
   - 创建mariadb容器后，执行一次mariadb-setup，用于初始化。
- 测试
   - 数据库连接客户端工具 连接测试。
- 常见问题
   - /docker-entrypoint-initdb.d/init.sql: Permission denied：改为在容器内执行。
   - init.sql未执行：docker-entrypoint-initdb.d 文件夹只会在创建(实例化)容器时运行一次，因此实际上必须执行 docker-compose up -d --force-recreate
- 备注
   - 创建容器时init.sql可不执行，因为在setup中会执行。
```shell
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

#### postgres

- 流程
   - 创建postgres后，执行一次postgres-setup，用于初始化。
- 测试
   - 数据库连接客户端工具 连接测试。
- 常见问题
   - 切换数据库后， 少了 【analytics】【ingestion】【govern-domain】等：登出再登录即可。首次登录缺少[部分数据](https://github.com/kate0603/component_deployment/blob/main/datahub_docker/datahub/fix_db.xlsx)。
- 备注
   - 创建容器时init.sql可不执行，因为在setup中会执行。
```shell
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

### 元数据搜索容器
Datahub还需要一个用于搜索元数据的容器。您可以使用Apache Solr或Elasticsearch作为搜索引擎，并使用独立容器将其部署到系统中。

- 流程
   - 创建elasticsearch后，执行一次elasticsearch-setup，用于初始化。
- 测试
```shell
# 可以使用以下 curl 命令测试 DataHub Elasticsearch 是否已成功部署：
curl http://localhost:9200/
# 如果您看到类似以下内容的输出，那么 DataHub Elasticsearch 已成功部署：
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
# 如果出现错误或其他输出，请检查 Elasticsearch 的配置和日志，以查找问题。
```
```shell
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

- 常用操作命令
```shell
# 删除
curl -X DELETE "http://localhost:9200/datahubpolicyindex_v2?pretty"
# 获取
curl -X GET "http://localhost:9200/my_index/_search?q=my_field:my_value&pretty"
# 增加alias
curl -X POST "http://localhost:9200/_aliases?pretty" -H 'Content-Type: application/json' -d'{"actions" : [{ "add" : { "index" : "datahub-policy-index_v2", "alias" : "datahubpolicyindex_v2" } }]}'
# 增加属性
curl -X PUT "http://localhost:9200/datahub-policy-index_v2/_mapping" -H 'Content-Type: application/json' -d'{"properties": {"lastUpdatedTimestamp": {"type": "date"}}}'

```

- DataHub Elasticsearch 中存储的所有索引的列表
   -  datahub-frontend** ：DataHub 前端 Web 应用程序使用的存储索引；通常包含用户和团队信息。
   - datahub-gmsauditlog** ：DataHub GMS 使用的审核日志记录的索引；用于记录所有提交到 DataHub 的操作。
   - datahub-**lineage** ：DataHub 程序的血缘数据索引，用于跟踪数据资产之间的关系。
   - datahub-mce** ：DataHub GMS 使用的 MCE（Metadata Change Event）索引，用于记录 DataHub 中发生的所有元数据更改。
   - datahub-metadata** ：DataHub 中存储元数据的索引，包括数据集、数据源和其他相关对象的信息。
   - datahub-**policyindex** ：DataHub 中存储策略配置的索引，用于记录策略配置信息。
   -  datahub-**search** ：DataHub 中存储搜索相关信息的索引，包括搜索结果、过滤器和其他相关信息。datahub-tag** ：DataHub 中存储标签的索引，用于标识数据集、数据源和其他相关对象。

注意：索引名称中带有 "**" 的部分是通配符，表示该索引名称可能包含额外的标识符，例如日期或时间戳。这通常是由于索引自动滚动或分割导致的。

### 消息队列容器
Datahub使用Kafka作为消息队列，以收集和处理元数据。因此，您可以使用一个独立的Kafka容器来管理消息队列。
#### zookeeper

- Kafka 依赖于 Zookeeper 来实现元数据管理、协调、故障转移等重要功能，以确保 Kafka 集群的高可用性和可靠性。Kafka 借助 Zookeeper 来协调以下问题：
   - Broker 认证：Kafka Broker 使用 Zookeeper 来实现身份验证和授权，以确保只有授权的 Broker 才可以加入集群并具有生产者和消费者的权限。Zookeeper 中存储了 Kafka 集群的元数据，包括 Broker ID、Broker 地址、Topic 分区信息等。
   - Topic 管理：Zookeeper 存储了 Kafka 集群的元数据，其中包括 Kafka Topic 的元数据信息。生产者和消费者在向 Broker 发送或接收消息时，需要知道 Topic 的哪些分区可用，以及哪些 Broker 是生产者和消费者可用的。
   - Partition 协调：多个消费者可能会同时消费同一个 Topic 的不同分区，Zookeeper 用于协调消费者并确保每个消费者都仅消费 Topic 的一部分分区，以防止重复消费或竞争条件。
   - Group 协调：Kafka 支持消费者组，Zookeeper 用于协调组的成员和分配分区，以确保每个消费者组中的消费者消费不同的 Topic 分区。在分配分区之后，Zookeeper 还用于监视消费者是否已经离线并将分区分配给其他消费者。
- 测试
```shell
# 使用 telnet 命令测试：在命令行窗口中输入以下命令以测试 ZooKeeper 是否成功连接：
telnet localhost 21811
# 如果成功连接则会返回以下输出：
Trying 127.0.0.1...
   Connected to localhost.
   Escape character is '^]'.
# 如果连接失败则会返回以下输出：
Trying 127.0.0.1...
   telnet: Unable to connect to remote host: Connection refused
```

- 常见问题
   - 在同一个主机下部署的容器，却无法访问到zk。
```
# docker-compose.yml增加
networks:
  default:
    name: datahub_network_new
```
#### schema-registry

- Kafka Schema Registry 是一个基于 REST API 的服务，它用于管理 Kafka 数据流中使用的数据结构。Schema Registry 为序列化和反序列化消息提供了中心化的架构，并提供了以下优点：
   - 数据兼容性：当数据结构发生变化时，Schema Registry 通过维护历史模式版本来确保集群中现有的生产者和消费者仍能够使用旧版本的模式进行序列化和反序列化。这使得在应用程序的演化期间，无需将集群中所有的生产者和消费者同时修改。 
   - 数据合规性：Schema Registry 可以用于验证输入和输出数据是否符合预期的模式，以减少错误和数据质量问题。Schema Registry 还可以强制执行数据质量规则，例如模式版本控制和必填字段，以减少对数据的错误处理。 
   - 数据清晰度：Schema Registry 可以帮助开发人员和数据工程师更好地了解现有数据结构的基本信息，例如数据类型、结构、字段名称和默认值等。 
   - 数据重复使用：Schema Registry 可以帮助组织将现有的数据结构转换为可重用的元数据资源，以便根据需要对其进行查找、使用和共享。 
- 测试
```shell
# 1. 确定 Docker 容器已启动，这将显示在 Docker 中启动的所有容器的列表。
   docker ps
# 2. 确定 Schema-Registry 容器的 IP 地址，在输出中找到  IPAddress  字段，这是 Schema-Registry 容器的 IP 地址。
docker inspect <schema-registry-container-name>
# 3. 使用 curl 命令测试 Schema-Registry，这将向 Schema-Registry 发送一个简单的测试请求。
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
     --data '{"schema": "{\"type\":\"string\"}"}' \
     http://<schema-registry-ip-address>:8081/subjects/test/versions

# 4. 检查响应是否返回200 OK，如果成功部署了 Schema-Registry，则应返回200 OK。
curl -s -o /dev/null -w "%{http_code}" \
     http://<schema-registry-ip-address>:8081/subjects/test/versions
```
#### broker

- 流程
   - 创建broker后，执行一次kafka-setup，用于初始化配置。
```
Attaching to kafka-setup
kafka-setup  | DATAHUB_PRECREATE_TOPICS=false
kafka-setup  | Pre-creation of topics has been turned off, exiting
kafka-setup exited with code 0
```

- 测试
```shell
# 1. 创建一个主题：
docker-compose exec broker kafka-topics --bootstrap-server localhost:29092 --create --topic my-topic --partitions 1 --replication-factor 1
# 2. 启动一个消费者：
docker-compose exec broker kafka-console-consumer --bootstrap-server localhost:29092 --topic my-topic --from-beginning
# 3. 启动一个生产者并发送消息：
docker-compose exec broker bash -c "echo 'hello world' | kafka-console-producer --broker-list localhost:29092 --topic my-topic > /dev/null"
# 4. 在消费者终端查看是否收到了消息。如果提示消费者已经订阅了主题并且能够收到消息，那么 DataHub Broker 部署成功并且能够正常工作。
```

- 常见问题
   - service "broker" is not running container #1：检查zk是否连接成功 docker-compose logs broker。

### 元数据管理容器
Datahub还带有自己的界面。将您可以使用专门的容器将Datahub UI界面部署到一个单独的容器中。
#### datahub-upgrade

- 随着 DataHub 的不断发展和迭代，新版本的 DataHub 功能和性能通常会得到改进和优化。使用 DataHub Upgrade 工具，您可以轻松地将旧版本的 DataHub 升级到最新版本，并享受最新的功能和性能优势。
- DataHub Upgrade 工具的主要作用如下：
   - 支持多版本升级：DataHub Upgrade 工具可以将旧版本的 DataHub 升级到最新版本，同时支持多个中间版本，从而允许您跳过某些版本。
   - 自动化：DataHub Upgrade 工具可以自动升级 DataHub 的各个组件，包括 GMS（元数据服务）、MAE（元数据审计事件）和 DataHub（数据血统服务）等。
   - 可定制：DataHub Upgrade 工具提供了许多配置选项，允许您根据自己的需求定制升级流程。
   - 安全性：DataHub Upgrade 工具可以自动备份您的数据，并在升级期间确保数据的安全性和一致性。
#### datahub-frontend-react

- 用于展示数据平台中的各种数据和元数据，并提供搜索、过滤和导航等功能。Datahub-frontend-react 支持多种数据源，包括 Kafka、Hadoop 和 MySQL 等。它使用 TypeScript 和 React Hooks 构建，并使用 Less、Babel 和 Webpack 进行编译和打包。Datahub-frontend-react 还提供了基于 REST API 的后端服务，用于从 DataHub GMS（元数据服务）和 DataHub（数据血统服务）中检索和展示数据。 
- 测试
   - curl [http://localhost:](http://localhost:8080/)9002/,  是否正常响应。
#### datahub-gms

-   DataHub GMS 支持自定义的实体类型和属性，并包含内置的数据架构和数据血统实体类型。它还提供了用于搜索、筛选和使用元数据的简单 REST API。DataHub GMS 是基于 Apache Kafka 和 Apache Samza 构建的，并使用 Apache Kafka Connect 从各种数据源中提取元数据。此外，DataHub GMS 还与其他 LinkedIn 数据平台工具集集成，例如 DataHub、Data Pipeline 和 LinkedIn 面向数据科学家的平台 Luminol。
- 测试
   - curl [http://localhost:8080/healthcheck](http://localhost:8080/healthcheck) ,响应是否正常。
- 常见问题
   - "reason":"no such index [datahubpolicyindex_v2]：需先执行datahub-update镜像，更新索引。

# 常用命令
## docker-compose命令
```powershell
docker-compose build

docker-compose -f docker-compose-dev.yml up

docker-compose logs zookeeper

docker inspect  elasticsearch

some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres:latest tail -f /dev/null
此命令将在后台运行 Postgres 容器，并使用  tail -f /dev/null  命令启动容器。这将防止容器在完成启动任务后退出。这种方法适用于在容器中运行常驻服务（如数据库）的情况。
```
## 数据管理
```shell
# 前置依赖条件，需要设置鉴权
export DATAHUB_GMS_TOKEN=xxx

# 删除某个 urn
python3 -m datahub delete --urn "urn:li:dataJob:(urn:li:dataFlow:(nifi,1c92020f-0180-1000-cb79-26e7eb563c40,PROD),google)" --hard
# 删除某个大类型下的某个平台
python3.7 -m datahub delete --entity_type datajob --platform nifi --hard
```
# 常见问题
## Error 401 Unauthoriz
token或者缺失，在【设置】=》【access tokens】配置token
## datahub-gms is still starting
如果Datahub-gms一直在启动中，有几种可能的原因：

1.  内存不足：Datahub-gms需要一定的内存来启动和运行。请检查您的服务器上是否有足够的内存可用，或者考虑增加服务器的内存。 
2.  端口冲突：Datahub-gms默认使用9002端口。确保该端口未被其他服务占用，或者更改Datahub-gms的端口设置以避免端口冲突。 
3.  数据库连接问题：Datahub-gms需要连接到MySQL数据库才能启动。请确保您的MySQL数据库正在运行，并且Datahub-gms的连接设置是正确的。 
4.  网络问题：网络问题可能导致Datahub-gms无法启动。请确保您的服务器能够连接到所需的Internet资源，或者考虑使用VPN等工具进行连接。 
5.  文件权限问题：Datahub-gms可能需要读写某些文件或目录。请确保相关文件或目录的权限设置正确。 

如果以上措施都无法解决问题，您可以查看Datahub-gms的日志文件以获取更多信息，或者尝试重新安装Datahub。 如果问题仍然存在，请向Datahub社区提出问题。
## docker-volumes 挂载在主机的数据并没有存储
容器内的路径需要写到具体的数据目录下，eg： /var/lib/postgres/data 而不是/var/lib/postgres
## 镜像无法拉取

- 错误内容：Error response from daemon: error parsing HTTP 408 response body: invalid character '<' looking for beginning of value: "<html><body><h1>408 Request Time-out</h1>\nYour browser didn't send a complete request in time.\n</body></html>\n"
- 方案：修改docker数据源。
# 文档

- [quickstart](https://datahubproject.io/docs/quickstart/) 、[github-quickstart](https://github.com/datahub-project/datahub/blob/a20821dc4d6c9c330a2b8d45a89462e752af9f14/docs/quickstart.md)
- [DataHub安装配置详细过程](https://blog.csdn.net/Forget_Ying/article/details/119870931)
