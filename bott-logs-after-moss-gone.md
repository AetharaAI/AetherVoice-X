ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x$ cd AetherVoice-X
ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/AetherVoice-X$ git pull origin qwentest
remote: Enumerating objects: 64, done.
remote: Counting objects: 100% (64/64), done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 34 (delta 26), reused 34 (delta 26), pack-reused 0 (from 0)
Unpacking objects: 100% (34/34), 10.22 KiB | 1.28 MiB/s, done.
From https://github.com/AetharaAI/AetherVoice-X
 * branch            qwentest   -> FETCH_HEAD
   be14a57..03d1c07  qwentest   -> origin/qwentest
Updating be14a57..03d1c07
Fast-forward
 .env.example                                          |  85 +----------------------------------------------
 .env.moss.example                                     | 215 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 .gitignore                                            |   1 +
 MOSS_DECOMMISSION_QWENTEST_PLAN_2026-03-18.md         | 144 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 docker-compose.yml                                    | 219 --------------------------------------------------------------------------------------------------------------------------
 services/frontend/src/pages/ASRLive.tsx               |   6 +---
 services/frontend/src/pages/TTSFile.tsx               |   2 +-
 services/frontend/src/pages/TTSLive.tsx               |  13 ++------
 services/frontend/src/pages/TTSStudio.tsx             |  75 ++++++++++++++++++------------------------
 services/frontend/src/types/api.ts                    |   4 +--
 services/tts/app/schemas/studio.py                    |   2 +-
 services/tts/app/services/model_registry.py           |  43 +++---------------------
 services/tts/app/services/streaming_service.py        |   4 +--
 services/tts/app/services/studio_service.py           | 173 ++++++++++++++++++++----------------------------------------------------------------------------
 services/tts/app/services/voice_turn_service.py       |   2 +-
 services/worker-common/aether_common/model_aliases.py |  19 -----------
 services/worker-common/aether_common/settings.py      |  22 -------------
 tests/unit/test_studio_service.py                     |  20 ++++--------
 tests/unit/test_tts_streaming_service.py              |  26 +++++++--------
 tests/unit/test_tts_synthesis_fallback.py             |  50 ++++++++++++++--------------
 20 files changed, 485 insertions(+), 640 deletions(-)
 create mode 100644 .env.moss.example
 create mode 100644 MOSS_DECOMMISSION_QWENTEST_PLAN_2026-03-18.md
ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/AetherVoice-X$ sudo mv .env .env.moss
ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/AetherVoice-X$ sudo nano .env
ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/AetherVoice-X$ docker compose down
[+] down 10/10
 ✔ Container aethervoice-x-grafana-1    Removed                                                                                                                                    0.3ss
 ✔ Container aethervoice-x-frontend-1   Removed                                                                                                                                    0.3ss
 ✔ Container aethervoice-x-prometheus-1 Removed                                                                                                                                    0.2ss
 ✔ Container aethervoice-x-gateway-1    Removed                                                                                                                                    10.2s
 ✔ Container aethervoice-x-tts-1        Removed                                                                                                                                    10.3s
 ✔ Container aethervoice-x-asr-1        Removed                                                                                                                                    10.4s
 ✔ Container aethervoice-x-postgres-1   Removed                                                                                                                                    0.2s
 ✔ Container aethervoice-x-minio-1      Removed                                                                                                                                    0.3s
 ✔ Container aethervoice-x-redis-1      Removed                                                                                                                                    1.0s
 ! Network aethervoice-x_default        Resource is still in use                                                                                                                   0.0s
ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/AetherVoice-X$ docker compose up -d
WARN[0000] Found orphan containers ([aethervoice-x-moss-tts-1 aethervoice-x-moss-1 aethervoice-x-moss-voice-generator-1 aethervoice-x-moss-ttsd-1 aethervoice-x-moss-soundeffect-1]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
[+] up 9/9
 ✔ Container aethervoice-x-redis-1      Created                                                                                                                                     0.1s
 ✔ Container aethervoice-x-minio-1      Created                                                                                                                                     0.0s
 ✔ Container aethervoice-x-postgres-1   Created                                                                                                                                     0.1s
 ✔ Container aethervoice-x-asr-1        Created                                                                                                                                     0.1s
 ✔ Container aethervoice-x-tts-1        Created                                                                                                                                     0.0s
 ✔ Container aethervoice-x-gateway-1    Created                                                                                                                                     0.0s
 ✔ Container aethervoice-x-frontend-1   Created                                                                                                                                     0.0s
 ✔ Container aethervoice-x-prometheus-1 Created                                                                                                                                     0.0s
 ✔ Container aethervoice-x-grafana-1    Created                                                                                                                                     0.0s
ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/AetherVoice-X$ docker compose logs f
no such service: f
ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/AetherVoice-X$ docker compose logs -f
redis-1  | 1:C 18 Mar 2026 08:58:39.957 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-1  | 1:C 18 Mar 2026 08:58:39.957 * Redis version=7.4.8, bits=64, commit=00000000, modified=0, pid=1, just started
redis-1  | 1:C 18 Mar 2026 08:58:39.957 * Configuration loaded
redis-1  | 1:M 18 Mar 2026 08:58:39.958 * Increased maximum number of open files to 10032 (it was originally set to 1024).
redis-1  | 1:M 18 Mar 2026 08:58:39.958 * monotonic clock: POSIX clock_gettime
redis-1  | 1:M 18 Mar 2026 08:58:39.959 * Running mode=standalone, port=6379.
redis-1  | 1:M 18 Mar 2026 08:58:39.959 * Server initialized
redis-1  | 1:M 18 Mar 2026 08:58:39.960 * Creating AOF base file appendonly.aof.1.base.rdb on server start
redis-1  | 1:M 18 Mar 2026 08:58:39.962 * Creating AOF incr file appendonly.aof.1.incr.aof on server start
redis-1  | 1:M 18 Mar 2026 08:58:39.962 * Ready to accept connections tcp
frontend-1  | 
frontend-1  | > aether-voice-console@1.0.0 dev
frontend-1  | > vite --host 0.0.0.0 --port 3010
frontend-1  | 
frontend-1  | 
frontend-1  |   VITE v7.3.1  ready in 212 ms
frontend-1  | 
frontend-1  |   ➜  Local:   http://localhost:3010/
frontend-1  |   ➜  Network: http://172.18.0.15:3010/
grafana-1   | logger=settings t=2026-03-18T08:58:40.871022788Z level=info msg="Starting Grafana" version=12.4.0 commit=d1729c53a7f44e2e58947eb44eb896c2fb1c30b3 branch=release-12.4.0 compiled=2026-03-18T08:58:40Z
grafana-1   | logger=settings t=2026-03-18T08:58:40.871441781Z level=info msg="Unified migration configs enforced"
grafana-1     | logger=settings t=2026-03-18T08:58:40.87145429Z level=info msg="Enforcing mode 5 for resource in unified storage" resource=playlists.playlist.grafana.app
grafana-1     | logger=settings t=2026-03-18T08:58:40.87149599Z level=info msg="Config loaded from" file=/usr/share/grafana/conf/defaults.ini
grafana-1     | logger=settings t=2026-03-18T08:58:40.871506899Z level=info msg="Config loaded from" file=/etc/grafana/grafana.ini
grafana-1     | logger=settings t=2026-03-18T08:58:40.871509519Z level=info msg="Config overridden from command line" arg="default.paths.data=/var/lib/grafana"
gateway-1     | INFO:     Started server process [10]
gateway-1     | INFO:     Waiting for application startup.
gateway-1     | {"level": "INFO", "message": "gateway_started", "service": "gateway", "logger": "gateway", "time": "2026-03-18 08:58:41,395", "taskName": "Task-2"}
gateway-1     | INFO:     Application startup complete.
gateway-1     | INFO:     Uvicorn running on http://0.0.0.0:8010 (Press CTRL+C to quit)
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:42,810", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:42,853", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:53390 - "GET /v1/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:51,863", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:51,901", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:43896 - "GET /v1/health HTTP/1.1" 200 OK
grafana-1     | logger=settings t=2026-03-18T08:58:40.871511809Z level=info msg="Config overridden from command line" arg="default.paths.logs=/var/log/grafana"
tts-1         | INFO:     Started server process [10]
asr-1         | INFO:     Started server process [54]
asr-1         | INFO:     Waiting for application startup.
asr-1         | {"level": "INFO", "message": "voxtral_adapter_initialized", "service": "asr", "logger": "asr", "time": "2026-03-18 08:58:41,374", "taskName": "Task-2"}
asr-1         | {"level": "INFO", "message": "asr_started", "service": "asr", "logger": "asr", "time": "2026-03-18 08:58:41,375", "taskName": "Task-2"}
asr-1         | INFO:     Application startup complete.
asr-1         | INFO:     Uvicorn running on http://0.0.0.0:8090 (Press CTRL+C to quit)
postgres-1    | 
postgres-1    | PostgreSQL Database directory appears to contain a database; Skipping initialization
postgres-1    | 
postgres-1    | 2026-03-18 08:58:39.973 UTC [1] LOG:  starting PostgreSQL 16.13 (Debian 16.13-1.pgdg13+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
postgres-1    | 2026-03-18 08:58:39.973 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
postgres-1    | 2026-03-18 08:58:39.973 UTC [1] LOG:  listening on IPv6 address "::", port 5432
postgres-1    | 2026-03-18 08:58:39.975 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
postgres-1    | 2026-03-18 08:58:39.979 UTC [29] LOG:  database system was shut down at 2026-03-18 08:58:24 UTC
postgres-1    | 2026-03-18 08:58:39.983 UTC [1] LOG:  database system is ready to accept connections
prometheus-1  | time=2026-03-18T08:58:40.645Z level=INFO source=main.go:1611 msg="updated GOGC" old=100 new=75
prometheus-1  | time=2026-03-18T08:58:40.645Z level=INFO source=main.go:723 msg="Leaving GOMAXPROCS=90: CPU quota undefined" component=automaxprocs
grafana-1     | logger=settings t=2026-03-18T08:58:40.871514699Z level=info msg="Config overridden from command line" arg="default.paths.plugins=/var/lib/grafana/plugins"
asr-1         | INFO:     172.18.0.11:44686 - "GET /internal/health HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.14:49028 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:45542 - "GET /internal/health HTTP/1.1" 200 OK
prometheus-1  | time=2026-03-18T08:58:40.645Z level=INFO source=memlimit.go:198 msg="GOMEMLIMIT is updated" component=automemlimit package=github.com/KimMachineGun/automemlimit/memlimit GOMEMLIMIT=334110265344 previous=9223372036854775807
prometheus-1  | time=2026-03-18T08:58:40.645Z level=INFO source=main.go:771 msg="No time or size retention was set so using the default time retention" duration=15d
prometheus-1  | time=2026-03-18T08:58:40.645Z level=INFO source=main.go:822 msg="Starting Prometheus Server" mode=server version="(version=3.10.0, branch=HEAD, revision=54e010926b0a270cadb22be1113ad45fe9bcb90a)"
prometheus-1  | time=2026-03-18T08:58:40.645Z level=INFO source=main.go:827 msg="operational information" build_context="(go=go1.26.0, platform=linux/amd64, user=root@2ee2be8e6652, date=20260225-21:12:02, tags=netgo,builtinassets)" host_details="(Linux 6.8.0-86-generic #87-Ubuntu SMP PREEMPT_DYNAMIC Mon Sep 22 18:03:36 UTC 2025 x86_64 fed5b42d4cd7 (none))" fd_limits="(soft=524287, hard=524288)" vm_limits="(soft=unlimited, hard=unlimited)"
prometheus-1  | time=2026-03-18T08:58:40.750Z level=INFO source=web.go:696 msg="Start listening for connections" component=web address=0.0.0.0:9090
prometheus-1  | time=2026-03-18T08:58:40.751Z level=INFO source=main.go:1350 msg="Starting TSDB ..."
prometheus-1  | time=2026-03-18T08:58:40.753Z level=INFO source=tls_config.go:354 msg="Listening on" component=web address=[::]:9090
prometheus-1  | time=2026-03-18T08:58:40.753Z level=INFO source=tls_config.go:357 msg="TLS is disabled." component=web http2=false address=[::]:9090
prometheus-1  | time=2026-03-18T08:58:40.756Z level=INFO source=head.go:680 msg="Replaying on-disk memory mappable chunks if any" component=tsdb
grafana-1     | logger=settings t=2026-03-18T08:58:40.871516909Z level=info msg="Config overridden from command line" arg="default.paths.provisioning=/etc/grafana/provisioning"
grafana-1     | logger=settings t=2026-03-18T08:58:40.871519169Z level=info msg="Config overridden from command line" arg="default.log.mode=console"
grafana-1     | logger=settings t=2026-03-18T08:58:40.871521959Z level=info msg="Config overridden from Environment variable" var="GF_PATHS_DATA=/var/lib/grafana"
grafana-1     | logger=settings t=2026-03-18T08:58:40.871525329Z level=info msg="Config overridden from Environment variable" var="GF_PATHS_LOGS=/var/log/grafana"
grafana-1     | logger=settings t=2026-03-18T08:58:40.871527639Z level=info msg="Config overridden from Environment variable" var="GF_PATHS_PLUGINS=/var/lib/grafana/plugins"
grafana-1     | logger=settings t=2026-03-18T08:58:40.871529949Z level=info msg="Config overridden from Environment variable" var="GF_PATHS_PROVISIONING=/etc/grafana/provisioning"
grafana-1     | logger=settings t=2026-03-18T08:58:40.871532439Z level=info msg="Config overridden from Environment variable" var="GF_SECURITY_ADMIN_USER=admin"
grafana-1     | logger=settings t=2026-03-18T08:58:40.871534689Z level=info msg="Config overridden from Environment variable" var="GF_SECURITY_ADMIN_PASSWORD=*********"
prometheus-1  | time=2026-03-18T08:58:40.756Z level=INFO source=head.go:766 msg="On-disk memory mappable chunks replay completed" component=tsdb duration=920ns
prometheus-1  | time=2026-03-18T08:58:40.756Z level=INFO source=head.go:774 msg="Replaying WAL, this may take a while" component=tsdb
prometheus-1  | time=2026-03-18T08:58:40.759Z level=INFO source=head.go:847 msg="WAL segment loaded" component=tsdb segment=0 maxSegment=0 duration=2.657685ms
prometheus-1  | time=2026-03-18T08:58:40.759Z level=INFO source=head.go:884 msg="WAL replay completed" component=tsdb checkpoint_replay_duration=28.611µs wal_replay_duration=2.94154ms wbl_replay_duration=160ns chunk_snapshot_load_duration=0s mmap_chunk_replay_duration=920ns total_replay_duration=2.98445ms
prometheus-1  | time=2026-03-18T08:58:40.761Z level=INFO source=main.go:1371 msg="filesystem information" fs_type=EXT4_SUPER_MAGIC
prometheus-1  | time=2026-03-18T08:58:40.761Z level=INFO source=main.go:1374 msg="TSDB started"
prometheus-1  | time=2026-03-18T08:58:40.761Z level=INFO source=main.go:1564 msg="Loading configuration file" filename=/etc/prometheus/prometheus.yml
minio-1       | MinIO Object Storage Server
minio-1       | Copyright: 2015-2026 MinIO, Inc.
minio-1       | License: GNU AGPLv3 - https://www.gnu.org/licenses/agpl-3.0.html
prometheus-1  | time=2026-03-18T08:58:40.761Z level=INFO source=main.go:1604 msg="Completed loading of configuration file" db_storage=980ns remote_storage=1.84µs web_handler=520ns query_engine=880ns scrape=245.056µs scrape_sd=33.89µs notify=1.061µs notify_sd=699ns rules=1.369µs tracing=3.97µs filename=/etc/prometheus/prometheus.yml totalDuration=545.41µs
prometheus-1  | time=2026-03-18T08:58:40.761Z level=INFO source=main.go:1335 msg="Server is ready to receive web requests."
prometheus-1  | time=2026-03-18T08:58:40.761Z level=INFO source=manager.go:202 msg="Starting rule manager..." component="rule manager"
tts-1         | INFO:     Waiting for application startup.
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:40,987", "taskName": "Task-2"}
minio-1       | Version: RELEASE.2025-09-07T16-13-09Z (go1.24.6 linux/amd64)
minio-1       | 
minio-1       | API: http://172.18.0.2:9000  http://127.0.0.1:9000 
minio-1       | WebUI: http://172.18.0.2:9001 http://127.0.0.1:9001  
minio-1       | 
grafana-1     | logger=settings t=2026-03-18T08:58:40.871537099Z level=info msg=Target target=[all]
grafana-1     | logger=settings t=2026-03-18T08:58:40.871543669Z level=info msg="Path Home" path=/usr/share/grafana
grafana-1     | logger=settings t=2026-03-18T08:58:40.871546049Z level=info msg="Path Data" path=/var/lib/grafana
grafana-1     | logger=settings t=2026-03-18T08:58:40.871548129Z level=info msg="Path Logs" path=/var/log/grafana
grafana-1     | logger=settings t=2026-03-18T08:58:40.871550349Z level=info msg="Path Plugins" path=/var/lib/grafana/plugins
grafana-1     | logger=settings t=2026-03-18T08:58:40.871552919Z level=info msg="Path Provisioning" path=/etc/grafana/provisioning
grafana-1     | logger=settings t=2026-03-18T08:58:40.871555059Z level=info msg="App mode production"
grafana-1     | logger=featuremgmt t=2026-03-18T08:58:40.87438581Z level=info msg=FeatureToggles enableSCIM=true dashgpt=true alertingSaveStateCompressed=true grafanaAssistantInProfilesDrilldown=true onlyStoreActionSets=true annotationPermissionUpdate=true alertingBulkActionsInUI=true alertRuleRestore=true alertingMigrationUI=true alertingRuleVersionHistoryRestore=true newLogsPanel=true awsDatasourcesTempCredentials=true awsAsyncQueryCaching=true newPanelPadding=true alertingUseNewSimplifiedRoutingHashAlgorithm=true azureMonitorPrometheusExemplars=true alertingImportYAMLUI=true kubernetesDashboards=true alertingNotificationsStepMode=true alertingRulePermanentlyDelete=true alertingQueryAndExpressionsStepMode=true azureMonitorEnableUserAuth=true azureResourcePickerUpdates=true useSessionStorageForRedirection=true logsExploreTableVisualisation=true sharingDashboardImage=true improvedExternalSessionHandlingSAML=true cloudWatchCrossAccountQuerying=true preventPanelChromeOverflow=true logsContextDatasourceUi=true alertingRuleRecoverDeleted=true dashboardScene=true prometheusAzureOverrideAudience=true cloudWatchNewLabelParsing=true logsPanelControls=true lokiQuerySplitting=true newTimeRangeZoomShortcuts=true improvedExternalSessionHandling=true alertingUIOptimizeReducer=true timeRangePan=true grafanaconThemes=true lokiLabelNamesQueryApi=true cloudWatchRoundUpEndTime=true newFiltersUI=true publicDashboardsScene=true influxdbBackendMigration=true
grafana-1     | logger=sqlstore t=2026-03-18T08:58:40.874527308Z level=info msg="Connecting to DB" dbtype=sqlite3
grafana-1     | logger=sqlstore t=2026-03-18T08:58:40.874547408Z level=info msg="Using SQLite driver" driver="mattn/go-sqlite3 (CGO enabled)"
grafana-1     | logger=sqlstore t=2026-03-18T08:58:40.874562937Z level=info msg="Creating SQLite database file" path=/var/lib/grafana/grafana.db
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:41,031", "taskName": "Task-2"}
tts-1         | {"level": "INFO", "message": "tts_started", "service": "tts", "logger": "tts", "time": "2026-03-18 08:58:41,047", "taskName": "Task-2"}
tts-1         | INFO:     Application startup complete.
tts-1         | INFO:     Uvicorn running on http://0.0.0.0:8091 (Press CTRL+C to quit)
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:42,819", "taskName": "Task-7"}
grafana-1     | logger=migrator t=2026-03-18T08:58:40.878140296Z level=info msg="Locking database"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.878155586Z level=info msg="Starting DB migrations"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.878743316Z level=info msg="Executing migration" id="create migration_log table"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.879334626Z level=info msg="Migration successfully executed" id="create migration_log table" duration=590.81µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.881636747Z level=info msg="Executing migration" id="create user table"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.882060129Z level=info msg="Migration successfully executed" id="create user table" duration=422.812µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.88435382Z level=info msg="Executing migration" id="add unique index user.login"
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:42,842", "taskName": "Task-7"}
tts-1         | INFO:     172.18.0.11:37576 - "GET /internal/health HTTP/1.1" 200 OK
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:51,872", "taskName": "Task-8"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:51,894", "taskName": "Task-8"}
tts-1         | INFO:     172.18.0.11:60634 - "GET /internal/health HTTP/1.1" 200 OK
minio-1       | Docs: https://docs.min.io
grafana-1     | logger=migrator t=2026-03-18T08:58:40.884796113Z level=info msg="Migration successfully executed" id="add unique index user.login" duration=441.753µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.886483484Z level=info msg="Executing migration" id="add unique index user.email"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.886909877Z level=info msg="Migration successfully executed" id="add unique index user.email" duration=426.113µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.888625927Z level=info msg="Executing migration" id="drop index UQE_user_login - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.889095299Z level=info msg="Migration successfully executed" id="drop index UQE_user_login - v1" duration=468.842µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.891244733Z level=info msg="Executing migration" id="drop index UQE_user_email - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.891693315Z level=info msg="Migration successfully executed" id="drop index UQE_user_email - v1" duration=448.172µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.893380216Z level=info msg="Executing migration" id="Rename table user to user_v1 - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.894711853Z level=info msg="Migration successfully executed" id="Rename table user to user_v1 - v1" duration=1.331057ms
grafana-1     | logger=migrator t=2026-03-18T08:58:40.896417174Z level=info msg="Executing migration" id="create user table v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.896831357Z level=info msg="Migration successfully executed" id="create user table v2" duration=413.963µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.898493719Z level=info msg="Executing migration" id="create index UQE_user_login - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.898934141Z level=info msg="Migration successfully executed" id="create index UQE_user_login - v2" duration=439.782µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.900546434Z level=info msg="Executing migration" id="create index UQE_user_email - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.900946387Z level=info msg="Migration successfully executed" id="create index UQE_user_email - v2" duration=398.013µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.904223941Z level=info msg="Executing migration" id="copy data_source v1 to v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.904478297Z level=info msg="Migration successfully executed" id="copy data_source v1 to v2" duration=254.126µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.906854616Z level=info msg="Executing migration" id="Drop old table user_v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.90722092Z level=info msg="Migration successfully executed" id="Drop old table user_v1" duration=365.994µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.908902321Z level=info msg="Executing migration" id="Add column help_flags1 to user table"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.909719457Z level=info msg="Migration successfully executed" id="Add column help_flags1 to user table" duration=816.816µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.911350099Z level=info msg="Executing migration" id="Update user table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.911366829Z level=info msg="Migration successfully executed" id="Update user table charset" duration=16.85µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.91304689Z level=info msg="Executing migration" id="Add last_seen_at column to user"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.913767718Z level=info msg="Migration successfully executed" id="Add last_seen_at column to user" duration=720.498µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.915506428Z level=info msg="Executing migration" id="Add missing user data"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.915642776Z level=info msg="Migration successfully executed" id="Add missing user data" duration=136.238µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.917323877Z level=info msg="Executing migration" id="Add is_disabled column to user"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.918031085Z level=info msg="Migration successfully executed" id="Add is_disabled column to user" duration=706.588µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.919741276Z level=info msg="Executing migration" id="Add index user.login/user.email"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.920185858Z level=info msg="Migration successfully executed" id="Add index user.login/user.email" duration=442.862µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.92183224Z level=info msg="Executing migration" id="Add is_service_account column to user"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.922608377Z level=info msg="Migration successfully executed" id="Add is_service_account column to user" duration=775.917µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.927298087Z level=info msg="Executing migration" id="Update is_service_account column to nullable"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.931578784Z level=info msg="Migration successfully executed" id="Update is_service_account column to nullable" duration=4.280227ms
grafana-1     | logger=migrator t=2026-03-18T08:58:40.933291165Z level=info msg="Executing migration" id="Add uid column to user"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.934056472Z level=info msg="Migration successfully executed" id="Add uid column to user" duration=763.657µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.936250334Z level=info msg="Executing migration" id="Update uid column values for users"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.936552019Z level=info msg="Migration successfully executed" id="Update uid column values for users" duration=306.235µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.938403807Z level=info msg="Executing migration" id="Make sure users uid are set"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.938550415Z level=info msg="Migration successfully executed" id="Make sure users uid are set" duration=146.458µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.940639709Z level=info msg="Executing migration" id="Add unique index user_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.94115285Z level=info msg="Migration successfully executed" id="Add unique index user_uid" duration=512.831µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.94351744Z level=info msg="Executing migration" id="Add is_provisioned column to user"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.944332636Z level=info msg="Migration successfully executed" id="Add is_provisioned column to user" duration=814.866µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.946151585Z level=info msg="Executing migration" id="update login field with orgid to allow for multiple service accounts with same name across orgs"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.946375981Z level=info msg="Migration successfully executed" id="update login field with orgid to allow for multiple service accounts with same name across orgs" duration=224.296µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.948103692Z level=info msg="Executing migration" id="update service accounts login field orgid to appear only once"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.948442806Z level=info msg="Migration successfully executed" id="update service accounts login field orgid to appear only once" duration=339.064µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.950111618Z level=info msg="Executing migration" id="update login and email fields to lowercase"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.950449042Z level=info msg="Migration successfully executed" id="update login and email fields to lowercase" duration=337.104µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.952174382Z level=info msg="Executing migration" id="update login and email fields to lowercase2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.952370079Z level=info msg="Migration successfully executed" id="update login and email fields to lowercase2" duration=196.607µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.9540965Z level=info msg="Executing migration" id="Add index on user.is_service_account and user.last_seen_at"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.954551062Z level=info msg="Migration successfully executed" id="Add index on user.is_service_account and user.last_seen_at" duration=455.792µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.956232053Z level=info msg="Executing migration" id="Expand user.uid length to 190"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.956267222Z level=info msg="Migration successfully executed" id="Expand user.uid length to 190" duration=35.359µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.958017153Z level=info msg="Executing migration" id="Prefix SCIM uid for provisioned users"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.95816157Z level=info msg="Migration successfully executed" id="Prefix SCIM uid for provisioned users" duration=144.407µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.960267424Z level=info msg="Executing migration" id="create temp user table v1-7"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.960664577Z level=info msg="Migration successfully executed" id="create temp user table v1-7" duration=396.043µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.963092246Z level=info msg="Executing migration" id="create index IDX_temp_user_email - v1-7"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.963752945Z level=info msg="Migration successfully executed" id="create index IDX_temp_user_email - v1-7" duration=661.709µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.965978457Z level=info msg="Executing migration" id="create index IDX_temp_user_org_id - v1-7"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.966440369Z level=info msg="Migration successfully executed" id="create index IDX_temp_user_org_id - v1-7" duration=460.702µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.968076601Z level=info msg="Executing migration" id="create index IDX_temp_user_code - v1-7"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.968509303Z level=info msg="Migration successfully executed" id="create index IDX_temp_user_code - v1-7" duration=431.082µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.970173465Z level=info msg="Executing migration" id="create index IDX_temp_user_status - v1-7"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.970599988Z level=info msg="Migration successfully executed" id="create index IDX_temp_user_status - v1-7" duration=426.283µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.972307999Z level=info msg="Executing migration" id="Update temp_user table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.972327278Z level=info msg="Migration successfully executed" id="Update temp_user table charset" duration=19.429µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.97397576Z level=info msg="Executing migration" id="drop index IDX_temp_user_email - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.974431072Z level=info msg="Migration successfully executed" id="drop index IDX_temp_user_email - v1" duration=453.732µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.976048165Z level=info msg="Executing migration" id="drop index IDX_temp_user_org_id - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.976497847Z level=info msg="Migration successfully executed" id="drop index IDX_temp_user_org_id - v1" duration=447.732µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.97809928Z level=info msg="Executing migration" id="drop index IDX_temp_user_code - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.978546912Z level=info msg="Migration successfully executed" id="drop index IDX_temp_user_code - v1" duration=447.492µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.981421033Z level=info msg="Executing migration" id="drop index IDX_temp_user_status - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.981837246Z level=info msg="Migration successfully executed" id="drop index IDX_temp_user_status - v1" duration=416.863µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.983522977Z level=info msg="Executing migration" id="Rename table temp_user to temp_user_tmp_qwerty - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.985178389Z level=info msg="Migration successfully executed" id="Rename table temp_user to temp_user_tmp_qwerty - v1" duration=1.654932ms
grafana-1     | logger=migrator t=2026-03-18T08:58:40.98686349Z level=info msg="Executing migration" id="create temp_user v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.987295283Z level=info msg="Migration successfully executed" id="create temp_user v2" duration=431.343µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.989314998Z level=info msg="Executing migration" id="create index IDX_temp_user_email - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.989756191Z level=info msg="Migration successfully executed" id="create index IDX_temp_user_email - v2" duration=440.123µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.991809906Z level=info msg="Executing migration" id="create index IDX_temp_user_org_id - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.992268858Z level=info msg="Migration successfully executed" id="create index IDX_temp_user_org_id - v2" duration=459.922µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.993969099Z level=info msg="Executing migration" id="create index IDX_temp_user_code - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.994431491Z level=info msg="Migration successfully executed" id="create index IDX_temp_user_code - v2" duration=462.382µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.996056523Z level=info msg="Executing migration" id="create index IDX_temp_user_status - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.996495406Z level=info msg="Migration successfully executed" id="create index IDX_temp_user_status - v2" duration=438.633µs
grafana-1     | logger=migrator t=2026-03-18T08:58:40.998337264Z level=info msg="Executing migration" id="copy temp_user v1 to v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:40.99859793Z level=info msg="Migration successfully executed" id="copy temp_user v1 to v2" duration=260.726µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.000708604Z level=info msg="Executing migration" id="drop temp_user_tmp_qwerty"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.001056288Z level=info msg="Migration successfully executed" id="drop temp_user_tmp_qwerty" duration=346.144µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.003491166Z level=info msg="Executing migration" id="Set created for temp users that will otherwise prematurely expire"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.003761792Z level=info msg="Migration successfully executed" id="Set created for temp users that will otherwise prematurely expire" duration=269.646µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.005462893Z level=info msg="Executing migration" id="create star table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.005806337Z level=info msg="Migration successfully executed" id="create star table" duration=343.324µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.008067918Z level=info msg="Executing migration" id="add unique index star.user_id_dashboard_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.00851765Z level=info msg="Migration successfully executed" id="add unique index star.user_id_dashboard_id" duration=449.642µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.010178062Z level=info msg="Executing migration" id="Add column dashboard_uid in star"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.011023498Z level=info msg="Migration successfully executed" id="Add column dashboard_uid in star" duration=845.276µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.01265961Z level=info msg="Executing migration" id="Add column org_id in star"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.013502845Z level=info msg="Migration successfully executed" id="Add column org_id in star" duration=844.105µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.015325934Z level=info msg="Executing migration" id="Add column updated in star"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.0161589Z level=info msg="Migration successfully executed" id="Add column updated in star" duration=832.736µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.017972019Z level=info msg="Executing migration" id="add index in star table on dashboard_uid, org_id and user_id columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.018452361Z level=info msg="Migration successfully executed" id="add index in star table on dashboard_uid, org_id and user_id columns" duration=477.852µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.020988748Z level=info msg="Executing migration" id="create org table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.021386341Z level=info msg="Migration successfully executed" id="create org table v1" duration=397.403µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.023058162Z level=info msg="Executing migration" id="create index UQE_org_name - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.023498195Z level=info msg="Migration successfully executed" id="create index UQE_org_name - v1" duration=439.553µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.025142137Z level=info msg="Executing migration" id="create org_user table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.02550704Z level=info msg="Migration successfully executed" id="create org_user table v1" duration=364.793µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.027203881Z level=info msg="Executing migration" id="create index IDX_org_user_org_id - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.027646904Z level=info msg="Migration successfully executed" id="create index IDX_org_user_org_id - v1" duration=443.373µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.029269746Z level=info msg="Executing migration" id="create index UQE_org_user_org_id_user_id - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.029710669Z level=info msg="Migration successfully executed" id="create index UQE_org_user_org_id_user_id - v1" duration=440.593µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.03137574Z level=info msg="Executing migration" id="create index IDX_org_user_user_id - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.031830552Z level=info msg="Migration successfully executed" id="create index IDX_org_user_user_id - v1" duration=456.132µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.033523933Z level=info msg="Executing migration" id="Update org table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.033542843Z level=info msg="Migration successfully executed" id="Update org table charset" duration=19.17µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.035253814Z level=info msg="Executing migration" id="Update org_user table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.035271484Z level=info msg="Migration successfully executed" id="Update org_user table charset" duration=18.3µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.036971685Z level=info msg="Executing migration" id="Migrate all Read Only Viewers to Viewers"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.037084753Z level=info msg="Migration successfully executed" id="Migrate all Read Only Viewers to Viewers" duration=113.388µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.038772534Z level=info msg="Executing migration" id="create dashboard table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.039223596Z level=info msg="Migration successfully executed" id="create dashboard table" duration=451.112µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.041056985Z level=info msg="Executing migration" id="add index dashboard.account_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.041505757Z level=info msg="Migration successfully executed" id="add index dashboard.account_id" duration=448.532µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.043877617Z level=info msg="Executing migration" id="add unique index dashboard_account_id_slug"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.044442317Z level=info msg="Migration successfully executed" id="add unique index dashboard_account_id_slug" duration=564.32µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.046226167Z level=info msg="Executing migration" id="create dashboard_tag table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.046676469Z level=info msg="Migration successfully executed" id="create dashboard_tag table" duration=449.902µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.049163396Z level=info msg="Executing migration" id="add unique index dashboard_tag.dasboard_id_term"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.049634368Z level=info msg="Migration successfully executed" id="add unique index dashboard_tag.dasboard_id_term" duration=471.061µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.05186219Z level=info msg="Executing migration" id="drop index UQE_dashboard_tag_dashboard_id_term - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.052397251Z level=info msg="Migration successfully executed" id="drop index UQE_dashboard_tag_dashboard_id_term - v1" duration=534.301µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.05425654Z level=info msg="Executing migration" id="Rename table dashboard to dashboard_v1 - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.056676618Z level=info msg="Migration successfully executed" id="Rename table dashboard to dashboard_v1 - v1" duration=2.419578ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.058976549Z level=info msg="Executing migration" id="create dashboard v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.059404002Z level=info msg="Migration successfully executed" id="create dashboard v2" duration=426.473µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.06183439Z level=info msg="Executing migration" id="create index IDX_dashboard_org_id - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.062344471Z level=info msg="Migration successfully executed" id="create index IDX_dashboard_org_id - v2" duration=510.221µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.064872898Z level=info msg="Executing migration" id="create index UQE_dashboard_org_id_slug - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.06538424Z level=info msg="Migration successfully executed" id="create index UQE_dashboard_org_id_slug - v2" duration=511.342µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.067243458Z level=info msg="Executing migration" id="copy dashboard v1 to v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.067474314Z level=info msg="Migration successfully executed" id="copy dashboard v1 to v2" duration=227.906µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.07003112Z level=info msg="Executing migration" id="drop table dashboard_v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.07062744Z level=info msg="Migration successfully executed" id="drop table dashboard_v1" duration=595.91µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.07238359Z level=info msg="Executing migration" id="alter dashboard.data to mediumtext v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.07239604Z level=info msg="Migration successfully executed" id="alter dashboard.data to mediumtext v1" duration=14.4µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.07415702Z level=info msg="Executing migration" id="Add column updated_by in dashboard - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.075229972Z level=info msg="Migration successfully executed" id="Add column updated_by in dashboard - v2" duration=1.070872ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.076980822Z level=info msg="Executing migration" id="Add column created_by in dashboard - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.077953575Z level=info msg="Migration successfully executed" id="Add column created_by in dashboard - v2" duration=970.973µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.079799334Z level=info msg="Executing migration" id="Add column gnetId in dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.080791747Z level=info msg="Migration successfully executed" id="Add column gnetId in dashboard" duration=992.023µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.082717054Z level=info msg="Executing migration" id="Add index for gnetId in dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.083232215Z level=info msg="Migration successfully executed" id="Add index for gnetId in dashboard" duration=515.051µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.088013563Z level=info msg="Executing migration" id="Add column plugin_id in dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.089070195Z level=info msg="Migration successfully executed" id="Add column plugin_id in dashboard" duration=1.054552ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.090929493Z level=info msg="Executing migration" id="Add index for plugin_id in dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.091415055Z level=info msg="Migration successfully executed" id="Add index for plugin_id in dashboard" duration=485.212µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.093216904Z level=info msg="Executing migration" id="Add index for dashboard_id in dashboard_tag"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.093674237Z level=info msg="Migration successfully executed" id="Add index for dashboard_id in dashboard_tag" duration=457.153µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.095490426Z level=info msg="Executing migration" id="Update dashboard table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.095505045Z level=info msg="Migration successfully executed" id="Update dashboard table charset" duration=14.869µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.097311235Z level=info msg="Executing migration" id="Update dashboard_tag table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.097325604Z level=info msg="Migration successfully executed" id="Update dashboard_tag table charset" duration=14.859µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.099248881Z level=info msg="Executing migration" id="Add column folder_id in dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.100329453Z level=info msg="Migration successfully executed" id="Add column folder_id in dashboard" duration=1.080722ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.103940401Z level=info msg="Executing migration" id="Add column isFolder in dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.104993093Z level=info msg="Migration successfully executed" id="Add column isFolder in dashboard" duration=1.052932ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.10751085Z level=info msg="Executing migration" id="Add column has_acl in dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.108614972Z level=info msg="Migration successfully executed" id="Add column has_acl in dashboard" duration=1.104192ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.110315222Z level=info msg="Executing migration" id="Add column uid in dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.111404584Z level=info msg="Migration successfully executed" id="Add column uid in dashboard" duration=1.089172ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.113188593Z level=info msg="Executing migration" id="Update uid column values in dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.113329011Z level=info msg="Migration successfully executed" id="Update uid column values in dashboard" duration=142.997µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.115084391Z level=info msg="Executing migration" id="Add unique index dashboard_org_id_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.115570883Z level=info msg="Migration successfully executed" id="Add unique index dashboard_org_id_uid" duration=483.152µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.117327963Z level=info msg="Executing migration" id="Remove unique index org_id_slug"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.117760085Z level=info msg="Migration successfully executed" id="Remove unique index org_id_slug" duration=432.082µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.119488646Z level=info msg="Executing migration" id="Update dashboard title length"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.119503336Z level=info msg="Migration successfully executed" id="Update dashboard title length" duration=15.15µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.121258046Z level=info msg="Executing migration" id="Add unique index for dashboard_org_id_title_folder_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.121744777Z level=info msg="Migration successfully executed" id="Add unique index for dashboard_org_id_title_folder_id" duration=486.701µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.123500027Z level=info msg="Executing migration" id="create dashboard_provisioning"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.123878581Z level=info msg="Migration successfully executed" id="create dashboard_provisioning" duration=378.434µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.125620561Z level=info msg="Executing migration" id="Rename table dashboard_provisioning to dashboard_provisioning_tmp_qwerty - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.128110619Z level=info msg="Migration successfully executed" id="Rename table dashboard_provisioning to dashboard_provisioning_tmp_qwerty - v1" duration=2.488938ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.129942167Z level=info msg="Executing migration" id="create dashboard_provisioning v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.13035452Z level=info msg="Migration successfully executed" id="create dashboard_provisioning v2" duration=413.103µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.135368965Z level=info msg="Executing migration" id="create index IDX_dashboard_provisioning_dashboard_id - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.135926205Z level=info msg="Migration successfully executed" id="create index IDX_dashboard_provisioning_dashboard_id - v2" duration=557.45µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.137790853Z level=info msg="Executing migration" id="create index IDX_dashboard_provisioning_dashboard_id_name - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.138435002Z level=info msg="Migration successfully executed" id="create index IDX_dashboard_provisioning_dashboard_id_name - v2" duration=644.309µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.142877257Z level=info msg="Executing migration" id="copy dashboard_provisioning v1 to v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.143188121Z level=info msg="Migration successfully executed" id="copy dashboard_provisioning v1 to v2" duration=310.624µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.144982001Z level=info msg="Executing migration" id="drop dashboard_provisioning_tmp_qwerty"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.145416733Z level=info msg="Migration successfully executed" id="drop dashboard_provisioning_tmp_qwerty" duration=431.562µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.147261992Z level=info msg="Executing migration" id="Add check_sum column"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.148664928Z level=info msg="Migration successfully executed" id="Add check_sum column" duration=1.402636ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.150684673Z level=info msg="Executing migration" id="Add index for dashboard_title"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.151181845Z level=info msg="Migration successfully executed" id="Add index for dashboard_title" duration=497.252µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.152853916Z level=info msg="Executing migration" id="delete tags for deleted dashboards"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.152983074Z level=info msg="Migration successfully executed" id="delete tags for deleted dashboards" duration=129.128µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.154768664Z level=info msg="Executing migration" id="delete stars for deleted dashboards"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.154916261Z level=info msg="Migration successfully executed" id="delete stars for deleted dashboards" duration=147.577µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.157002775Z level=info msg="Executing migration" id="Add index for dashboard_is_folder"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.157478387Z level=info msg="Migration successfully executed" id="Add index for dashboard_is_folder" duration=475.432µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.160806751Z level=info msg="Executing migration" id="Add isPublic for dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.162080389Z level=info msg="Migration successfully executed" id="Add isPublic for dashboard" duration=1.273618ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.16378985Z level=info msg="Executing migration" id="Add deleted for dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.164968339Z level=info msg="Migration successfully executed" id="Add deleted for dashboard" duration=1.17806ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.166738869Z level=info msg="Executing migration" id="Add index for deleted"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.16726175Z level=info msg="Migration successfully executed" id="Add index for deleted" duration=522.821µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.16963744Z level=info msg="Executing migration" id="Add column dashboard_uid in dashboard_tag"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.170826519Z level=info msg="Migration successfully executed" id="Add column dashboard_uid in dashboard_tag" duration=1.18913ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.173075591Z level=info msg="Executing migration" id="Add column org_id in dashboard_tag"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.174228421Z level=info msg="Migration successfully executed" id="Add column org_id in dashboard_tag" duration=1.15088ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.176406494Z level=info msg="Executing migration" id="Add missing dashboard_uid and org_id to dashboard_tag"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.17667763Z level=info msg="Migration successfully executed" id="Add missing dashboard_uid and org_id to dashboard_tag" duration=270.836µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.178817553Z level=info msg="Executing migration" id="Add apiVersion for dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.179934824Z level=info msg="Migration successfully executed" id="Add apiVersion for dashboard" duration=1.117101ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.181963799Z level=info msg="Executing migration" id="Add index for dashboard_uid on dashboard_tag table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.182428711Z level=info msg="Migration successfully executed" id="Add index for dashboard_uid on dashboard_tag table" duration=464.902µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.185176944Z level=info msg="Executing migration" id="Add missing dashboard_uid and org_id to star"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.18545981Z level=info msg="Migration successfully executed" id="Add missing dashboard_uid and org_id to star" duration=282.825µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.187870358Z level=info msg="Executing migration" id="create data_source table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.188307651Z level=info msg="Migration successfully executed" id="create data_source table" duration=437.563µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.190605172Z level=info msg="Executing migration" id="add index data_source.account_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.191065934Z level=info msg="Migration successfully executed" id="add index data_source.account_id" duration=460.382µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.192845404Z level=info msg="Executing migration" id="add unique index data_source.account_id_name"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.193322075Z level=info msg="Migration successfully executed" id="add unique index data_source.account_id_name" duration=476.491µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.195551447Z level=info msg="Executing migration" id="drop index IDX_data_source_account_id - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.19599743Z level=info msg="Migration successfully executed" id="drop index IDX_data_source_account_id - v1" duration=444.413µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.198021205Z level=info msg="Executing migration" id="drop index UQE_data_source_account_id_name - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.198479767Z level=info msg="Migration successfully executed" id="drop index UQE_data_source_account_id_name - v1" duration=462.012µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.20008414Z level=info msg="Executing migration" id="Rename table data_source to data_source_v1 - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.202574207Z level=info msg="Migration successfully executed" id="Rename table data_source to data_source_v1 - v1" duration=2.489717ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.204633102Z level=info msg="Executing migration" id="create data_source table v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.205084915Z level=info msg="Migration successfully executed" id="create data_source table v2" duration=451.773µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.206722237Z level=info msg="Executing migration" id="create index IDX_data_source_org_id - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.207170489Z level=info msg="Migration successfully executed" id="create index IDX_data_source_org_id - v2" duration=449.552µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.208802131Z level=info msg="Executing migration" id="create index UQE_data_source_org_id_name - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.209292633Z level=info msg="Migration successfully executed" id="create index UQE_data_source_org_id_name - v2" duration=490.352µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.211032453Z level=info msg="Executing migration" id="Drop old table data_source_v1 #2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.211401157Z level=info msg="Migration successfully executed" id="Drop old table data_source_v1 #2" duration=368.554µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.213406023Z level=info msg="Executing migration" id="Add column with_credentials"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.214604542Z level=info msg="Migration successfully executed" id="Add column with_credentials" duration=1.198319ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.216207195Z level=info msg="Executing migration" id="Add secure json data column"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.217408874Z level=info msg="Migration successfully executed" id="Add secure json data column" duration=1.201029ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.219002407Z level=info msg="Executing migration" id="Update data_source table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.219017757Z level=info msg="Migration successfully executed" id="Update data_source table charset" duration=15.65µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.220719178Z level=info msg="Executing migration" id="Update initial version to 1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.220864845Z level=info msg="Migration successfully executed" id="Update initial version to 1" duration=145.737µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.222467558Z level=info msg="Executing migration" id="Add read_only data column"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.223644358Z level=info msg="Migration successfully executed" id="Add read_only data column" duration=1.17525ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.22525099Z level=info msg="Executing migration" id="Migrate logging ds to loki ds"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.225382958Z level=info msg="Migration successfully executed" id="Migrate logging ds to loki ds" duration=131.738µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.22703516Z level=info msg="Executing migration" id="Update json_data with nulls"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.227178657Z level=info msg="Migration successfully executed" id="Update json_data with nulls" duration=143.367µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.22878039Z level=info msg="Executing migration" id="Add uid column"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.22995253Z level=info msg="Migration successfully executed" id="Add uid column" duration=1.1718ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.231956136Z level=info msg="Executing migration" id="Update uid value"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.232088824Z level=info msg="Migration successfully executed" id="Update uid value" duration=129.328µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.234302086Z level=info msg="Executing migration" id="Add unique index datasource_org_id_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.234760168Z level=info msg="Migration successfully executed" id="Add unique index datasource_org_id_uid" duration=457.892µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.236789043Z level=info msg="Executing migration" id="add unique index datasource_org_id_is_default"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.237243296Z level=info msg="Migration successfully executed" id="add unique index datasource_org_id_is_default" duration=454.033µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.238900497Z level=info msg="Executing migration" id="Add is_prunable column"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.240141536Z level=info msg="Migration successfully executed" id="Add is_prunable column" duration=1.226219ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.241709379Z level=info msg="Executing migration" id="Add api_version column"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.242922859Z level=info msg="Migration successfully executed" id="Add api_version column" duration=1.21326ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.2445774Z level=info msg="Executing migration" id="Update secure_json_data column to MediumText"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.24459182Z level=info msg="Migration successfully executed" id="Update secure_json_data column to MediumText" duration=14.92µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.246240552Z level=info msg="Executing migration" id="Update json_data column to MediumText"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.246251482Z level=info msg="Migration successfully executed" id="Update json_data column to MediumText" duration=11.52µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.247902594Z level=info msg="Executing migration" id="create api_key table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.248299597Z level=info msg="Migration successfully executed" id="create api_key table" duration=396.853µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.249983488Z level=info msg="Executing migration" id="add index api_key.account_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.25044972Z level=info msg="Migration successfully executed" id="add index api_key.account_id" duration=466.312µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.252117712Z level=info msg="Executing migration" id="add index api_key.key"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.252577974Z level=info msg="Migration successfully executed" id="add index api_key.key" duration=460.002µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.254250465Z level=info msg="Executing migration" id="add index api_key.account_id_name"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.254698888Z level=info msg="Migration successfully executed" id="add index api_key.account_id_name" duration=448.593µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.25632002Z level=info msg="Executing migration" id="drop index IDX_api_key_account_id - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.256762132Z level=info msg="Migration successfully executed" id="drop index IDX_api_key_account_id - v1" duration=443.202µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.258347345Z level=info msg="Executing migration" id="drop index UQE_api_key_key - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.258772658Z level=info msg="Migration successfully executed" id="drop index UQE_api_key_key - v1" duration=425.243µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.26042042Z level=info msg="Executing migration" id="drop index UQE_api_key_account_id_name - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.260855982Z level=info msg="Migration successfully executed" id="drop index UQE_api_key_account_id_name - v1" duration=435.322µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.262443105Z level=info msg="Executing migration" id="Rename table api_key to api_key_v1 - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.265166169Z level=info msg="Migration successfully executed" id="Rename table api_key to api_key_v1 - v1" duration=2.722674ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.266783871Z level=info msg="Executing migration" id="create api_key table v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.267180344Z level=info msg="Migration successfully executed" id="create api_key table v2" duration=396.403µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.268783967Z level=info msg="Executing migration" id="create index IDX_api_key_org_id - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.269235149Z level=info msg="Migration successfully executed" id="create index IDX_api_key_org_id - v2" duration=450.592µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.270826762Z level=info msg="Executing migration" id="create index UQE_api_key_key - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.271283624Z level=info msg="Migration successfully executed" id="create index UQE_api_key_key - v2" duration=457.042µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.272968376Z level=info msg="Executing migration" id="create index UQE_api_key_org_id_name - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.273440848Z level=info msg="Migration successfully executed" id="create index UQE_api_key_org_id_name - v2" duration=480.032µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.27508642Z level=info msg="Executing migration" id="copy api_key v1 to v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.275319326Z level=info msg="Migration successfully executed" id="copy api_key v1 to v2" duration=232.806µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.276883999Z level=info msg="Executing migration" id="Drop old table api_key_v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.277247983Z level=info msg="Migration successfully executed" id="Drop old table api_key_v1" duration=368.844µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.278828066Z level=info msg="Executing migration" id="Update api_key table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.278843525Z level=info msg="Migration successfully executed" id="Update api_key table charset" duration=15.759µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.280474088Z level=info msg="Executing migration" id="Add expires to api_key table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.281736846Z level=info msg="Migration successfully executed" id="Add expires to api_key table" duration=1.262368ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.283321679Z level=info msg="Executing migration" id="Add service account foreign key"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.284560238Z level=info msg="Migration successfully executed" id="Add service account foreign key" duration=1.238289ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.286123811Z level=info msg="Executing migration" id="set service account foreign key to nil if 0"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.286241759Z level=info msg="Migration successfully executed" id="set service account foreign key to nil if 0" duration=117.948µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.287889551Z level=info msg="Executing migration" id="Add last_used_at to api_key table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.289147319Z level=info msg="Migration successfully executed" id="Add last_used_at to api_key table" duration=1.257518ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.290750942Z level=info msg="Executing migration" id="Add is_revoked column to api_key table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.29205741Z level=info msg="Migration successfully executed" id="Add is_revoked column to api_key table" duration=1.305928ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.293735651Z level=info msg="Executing migration" id="create dashboard_snapshot table v4"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.294160894Z level=info msg="Migration successfully executed" id="create dashboard_snapshot table v4" duration=426.163µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.295815176Z level=info msg="Executing migration" id="drop table dashboard_snapshot_v4 #1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.296222419Z level=info msg="Migration successfully executed" id="drop table dashboard_snapshot_v4 #1" duration=406.943µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.297847201Z level=info msg="Executing migration" id="create dashboard_snapshot table v5 #2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.298285683Z level=info msg="Migration successfully executed" id="create dashboard_snapshot table v5 #2" duration=438.392µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.299924906Z level=info msg="Executing migration" id="create index UQE_dashboard_snapshot_key - v5"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.300431877Z level=info msg="Migration successfully executed" id="create index UQE_dashboard_snapshot_key - v5" duration=506.881µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.302075639Z level=info msg="Executing migration" id="create index UQE_dashboard_snapshot_delete_key - v5"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.30259143Z level=info msg="Migration successfully executed" id="create index UQE_dashboard_snapshot_delete_key - v5" duration=515.521µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.304299471Z level=info msg="Executing migration" id="create index IDX_dashboard_snapshot_user_id - v5"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.304783453Z level=info msg="Migration successfully executed" id="create index IDX_dashboard_snapshot_user_id - v5" duration=483.822µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.306846037Z level=info msg="Executing migration" id="alter dashboard_snapshot to mediumtext v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.306858167Z level=info msg="Migration successfully executed" id="alter dashboard_snapshot to mediumtext v2" duration=12.49µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.308844683Z level=info msg="Executing migration" id="Update dashboard_snapshot table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.308861373Z level=info msg="Migration successfully executed" id="Update dashboard_snapshot table charset" duration=17.3µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.310884638Z level=info msg="Executing migration" id="Add column external_delete_url to dashboard_snapshots table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.312279905Z level=info msg="Migration successfully executed" id="Add column external_delete_url to dashboard_snapshots table" duration=1.393427ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.313940966Z level=info msg="Executing migration" id="Add encrypted dashboard json column"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.315262044Z level=info msg="Migration successfully executed" id="Add encrypted dashboard json column" duration=1.320698ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.316907416Z level=info msg="Executing migration" id="Change dashboard_encrypted column to MEDIUMBLOB"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.316919235Z level=info msg="Migration successfully executed" id="Change dashboard_encrypted column to MEDIUMBLOB" duration=12.229µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.318589267Z level=info msg="Executing migration" id="create quota table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.318947961Z level=info msg="Migration successfully executed" id="create quota table v1" duration=358.454µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.320617182Z level=info msg="Executing migration" id="create index UQE_quota_org_id_user_id_target - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.321088674Z level=info msg="Migration successfully executed" id="create index UQE_quota_org_id_user_id_target - v1" duration=471.382µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.322753496Z level=info msg="Executing migration" id="Update quota table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.322769205Z level=info msg="Migration successfully executed" id="Update quota table charset" duration=15.869µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.324418157Z level=info msg="Executing migration" id="create plugin_setting table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.32486136Z level=info msg="Migration successfully executed" id="create plugin_setting table" duration=444.463µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.326544471Z level=info msg="Executing migration" id="create index UQE_plugin_setting_org_id_plugin_id - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.327006453Z level=info msg="Migration successfully executed" id="create index UQE_plugin_setting_org_id_plugin_id - v1" duration=461.652µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.328685844Z level=info msg="Executing migration" id="Add column plugin_version to plugin_settings"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.330062131Z level=info msg="Migration successfully executed" id="Add column plugin_version to plugin_settings" duration=1.368856ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.331702793Z level=info msg="Executing migration" id="Update plugin_setting table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.331726693Z level=info msg="Migration successfully executed" id="Update plugin_setting table charset" duration=24.17µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.333790907Z level=info msg="Executing migration" id="update NULL org_id to 1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.334003144Z level=info msg="Migration successfully executed" id="update NULL org_id to 1" duration=212.227µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.335639886Z level=info msg="Executing migration" id="make org_id NOT NULL and DEFAULT VALUE 1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.339694786Z level=info msg="Migration successfully executed" id="make org_id NOT NULL and DEFAULT VALUE 1" duration=4.05418ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.341444567Z level=info msg="Executing migration" id="create session table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.341865229Z level=info msg="Migration successfully executed" id="create session table" duration=420.502µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.34359107Z level=info msg="Executing migration" id="Drop old table playlist table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.343666999Z level=info msg="Migration successfully executed" id="Drop old table playlist table" duration=76.159µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.34534904Z level=info msg="Executing migration" id="Drop old table playlist_item table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.345425259Z level=info msg="Migration successfully executed" id="Drop old table playlist_item table" duration=76.339µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.34707997Z level=info msg="Executing migration" id="create playlist table v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.347473664Z level=info msg="Migration successfully executed" id="create playlist table v2" duration=392.224µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.349165515Z level=info msg="Executing migration" id="create playlist item table v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.349553988Z level=info msg="Migration successfully executed" id="create playlist item table v2" duration=389.663µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.351749031Z level=info msg="Executing migration" id="Update playlist table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.35176553Z level=info msg="Migration successfully executed" id="Update playlist table charset" duration=17.069µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.353488491Z level=info msg="Executing migration" id="Update playlist_item table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.353505791Z level=info msg="Migration successfully executed" id="Update playlist_item table charset" duration=17.4µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.355605025Z level=info msg="Executing migration" id="Add playlist column created_at"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.3570738Z level=info msg="Migration successfully executed" id="Add playlist column created_at" duration=1.469135ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.358741331Z level=info msg="Executing migration" id="Add playlist column updated_at"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.360171757Z level=info msg="Migration successfully executed" id="Add playlist column updated_at" duration=1.430246ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.36177472Z level=info msg="Executing migration" id="drop preferences table v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.361835339Z level=info msg="Migration successfully executed" id="drop preferences table v2" duration=60.679µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.363473381Z level=info msg="Executing migration" id="drop preferences table v3"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.36353242Z level=info msg="Migration successfully executed" id="drop preferences table v3" duration=59.229µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.365180351Z level=info msg="Executing migration" id="create preferences table v3"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.365610494Z level=info msg="Migration successfully executed" id="create preferences table v3" duration=429.983µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.367833156Z level=info msg="Executing migration" id="Update preferences table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.367848296Z level=info msg="Migration successfully executed" id="Update preferences table charset" duration=16.36µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.369499768Z level=info msg="Executing migration" id="Add column team_id in preferences"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.370945193Z level=info msg="Migration successfully executed" id="Add column team_id in preferences" duration=1.445045ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.372673873Z level=info msg="Executing migration" id="Update team_id column values in preferences"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.372778332Z level=info msg="Migration successfully executed" id="Update team_id column values in preferences" duration=105.008µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.374416664Z level=info msg="Executing migration" id="Add column week_start in preferences"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.375966327Z level=info msg="Migration successfully executed" id="Add column week_start in preferences" duration=1.549433ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.377614049Z level=info msg="Executing migration" id="Add column preferences.json_data"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.379093274Z level=info msg="Migration successfully executed" id="Add column preferences.json_data" duration=1.479115ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.380796975Z level=info msg="Executing migration" id="alter preferences.json_data to mediumtext v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.380809265Z level=info msg="Migration successfully executed" id="alter preferences.json_data to mediumtext v1" duration=12.79µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.382464456Z level=info msg="Executing migration" id="Add preferences index org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.382920749Z level=info msg="Migration successfully executed" id="Add preferences index org_id" duration=456.163µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.38459706Z level=info msg="Executing migration" id="Add preferences index user_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.385079812Z level=info msg="Migration successfully executed" id="Add preferences index user_id" duration=482.712µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.386840122Z level=info msg="Executing migration" id="Add home_dashboard_uid column to preferences table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.388380695Z level=info msg="Migration successfully executed" id="Add home_dashboard_uid column to preferences table" duration=1.540203ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.390022667Z level=info msg="Executing migration" id="Add missing dashboard_uid to preferences table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.390291463Z level=info msg="Migration successfully executed" id="Add missing dashboard_uid to preferences table" duration=268.526µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.392002933Z level=info msg="Executing migration" id="create alert table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.392462036Z level=info msg="Migration successfully executed" id="create alert table v1" duration=455.883µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.394109268Z level=info msg="Executing migration" id="add index alert org_id & id "
grafana-1     | logger=migrator t=2026-03-18T08:58:41.394588809Z level=info msg="Migration successfully executed" id="add index alert org_id & id " duration=479.161µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.396247191Z level=info msg="Executing migration" id="add index alert state"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.396703633Z level=info msg="Migration successfully executed" id="add index alert state" duration=456.132µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.398906906Z level=info msg="Executing migration" id="add index alert dashboard_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.399388727Z level=info msg="Migration successfully executed" id="add index alert dashboard_id" duration=480.061µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.401085698Z level=info msg="Executing migration" id="Create alert_rule_tag table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.401447302Z level=info msg="Migration successfully executed" id="Create alert_rule_tag table v1" duration=359.624µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.403154923Z level=info msg="Executing migration" id="Add unique index alert_rule_tag.alert_id_tag_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.403600426Z level=info msg="Migration successfully executed" id="Add unique index alert_rule_tag.alert_id_tag_id" duration=445.173µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.405227158Z level=info msg="Executing migration" id="drop index UQE_alert_rule_tag_alert_id_tag_id - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.40567382Z level=info msg="Migration successfully executed" id="drop index UQE_alert_rule_tag_alert_id_tag_id - v1" duration=446.502µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.407309682Z level=info msg="Executing migration" id="Rename table alert_rule_tag to alert_rule_tag_v1 - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.411734657Z level=info msg="Migration successfully executed" id="Rename table alert_rule_tag to alert_rule_tag_v1 - v1" duration=4.424695ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.413454217Z level=info msg="Executing migration" id="Create alert_rule_tag table v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.413815571Z level=info msg="Migration successfully executed" id="Create alert_rule_tag table v2" duration=361.184µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.415455623Z level=info msg="Executing migration" id="create index UQE_alert_rule_tag_alert_id_tag_id - Add unique index alert_rule_tag.alert_id_tag_id V2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.415915565Z level=info msg="Migration successfully executed" id="create index UQE_alert_rule_tag_alert_id_tag_id - Add unique index alert_rule_tag.alert_id_tag_id V2" duration=459.622µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.417649106Z level=info msg="Executing migration" id="copy alert_rule_tag v1 to v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.417854032Z level=info msg="Migration successfully executed" id="copy alert_rule_tag v1 to v2" duration=205.136µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.420366409Z level=info msg="Executing migration" id="drop table alert_rule_tag_v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.420696314Z level=info msg="Migration successfully executed" id="drop table alert_rule_tag_v1" duration=329.365µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.422492023Z level=info msg="Executing migration" id="create alert_notification table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.422883666Z level=info msg="Migration successfully executed" id="create alert_notification table v1" duration=391.393µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.424533538Z level=info msg="Executing migration" id="Add column is_default"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.426121971Z level=info msg="Migration successfully executed" id="Add column is_default" duration=1.589633ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.435728007Z level=info msg="Executing migration" id="Add column frequency"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.437372679Z level=info msg="Migration successfully executed" id="Add column frequency" duration=1.644652ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.43908288Z level=info msg="Executing migration" id="Add column send_reminder"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.440683832Z level=info msg="Migration successfully executed" id="Add column send_reminder" duration=1.601232ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.442343264Z level=info msg="Executing migration" id="Add column disable_resolve_message"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.443965126Z level=info msg="Migration successfully executed" id="Add column disable_resolve_message" duration=1.621252ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.446486823Z level=info msg="Executing migration" id="add index alert_notification org_id & name"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.446937186Z level=info msg="Migration successfully executed" id="add index alert_notification org_id & name" duration=450.223µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.448637427Z level=info msg="Executing migration" id="Update alert table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.448652736Z level=info msg="Migration successfully executed" id="Update alert table charset" duration=15.589µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.450412256Z level=info msg="Executing migration" id="Update alert_notification table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.450427116Z level=info msg="Migration successfully executed" id="Update alert_notification table charset" duration=15.22µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.452066058Z level=info msg="Executing migration" id="create notification_journal table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.452470491Z level=info msg="Migration successfully executed" id="create notification_journal table v1" duration=404.963µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.454165602Z level=info msg="Executing migration" id="add index notification_journal org_id & alert_id & notifier_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.454631064Z level=info msg="Migration successfully executed" id="add index notification_journal org_id & alert_id & notifier_id" duration=465.212µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.456302416Z level=info msg="Executing migration" id="drop alert_notification_journal"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.456729568Z level=info msg="Migration successfully executed" id="drop alert_notification_journal" duration=427.233µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.458343691Z level=info msg="Executing migration" id="create alert_notification_state table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.458736194Z level=info msg="Migration successfully executed" id="create alert_notification_state table v1" duration=392.203µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.460308317Z level=info msg="Executing migration" id="add index alert_notification_state org_id & alert_id & notifier_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.46076578Z level=info msg="Migration successfully executed" id="add index alert_notification_state org_id & alert_id & notifier_id" duration=457.273µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.462340773Z level=info msg="Executing migration" id="Add for to alert table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.464039624Z level=info msg="Migration successfully executed" id="Add for to alert table" duration=1.698631ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.465699325Z level=info msg="Executing migration" id="Add column uid in alert_notification"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.467394756Z level=info msg="Migration successfully executed" id="Add column uid in alert_notification" duration=1.695081ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.468983029Z level=info msg="Executing migration" id="Update uid column values in alert_notification"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.469091907Z level=info msg="Migration successfully executed" id="Update uid column values in alert_notification" duration=108.408µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.47072127Z level=info msg="Executing migration" id="Add unique index alert_notification_org_id_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.471210121Z level=info msg="Migration successfully executed" id="Add unique index alert_notification_org_id_uid" duration=488.581µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.472862693Z level=info msg="Executing migration" id="Remove unique index org_id_name"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.473319745Z level=info msg="Migration successfully executed" id="Remove unique index org_id_name" duration=457.052µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.474960417Z level=info msg="Executing migration" id="Add column secure_settings in alert_notification"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.476602409Z level=info msg="Migration successfully executed" id="Add column secure_settings in alert_notification" duration=1.641672ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.478211592Z level=info msg="Executing migration" id="alter alert.settings to mediumtext"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.478220912Z level=info msg="Migration successfully executed" id="alter alert.settings to mediumtext" duration=9.74µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.480005271Z level=info msg="Executing migration" id="Add non-unique index alert_notification_state_alert_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.480495283Z level=info msg="Migration successfully executed" id="Add non-unique index alert_notification_state_alert_id" duration=488.182µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.482080476Z level=info msg="Executing migration" id="Add non-unique index alert_rule_tag_alert_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.482546488Z level=info msg="Migration successfully executed" id="Add non-unique index alert_rule_tag_alert_id" duration=465.792µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.484207919Z level=info msg="Executing migration" id="Drop old annotation table v4"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.484260398Z level=info msg="Migration successfully executed" id="Drop old annotation table v4" duration=52.729µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.48594154Z level=info msg="Executing migration" id="create annotation table v5"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.486421972Z level=info msg="Migration successfully executed" id="create annotation table v5" duration=480.172µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.488115273Z level=info msg="Executing migration" id="add index annotation 0 v3"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.488607294Z level=info msg="Migration successfully executed" id="add index annotation 0 v3" duration=491.681µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.490244976Z level=info msg="Executing migration" id="add index annotation 1 v3"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.490715288Z level=info msg="Migration successfully executed" id="add index annotation 1 v3" duration=470.142µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.4923899Z level=info msg="Executing migration" id="add index annotation 2 v3"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.492876591Z level=info msg="Migration successfully executed" id="add index annotation 2 v3" duration=484.661µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.494502034Z level=info msg="Executing migration" id="add index annotation 3 v3"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.494974186Z level=info msg="Migration successfully executed" id="add index annotation 3 v3" duration=471.962µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.496631767Z level=info msg="Executing migration" id="add index annotation 4 v3"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.49708008Z level=info msg="Migration successfully executed" id="add index annotation 4 v3" duration=448.093µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.498771451Z level=info msg="Executing migration" id="Update annotation table charset"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.498784261Z level=info msg="Migration successfully executed" id="Update annotation table charset" duration=13.13µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.500432112Z level=info msg="Executing migration" id="Add column region_id to annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.502193642Z level=info msg="Migration successfully executed" id="Add column region_id to annotation table" duration=1.76147ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.503824704Z level=info msg="Executing migration" id="Drop category_id index"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.504296556Z level=info msg="Migration successfully executed" id="Drop category_id index" duration=471.612µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.505912459Z level=info msg="Executing migration" id="Add column tags to annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.507675629Z level=info msg="Migration successfully executed" id="Add column tags to annotation table" duration=1.7629ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.509267862Z level=info msg="Executing migration" id="Create annotation_tag table v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.509638235Z level=info msg="Migration successfully executed" id="Create annotation_tag table v2" duration=372.313µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.511258607Z level=info msg="Executing migration" id="Add unique index annotation_tag.annotation_id_tag_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.51171587Z level=info msg="Migration successfully executed" id="Add unique index annotation_tag.annotation_id_tag_id" duration=455.772µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.513386511Z level=info msg="Executing migration" id="drop index UQE_annotation_tag_annotation_id_tag_id - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.513847323Z level=info msg="Migration successfully executed" id="drop index UQE_annotation_tag_annotation_id_tag_id - v2" duration=460.692µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.515460056Z level=info msg="Executing migration" id="Rename table annotation_tag to annotation_tag_v2 - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.519692744Z level=info msg="Migration successfully executed" id="Rename table annotation_tag to annotation_tag_v2 - v2" duration=4.232358ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.521305466Z level=info msg="Executing migration" id="Create annotation_tag table v3"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.52165328Z level=info msg="Migration successfully executed" id="Create annotation_tag table v3" duration=347.434µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.523330321Z level=info msg="Executing migration" id="create index UQE_annotation_tag_annotation_id_tag_id - Add unique index annotation_tag.annotation_id_tag_id V3"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.523823893Z level=info msg="Migration successfully executed" id="create index UQE_annotation_tag_annotation_id_tag_id - Add unique index annotation_tag.annotation_id_tag_id V3" duration=493.402µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.525466285Z level=info msg="Executing migration" id="copy annotation_tag v2 to v3"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.525654222Z level=info msg="Migration successfully executed" id="copy annotation_tag v2 to v3" duration=187.607µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.527235205Z level=info msg="Executing migration" id="drop table annotation_tag_v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.527558079Z level=info msg="Migration successfully executed" id="drop table annotation_tag_v2" duration=322.634µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.529118823Z level=info msg="Executing migration" id="Update alert annotations and set TEXT to empty"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.52925594Z level=info msg="Migration successfully executed" id="Update alert annotations and set TEXT to empty" duration=137.057µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.530870073Z level=info msg="Executing migration" id="Add created time to annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.532648142Z level=info msg="Migration successfully executed" id="Add created time to annotation table" duration=1.777799ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.534247235Z level=info msg="Executing migration" id="Add updated time to annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.536018055Z level=info msg="Migration successfully executed" id="Add updated time to annotation table" duration=1.77054ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.537619968Z level=info msg="Executing migration" id="Add index for created in annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.53808314Z level=info msg="Migration successfully executed" id="Add index for created in annotation table" duration=462.852µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.53981049Z level=info msg="Executing migration" id="Add index for updated in annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.540293332Z level=info msg="Migration successfully executed" id="Add index for updated in annotation table" duration=483.032µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.541979403Z level=info msg="Executing migration" id="Convert existing annotations from seconds to milliseconds"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.542115661Z level=info msg="Migration successfully executed" id="Convert existing annotations from seconds to milliseconds" duration=136.288µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.543765943Z level=info msg="Executing migration" id="Add epoch_end column"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.545588161Z level=info msg="Migration successfully executed" id="Add epoch_end column" duration=1.821668ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.547211264Z level=info msg="Executing migration" id="Add index for epoch_end"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.547706575Z level=info msg="Migration successfully executed" id="Add index for epoch_end" duration=495.131µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.549329698Z level=info msg="Executing migration" id="Make epoch_end the same as epoch"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.549427946Z level=info msg="Migration successfully executed" id="Make epoch_end the same as epoch" duration=98.438µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.551039588Z level=info msg="Executing migration" id="Move region to single row"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.551268474Z level=info msg="Migration successfully executed" id="Move region to single row" duration=226.597µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.552876457Z level=info msg="Executing migration" id="Remove index org_id_epoch from annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.553344379Z level=info msg="Migration successfully executed" id="Remove index org_id_epoch from annotation table" duration=467.732µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.554968801Z level=info msg="Executing migration" id="Remove index org_id_dashboard_id_panel_id_epoch from annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.555443023Z level=info msg="Migration successfully executed" id="Remove index org_id_dashboard_id_panel_id_epoch from annotation table" duration=474.022µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.557049646Z level=info msg="Executing migration" id="Add index for org_id_dashboard_id_epoch_end_epoch on annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.557557957Z level=info msg="Migration successfully executed" id="Add index for org_id_dashboard_id_epoch_end_epoch on annotation table" duration=507.971µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.559190179Z level=info msg="Executing migration" id="Add index for org_id_epoch_end_epoch on annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.55970073Z level=info msg="Migration successfully executed" id="Add index for org_id_epoch_end_epoch on annotation table" duration=510.142µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.561313203Z level=info msg="Executing migration" id="Remove index org_id_epoch_epoch_end from annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.561773225Z level=info msg="Migration successfully executed" id="Remove index org_id_epoch_epoch_end from annotation table" duration=459.752µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.563420997Z level=info msg="Executing migration" id="Add index for alert_id on annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.563907309Z level=info msg="Migration successfully executed" id="Add index for alert_id on annotation table" duration=486.052µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.565476942Z level=info msg="Executing migration" id="Increase tags column to length 4096"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.565487782Z level=info msg="Migration successfully executed" id="Increase tags column to length 4096" duration=11.34µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.567160763Z level=info msg="Executing migration" id="Increase prev_state column to length 40 not null"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.567170893Z level=info msg="Migration successfully executed" id="Increase prev_state column to length 40 not null" duration=12.35µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.568802275Z level=info msg="Executing migration" id="Increase new_state column to length 40 not null"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.568810985Z level=info msg="Migration successfully executed" id="Increase new_state column to length 40 not null" duration=9.2µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.570413688Z level=info msg="Executing migration" id="Add dashboard_uid column to annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.572227297Z level=info msg="Migration successfully executed" id="Add dashboard_uid column to annotation table" duration=1.813189ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.57379772Z level=info msg="Executing migration" id="Add missing dashboard_uid to annotation table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.57381312Z level=info msg="Starting batched dashboard_uid migration for annotations (newest first)" batchSize=5000
grafana-1     | logger=migrator t=2026-03-18T08:58:41.574315841Z level=info msg="Completed dashboard_uid migration for annotations" totalUpdated=0
grafana-1     | logger=migrator t=2026-03-18T08:58:41.574337251Z level=info msg="Migration successfully executed" id="Add missing dashboard_uid to annotation table" duration=539.941µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.575959643Z level=info msg="Executing migration" id="create test_data table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.576358236Z level=info msg="Migration successfully executed" id="create test_data table" duration=398.423µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.577957679Z level=info msg="Executing migration" id="create dashboard_version table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.578354942Z level=info msg="Migration successfully executed" id="create dashboard_version table v1" duration=396.983µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.580046553Z level=info msg="Executing migration" id="add index dashboard_version.dashboard_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.580517805Z level=info msg="Migration successfully executed" id="add index dashboard_version.dashboard_id" duration=471.112µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.582141907Z level=info msg="Executing migration" id="add unique index dashboard_version.dashboard_id and dashboard_version.version"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.582647849Z level=info msg="Migration successfully executed" id="add unique index dashboard_version.dashboard_id and dashboard_version.version" duration=518.071µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.584301511Z level=info msg="Executing migration" id="Set dashboard version to 1 where 0"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.584411059Z level=info msg="Migration successfully executed" id="Set dashboard version to 1 where 0" duration=109.848µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.586027641Z level=info msg="Executing migration" id="save existing dashboard data in dashboard_version table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.586265267Z level=info msg="Migration successfully executed" id="save existing dashboard data in dashboard_version table v1" duration=237.356µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.58782665Z level=info msg="Executing migration" id="alter dashboard_version.data to mediumtext v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.58783916Z level=info msg="Migration successfully executed" id="alter dashboard_version.data to mediumtext v1" duration=11.85µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.589440823Z level=info msg="Executing migration" id="Add apiVersion for dashboard_version"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.591330361Z level=info msg="Migration successfully executed" id="Add apiVersion for dashboard_version" duration=1.888018ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.592931613Z level=info msg="Executing migration" id="create team table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.593334426Z level=info msg="Migration successfully executed" id="create team table" duration=402.563µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.595036557Z level=info msg="Executing migration" id="add index team.org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.595563598Z level=info msg="Migration successfully executed" id="add index team.org_id" duration=526.861µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.59721753Z level=info msg="Executing migration" id="add unique index team_org_id_name"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.597735961Z level=info msg="Migration successfully executed" id="add unique index team_org_id_name" duration=516.681µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.599373103Z level=info msg="Executing migration" id="Add column uid in team"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.601236891Z level=info msg="Migration successfully executed" id="Add column uid in team" duration=1.863618ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.602821674Z level=info msg="Executing migration" id="Update uid column values in team"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.602926363Z level=info msg="Migration successfully executed" id="Update uid column values in team" duration=104.729µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.604589714Z level=info msg="Executing migration" id="Add unique index team_org_id_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.605053646Z level=info msg="Migration successfully executed" id="Add unique index team_org_id_uid" duration=463.752µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.606739837Z level=info msg="Executing migration" id="Add column external_uid in team"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.608661265Z level=info msg="Migration successfully executed" id="Add column external_uid in team" duration=1.921608ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.610251518Z level=info msg="Executing migration" id="Add column is_provisioned in team"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.612157045Z level=info msg="Migration successfully executed" id="Add column is_provisioned in team" duration=1.905167ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.613810967Z level=info msg="Executing migration" id="create team member table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.61422507Z level=info msg="Migration successfully executed" id="create team member table" duration=413.693µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.61595144Z level=info msg="Executing migration" id="add index team_member.org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.616470251Z level=info msg="Migration successfully executed" id="add index team_member.org_id" duration=518.521µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.618153543Z level=info msg="Executing migration" id="add unique index team_member_org_id_team_id_user_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.618638454Z level=info msg="Migration successfully executed" id="add unique index team_member_org_id_team_id_user_id" duration=484.721µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.620248587Z level=info msg="Executing migration" id="add index team_member.team_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.620699799Z level=info msg="Migration successfully executed" id="add index team_member.team_id" duration=448.832µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.622299702Z level=info msg="Executing migration" id="Add column email to team table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.624331557Z level=info msg="Migration successfully executed" id="Add column email to team table" duration=2.031175ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.625994009Z level=info msg="Executing migration" id="Add column external to team_member table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.627942845Z level=info msg="Migration successfully executed" id="Add column external to team_member table" duration=1.949417ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.629519549Z level=info msg="Executing migration" id="Add column permission to team_member table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.631469305Z level=info msg="Migration successfully executed" id="Add column permission to team_member table" duration=1.949626ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.633079478Z level=info msg="Executing migration" id="add unique index team_member_user_id_org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.633581549Z level=info msg="Migration successfully executed" id="add unique index team_member_user_id_org_id" duration=501.771µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.635258361Z level=info msg="Executing migration" id="Add column uid in team_member"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.637214317Z level=info msg="Migration successfully executed" id="Add column uid in team_member" duration=1.955696ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.63879101Z level=info msg="Executing migration" id="Update uid column values in team_member"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.638910578Z level=info msg="Migration successfully executed" id="Update uid column values in team_member" duration=119.538µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.640501551Z level=info msg="Executing migration" id="Add unique index team_member_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.640962083Z level=info msg="Migration successfully executed" id="Add unique index team_member_uid" duration=460.392µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.642616305Z level=info msg="Executing migration" id="create dashboard acl table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.643012198Z level=info msg="Migration successfully executed" id="create dashboard acl table" duration=395.703µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.64467852Z level=info msg="Executing migration" id="add index dashboard_acl_dashboard_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.645158702Z level=info msg="Migration successfully executed" id="add index dashboard_acl_dashboard_id" duration=480.072µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.646773544Z level=info msg="Executing migration" id="add unique index dashboard_acl_dashboard_id_user_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.647270016Z level=info msg="Migration successfully executed" id="add unique index dashboard_acl_dashboard_id_user_id" duration=496.102µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.648920807Z level=info msg="Executing migration" id="add unique index dashboard_acl_dashboard_id_team_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.649425269Z level=info msg="Migration successfully executed" id="add unique index dashboard_acl_dashboard_id_team_id" duration=504.232µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.651056711Z level=info msg="Executing migration" id="add index dashboard_acl_user_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.651556352Z level=info msg="Migration successfully executed" id="add index dashboard_acl_user_id" duration=499.561µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.653174575Z level=info msg="Executing migration" id="add index dashboard_acl_team_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.653637777Z level=info msg="Migration successfully executed" id="add index dashboard_acl_team_id" duration=463.892µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.655254479Z level=info msg="Executing migration" id="add index dashboard_acl_org_id_role"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.655725041Z level=info msg="Migration successfully executed" id="add index dashboard_acl_org_id_role" duration=468.962µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.657325334Z level=info msg="Executing migration" id="add index dashboard_permission"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.657793766Z level=info msg="Migration successfully executed" id="add index dashboard_permission" duration=468.212µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.659575605Z level=info msg="Executing migration" id="save default acl rules in dashboard_acl table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.65988381Z level=info msg="Migration successfully executed" id="save default acl rules in dashboard_acl table" duration=307.975µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.661463453Z level=info msg="Executing migration" id="delete acl rules for deleted dashboards and folders"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.661592741Z level=info msg="Migration successfully executed" id="delete acl rules for deleted dashboards and folders" duration=129.228µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.663234463Z level=info msg="Executing migration" id="create tag table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.663619266Z level=info msg="Migration successfully executed" id="create tag table" duration=384.463µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.665254358Z level=info msg="Executing migration" id="add index tag.key_value"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.66574241Z level=info msg="Migration successfully executed" id="add index tag.key_value" duration=487.862µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.667374312Z level=info msg="Executing migration" id="create login attempt table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.667800575Z level=info msg="Migration successfully executed" id="create login attempt table" duration=425.843µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.669579625Z level=info msg="Executing migration" id="add index login_attempt.username"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.670073976Z level=info msg="Migration successfully executed" id="add index login_attempt.username" duration=496.181µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.671749798Z level=info msg="Executing migration" id="drop index IDX_login_attempt_username - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.672258789Z level=info msg="Migration successfully executed" id="drop index IDX_login_attempt_username - v1" duration=508.731µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.673823632Z level=info msg="Executing migration" id="Rename table login_attempt to login_attempt_tmp_qwerty - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.67923783Z level=info msg="Migration successfully executed" id="Rename table login_attempt to login_attempt_tmp_qwerty - v1" duration=5.412208ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.681078978Z level=info msg="Executing migration" id="create login_attempt v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.681523681Z level=info msg="Migration successfully executed" id="create login_attempt v2" duration=444.493µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.683180053Z level=info msg="Executing migration" id="create index IDX_login_attempt_username - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.683646275Z level=info msg="Migration successfully executed" id="create index IDX_login_attempt_username - v2" duration=466.092µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.685273297Z level=info msg="Executing migration" id="copy login_attempt v1 to v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.685466513Z level=info msg="Migration successfully executed" id="copy login_attempt v1 to v2" duration=192.956µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.687025517Z level=info msg="Executing migration" id="drop login_attempt_tmp_qwerty"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.68741415Z level=info msg="Migration successfully executed" id="drop login_attempt_tmp_qwerty" duration=388.313µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.689146771Z level=info msg="Executing migration" id="increase login_attempt.ip_address column length for IPv6 support"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.68915909Z level=info msg="Migration successfully executed" id="increase login_attempt.ip_address column length for IPv6 support" duration=12.859µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.690819692Z level=info msg="Executing migration" id="alter table login_attempt alter column created type to bigint"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.690831762Z level=info msg="Migration successfully executed" id="alter table login_attempt alter column created type to bigint" duration=12.9µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.692471934Z level=info msg="Executing migration" id="create user auth table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.692889067Z level=info msg="Migration successfully executed" id="create user auth table" duration=415.723µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.694495359Z level=info msg="Executing migration" id="create index IDX_user_auth_auth_module_auth_id - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.695008311Z level=info msg="Migration successfully executed" id="create index IDX_user_auth_auth_module_auth_id - v1" duration=512.962µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.696756821Z level=info msg="Executing migration" id="alter user_auth.auth_id to length 190"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.696769451Z level=info msg="Migration successfully executed" id="alter user_auth.auth_id to length 190" duration=12.92µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.698416672Z level=info msg="Executing migration" id="Add OAuth access token to user_auth"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.700575596Z level=info msg="Migration successfully executed" id="Add OAuth access token to user_auth" duration=2.158574ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.702185858Z level=info msg="Executing migration" id="Add OAuth refresh token to user_auth"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.704358951Z level=info msg="Migration successfully executed" id="Add OAuth refresh token to user_auth" duration=2.172923ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.706036252Z level=info msg="Executing migration" id="Add OAuth token type to user_auth"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.708221475Z level=info msg="Migration successfully executed" id="Add OAuth token type to user_auth" duration=2.184603ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.710004235Z level=info msg="Executing migration" id="Add OAuth expiry to user_auth"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.712172967Z level=info msg="Migration successfully executed" id="Add OAuth expiry to user_auth" duration=2.166043ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.713850889Z level=info msg="Executing migration" id="Add index to user_id column in user_auth"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.71436596Z level=info msg="Migration successfully executed" id="Add index to user_id column in user_auth" duration=515.241µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.716023302Z level=info msg="Executing migration" id="Add OAuth ID token to user_auth"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.718163895Z level=info msg="Migration successfully executed" id="Add OAuth ID token to user_auth" duration=2.140483ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.72025084Z level=info msg="Executing migration" id="Add user_unique_id to user_auth"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.722642449Z level=info msg="Migration successfully executed" id="Add user_unique_id to user_auth" duration=2.388129ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.724257591Z level=info msg="Executing migration" id="Add user_uid to user_auth"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.726444884Z level=info msg="Migration successfully executed" id="Add user_uid to user_auth" duration=2.187193ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.728080186Z level=info msg="Executing migration" id="Populate user_uid in user_auth from user table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.728329912Z level=info msg="Migration successfully executed" id="Populate user_uid in user_auth from user table" duration=249.556µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.729990363Z level=info msg="Executing migration" id="create server_lock table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.730437726Z level=info msg="Migration successfully executed" id="create server_lock table" duration=456.882µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.732238525Z level=info msg="Executing migration" id="add index server_lock.operation_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.732745756Z level=info msg="Migration successfully executed" id="add index server_lock.operation_uid" duration=506.911µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.734465207Z level=info msg="Executing migration" id="create user auth token table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.734954139Z level=info msg="Migration successfully executed" id="create user auth token table" duration=488.642µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.73663486Z level=info msg="Executing migration" id="add unique index user_auth_token.auth_token"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.737119002Z level=info msg="Migration successfully executed" id="add unique index user_auth_token.auth_token" duration=483.872µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.738787353Z level=info msg="Executing migration" id="add unique index user_auth_token.prev_auth_token"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.739292455Z level=info msg="Migration successfully executed" id="add unique index user_auth_token.prev_auth_token" duration=505.082µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.740971606Z level=info msg="Executing migration" id="add index user_auth_token.user_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.741463037Z level=info msg="Migration successfully executed" id="add index user_auth_token.user_id" duration=491.171µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.743123479Z level=info msg="Executing migration" id="Add revoked_at to the user auth token"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.745385011Z level=info msg="Migration successfully executed" id="Add revoked_at to the user auth token" duration=2.261272ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.747039212Z level=info msg="Executing migration" id="add index user_auth_token.revoked_at"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.747550624Z level=info msg="Migration successfully executed" id="add index user_auth_token.revoked_at" duration=512.702µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.749246045Z level=info msg="Executing migration" id="add external_session_id to user_auth_token"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.751488166Z level=info msg="Migration successfully executed" id="add external_session_id to user_auth_token" duration=2.241401ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.753121638Z level=info msg="Executing migration" id="create cache_data table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.753578441Z level=info msg="Migration successfully executed" id="create cache_data table" duration=456.613µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.755285721Z level=info msg="Executing migration" id="add unique index cache_data.cache_key"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.755821632Z level=info msg="Migration successfully executed" id="add unique index cache_data.cache_key" duration=535.531µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.757528983Z level=info msg="Executing migration" id="create short_url table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.757946796Z level=info msg="Migration successfully executed" id="create short_url table v1" duration=417.403µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.759612798Z level=info msg="Executing migration" id="add index short_url.org_id-uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.760109839Z level=info msg="Migration successfully executed" id="add index short_url.org_id-uid" duration=496.721µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.761775511Z level=info msg="Executing migration" id="alter table short_url alter column created_by type to bigint"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.76178764Z level=info msg="Migration successfully executed" id="alter table short_url alter column created_by type to bigint" duration=12.599µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.763470182Z level=info msg="Executing migration" id="delete alert_definition table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.763525161Z level=info msg="Migration successfully executed" id="delete alert_definition table" duration=55.169µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.765181083Z level=info msg="Executing migration" id="recreate alert_definition table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.765636775Z level=info msg="Migration successfully executed" id="recreate alert_definition table" duration=453.962µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.767333006Z level=info msg="Executing migration" id="add index in alert_definition on org_id and title columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.767859667Z level=info msg="Migration successfully executed" id="add index in alert_definition on org_id and title columns" duration=526.401µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.769606667Z level=info msg="Executing migration" id="add index in alert_definition on org_id and uid columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.770107908Z level=info msg="Migration successfully executed" id="add index in alert_definition on org_id and uid columns" duration=499.211µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.771851349Z level=info msg="Executing migration" id="alter alert_definition table data column to mediumtext in mysql"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.771862918Z level=info msg="Migration successfully executed" id="alter alert_definition table data column to mediumtext in mysql" duration=11.919µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.7735078Z level=info msg="Executing migration" id="drop index in alert_definition on org_id and title columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.774018052Z level=info msg="Migration successfully executed" id="drop index in alert_definition on org_id and title columns" duration=510.282µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.775702343Z level=info msg="Executing migration" id="drop index in alert_definition on org_id and uid columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.776213964Z level=info msg="Migration successfully executed" id="drop index in alert_definition on org_id and uid columns" duration=511.251µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.777841706Z level=info msg="Executing migration" id="add unique index in alert_definition on org_id and title columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.778366807Z level=info msg="Migration successfully executed" id="add unique index in alert_definition on org_id and title columns" duration=524.641µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.77997005Z level=info msg="Executing migration" id="add unique index in alert_definition on org_id and uid columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.780480661Z level=info msg="Migration successfully executed" id="add unique index in alert_definition on org_id and uid columns" duration=510.351µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.782158253Z level=info msg="Executing migration" id="Add column paused in alert_definition"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.784543642Z level=info msg="Migration successfully executed" id="Add column paused in alert_definition" duration=2.385289ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.786172994Z level=info msg="Executing migration" id="drop alert_definition table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.786754334Z level=info msg="Migration successfully executed" id="drop alert_definition table" duration=580.26µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.788421396Z level=info msg="Executing migration" id="delete alert_definition_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.788475425Z level=info msg="Migration successfully executed" id="delete alert_definition_version table" duration=54.219µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.790124627Z level=info msg="Executing migration" id="recreate alert_definition_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.790597799Z level=info msg="Migration successfully executed" id="recreate alert_definition_version table" duration=472.922µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.792241941Z level=info msg="Executing migration" id="add index in alert_definition_version table on alert_definition_id and version columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.792756432Z level=info msg="Migration successfully executed" id="add index in alert_definition_version table on alert_definition_id and version columns" duration=514.631µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.794341645Z level=info msg="Executing migration" id="add index in alert_definition_version table on alert_definition_uid and version columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.794835516Z level=info msg="Migration successfully executed" id="add index in alert_definition_version table on alert_definition_uid and version columns" duration=493.581µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.796537527Z level=info msg="Executing migration" id="alter alert_definition_version table data column to mediumtext in mysql"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.796553417Z level=info msg="Migration successfully executed" id="alter alert_definition_version table data column to mediumtext in mysql" duration=15.34µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.798221168Z level=info msg="Executing migration" id="drop alert_definition_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.798790989Z level=info msg="Migration successfully executed" id="drop alert_definition_version table" duration=569.201µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.8004719Z level=info msg="Executing migration" id="create alert_instance table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.800961402Z level=info msg="Migration successfully executed" id="create alert_instance table" duration=489.132µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.802631123Z level=info msg="Executing migration" id="add index in alert_instance table on def_org_id, def_uid and current_state columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.803147494Z level=info msg="Migration successfully executed" id="add index in alert_instance table on def_org_id, def_uid and current_state columns" duration=516.071µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.804761007Z level=info msg="Executing migration" id="add index in alert_instance table on def_org_id, current_state columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.805268488Z level=info msg="Migration successfully executed" id="add index in alert_instance table on def_org_id, current_state columns" duration=507.201µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.806979029Z level=info msg="Executing migration" id="add column current_state_end to alert_instance"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.809359708Z level=info msg="Migration successfully executed" id="add column current_state_end to alert_instance" duration=2.380279ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.8110018Z level=info msg="Executing migration" id="remove index def_org_id, def_uid, current_state on alert_instance"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.811563011Z level=info msg="Migration successfully executed" id="remove index def_org_id, def_uid, current_state on alert_instance" duration=561.871µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.813224142Z level=info msg="Executing migration" id="remove index def_org_id, current_state on alert_instance"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.813715734Z level=info msg="Migration successfully executed" id="remove index def_org_id, current_state on alert_instance" duration=491.592µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.815357866Z level=info msg="Executing migration" id="rename def_org_id to rule_org_id in alert_instance"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.826542035Z level=info msg="Migration successfully executed" id="rename def_org_id to rule_org_id in alert_instance" duration=11.182779ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.828217596Z level=info msg="Executing migration" id="rename def_uid to rule_uid in alert_instance"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.838486461Z level=info msg="Migration successfully executed" id="rename def_uid to rule_uid in alert_instance" duration=10.268105ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.840348919Z level=info msg="Executing migration" id="add index rule_org_id, rule_uid, current_state on alert_instance"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.84087507Z level=info msg="Migration successfully executed" id="add index rule_org_id, rule_uid, current_state on alert_instance" duration=525.891µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.842483853Z level=info msg="Executing migration" id="add index rule_org_id, current_state on alert_instance"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.842983664Z level=info msg="Migration successfully executed" id="add index rule_org_id, current_state on alert_instance" duration=499.431µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.844597037Z level=info msg="Executing migration" id="add current_reason column related to current_state"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.847074364Z level=info msg="Migration successfully executed" id="add current_reason column related to current_state" duration=2.477017ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.848735606Z level=info msg="Executing migration" id="add result_fingerprint column to alert_instance"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.851096236Z level=info msg="Migration successfully executed" id="add result_fingerprint column to alert_instance" duration=2.36033ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.852789167Z level=info msg="Executing migration" id="create alert_rule table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.853281468Z level=info msg="Migration successfully executed" id="create alert_rule table" duration=492.082µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.855009229Z level=info msg="Executing migration" id="add index in alert_rule on org_id and title columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.85555177Z level=info msg="Migration successfully executed" id="add index in alert_rule on org_id and title columns" duration=542.121µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.857321789Z level=info msg="Executing migration" id="add index in alert_rule on org_id and uid columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.857816091Z level=info msg="Migration successfully executed" id="add index in alert_rule on org_id and uid columns" duration=494.341µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.859533692Z level=info msg="Executing migration" id="add index in alert_rule on org_id, namespace_uid, group_uid columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.860058473Z level=info msg="Migration successfully executed" id="add index in alert_rule on org_id, namespace_uid, group_uid columns" duration=524.511µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.861763604Z level=info msg="Executing migration" id="alter alert_rule table data column to mediumtext in mysql"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.861776083Z level=info msg="Migration successfully executed" id="alter alert_rule table data column to mediumtext in mysql" duration=12.889µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.863463255Z level=info msg="Executing migration" id="add column for to alert_rule"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.866013251Z level=info msg="Migration successfully executed" id="add column for to alert_rule" duration=2.549926ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.867659303Z level=info msg="Executing migration" id="add column annotations to alert_rule"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.870223679Z level=info msg="Migration successfully executed" id="add column annotations to alert_rule" duration=2.569196ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.871871091Z level=info msg="Executing migration" id="add column labels to alert_rule"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.874359909Z level=info msg="Migration successfully executed" id="add column labels to alert_rule" duration=2.488508ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.87601568Z level=info msg="Executing migration" id="remove unique index from alert_rule on org_id, title columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.876557551Z level=info msg="Migration successfully executed" id="remove unique index from alert_rule on org_id, title columns" duration=542.121µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.878191553Z level=info msg="Executing migration" id="add index in alert_rule on org_id, namespase_uid and title columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.878750074Z level=info msg="Migration successfully executed" id="add index in alert_rule on org_id, namespase_uid and title columns" duration=558.081µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.880529153Z level=info msg="Executing migration" id="add dashboard_uid column to alert_rule"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.88305894Z level=info msg="Migration successfully executed" id="add dashboard_uid column to alert_rule" duration=2.529477ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.884710632Z level=info msg="Executing migration" id="add panel_id column to alert_rule"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.88717378Z level=info msg="Migration successfully executed" id="add panel_id column to alert_rule" duration=2.462988ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.888817542Z level=info msg="Executing migration" id="add index in alert_rule on org_id, dashboard_uid and panel_id columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.889369562Z level=info msg="Migration successfully executed" id="add index in alert_rule on org_id, dashboard_uid and panel_id columns" duration=551.6µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.891123782Z level=info msg="Executing migration" id="add rule_group_idx column to alert_rule"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.893578391Z level=info msg="Migration successfully executed" id="add rule_group_idx column to alert_rule" duration=2.454299ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.895225432Z level=info msg="Executing migration" id="add is_paused column to alert_rule table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.897788639Z level=info msg="Migration successfully executed" id="add is_paused column to alert_rule table" duration=2.562857ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.899419461Z level=info msg="Executing migration" id="fix is_paused column for alert_rule table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.899431271Z level=info msg="Migration successfully executed" id="fix is_paused column for alert_rule table" duration=12.16µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.901066723Z level=info msg="Executing migration" id="alter table alert_rule alter column rule_group_idx type to bigint"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.901078562Z level=info msg="Migration successfully executed" id="alter table alert_rule alter column rule_group_idx type to bigint" duration=12.189µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.902799973Z level=info msg="Executing migration" id="create alert_rule_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.903344074Z level=info msg="Migration successfully executed" id="create alert_rule_version table" duration=544.821µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.905073064Z level=info msg="Executing migration" id="add index in alert_rule_version table on rule_org_id, rule_uid and version columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.905629005Z level=info msg="Migration successfully executed" id="add index in alert_rule_version table on rule_org_id, rule_uid and version columns" duration=555.651µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.907296786Z level=info msg="Executing migration" id="add index in alert_rule_version table on rule_org_id, rule_namespace_uid and rule_group columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.907803068Z level=info msg="Migration successfully executed" id="add index in alert_rule_version table on rule_org_id, rule_namespace_uid and rule_group columns" duration=505.962µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.909472679Z level=info msg="Executing migration" id="alter alert_rule_version table data column to mediumtext in mysql"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.909484239Z level=info msg="Migration successfully executed" id="alter alert_rule_version table data column to mediumtext in mysql" duration=12.22µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.91116149Z level=info msg="Executing migration" id="add column for to alert_rule_version"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.913834955Z level=info msg="Migration successfully executed" id="add column for to alert_rule_version" duration=2.672275ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.915488356Z level=info msg="Executing migration" id="add column annotations to alert_rule_version"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.918033103Z level=info msg="Migration successfully executed" id="add column annotations to alert_rule_version" duration=2.544146ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.919710504Z level=info msg="Executing migration" id="add column labels to alert_rule_version"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.922264811Z level=info msg="Migration successfully executed" id="add column labels to alert_rule_version" duration=2.553667ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.923971932Z level=info msg="Executing migration" id="add rule_group_idx column to alert_rule_version"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.926707335Z level=info msg="Migration successfully executed" id="add rule_group_idx column to alert_rule_version" duration=2.733413ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.928340007Z level=info msg="Executing migration" id="add is_paused column to alert_rule_versions table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.930939883Z level=info msg="Migration successfully executed" id="add is_paused column to alert_rule_versions table" duration=2.599386ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.932629474Z level=info msg="Executing migration" id="fix is_paused column for alert_rule_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.932641874Z level=info msg="Migration successfully executed" id="fix is_paused column for alert_rule_version table" duration=12.94µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.934307305Z level=info msg="Executing migration" id="alter table alert_rule_version alter column rule_group_idx type to bigint"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.934325445Z level=info msg="Migration successfully executed" id="alter table alert_rule_version alter column rule_group_idx type to bigint" duration=18.75µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.935968977Z level=info msg="Executing migration" id=create_alert_configuration_table
grafana-1     | logger=migrator t=2026-03-18T08:58:41.936428009Z level=info msg="Migration successfully executed" id=create_alert_configuration_table duration=458.842µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.938092761Z level=info msg="Executing migration" id="Add column default in alert_configuration"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.940688376Z level=info msg="Migration successfully executed" id="Add column default in alert_configuration" duration=2.596135ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.942393317Z level=info msg="Executing migration" id="alert alert_configuration alertmanager_configuration column from TEXT to MEDIUMTEXT if mysql"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.942407747Z level=info msg="Migration successfully executed" id="alert alert_configuration alertmanager_configuration column from TEXT to MEDIUMTEXT if mysql" duration=15.18µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.944075488Z level=info msg="Executing migration" id="add column org_id in alert_configuration"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.946810382Z level=info msg="Migration successfully executed" id="add column org_id in alert_configuration" duration=2.734104ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.948456674Z level=info msg="Executing migration" id="add index in alert_configuration table on org_id column"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.949009654Z level=info msg="Migration successfully executed" id="add index in alert_configuration table on org_id column" duration=554.56µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.950859393Z level=info msg="Executing migration" id="add configuration_hash column to alert_configuration"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.953610266Z level=info msg="Migration successfully executed" id="add configuration_hash column to alert_configuration" duration=2.749993ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.955342966Z level=info msg="Executing migration" id=create_ngalert_configuration_table
grafana-1     | logger=migrator t=2026-03-18T08:58:41.955763479Z level=info msg="Migration successfully executed" id=create_ngalert_configuration_table duration=420.153µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.957413141Z level=info msg="Executing migration" id="add index in ngalert_configuration on org_id column"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.958006131Z level=info msg="Migration successfully executed" id="add index in ngalert_configuration on org_id column" duration=592.56µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.959760581Z level=info msg="Executing migration" id="add column send_alerts_to in ngalert_configuration"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.962404745Z level=info msg="Migration successfully executed" id="add column send_alerts_to in ngalert_configuration" duration=2.643755ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.964028738Z level=info msg="Executing migration" id="create provenance_type table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.964443121Z level=info msg="Migration successfully executed" id="create provenance_type table" duration=414.353µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.966125832Z level=info msg="Executing migration" id="add index to uniquify (record_key, record_type, org_id) columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.966694402Z level=info msg="Migration successfully executed" id="add index to uniquify (record_key, record_type, org_id) columns" duration=568.35µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.968365334Z level=info msg="Executing migration" id="create alert_image table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.968765597Z level=info msg="Migration successfully executed" id="create alert_image table" duration=400.223µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.970391959Z level=info msg="Executing migration" id="add unique index on token to alert_image table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.97090241Z level=info msg="Migration successfully executed" id="add unique index on token to alert_image table" duration=510.261µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.972583842Z level=info msg="Executing migration" id="support longer URLs in alert_image table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.972597562Z level=info msg="Migration successfully executed" id="support longer URLs in alert_image table" duration=14.24µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.974271803Z level=info msg="Executing migration" id=create_alert_configuration_history_table
grafana-1     | logger=migrator t=2026-03-18T08:58:41.974752665Z level=info msg="Migration successfully executed" id=create_alert_configuration_history_table duration=480.612µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.976493055Z level=info msg="Executing migration" id="drop non-unique orgID index on alert_configuration"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.977040506Z level=info msg="Migration successfully executed" id="drop non-unique orgID index on alert_configuration" duration=546.781µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.978674688Z level=info msg="Executing migration" id="drop unique orgID index on alert_configuration if exists"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.978868514Z level=warn msg="Skipping migration: Already executed, but not recorded in migration log" id="drop unique orgID index on alert_configuration if exists"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.980512116Z level=info msg="Executing migration" id="extract alertmanager configuration history to separate table"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.980808121Z level=info msg="Migration successfully executed" id="extract alertmanager configuration history to separate table" duration=295.705µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.982415984Z level=info msg="Executing migration" id="add unique index on orgID to alert_configuration"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.982939935Z level=info msg="Migration successfully executed" id="add unique index on orgID to alert_configuration" duration=523.641µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.984572647Z level=info msg="Executing migration" id="add last_applied column to alert_configuration_history"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.987470968Z level=info msg="Migration successfully executed" id="add last_applied column to alert_configuration_history" duration=2.897991ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.98906537Z level=info msg="Executing migration" id="add message column to alert_rule_version"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.99202722Z level=info msg="Migration successfully executed" id="add message column to alert_rule_version" duration=2.9614ms
grafana-1     | logger=migrator t=2026-03-18T08:58:41.993674202Z level=info msg="Executing migration" id="create library_element table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.994115674Z level=info msg="Migration successfully executed" id="create library_element table v1" duration=441.222µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.995831265Z level=info msg="Executing migration" id="add index library_element org_id-folder_id-name-kind"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.996397825Z level=info msg="Migration successfully executed" id="add index library_element org_id-folder_id-name-kind" duration=566.09µs
grafana-1     | logger=migrator t=2026-03-18T08:58:41.998056237Z level=info msg="Executing migration" id="create library_element_connection table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:41.998492649Z level=info msg="Migration successfully executed" id="create library_element_connection table v1" duration=436.122µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.00022264Z level=info msg="Executing migration" id="add index library_element_connection element_id-kind-connection_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.000751261Z level=info msg="Migration successfully executed" id="add index library_element_connection element_id-kind-connection_id" duration=532.971µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.002382903Z level=info msg="Executing migration" id="add unique index library_element org_id_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.002907434Z level=info msg="Migration successfully executed" id="add unique index library_element org_id_uid" duration=516.661µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.004605205Z level=info msg="Executing migration" id="increase max description length to 2048"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.004621485Z level=info msg="Migration successfully executed" id="increase max description length to 2048" duration=16.75µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.006270637Z level=info msg="Executing migration" id="alter library_element model to mediumtext"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.006282886Z level=info msg="Migration successfully executed" id="alter library_element model to mediumtext" duration=12.489µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.007995687Z level=info msg="Executing migration" id="add library_element folder uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.010980756Z level=info msg="Migration successfully executed" id="add library_element folder uid" duration=2.984069ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.012610308Z level=info msg="Executing migration" id="populate library_element folder_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.012854984Z level=info msg="Migration successfully executed" id="populate library_element folder_uid" duration=244.406µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.014486846Z level=info msg="Executing migration" id="add index library_element org_id-folder_uid-name-kind"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.015045317Z level=info msg="Migration successfully executed" id="add index library_element org_id-folder_uid-name-kind" duration=558.021µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.016752888Z level=info msg="Executing migration" id="drop unique name in folder index (id)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.017308198Z level=info msg="Migration successfully executed" id="drop unique name in folder index (id)" duration=554.95µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.01896366Z level=info msg="Executing migration" id="drop unique name in folder index"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.019511571Z level=info msg="Migration successfully executed" id="drop unique name in folder index" duration=547.471µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.021141053Z level=info msg="Executing migration" id="clone move dashboard alerts to unified alerting"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.02131692Z level=info msg="Migration successfully executed" id="clone move dashboard alerts to unified alerting" duration=174.407µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.022958102Z level=info msg="Executing migration" id="create data_keys table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.023455453Z level=info msg="Migration successfully executed" id="create data_keys table" duration=497.081µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.025201463Z level=info msg="Executing migration" id="create secrets table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.025612876Z level=info msg="Migration successfully executed" id="create secrets table" duration=411.473µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.027310507Z level=info msg="Executing migration" id="rename data_keys name column to id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.041985917Z level=info msg="Migration successfully executed" id="rename data_keys name column to id" duration=14.6741ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.043854735Z level=info msg="Executing migration" id="add name column into data_keys"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.046891443Z level=info msg="Migration successfully executed" id="add name column into data_keys" duration=3.030808ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.048506916Z level=info msg="Executing migration" id="copy data_keys id column values into name"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.048597544Z level=info msg="Migration successfully executed" id="copy data_keys id column values into name" duration=90.738µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.050235136Z level=info msg="Executing migration" id="rename data_keys name column to label"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.063375072Z level=info msg="Migration successfully executed" id="rename data_keys name column to label" duration=13.139036ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.06522164Z level=info msg="Executing migration" id="rename data_keys id column back to name"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.078935886Z level=info msg="Migration successfully executed" id="rename data_keys id column back to name" duration=13.712896ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.080865323Z level=info msg="Executing migration" id="create kv_store table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.081342505Z level=info msg="Migration successfully executed" id="create kv_store table v1" duration=477.352µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.083226523Z level=info msg="Executing migration" id="add index kv_store.org_id-namespace-key"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.083791543Z level=info msg="Migration successfully executed" id="add index kv_store.org_id-namespace-key" duration=564.72µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.085470514Z level=info msg="Executing migration" id="update dashboard_uid and panel_id from existing annotations"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.085615682Z level=info msg="Migration successfully executed" id="update dashboard_uid and panel_id from existing annotations" duration=145.188µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.087254854Z level=info msg="Executing migration" id="create permission table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.087666787Z level=info msg="Migration successfully executed" id="create permission table" duration=411.753µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.089370828Z level=info msg="Executing migration" id="add unique index permission.role_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.089966078Z level=info msg="Migration successfully executed" id="add unique index permission.role_id" duration=595.13µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.091673289Z level=info msg="Executing migration" id="add unique index role_id_action_scope"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.092245709Z level=info msg="Migration successfully executed" id="add unique index role_id_action_scope" duration=572.1µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.093901981Z level=info msg="Executing migration" id="create role table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.094423032Z level=info msg="Migration successfully executed" id="create role table" duration=520.851µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.096232571Z level=info msg="Executing migration" id="add column display_name"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.0992083Z level=info msg="Migration successfully executed" id="add column display_name" duration=2.975069ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.100928501Z level=info msg="Executing migration" id="add column group_name"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.103973329Z level=info msg="Migration successfully executed" id="add column group_name" duration=3.044268ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.1056362Z level=info msg="Executing migration" id="add index role.org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.106172851Z level=info msg="Migration successfully executed" id="add index role.org_id" duration=536.511µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.107868972Z level=info msg="Executing migration" id="add unique index role_org_id_name"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.108458002Z level=info msg="Migration successfully executed" id="add unique index role_org_id_name" duration=588.65µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.110160623Z level=info msg="Executing migration" id="add index role_org_id_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.110714244Z level=info msg="Migration successfully executed" id="add index role_org_id_uid" duration=553.891µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.112382355Z level=info msg="Executing migration" id="create team role table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.112791088Z level=info msg="Migration successfully executed" id="create team role table" duration=408.403µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.114504539Z level=info msg="Executing migration" id="add index team_role.org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.1150295Z level=info msg="Migration successfully executed" id="add index team_role.org_id" duration=524.741µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.11738467Z level=info msg="Executing migration" id="add unique index team_role_org_id_team_id_role_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.11792019Z level=info msg="Migration successfully executed" id="add unique index team_role_org_id_team_id_role_id" duration=535.081µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.119599992Z level=info msg="Executing migration" id="add index team_role.team_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.120116383Z level=info msg="Migration successfully executed" id="add index team_role.team_id" duration=516.091µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.121815454Z level=info msg="Executing migration" id="create user role table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.122237237Z level=info msg="Migration successfully executed" id="create user role table" duration=421.603µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.123952568Z level=info msg="Executing migration" id="add index user_role.org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.124487758Z level=info msg="Migration successfully executed" id="add index user_role.org_id" duration=536.31µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.12615442Z level=info msg="Executing migration" id="add unique index user_role_org_id_user_id_role_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.126692991Z level=info msg="Migration successfully executed" id="add unique index user_role_org_id_user_id_role_id" duration=537.961µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.128408961Z level=info msg="Executing migration" id="add index user_role.user_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.128928343Z level=info msg="Migration successfully executed" id="add index user_role.user_id" duration=519.362µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.130552505Z level=info msg="Executing migration" id="create builtin role table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.130955798Z level=info msg="Migration successfully executed" id="create builtin role table" duration=403.173µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.132684538Z level=info msg="Executing migration" id="add index builtin_role.role_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.133235549Z level=info msg="Migration successfully executed" id="add index builtin_role.role_id" duration=550.961µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.134875911Z level=info msg="Executing migration" id="add index builtin_role.name"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.135488941Z level=info msg="Migration successfully executed" id="add index builtin_role.name" duration=612.63µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.137199911Z level=info msg="Executing migration" id="Add column org_id to builtin_role table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.140428926Z level=info msg="Migration successfully executed" id="Add column org_id to builtin_role table" duration=3.228775ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.142046549Z level=info msg="Executing migration" id="add index builtin_role.org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.142601529Z level=info msg="Migration successfully executed" id="add index builtin_role.org_id" duration=554.73µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.144264331Z level=info msg="Executing migration" id="add unique index builtin_role_org_id_role_id_role"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.144846771Z level=info msg="Migration successfully executed" id="add unique index builtin_role_org_id_role_id_role" duration=582.29µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.14662255Z level=info msg="Executing migration" id="Remove unique index role_org_id_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.147170201Z level=info msg="Migration successfully executed" id="Remove unique index role_org_id_uid" duration=547.371µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.148779644Z level=info msg="Executing migration" id="add unique index role.uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.149337074Z level=info msg="Migration successfully executed" id="add unique index role.uid" duration=557.31µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.150934057Z level=info msg="Executing migration" id="create seed assignment table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.1513637Z level=info msg="Migration successfully executed" id="create seed assignment table" duration=429.343µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.153056661Z level=info msg="Executing migration" id="add unique index builtin_role_role_name"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.153605951Z level=info msg="Migration successfully executed" id="add unique index builtin_role_role_name" duration=547.78µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.155306262Z level=info msg="Executing migration" id="add column hidden to role table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.158555437Z level=info msg="Migration successfully executed" id="add column hidden to role table" duration=3.248725ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.160189019Z level=info msg="Executing migration" id="permission kind migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.163430484Z level=info msg="Migration successfully executed" id="permission kind migration" duration=3.241035ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.165047786Z level=info msg="Executing migration" id="permission attribute migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.16830098Z level=info msg="Migration successfully executed" id="permission attribute migration" duration=3.252924ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.169964262Z level=info msg="Executing migration" id="permission identifier migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.173247396Z level=info msg="Migration successfully executed" id="permission identifier migration" duration=3.282764ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.174965227Z level=info msg="Executing migration" id="add permission identifier index"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.175544247Z level=info msg="Migration successfully executed" id="add permission identifier index" duration=578.71µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.177237638Z level=info msg="Executing migration" id="add permission action scope role_id index"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.177818378Z level=info msg="Migration successfully executed" id="add permission action scope role_id index" duration=580.27µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.179533859Z level=info msg="Executing migration" id="remove permission role_id action scope index"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.180073769Z level=info msg="Migration successfully executed" id="remove permission role_id action scope index" duration=539.79µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.181725421Z level=info msg="Executing migration" id="add group mapping UID column to user_role table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.185036155Z level=info msg="Migration successfully executed" id="add group mapping UID column to user_role table" duration=3.310414ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.186766765Z level=info msg="Executing migration" id="add user_role org ID, user ID, role ID, group mapping UID index"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.187368795Z level=info msg="Migration successfully executed" id="add user_role org ID, user ID, role ID, group mapping UID index" duration=601.79µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.188996317Z level=info msg="Executing migration" id="remove user_role org ID, user ID, role ID index"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.189551658Z level=info msg="Migration successfully executed" id="remove user_role org ID, user ID, role ID index" duration=555.031µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.19119234Z level=info msg="Executing migration" id="add permission role_id action index"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.19172942Z level=info msg="Migration successfully executed" id="add permission role_id action index" duration=536.8µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.193409022Z level=info msg="Executing migration" id="Remove permission role_id index"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.193956862Z level=info msg="Migration successfully executed" id="Remove permission role_id index" duration=547.81µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.195648354Z level=info msg="Executing migration" id="create query_history table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.196110756Z level=info msg="Migration successfully executed" id="create query_history table v1" duration=461.882µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.197806347Z level=info msg="Executing migration" id="add index query_history.org_id-created_by-datasource_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.198430546Z level=info msg="Migration successfully executed" id="add index query_history.org_id-created_by-datasource_uid" duration=622.199µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.200117757Z level=info msg="Executing migration" id="alter table query_history alter column created_by type to bigint"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.200142457Z level=info msg="Migration successfully executed" id="alter table query_history alter column created_by type to bigint" duration=23.97µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.201786959Z level=info msg="Executing migration" id="create query_history_details table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.202213721Z level=info msg="Migration successfully executed" id="create query_history_details table v1" duration=426.452µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.203982601Z level=info msg="Executing migration" id="rbac disabled migrator"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.204006481Z level=info msg="Migration successfully executed" id="rbac disabled migrator" duration=22.09µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.205705122Z level=info msg="Executing migration" id="teams permissions migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.205934418Z level=info msg="Migration successfully executed" id="teams permissions migration" duration=228.796µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.207632279Z level=info msg="Executing migration" id="dashboard permissions"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.207913404Z level=info msg="Migration successfully executed" id="dashboard permissions" duration=281.395µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.209573946Z level=info msg="Executing migration" id="dashboard permissions uid scopes"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.209857911Z level=info msg="Migration successfully executed" id="dashboard permissions uid scopes" duration=283.895µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.211497243Z level=info msg="Executing migration" id="drop managed folder create actions"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.211622931Z level=info msg="Migration successfully executed" id="drop managed folder create actions" duration=125.728µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.213252643Z level=info msg="Executing migration" id="alerting notification permissions"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.213544668Z level=info msg="Migration successfully executed" id="alerting notification permissions" duration=291.735µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.21518101Z level=info msg="Executing migration" id="create query_history_star table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.215634672Z level=info msg="Migration successfully executed" id="create query_history_star table v1" duration=453.392µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.217342413Z level=info msg="Executing migration" id="add index query_history.user_id-query_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.217892664Z level=info msg="Migration successfully executed" id="add index query_history.user_id-query_uid" duration=550.181µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.219540736Z level=info msg="Executing migration" id="add column org_id in query_history_star"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.22280687Z level=info msg="Migration successfully executed" id="add column org_id in query_history_star" duration=3.265724ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.224416562Z level=info msg="Executing migration" id="alter table query_history_star_mig column user_id type to bigint"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.224429512Z level=info msg="Migration successfully executed" id="alter table query_history_star_mig column user_id type to bigint" duration=13.39µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.226062474Z level=info msg="Executing migration" id="create correlation table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.226569046Z level=info msg="Migration successfully executed" id="create correlation table v1" duration=506.282µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.228244997Z level=info msg="Executing migration" id="add index correlations.uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.228798588Z level=info msg="Migration successfully executed" id="add index correlations.uid" duration=553.381µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.230469869Z level=info msg="Executing migration" id="add index correlations.source_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.23102356Z level=info msg="Migration successfully executed" id="add index correlations.source_uid" duration=553.401µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.23274213Z level=info msg="Executing migration" id="add correlation config column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.236099563Z level=info msg="Migration successfully executed" id="add correlation config column" duration=3.356803ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.237746555Z level=info msg="Executing migration" id="drop index IDX_correlation_uid - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.238328915Z level=info msg="Migration successfully executed" id="drop index IDX_correlation_uid - v1" duration=568.43µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.239964367Z level=info msg="Executing migration" id="drop index IDX_correlation_source_uid - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.240523357Z level=info msg="Migration successfully executed" id="drop index IDX_correlation_source_uid - v1" duration=558.74µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.24215219Z level=info msg="Executing migration" id="Rename table correlation to correlation_tmp_qwerty - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.25151889Z level=info msg="Migration successfully executed" id="Rename table correlation to correlation_tmp_qwerty - v1" duration=9.36582ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.25324743Z level=info msg="Executing migration" id="create correlation v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.253764271Z level=info msg="Migration successfully executed" id="create correlation v2" duration=516.511µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.255376744Z level=info msg="Executing migration" id="create index IDX_correlation_uid - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.255909575Z level=info msg="Migration successfully executed" id="create index IDX_correlation_uid - v2" duration=539.411µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.257629645Z level=info msg="Executing migration" id="create index IDX_correlation_source_uid - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.258197656Z level=info msg="Migration successfully executed" id="create index IDX_correlation_source_uid - v2" duration=567.681µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.259875717Z level=info msg="Executing migration" id="create index IDX_correlation_org_id - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.260422368Z level=info msg="Migration successfully executed" id="create index IDX_correlation_org_id - v2" duration=546.391µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.26206908Z level=info msg="Executing migration" id="copy correlation v1 to v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.262269086Z level=info msg="Migration successfully executed" id="copy correlation v1 to v2" duration=199.786µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.263910548Z level=info msg="Executing migration" id="drop correlation_tmp_qwerty"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.26438925Z level=info msg="Migration successfully executed" id="drop correlation_tmp_qwerty" duration=478.502µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.265970703Z level=info msg="Executing migration" id="add provisioning column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.269350885Z level=info msg="Migration successfully executed" id="add provisioning column" duration=3.379842ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.271059376Z level=info msg="Executing migration" id="add type column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.274381699Z level=info msg="Migration successfully executed" id="add type column" duration=3.322173ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.276056271Z level=info msg="Executing migration" id="create entity_events table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.276498423Z level=info msg="Migration successfully executed" id="create entity_events table" duration=441.952µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.278210214Z level=info msg="Executing migration" id="create dashboard public config v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.278719225Z level=info msg="Migration successfully executed" id="create dashboard public config v1" duration=509.101µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.280442876Z level=info msg="Executing migration" id="drop index UQE_dashboard_public_config_uid - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.280657232Z level=warn msg="Skipping migration: Already executed, but not recorded in migration log" id="drop index UQE_dashboard_public_config_uid - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.282306324Z level=info msg="Executing migration" id="drop index IDX_dashboard_public_config_org_id_dashboard_uid - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.28252986Z level=warn msg="Skipping migration: Already executed, but not recorded in migration log" id="drop index IDX_dashboard_public_config_org_id_dashboard_uid - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.284170602Z level=info msg="Executing migration" id="Drop old dashboard public config table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.284645854Z level=info msg="Migration successfully executed" id="Drop old dashboard public config table" duration=474.892µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.286242507Z level=info msg="Executing migration" id="recreate dashboard public config v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.286766638Z level=info msg="Migration successfully executed" id="recreate dashboard public config v1" duration=523.741µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.288473159Z level=info msg="Executing migration" id="create index UQE_dashboard_public_config_uid - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.289014589Z level=info msg="Migration successfully executed" id="create index UQE_dashboard_public_config_uid - v1" duration=541.141µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.29075239Z level=info msg="Executing migration" id="create index IDX_dashboard_public_config_org_id_dashboard_uid - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.29133416Z level=info msg="Migration successfully executed" id="create index IDX_dashboard_public_config_org_id_dashboard_uid - v1" duration=582.85µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.293386285Z level=info msg="Executing migration" id="drop index UQE_dashboard_public_config_uid - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.293927516Z level=info msg="Migration successfully executed" id="drop index UQE_dashboard_public_config_uid - v2" duration=540.931µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.295575438Z level=info msg="Executing migration" id="drop index IDX_dashboard_public_config_org_id_dashboard_uid - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.296121278Z level=info msg="Migration successfully executed" id="drop index IDX_dashboard_public_config_org_id_dashboard_uid - v2" duration=545.8µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.29777577Z level=info msg="Executing migration" id="Drop public config table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.298263922Z level=info msg="Migration successfully executed" id="Drop public config table" duration=487.882µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.299963803Z level=info msg="Executing migration" id="Recreate dashboard public config v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.300511383Z level=info msg="Migration successfully executed" id="Recreate dashboard public config v2" duration=547.51µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.302113896Z level=info msg="Executing migration" id="create index UQE_dashboard_public_config_uid - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.302689156Z level=info msg="Migration successfully executed" id="create index UQE_dashboard_public_config_uid - v2" duration=574.9µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.304307798Z level=info msg="Executing migration" id="create index IDX_dashboard_public_config_org_id_dashboard_uid - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.304920868Z level=info msg="Migration successfully executed" id="create index IDX_dashboard_public_config_org_id_dashboard_uid - v2" duration=612.96µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.306628839Z level=info msg="Executing migration" id="create index UQE_dashboard_public_config_access_token - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.307233078Z level=info msg="Migration successfully executed" id="create index UQE_dashboard_public_config_access_token - v2" duration=603.949µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.30890108Z level=info msg="Executing migration" id="Rename table dashboard_public_config to dashboard_public - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.319479589Z level=info msg="Migration successfully executed" id="Rename table dashboard_public_config to dashboard_public - v2" duration=10.577609ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.321231579Z level=info msg="Executing migration" id="add annotations_enabled column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.32472104Z level=info msg="Migration successfully executed" id="add annotations_enabled column" duration=3.489081ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.32644355Z level=info msg="Executing migration" id="add time_selection_enabled column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.32997052Z level=info msg="Migration successfully executed" id="add time_selection_enabled column" duration=3.52635ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.331633952Z level=info msg="Executing migration" id="delete orphaned public dashboards"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.33177042Z level=info msg="Migration successfully executed" id="delete orphaned public dashboards" duration=136.298µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.33351351Z level=info msg="Executing migration" id="add share column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.336889862Z level=info msg="Migration successfully executed" id="add share column" duration=3.375812ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.338585793Z level=info msg="Executing migration" id="backfill empty share column fields with default of public"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.338696741Z level=info msg="Migration successfully executed" id="backfill empty share column fields with default of public" duration=111.048µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.340343673Z level=info msg="Executing migration" id="create file table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.340790346Z level=info msg="Migration successfully executed" id="create file table" duration=446.473µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.342516326Z level=info msg="Executing migration" id="file table idx: path natural pk"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.343052477Z level=info msg="Migration successfully executed" id="file table idx: path natural pk" duration=535.871µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.344797507Z level=info msg="Executing migration" id="file table idx: parent_folder_path_hash fast folder retrieval"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.345383797Z level=info msg="Migration successfully executed" id="file table idx: parent_folder_path_hash fast folder retrieval" duration=585.88µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.347180166Z level=info msg="Executing migration" id="create file_meta table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.3475738Z level=info msg="Migration successfully executed" id="create file_meta table" duration=393.253µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.349216342Z level=info msg="Executing migration" id="file table idx: path key"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.349757672Z level=info msg="Migration successfully executed" id="file table idx: path key" duration=541.08µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.351448374Z level=info msg="Executing migration" id="set path collation in file table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.351460243Z level=info msg="Migration successfully executed" id="set path collation in file table" duration=14.389µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.353170164Z level=info msg="Executing migration" id="migrate contents column to mediumblob for MySQL"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.353181854Z level=info msg="Migration successfully executed" id="migrate contents column to mediumblob for MySQL" duration=11.94µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.354885855Z level=info msg="Executing migration" id="drop my_row_id and add primary key to file table if my_row_id exists (auto-generated mysql column)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.355041222Z level=warn msg="Skipping migration: Already executed, but not recorded in migration log" id="drop my_row_id and add primary key to file table if my_row_id exists (auto-generated mysql column)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.356708154Z level=info msg="Executing migration" id="drop file_path unique index from file table if it exists (mysql)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.35693092Z level=info msg="Migration successfully executed" id="drop file_path unique index from file table if it exists (mysql)" duration=223.096µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.358600222Z level=info msg="Executing migration" id="add primary key to file table if it doesn't exist (mysql)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.358611681Z level=info msg="Migration successfully executed" id="add primary key to file table if it doesn't exist (mysql)" duration=11.989µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.360244813Z level=info msg="Executing migration" id="add primary key to file table (postgres and sqlite)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.370543568Z level=info msg="Migration successfully executed" id="add primary key to file table (postgres and sqlite)" duration=10.297975ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.372472125Z level=info msg="Executing migration" id="drop my_row_id and add primary key to file_meta table if my_row_id exists (auto-generated mysql column)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.372617042Z level=warn msg="Skipping migration: Already executed, but not recorded in migration log" id="drop my_row_id and add primary key to file_meta table if my_row_id exists (auto-generated mysql column)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.374244834Z level=info msg="Executing migration" id="drop file_path unique index from file_meta table if it exists (mysql)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.37447494Z level=info msg="Migration successfully executed" id="drop file_path unique index from file_meta table if it exists (mysql)" duration=230.296µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.376123212Z level=info msg="Executing migration" id="add primary key to file_meta table if it doesn't exist (mysql)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.376148582Z level=info msg="Migration successfully executed" id="add primary key to file_meta table if it doesn't exist (mysql)" duration=25.61µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.377801184Z level=info msg="Executing migration" id="add primary key to file_meta table (postgres and sqlite)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.387545547Z level=info msg="Migration successfully executed" id="add primary key to file_meta table (postgres and sqlite)" duration=9.732134ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.389315767Z level=info msg="Executing migration" id="managed permissions migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.389591492Z level=info msg="Migration successfully executed" id="managed permissions migration" duration=275.586µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.391311573Z level=info msg="Executing migration" id="managed folder permissions alert actions migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.391446841Z level=info msg="Migration successfully executed" id="managed folder permissions alert actions migration" duration=140.388µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.393066253Z level=info msg="Executing migration" id="RBAC action name migrator"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.39383836Z level=info msg="Migration successfully executed" id="RBAC action name migrator" duration=771.658µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.395503741Z level=info msg="Executing migration" id="Add UID column to playlist"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.398957763Z level=info msg="Migration successfully executed" id="Add UID column to playlist" duration=3.453801ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.400666883Z level=info msg="Executing migration" id="Update uid column values in playlist"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.400765942Z level=info msg="Migration successfully executed" id="Update uid column values in playlist" duration=99.128µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.402451133Z level=info msg="Executing migration" id="Add index for uid in playlist"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.403010203Z level=info msg="Migration successfully executed" id="Add index for uid in playlist" duration=558.8µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.404649075Z level=info msg="Executing migration" id="update group index for alert rules"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.404864481Z level=info msg="Migration successfully executed" id="update group index for alert rules" duration=215.767µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.406525003Z level=info msg="Executing migration" id="managed folder permissions alert actions repeated migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.406648041Z level=info msg="Migration successfully executed" id="managed folder permissions alert actions repeated migration" duration=122.927µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.408307433Z level=info msg="Executing migration" id="admin only folder/dashboard permission"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.408574697Z level=info msg="Migration successfully executed" id="admin only folder/dashboard permission" duration=267.215µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.41022545Z level=info msg="Executing migration" id="add action column to seed_assignment"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.413791119Z level=info msg="Migration successfully executed" id="add action column to seed_assignment" duration=3.565139ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.41547318Z level=info msg="Executing migration" id="add scope column to seed_assignment"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.418810314Z level=info msg="Migration successfully executed" id="add scope column to seed_assignment" duration=3.336633ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.420473965Z level=info msg="Executing migration" id="remove unique index builtin_role_role_name before nullable update"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.421026136Z level=info msg="Migration successfully executed" id="remove unique index builtin_role_role_name before nullable update" duration=551.971µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.422664488Z level=info msg="Executing migration" id="update seed_assignment role_name column to nullable"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.458556385Z level=info msg="Migration successfully executed" id="update seed_assignment role_name column to nullable" duration=35.898157ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.460801126Z level=info msg="Executing migration" id="add unique index builtin_role_name back"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.461417006Z level=info msg="Migration successfully executed" id="add unique index builtin_role_name back" duration=615.62µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.463170696Z level=info msg="Executing migration" id="add unique index builtin_role_action_scope"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.463731887Z level=info msg="Migration successfully executed" id="add unique index builtin_role_action_scope" duration=561.271µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.465423058Z level=info msg="Executing migration" id="add primary key to seed_assigment"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.476288941Z level=info msg="Migration successfully executed" id="add primary key to seed_assigment" duration=10.855676ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.478369397Z level=info msg="Executing migration" id="add origin column to seed_assignment"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.481777959Z level=info msg="Migration successfully executed" id="add origin column to seed_assignment" duration=3.408222ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.483630416Z level=info msg="Executing migration" id="add origin to plugin seed_assignment"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.483784804Z level=info msg="Migration successfully executed" id="add origin to plugin seed_assignment" duration=154.177µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.485424796Z level=info msg="Executing migration" id="prevent seeding OnCall access"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.485534023Z level=info msg="Migration successfully executed" id="prevent seeding OnCall access" duration=109.158µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.487196755Z level=info msg="Executing migration" id="managed folder permissions alert actions repeated fixed migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.487326353Z level=info msg="Migration successfully executed" id="managed folder permissions alert actions repeated fixed migration" duration=129.678µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.488961925Z level=info msg="Executing migration" id="managed folder permissions library panel actions migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.489086274Z level=info msg="Migration successfully executed" id="managed folder permissions library panel actions migration" duration=124.428µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.490738406Z level=info msg="Executing migration" id="migrate external alertmanagers to datsourcse"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.490862503Z level=info msg="Migration successfully executed" id="migrate external alertmanagers to datsourcse" duration=124.037µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.492501445Z level=info msg="Executing migration" id="create folder table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.492958097Z level=info msg="Migration successfully executed" id="create folder table" duration=456.342µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.49459433Z level=info msg="Executing migration" id="Add index for parent_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.495210729Z level=info msg="Migration successfully executed" id="Add index for parent_uid" duration=617.498µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.496885561Z level=info msg="Executing migration" id="Add unique index for folder.uid and folder.org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.49748173Z level=info msg="Migration successfully executed" id="Add unique index for folder.uid and folder.org_id" duration=595.849µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.49922371Z level=info msg="Executing migration" id="Update folder title length"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.49924042Z level=info msg="Migration successfully executed" id="Update folder title length" duration=16.929µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.501409773Z level=info msg="Executing migration" id="Add unique index for folder.title and folder.parent_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.502018333Z level=info msg="Migration successfully executed" id="Add unique index for folder.title and folder.parent_uid" duration=608.3µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.503735414Z level=info msg="Executing migration" id="Remove unique index for folder.title and folder.parent_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.504312463Z level=info msg="Migration successfully executed" id="Remove unique index for folder.title and folder.parent_uid" duration=576.781µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.505939696Z level=info msg="Executing migration" id="Add unique index for title, parent_uid, and org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.506548696Z level=info msg="Migration successfully executed" id="Add unique index for title, parent_uid, and org_id" duration=608.55µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.508216027Z level=info msg="Executing migration" id="Sync dashboard and folder table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.508481643Z level=info msg="Migration successfully executed" id="Sync dashboard and folder table" duration=264.236µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.510110235Z level=info msg="Executing migration" id="Remove ghost folders from the folder table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.510278321Z level=info msg="Migration successfully executed" id="Remove ghost folders from the folder table" duration=168.057µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.511960463Z level=info msg="Executing migration" id="Remove unique index UQE_folder_uid_org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.512537583Z level=info msg="Migration successfully executed" id="Remove unique index UQE_folder_uid_org_id" duration=576.87µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.514143055Z level=info msg="Executing migration" id="Add unique index UQE_folder_org_id_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.514754826Z level=info msg="Migration successfully executed" id="Add unique index UQE_folder_org_id_uid" duration=611.561µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.516372108Z level=info msg="Executing migration" id="Remove unique index UQE_folder_title_parent_uid_org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.516913008Z level=info msg="Migration successfully executed" id="Remove unique index UQE_folder_title_parent_uid_org_id" duration=540.921µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.518548031Z level=info msg="Executing migration" id="Add unique index UQE_folder_org_id_parent_uid_title"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.519159049Z level=info msg="Migration successfully executed" id="Add unique index UQE_folder_org_id_parent_uid_title" duration=610.709µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.520810692Z level=info msg="Executing migration" id="Remove index IDX_folder_parent_uid_org_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.521379251Z level=info msg="Migration successfully executed" id="Remove index IDX_folder_parent_uid_org_id" duration=566.351µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.522978384Z level=info msg="Executing migration" id="Remove unique index UQE_folder_org_id_parent_uid_title"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.523552734Z level=info msg="Migration successfully executed" id="Remove unique index UQE_folder_org_id_parent_uid_title" duration=574.03µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.525197847Z level=info msg="Executing migration" id="Add index IDX_folder_org_id_parent_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.525796527Z level=info msg="Migration successfully executed" id="Add index IDX_folder_org_id_parent_uid" duration=596.59µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.527456519Z level=info msg="Executing migration" id="create anon_device table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.527897281Z level=info msg="Migration successfully executed" id="create anon_device table" duration=440.442µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.529507993Z level=info msg="Executing migration" id="add unique index anon_device.device_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.530090374Z level=info msg="Migration successfully executed" id="add unique index anon_device.device_id" duration=582.491µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.532337805Z level=info msg="Executing migration" id="add index anon_device.updated_at"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.532922974Z level=info msg="Migration successfully executed" id="add index anon_device.updated_at" duration=585.01µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.534643465Z level=info msg="Executing migration" id="create signing_key table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.535079489Z level=info msg="Migration successfully executed" id="create signing_key table" duration=435.813µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.536751749Z level=info msg="Executing migration" id="add unique index signing_key.key_id"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.537375298Z level=info msg="Migration successfully executed" id="add unique index signing_key.key_id" duration=623.249µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.539640681Z level=info msg="Executing migration" id="set legacy alert migration status in kvstore"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.54023971Z level=info msg="Migration successfully executed" id="set legacy alert migration status in kvstore" duration=598.869µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.541834883Z level=info msg="Executing migration" id="migrate record of created folders during legacy migration to kvstore"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.54200028Z level=info msg="Migration successfully executed" id="migrate record of created folders during legacy migration to kvstore" duration=165.547µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.544151414Z level=info msg="Executing migration" id="Add folder_uid for dashboard"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.547836421Z level=info msg="Migration successfully executed" id="Add folder_uid for dashboard" duration=3.684448ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.549509562Z level=info msg="Executing migration" id="Populate dashboard folder_uid column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.549959355Z level=info msg="Migration successfully executed" id="Populate dashboard folder_uid column" duration=449.933µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.552071138Z level=info msg="Executing migration" id="Add unique index for dashboard_org_id_folder_uid_title"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.552083538Z level=info msg="Migration successfully executed" id="Add unique index for dashboard_org_id_folder_uid_title" duration=14.89µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.554217642Z level=info msg="Executing migration" id="Delete unique index for dashboard_org_id_folder_id_title"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.554813092Z level=info msg="Migration successfully executed" id="Delete unique index for dashboard_org_id_folder_id_title" duration=595.359µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.556896256Z level=info msg="Executing migration" id="Delete unique index for dashboard_org_id_folder_uid_title"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.556908276Z level=info msg="Migration successfully executed" id="Delete unique index for dashboard_org_id_folder_uid_title" duration=12.37µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.558589307Z level=info msg="Executing migration" id="Add unique index for dashboard_org_id_folder_uid_title_is_folder"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.559224196Z level=info msg="Migration successfully executed" id="Add unique index for dashboard_org_id_folder_uid_title_is_folder" duration=634.539µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.561108024Z level=info msg="Executing migration" id="Restore index for dashboard_org_id_folder_id_title"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.56195715Z level=info msg="Migration successfully executed" id="Restore index for dashboard_org_id_folder_id_title" duration=850.866µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.563768139Z level=info msg="Executing migration" id="Remove unique index for dashboard_org_id_folder_uid_title_is_folder"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.564360158Z level=info msg="Migration successfully executed" id="Remove unique index for dashboard_org_id_folder_uid_title_is_folder" duration=591.65µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.566024489Z level=info msg="Executing migration" id="create sso_setting table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.56655772Z level=info msg="Migration successfully executed" id="create sso_setting table" duration=532.93µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.568218972Z level=info msg="Executing migration" id="update settings column to MEDIUMTEXT"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.568232143Z level=info msg="Migration successfully executed" id="update settings column to MEDIUMTEXT" duration=16.709µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.569860495Z level=info msg="Executing migration" id="copy kvstore migration status to each org"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.570364606Z level=info msg="Migration successfully executed" id="copy kvstore migration status to each org" duration=504.322µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.572391821Z level=info msg="Executing migration" id="add back entry for orgid=0 migrated status"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.572554849Z level=info msg="Migration successfully executed" id="add back entry for orgid=0 migrated status" duration=163.227µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.574648043Z level=info msg="Executing migration" id="managed dashboard permissions annotation actions migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.575037646Z level=info msg="Migration successfully executed" id="managed dashboard permissions annotation actions migration" duration=389.263µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.577123841Z level=info msg="Executing migration" id="create cloud_migration table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.577578223Z level=info msg="Migration successfully executed" id="create cloud_migration table v1" duration=453.702µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.579231384Z level=info msg="Executing migration" id="create cloud_migration_run table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.579656928Z level=info msg="Migration successfully executed" id="create cloud_migration_run table v1" duration=425.204µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.58127677Z level=info msg="Executing migration" id="add stack_id column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.584950257Z level=info msg="Migration successfully executed" id="add stack_id column" duration=3.673297ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.587202639Z level=info msg="Executing migration" id="add region_slug column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.590753738Z level=info msg="Migration successfully executed" id="add region_slug column" duration=3.550659ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.592451189Z level=info msg="Executing migration" id="add cluster_slug column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.596076117Z level=info msg="Migration successfully executed" id="add cluster_slug column" duration=3.624798ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.597708379Z level=info msg="Executing migration" id="add migration uid column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.601248208Z level=info msg="Migration successfully executed" id="add migration uid column" duration=3.53952ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.603412402Z level=info msg="Executing migration" id="Update uid column values for migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.603520529Z level=info msg="Migration successfully executed" id="Update uid column values for migration" duration=108.139µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.605238691Z level=info msg="Executing migration" id="Add unique index migration_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.605787201Z level=info msg="Migration successfully executed" id="Add unique index migration_uid" duration=548.34µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.607897705Z level=info msg="Executing migration" id="add migration run uid column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.611470744Z level=info msg="Migration successfully executed" id="add migration run uid column" duration=3.572719ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.613941671Z level=info msg="Executing migration" id="Update uid column values for migration run"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.61404696Z level=info msg="Migration successfully executed" id="Update uid column values for migration run" duration=105.758µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.616073576Z level=info msg="Executing migration" id="Add unique index migration_run_uid"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.616683165Z level=info msg="Migration successfully executed" id="Add unique index migration_run_uid" duration=609.409µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.618832799Z level=info msg="Executing migration" id="Rename table cloud_migration to cloud_migration_session_tmp_qwerty - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.629531365Z level=info msg="Migration successfully executed" id="Rename table cloud_migration to cloud_migration_session_tmp_qwerty - v1" duration=10.698217ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.631739108Z level=info msg="Executing migration" id="create cloud_migration_session v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.632213799Z level=info msg="Migration successfully executed" id="create cloud_migration_session v2" duration=474.962µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.63456755Z level=info msg="Executing migration" id="create index UQE_cloud_migration_session_uid - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.63518594Z level=info msg="Migration successfully executed" id="create index UQE_cloud_migration_session_uid - v2" duration=618.379µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.637680967Z level=info msg="Executing migration" id="copy cloud_migration_session v1 to v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.637892302Z level=info msg="Migration successfully executed" id="copy cloud_migration_session v1 to v2" duration=211.366µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.639474526Z level=info msg="Executing migration" id="drop cloud_migration_session_tmp_qwerty"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.639959227Z level=info msg="Migration successfully executed" id="drop cloud_migration_session_tmp_qwerty" duration=484.882µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.641977424Z level=info msg="Executing migration" id="Rename table cloud_migration_run to cloud_migration_snapshot_tmp_qwerty - v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.65153617Z level=info msg="Migration successfully executed" id="Rename table cloud_migration_run to cloud_migration_snapshot_tmp_qwerty - v1" duration=9.557996ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.653205662Z level=info msg="Executing migration" id="create cloud_migration_snapshot v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.653648014Z level=info msg="Migration successfully executed" id="create cloud_migration_snapshot v2" duration=442.302µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.655269657Z level=info msg="Executing migration" id="create index UQE_cloud_migration_snapshot_uid - v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.655881755Z level=info msg="Migration successfully executed" id="create index UQE_cloud_migration_snapshot_uid - v2" duration=616.33µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.658078469Z level=info msg="Executing migration" id="copy cloud_migration_snapshot v1 to v2"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.658326764Z level=info msg="Migration successfully executed" id="copy cloud_migration_snapshot v1 to v2" duration=248.065µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.659909217Z level=info msg="Executing migration" id="drop cloud_migration_snapshot_tmp_qwerty"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.660414238Z level=info msg="Migration successfully executed" id="drop cloud_migration_snapshot_tmp_qwerty" duration=504.763µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.662485173Z level=info msg="Executing migration" id="add snapshot upload_url column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.666096352Z level=info msg="Migration successfully executed" id="add snapshot upload_url column" duration=3.610619ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.668183286Z level=info msg="Executing migration" id="add snapshot status column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.671852224Z level=info msg="Migration successfully executed" id="add snapshot status column" duration=3.668668ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.673530134Z level=info msg="Executing migration" id="add snapshot local_directory column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.677387259Z level=info msg="Migration successfully executed" id="add snapshot local_directory column" duration=3.856793ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.679488893Z level=info msg="Executing migration" id="add snapshot gms_snapshot_uid column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.683054222Z level=info msg="Migration successfully executed" id="add snapshot gms_snapshot_uid column" duration=3.553ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.685206615Z level=info msg="Executing migration" id="add snapshot encryption_key column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.688838654Z level=info msg="Migration successfully executed" id="add snapshot encryption_key column" duration=3.631838ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.690517985Z level=info msg="Executing migration" id="add snapshot error_string column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.694177962Z level=info msg="Migration successfully executed" id="add snapshot error_string column" duration=3.659828ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.695852273Z level=info msg="Executing migration" id="create cloud_migration_resource table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.696315156Z level=info msg="Migration successfully executed" id="create cloud_migration_resource table v1" duration=462.303µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.698550968Z level=info msg="Executing migration" id="delete cloud_migration_snapshot.result column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.713272396Z level=info msg="Migration successfully executed" id="delete cloud_migration_snapshot.result column" duration=14.720508ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.715592997Z level=info msg="Executing migration" id="add cloud_migration_resource.name column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.71948706Z level=info msg="Migration successfully executed" id="add cloud_migration_resource.name column" duration=3.893983ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.721153521Z level=info msg="Executing migration" id="add cloud_migration_resource.parent_name column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.72476044Z level=info msg="Migration successfully executed" id="add cloud_migration_resource.parent_name column" duration=3.606788ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.726962013Z level=info msg="Executing migration" id="add cloud_migration_session.org_id column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.730696749Z level=info msg="Migration successfully executed" id="add cloud_migration_session.org_id column" duration=3.734357ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.732419299Z level=info msg="Executing migration" id="add cloud_migration_resource.error_code column"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.736116656Z level=info msg="Migration successfully executed" id="add cloud_migration_resource.error_code column" duration=3.696957ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.737758448Z level=info msg="Executing migration" id="increase resource_uid column length"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.737770308Z level=info msg="Migration successfully executed" id="increase resource_uid column length" duration=12.09µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.739462688Z level=info msg="Executing migration" id="create cloud_migration_snapshot_partition table v1"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.739932421Z level=info msg="Migration successfully executed" id="create cloud_migration_snapshot_partition table v1" duration=469.622µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.742190893Z level=info msg="Executing migration" id="add cloud_migration_snapshot_partition srp_unique index"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.742773712Z level=info msg="Migration successfully executed" id="add cloud_migration_snapshot_partition srp_unique index" duration=582.59µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.745011605Z level=info msg="Executing migration" id="add resource_storage_type column to cloud_migration_snapshot table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.748703682Z level=info msg="Migration successfully executed" id="add resource_storage_type column to cloud_migration_snapshot table" duration=3.691518ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.750310063Z level=info msg="Executing migration" id="add encryption_algo column to cloud_migration_snapshot table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.753954862Z level=info msg="Migration successfully executed" id="add encryption_algo column to cloud_migration_snapshot table" duration=3.652538ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.756105204Z level=info msg="Executing migration" id="add metadata column to cloud_migration_snapshot table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.759800672Z level=info msg="Migration successfully executed" id="add metadata column to cloud_migration_snapshot table" duration=3.695137ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.761895536Z level=info msg="Executing migration" id="add public_key column to cloud_migration_snapshot table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.765541603Z level=info msg="Migration successfully executed" id="add public_key column to cloud_migration_snapshot table" duration=3.645928ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.767776476Z level=info msg="Executing migration" id="drop my_row_id and add primary key with columns snapshot_uid,resource_type,partition_number to table cloud_migration_snapshot_partition if my_row_id exists (auto-generated mysql column)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.767923013Z level=warn msg="Skipping migration: Already executed, but not recorded in migration log" id="drop my_row_id and add primary key with columns snapshot_uid,resource_type,partition_number to table cloud_migration_snapshot_partition if my_row_id exists (auto-generated mysql column)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.769990018Z level=info msg="Executing migration" id="drop unique index UQE_cloud_migration_snapshot_partition_srp_unique from cloud_migration_snapshot_partition table if it exists (mysql)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.770233934Z level=info msg="Migration successfully executed" id="drop unique index UQE_cloud_migration_snapshot_partition_srp_unique from cloud_migration_snapshot_partition table if it exists (mysql)" duration=244.086µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.771854156Z level=info msg="Executing migration" id="add primary key with columns snapshot_uid,resource_type,partition_number to table cloud_migration_snapshot_partition if it doesn't exist (mysql)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.771875306Z level=info msg="Migration successfully executed" id="add primary key with columns snapshot_uid,resource_type,partition_number to table cloud_migration_snapshot_partition if it doesn't exist (mysql)" duration=21.28µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.773869352Z level=info msg="Executing migration" id="add primary key with columns snapshot_uid,resource_type,partition_number to table cloud_migration_snapshot_partition (postgres and sqlite)"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.784773995Z level=info msg="Migration successfully executed" id="add primary key with columns snapshot_uid,resource_type,partition_number to table cloud_migration_snapshot_partition (postgres and sqlite)" duration=10.903714ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.786649624Z level=info msg="Executing migration" id="alter kv_store.value to longtext"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.786662193Z level=info msg="Migration successfully executed" id="alter kv_store.value to longtext" duration=12.99µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.788253986Z level=info msg="Executing migration" id="add notification_settings column to alert_rule table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.792022222Z level=info msg="Migration successfully executed" id="add notification_settings column to alert_rule table" duration=3.767976ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.794113386Z level=info msg="Executing migration" id="add notification_settings column to alert_rule_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.79798116Z level=info msg="Migration successfully executed" id="add notification_settings column to alert_rule_version table" duration=3.867094ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.799596113Z level=info msg="Executing migration" id="removing scope from alert.instances:read action migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.799820759Z level=info msg="Migration successfully executed" id="removing scope from alert.instances:read action migration" duration=224.596µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.801810595Z level=info msg="Executing migration" id="managed folder permissions alerting silences actions migration"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.801952092Z level=info msg="Migration successfully executed" id="managed folder permissions alerting silences actions migration" duration=141.226µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.803565385Z level=info msg="Executing migration" id="add record column to alert_rule table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.807270642Z level=info msg="Migration successfully executed" id="add record column to alert_rule table" duration=3.704798ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.808855765Z level=info msg="Executing migration" id="add record column to alert_rule_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.81265019Z level=info msg="Migration successfully executed" id="add record column to alert_rule_version table" duration=3.794025ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.814772354Z level=info msg="Executing migration" id="add resolved_at column to alert_instance table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.818440521Z level=info msg="Migration successfully executed" id="add resolved_at column to alert_instance table" duration=3.667697ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.820375718Z level=info msg="Executing migration" id="add last_sent_at column to alert_instance table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.824205213Z level=info msg="Migration successfully executed" id="add last_sent_at column to alert_instance table" duration=3.829265ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.825808665Z level=info msg="Executing migration" id="Add scope to alert.notifications.receivers:read and alert.notifications.receivers.secrets:read"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.826176288Z level=info msg="Migration successfully executed" id="Add scope to alert.notifications.receivers:read and alert.notifications.receivers.secrets:read" duration=367.434µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.828482589Z level=info msg="Executing migration" id="add metadata column to alert_rule table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.832214625Z level=info msg="Migration successfully executed" id="add metadata column to alert_rule table" duration=3.731407ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.833762238Z level=info msg="Executing migration" id="add metadata column to alert_rule_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.837580813Z level=info msg="Migration successfully executed" id="add metadata column to alert_rule_version table" duration=3.818235ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.839196786Z level=info msg="Executing migration" id="delete orphaned service account permissions"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.839353943Z level=info msg="Migration successfully executed" id="delete orphaned service account permissions" duration=157.157µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.840932057Z level=info msg="Executing migration" id="adding action set permissions"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.841255841Z level=info msg="Migration successfully executed" id="adding action set permissions" duration=323.514µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.843515243Z level=info msg="Executing migration" id="create user_external_session table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.843993075Z level=info msg="Migration successfully executed" id="create user_external_session table" duration=477.642µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.845561357Z level=info msg="Executing migration" id="increase name_id column length to 1024"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.845573228Z level=info msg="Migration successfully executed" id="increase name_id column length to 1024" duration=12.45µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.84718582Z level=info msg="Executing migration" id="increase session_id column length to 1024"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.84720155Z level=info msg="Migration successfully executed" id="increase session_id column length to 1024" duration=19.271µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.849170406Z level=info msg="Executing migration" id="remove scope from alert.notifications.receivers:create"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.849403352Z level=info msg="Migration successfully executed" id="remove scope from alert.notifications.receivers:create" duration=232.606µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.851459917Z level=info msg="Executing migration" id="add created_by column to alert_rule_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.855236463Z level=info msg="Migration successfully executed" id="add created_by column to alert_rule_version table" duration=3.776296ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.857352707Z level=info msg="Executing migration" id="add updated_by column to alert_rule table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.861054883Z level=info msg="Migration successfully executed" id="add updated_by column to alert_rule table" duration=3.701995ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.862662676Z level=info msg="Executing migration" id="add alert_rule_state table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.863089069Z level=info msg="Migration successfully executed" id="add alert_rule_state table" duration=426.054µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.864730921Z level=info msg="Executing migration" id="add index to alert_rule_state on org_id and rule_uid columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.865332019Z level=info msg="Migration successfully executed" id="add index to alert_rule_state on org_id and rule_uid columns" duration=600.999µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.867414725Z level=info msg="Executing migration" id="add guid column to alert_rule table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.87119381Z level=info msg="Migration successfully executed" id="add guid column to alert_rule table" duration=3.776725ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.873370393Z level=info msg="Executing migration" id="add rule_guid column to alert_rule_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.87705872Z level=info msg="Migration successfully executed" id="add rule_guid column to alert_rule_version table" duration=3.687827ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.878762381Z level=info msg="Executing migration" id="cleanup alert_rule_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.878784561Z level=info msg="Rule version record limit is not set, fallback to 100" limit=0
grafana-1     | logger=migrator t=2026-03-18T08:58:42.878916558Z level=info msg="Cleaning up table `alert_rule_version`" batchSize=50 batches=0 keepVersions=100
grafana-1     | logger=migrator t=2026-03-18T08:58:42.878929368Z level=info msg="Migration successfully executed" id="cleanup alert_rule_version table" duration=167.898µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.88059137Z level=info msg="Executing migration" id="populate rule guid in alert rule table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.880925984Z level=info msg="Migration successfully executed" id="populate rule guid in alert rule table" duration=328.854µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.882967989Z level=info msg="Executing migration" id="drop index in alert_rule_version table on rule_org_id, rule_uid and version columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.883572308Z level=info msg="Migration successfully executed" id="drop index in alert_rule_version table on rule_org_id, rule_uid and version columns" duration=604.51µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.885092823Z level=info msg="Executing migration" id="add index in alert_rule_version table on rule_org_id, rule_uid, rule_guid and version columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.885735812Z level=info msg="Migration successfully executed" id="add index in alert_rule_version table on rule_org_id, rule_uid, rule_guid and version columns" duration=642.629µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.88763187Z level=info msg="Executing migration" id="add index in alert_rule_version table on rule_guid and version columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.888230659Z level=info msg="Migration successfully executed" id="add index in alert_rule_version table on rule_guid and version columns" duration=598.409µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.890287873Z level=info msg="Executing migration" id="add index in alert_rule table on guid columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.890857344Z level=info msg="Migration successfully executed" id="add index in alert_rule table on guid columns" duration=569.28µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.89290453Z level=info msg="Executing migration" id="add keep_firing_for column to alert_rule"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.896734674Z level=info msg="Migration successfully executed" id="add keep_firing_for column to alert_rule" duration=3.829795ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.898744569Z level=info msg="Executing migration" id="add keep_firing_for column to alert_rule_version"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.902550615Z level=info msg="Migration successfully executed" id="add keep_firing_for column to alert_rule_version" duration=3.805415ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.904195627Z level=info msg="Executing migration" id="add missing_series_evals_to_resolve column to alert_rule"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.907922993Z level=info msg="Migration successfully executed" id="add missing_series_evals_to_resolve column to alert_rule" duration=3.726966ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.90987336Z level=info msg="Executing migration" id="add missing_series_evals_to_resolve column to alert_rule_version"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.913650545Z level=info msg="Migration successfully executed" id="add missing_series_evals_to_resolve column to alert_rule_version" duration=3.769256ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.915234268Z level=info msg="Executing migration" id="remove the datasources:drilldown action"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.915344757Z level=info msg="Removed 0 datasources:drilldown permissions"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.915355645Z level=info msg="Migration successfully executed" id="remove the datasources:drilldown action" duration=121.687µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.917318763Z level=info msg="Executing migration" id="remove title in folder unique index"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.917885543Z level=info msg="Migration successfully executed" id="remove title in folder unique index" duration=566.641µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.919420736Z level=info msg="Executing migration" id="add fired_at column to alert_instance table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.923106473Z level=info msg="Migration successfully executed" id="add fired_at column to alert_instance table" duration=3.685337ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.92506768Z level=info msg="Executing migration" id="ensure rule_group column is case sensitive in returned results"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.92508495Z level=info msg="Migration successfully executed" id="ensure rule_group column is case sensitive in returned results" duration=12.978µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.926693943Z level=info msg="Executing migration" id="expand created_by in alert_rule_version table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.926729211Z level=info msg="Migration successfully executed" id="expand created_by in alert_rule_version table" duration=35.949µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.928714188Z level=info msg="Executing migration" id="expand updated_by in alert_rule table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.928748857Z level=info msg="Migration successfully executed" id="expand updated_by in alert_rule table" duration=35.09µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.93036204Z level=info msg="Executing migration" id="add index in alert_rule on org_id, namespace_uid, rule_group and rule_group_idx columns"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.930991649Z level=info msg="Migration successfully executed" id="add index in alert_rule on org_id, namespace_uid, rule_group and rule_group_idx columns" duration=629.37µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.932891997Z level=info msg="Executing migration" id="add annotations column to alert_instance table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.936647773Z level=info msg="Migration successfully executed" id="add annotations column to alert_instance table" duration=3.755477ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.938626328Z level=info msg="Executing migration" id="ensure namespace_uid column sorts the same way as golang"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.938637799Z level=info msg="Migration successfully executed" id="ensure namespace_uid column sorts the same way as golang" duration=12.06µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.940665434Z level=info msg="Executing migration" id="ensure rule_group column sorts the same way as golang"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.940677613Z level=info msg="Migration successfully executed" id="ensure rule_group column sorts the same way as golang" duration=13.029µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.942727679Z level=info msg="Executing migration" id="add 'alert.notifications.receivers.protected:write' to receiver admins"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.942962875Z level=info msg="Migration successfully executed" id="add 'alert.notifications.receivers.protected:write' to receiver admins" duration=235.116µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.944561738Z level=info msg="Executing migration" id="add evaluation_duration_ns column to alert_instance table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.948304304Z level=info msg="Migration successfully executed" id="add evaluation_duration_ns column to alert_instance table" duration=3.741717ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.950437387Z level=info msg="Executing migration" id="add last_error column to alert_instance table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.954293781Z level=info msg="Migration successfully executed" id="add last_error column to alert_instance table" duration=3.855904ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.956277398Z level=info msg="Executing migration" id="add last_result column to alert_instance table"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.959994403Z level=info msg="Migration successfully executed" id="add last_result column to alert_instance table" duration=3.716675ms
grafana-1     | logger=migrator t=2026-03-18T08:58:42.961574307Z level=info msg="Executing migration" id="add 'alert.notifications.receivers.test:create' to managed roles"
grafana-1     | logger=migrator t=2026-03-18T08:58:42.961790434Z level=info msg="Migration successfully executed" id="add 'alert.notifications.receivers.test:create' to managed roles" duration=215.857µs
grafana-1     | logger=migrator t=2026-03-18T08:58:42.963384136Z level=info msg="migrations completed" performed=710 skipped=0 duration=2.084670789s
grafana-1     | logger=migrator t=2026-03-18T08:58:42.963697401Z level=info msg="Unlocking database"
grafana-1     | logger=sqlstore t=2026-03-18T08:58:42.971447928Z level=info msg="Created default admin" user=admin
grafana-1     | logger=sqlstore t=2026-03-18T08:58:42.971597426Z level=info msg="Created default organization"
grafana-1     | logger=secrets t=2026-03-18T08:58:42.973313287Z level=info msg="Envelope encryption state" currentprovider=secretKey.v1
grafana-1     | logger=plugin.angulardetectorsprovider.dynamic t=2026-03-18T08:58:43.03990202Z level=info msg="Restored cache from database" duration=347.935µs
grafana-1     | logger=accesscontrol.service t=2026-03-18T08:58:43.040729385Z level=info msg="Starting migration to remove deprecated permissions" migration=removeDeprecatedPermissions
grafana-1     | logger=accesscontrol.service t=2026-03-18T08:58:43.040946402Z level=info msg="Completed migration to remove deprecated permissions" migration=removeDeprecatedPermissions totalRemoved=0 duration=217.707µs
grafana-1     | logger=plugin.store t=2026-03-18T08:58:43.041014241Z level=info msg="Loading plugins..."
grafana-1     | logger=plugin.store t=2026-03-18T08:58:43.089788037Z level=info msg="Plugins loaded" count=53 duration=48.774258ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.090557805Z level=info msg="Locking database"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.090568464Z level=info msg="Starting DB migrations"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.09136736Z level=info msg="Executing migration" id="create secret_migration_log table"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.091893601Z level=info msg="Migration successfully executed" id="create secret_migration_log table" duration=526.9µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.095012929Z level=info msg="Executing migration" id="Initialize secrets tables"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.095025439Z level=info msg="Migration successfully executed" id="Initialize secrets tables" duration=13.2µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.096823917Z level=info msg="Executing migration" id="drop table secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.096879697Z level=info msg="Migration successfully executed" id="drop table secret_secure_value" duration=55.929µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.09904078Z level=info msg="Executing migration" id="create table secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.099635749Z level=info msg="Migration successfully executed" id="create table secret_secure_value" duration=594.689µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.101434699Z level=info msg="Executing migration" id="create table secret_secure_value, index: 0"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.102042698Z level=info msg="Migration successfully executed" id="create table secret_secure_value, index: 0" duration=607.67µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.104284361Z level=info msg="Executing migration" id="create table secret_secure_value, index: 1"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.10489879Z level=info msg="Migration successfully executed" id="create table secret_secure_value, index: 1" duration=614.079µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.1066103Z level=info msg="Executing migration" id="drop table secret_keeper"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.106669739Z level=info msg="Migration successfully executed" id="drop table secret_keeper" duration=59.529µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.108404171Z level=info msg="Executing migration" id="create table secret_keeper"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.109151088Z level=info msg="Migration successfully executed" id="create table secret_keeper" duration=746.326µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.111969899Z level=info msg="Executing migration" id="create table secret_keeper, index: 0"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.112821924Z level=info msg="Migration successfully executed" id="create table secret_keeper, index: 0" duration=852.275µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.115009978Z level=info msg="Executing migration" id="drop table secret_data_key"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.115066156Z level=info msg="Migration successfully executed" id="drop table secret_data_key" duration=56.46µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.116749548Z level=info msg="Executing migration" id="create table secret_data_key"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.117274109Z level=info msg="Migration successfully executed" id="create table secret_data_key" duration=524.692µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.11948997Z level=info msg="Executing migration" id="drop table secret_encrypted_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.119556479Z level=info msg="Migration successfully executed" id="drop table secret_encrypted_value" duration=67.81µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.121226952Z level=info msg="Executing migration" id="create table secret_encrypted_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.121641254Z level=info msg="Migration successfully executed" id="create table secret_encrypted_value" duration=414.252µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.124289918Z level=info msg="Executing migration" id="create table secret_encrypted_value, index: 0"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.124873259Z level=info msg="Migration successfully executed" id="create table secret_encrypted_value, index: 0" duration=583.15µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.127045881Z level=info msg="Executing migration" id="create index for list on secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.127643351Z level=info msg="Migration successfully executed" id="create index for list on secret_secure_value" duration=597.049µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.129804834Z level=info msg="Executing migration" id="create index for list and read current on secret_data_key"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.130407934Z level=info msg="Migration successfully executed" id="create index for list and read current on secret_data_key" duration=602.98µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.132631506Z level=info msg="Executing migration" id="add owner_reference_api_group column to secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.136735057Z level=info msg="Migration successfully executed" id="add owner_reference_api_group column to secret_secure_value" duration=4.10173ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.138510176Z level=info msg="Executing migration" id="add owner_reference_api_version column to secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.143963963Z level=info msg="Migration successfully executed" id="add owner_reference_api_version column to secret_secure_value" duration=5.453216ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.146058368Z level=info msg="Executing migration" id="add owner_reference_kind column to secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.150107078Z level=info msg="Migration successfully executed" id="add owner_reference_kind column to secret_secure_value" duration=4.04812ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.152250062Z level=info msg="Executing migration" id="add owner_reference_name column to secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.156257332Z level=info msg="Migration successfully executed" id="add owner_reference_name column to secret_secure_value" duration=4.006762ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.158034782Z level=info msg="Executing migration" id="add lease_token column to secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.162009695Z level=info msg="Migration successfully executed" id="add lease_token column to secret_secure_value" duration=3.974612ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.163756436Z level=info msg="Executing migration" id="add lease_token index to secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.164543372Z level=info msg="Migration successfully executed" id="add lease_token index to secret_secure_value" duration=786.325µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.167241635Z level=info msg="Executing migration" id="add lease_created column to secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.171571262Z level=info msg="Migration successfully executed" id="add lease_created column to secret_secure_value" duration=4.329006ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.173268233Z level=info msg="Executing migration" id="add lease_created index to secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.173907972Z level=info msg="Migration successfully executed" id="add lease_created index to secret_secure_value" duration=639.72µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.175659251Z level=info msg="Executing migration" id="add data_key_id column to secret_encrypted_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.179774112Z level=info msg="Migration successfully executed" id="add data_key_id column to secret_encrypted_value" duration=4.114351ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.182006733Z level=info msg="Executing migration" id="add data_key_id index to secret_encrypted_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.182638242Z level=info msg="Migration successfully executed" id="add data_key_id index to secret_encrypted_value" duration=631.319µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.184376403Z level=info msg="Executing migration" id="add active column to secret_keeper"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.188410984Z level=info msg="Migration successfully executed" id="add active column to secret_keeper" duration=4.034132ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.190649315Z level=info msg="Executing migration" id="add active column index to secret_keeper"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.191480922Z level=info msg="Migration successfully executed" id="add active column index to secret_keeper" duration=831.327µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.193270012Z level=info msg="Executing migration" id="set secret_secure_value.keeper to 'system' where keeper is null in secret_secure_value"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.19338948Z level=info msg="Migration successfully executed" id="set secret_secure_value.keeper to 'system' where keeper is null in secret_secure_value" duration=119.668µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.19508344Z level=info msg="Executing migration" id="drop my_row_id and add primary key with columns namespace,name,version to table secret_encrypted_value if my_row_id exists (auto-generated mysql column)"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.195252418Z level=warn msg="Skipping migration: Already executed, but not recorded in migration log" id="drop my_row_id and add primary key with columns namespace,name,version to table secret_encrypted_value if my_row_id exists (auto-generated mysql column)"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.197416621Z level=info msg="Executing migration" id="drop unique index UQE_secret_encrypted_value_namespace_name_version from secret_encrypted_value table if it exists (mysql)"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.197668545Z level=info msg="Migration successfully executed" id="drop unique index UQE_secret_encrypted_value_namespace_name_version from secret_encrypted_value table if it exists (mysql)" duration=252.125µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.199320818Z level=info msg="Executing migration" id="add primary key with columns namespace,name,version to table secret_encrypted_value if it doesn't exist (mysql)"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.199332338Z level=info msg="Migration successfully executed" id="add primary key with columns namespace,name,version to table secret_encrypted_value if it doesn't exist (mysql)" duration=12.12µs
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.201494221Z level=info msg="Executing migration" id="add primary key with columns namespace,name,version to table secret_encrypted_value (postgres and sqlite)"
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.213499725Z level=info msg="Migration successfully executed" id="add primary key with columns namespace,name,version to table secret_encrypted_value (postgres and sqlite)" duration=12.004835ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.215415424Z level=info msg="migrations completed" performed=33 skipped=0 duration=124.077051ms
grafana-1     | logger=secret-migrator t=2026-03-18T08:58:43.215783377Z level=info msg="Unlocking database"
grafana-1     | logger=resource-db t=2026-03-18T08:58:43.221477Z level=info msg="Using database section" db_type=sqlite3
grafana-1     | logger=resource-db t=2026-03-18T08:58:43.221628287Z level=info msg="Initializing Resource DB" db_type=sqlite3 open_conn=0 in_use_conn=0 idle_conn=0 max_open_conn=0
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.225452911Z level=info msg="Locking database"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.225465761Z level=info msg="Starting DB migrations"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.229770548Z level=info msg="Executing migration" id="create resource_migration_log table"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.23026661Z level=info msg="Migration successfully executed" id="create resource_migration_log table" duration=495.803µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.232643659Z level=info msg="Executing migration" id="Initialize resource tables"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.232658508Z level=info msg="Migration successfully executed" id="Initialize resource tables" duration=13.891µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.23492086Z level=info msg="Executing migration" id="drop table resource"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.234983249Z level=info msg="Migration successfully executed" id="drop table resource" duration=62.599µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.23672194Z level=info msg="Executing migration" id="create table resource"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.237274429Z level=info msg="Migration successfully executed" id="create table resource" duration=552.24µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.239659919Z level=info msg="Executing migration" id="create table resource, index: 0"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.240330667Z level=info msg="Migration successfully executed" id="create table resource, index: 0" duration=670.399µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.242065329Z level=info msg="Executing migration" id="drop table resource_history"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.242141977Z level=info msg="Migration successfully executed" id="drop table resource_history" duration=76.318µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.243941675Z level=info msg="Executing migration" id="create table resource_history"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.244697334Z level=info msg="Migration successfully executed" id="create table resource_history" duration=756.778µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.247466225Z level=info msg="Executing migration" id="create table resource_history, index: 0"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.248192224Z level=info msg="Migration successfully executed" id="create table resource_history, index: 0" duration=725.838µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.249954453Z level=info msg="Executing migration" id="create table resource_history, index: 1"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.250606172Z level=info msg="Migration successfully executed" id="create table resource_history, index: 1" duration=651.349µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.252826614Z level=info msg="Executing migration" id="drop table resource_version"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.252888403Z level=info msg="Migration successfully executed" id="drop table resource_version" duration=62.029µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.255000828Z level=info msg="Executing migration" id="create table resource_version"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.255455489Z level=info msg="Migration successfully executed" id="create table resource_version" duration=454.303µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.258030546Z level=info msg="Executing migration" id="create table resource_version, index: 0"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.258696775Z level=info msg="Migration successfully executed" id="create table resource_version, index: 0" duration=666.168µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.260880596Z level=info msg="Executing migration" id="drop table resource_blob"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.260935715Z level=info msg="Migration successfully executed" id="drop table resource_blob" duration=55.279µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.262670166Z level=info msg="Executing migration" id="create table resource_blob"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.263241177Z level=info msg="Migration successfully executed" id="create table resource_blob" duration=569.38µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.265540627Z level=info msg="Executing migration" id="create table resource_blob, index: 0"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.266213166Z level=info msg="Migration successfully executed" id="create table resource_blob, index: 0" duration=672.238µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.268477867Z level=info msg="Executing migration" id="create table resource_blob, index: 1"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.269305193Z level=info msg="Migration successfully executed" id="create table resource_blob, index: 1" duration=826.945µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.271579795Z level=info msg="Executing migration" id="drop table resource_last_import_time"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.271653452Z level=info msg="Migration successfully executed" id="drop table resource_last_import_time" duration=73.627µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.273813015Z level=info msg="Executing migration" id="create table resource_last_import_time"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.274386747Z level=info msg="Migration successfully executed" id="create table resource_last_import_time" duration=573.409µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.276185796Z level=info msg="Executing migration" id="Add column previous_resource_version in resource_history"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.280747337Z level=info msg="Migration successfully executed" id="Add column previous_resource_version in resource_history" duration=4.561233ms
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.282470258Z level=info msg="Executing migration" id="Add column previous_resource_version in resource"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.286890902Z level=info msg="Migration successfully executed" id="Add column previous_resource_version in resource" duration=4.419693ms
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.289024167Z level=info msg="Executing migration" id="Add index to resource_history for polling"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.289693685Z level=info msg="Migration successfully executed" id="Add index to resource_history for polling" duration=669.188µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.291420075Z level=info msg="Executing migration" id="Add index to resource for loading"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.292059734Z level=info msg="Migration successfully executed" id="Add index to resource for loading" duration=639.189µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.294344286Z level=info msg="Executing migration" id="Add column folder in resource_history"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.300254945Z level=info msg="Migration successfully executed" id="Add column folder in resource_history" duration=5.909928ms
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.302378808Z level=info msg="Executing migration" id="Add column folder in resource"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.30694176Z level=info msg="Migration successfully executed" id="Add column folder in resource" duration=4.562762ms
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.309096064Z level=info msg="Executing migration" id="Migrate DeletionMarkers to real Resource objects"
grafana-1     | logger=deletion-marker-migrator t=2026-03-18T08:58:43.309157892Z level=info msg="finding any deletion markers"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.309395168Z level=info msg="Migration successfully executed" id="Migrate DeletionMarkers to real Resource objects" duration=297.326µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.31109476Z level=info msg="Executing migration" id="Add index to resource_history for get trash"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.311781517Z level=info msg="Migration successfully executed" id="Add index to resource_history for get trash" duration=686.548µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.313504858Z level=info msg="Executing migration" id="Add generation to resource history"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.317989731Z level=info msg="Migration successfully executed" id="Add generation to resource history" duration=4.484542ms
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.320319901Z level=info msg="Executing migration" id="Add generation index to resource history"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.32098861Z level=info msg="Migration successfully executed" id="Add generation index to resource history" duration=668.398µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.322702251Z level=info msg="Executing migration" id="Add UQE_resource_last_import_time_last_import_time index"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.323344591Z level=info msg="Migration successfully executed" id="Add UQE_resource_last_import_time_last_import_time index" duration=642.109µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.325535713Z level=info msg="Executing migration" id="Add key_path column to resource_history"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.330149385Z level=info msg="Migration successfully executed" id="Add key_path column to resource_history" duration=4.612813ms
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.332341456Z level=info msg="Executing migration" id="create table resource_events"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.332995885Z level=info msg="Migration successfully executed" id="create table resource_events" duration=654.288µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.335287206Z level=info msg="Executing migration" id="Add IDX_resource_history_key_path index"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.335957496Z level=info msg="Migration successfully executed" id="Add IDX_resource_history_key_path index" duration=670.179µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.33800123Z level=info msg="Executing migration" id="drop my_row_id and add primary key with columns group,resource to table resource_version if my_row_id exists (auto-generated mysql column)"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.338168827Z level=warn msg="Skipping migration: Already executed, but not recorded in migration log" id="drop my_row_id and add primary key with columns group,resource to table resource_version if my_row_id exists (auto-generated mysql column)"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.340398239Z level=info msg="Executing migration" id="drop unique index UQE_resource_version_group_resource from resource_version table if it exists (mysql)"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.340669624Z level=info msg="Migration successfully executed" id="drop unique index UQE_resource_version_group_resource from resource_version table if it exists (mysql)" duration=271.744µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.342376875Z level=info msg="Executing migration" id="add primary key with columns group,resource to table resource_version if it doesn't exist (mysql)"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.342388165Z level=info msg="Migration successfully executed" id="add primary key with columns group,resource to table resource_version if it doesn't exist (mysql)" duration=11.829µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.34450559Z level=info msg="Executing migration" id="add primary key with columns group,resource to table resource_version (postgres and sqlite)"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.357861301Z level=info msg="Migration successfully executed" id="add primary key with columns group,resource to table resource_version (postgres and sqlite)" duration=13.354523ms
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.360470437Z level=info msg="Executing migration" id="Change key_path collation of resource_history in postgres"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.360482397Z level=info msg="Migration successfully executed" id="Change key_path collation of resource_history in postgres" duration=12.64µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.362913195Z level=info msg="Executing migration" id="Change key_path collation of resource_events in postgres"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.362929014Z level=info msg="Migration successfully executed" id="Change key_path collation of resource_events in postgres" duration=14.37µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.365189797Z level=info msg="Executing migration" id="resource_history key_path backfill"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.36556194Z level=info msg="Migration successfully executed" id="resource_history key_path backfill" duration=371.823µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.367755682Z level=info msg="Executing migration" id="Add index to resource_history for garbage collection"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.368467051Z level=info msg="Migration successfully executed" id="Add index to resource_history for garbage collection" duration=711.479µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.370140952Z level=info msg="Executing migration" id="Fix small resource versions"
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.370514146Z level=info msg="Migration successfully executed" id="Fix small resource versions" duration=372.634µs
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.372634029Z level=info msg="migrations completed" performed=41 skipped=0 duration=142.89021ms
grafana-1     | logger=resource-migrator t=2026-03-18T08:58:43.372945944Z level=info msg="Unlocking database"
grafana-1     | t=2026-03-18T08:58:43.373071932Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.373054391Z msg="Using channel notifier" logger=sql-resource-server
grafana-1     | logger=resource-search t=2026-03-18T08:58:43.377458196Z level=info msg="search index initialized" duration_secs=0 total_docs=0
grafana-1     | logger=storage.unified.migrations t=2026-03-18T08:58:43.377940038Z level=info msg="Running migrations for unified storage"
grafana-1     | logger=storage.unified.migrations t=2026-03-18T08:58:43.382070517Z level=warn msg="Failed to check if migration exists" migration=folders-dashboards error="failed to check migration existence: no such table: unifiedstorage_migration_log"
grafana-1     | logger=storage.unified.migrations t=2026-03-18T08:58:43.382237215Z level=info msg="Resource count for auto migration check" resource=folders.folder.grafana.app count=0 threshold=10
grafana-1     | logger=storage.unified.migrations t=2026-03-18T08:58:43.382298344Z level=warn msg="Failed to check if migration exists" migration=folders-dashboards error="failed to check migration existence: no such table: unifiedstorage_migration_log"
grafana-1     | logger=storage.unified.migrations t=2026-03-18T08:58:43.382411622Z level=info msg="Resource count for auto migration check" resource=dashboards.dashboard.grafana.app count=0 threshold=10
grafana-1     | logger=storage.unified.migrations t=2026-03-18T08:58:43.382424772Z level=info msg="Auto-migration enabled for migration" migration=folders-dashboards
grafana-1     | logger=storage.unified.migrations t=2026-03-18T08:58:43.382437052Z level=info msg="Migration is disabled in config, skipping" migration=shorturls
grafana-1     | logger=unifiedstorage-migrator t=2026-03-18T08:58:43.382466521Z level=info msg="Locking database"
grafana-1     | logger=unifiedstorage-migrator t=2026-03-18T08:58:43.38247324Z level=info msg="Starting DB migrations"
grafana-1     | logger=unifiedstorage-migrator t=2026-03-18T08:58:43.386905675Z level=info msg="Executing migration" id="create unifiedstorage_migration_log table"
grafana-1     | logger=unifiedstorage-migrator t=2026-03-18T08:58:43.387597583Z level=info msg="Migration successfully executed" id="create unifiedstorage_migration_log table" duration=691.628µs
grafana-1     | logger=unifiedstorage-migrator t=2026-03-18T08:58:43.390544634Z level=info msg="Executing migration" id="folders and dashboards migration"
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.390720761Z level=info msg="Starting migration for all organizations" org_count=1 resources="[folders.folder.grafana.app dashboards.dashboard.grafana.app]"
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.39073796Z level=info msg="Stored migrator transaction in context for bulk operations (SQLite compatibility)"
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.390742529Z level=info msg="Migrating organization" org_id=1 namespace=default
grafana-1     | logger=storage.unified.migrator t=2026-03-18T08:58:43.390797639Z level=info msg="start migrating legacy resources" namespace=default orgId=1 stackId=0
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.390809618Z level=info msg="Migration progress" org_id=1 count=-1 message="migrating folders..."
grafana-1     | t=2026-03-18T08:58:43.390968535Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.390961725Z msg="Using SQLite transaction from client context" logger=sql-resource-server
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.395722195Z level=info msg="Migration progress" org_id=1 count=-2 message="finished folders... (0)"
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.395740604Z level=info msg="Migration progress" org_id=1 count=-1 message="migrating dashboards..."
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.396155367Z level=info msg="Migration progress" org_id=1 count=-2 message="finished dashboards... (0)"
grafana-1     | logger=storage.unified.migrator t=2026-03-18T08:58:43.396168477Z level=info msg="finished migrating legacy resources" namespace=default orgId=1 stackId=0
grafana-1     | t=2026-03-18T08:58:43.396189556Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.396184097Z msg="synchronize collection" key=default/folder.grafana.app/folders
grafana-1     | t=2026-03-18T08:58:43.397043133Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.397037912Z msg="get stats (still in transaction)" key=default/folder.grafana.app/folders
grafana-1     | t=2026-03-18T08:58:43.398035786Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.398029826Z msg="successfully locked RV" logger=sql-resource-server nextRV=1773824323396995 key=default/folder.grafana.app/folders
grafana-1     | t=2026-03-18T08:58:43.398195543Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.398191562Z msg="successfully saved RV" logger=sql-resource-server rv=1773824323396995 key=default/folder.grafana.app/folders
grafana-1     | t=2026-03-18T08:58:43.398415888Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.398411328Z msg="synchronize collection" key=default/dashboard.grafana.app/dashboards
grafana-1     | t=2026-03-18T08:58:43.399240064Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.399234834Z msg="get stats (still in transaction)" key=default/dashboard.grafana.app/dashboards
grafana-1     | t=2026-03-18T08:58:43.399970942Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.399964572Z msg="successfully locked RV" logger=sql-resource-server nextRV=1773824323399007 key=default/dashboard.grafana.app/dashboards
grafana-1     | t=2026-03-18T08:58:43.40010775Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.400103809Z msg="successfully saved RV" logger=sql-resource-server rv=1773824323399007 key=default/dashboard.grafana.app/dashboards
grafana-1     | logger=storage.unified.migrator t=2026-03-18T08:58:43.400452464Z level=info msg="start rebuilding index for resources" namespace=default orgId=1 resources="[folders.folder.grafana.app dashboards.dashboard.grafana.app]"
grafana-1     | logger=storage.unified.migrator t=2026-03-18T08:58:43.404697771Z level=info msg="finished rebuilding index for resources" namespace=default orgId=1 resources="[folders.folder.grafana.app dashboards.dashboard.grafana.app]"
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.404928207Z level=info msg="Count validation" resource=folders.folder.grafana.app namespace=default legacy_count=0 unified_count=0 migration_summary_count=0 rejected=0 history=0
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.405111345Z level=info msg="Count validation" resource=dashboards.dashboard.grafana.app namespace=default legacy_count=0 unified_count=0 migration_summary_count=0 rejected=0 history=0
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.405349471Z level=info msg="Folder tree structure validation passed" folder_count=0 namespace=default
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.405364181Z level=info msg="Migration completed for organization" org_id=1 duration=14.613711ms processed=0 summaries=2 rejected=0
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.405369999Z level=info msg="Auto-enabling mode 5 for resource" resource=folders.folder.grafana.app
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.40537362Z level=info msg="Auto-enabling mode 5 for resource" resource=dashboards.dashboard.grafana.app
grafana-1     | logger=storage.unified.migration_runner.folders-dashboards t=2026-03-18T08:58:43.4053765Z level=info msg="Migration completed successfully for all organizations" org_count=1
grafana-1     | logger=unifiedstorage-migrator t=2026-03-18T08:58:43.405381199Z level=info msg="Migration successfully executed" id="folders and dashboards migration" duration=14.836157ms
grafana-1     | logger=unifiedstorage-migrator t=2026-03-18T08:58:43.407362695Z level=info msg="Executing migration" id="playlists migration"
grafana-1     | logger=storage.unified.migration_runner.playlists t=2026-03-18T08:58:43.407489314Z level=info msg="Starting migration for all organizations" org_count=1 resources=[playlists.playlist.grafana.app]
grafana-1     | logger=storage.unified.migration_runner.playlists t=2026-03-18T08:58:43.407501643Z level=info msg="Stored migrator transaction in context for bulk operations (SQLite compatibility)"
grafana-1     | logger=storage.unified.migration_runner.playlists t=2026-03-18T08:58:43.407504973Z level=info msg="Migrating organization" org_id=1 namespace=default
grafana-1     | logger=storage.unified.migrator t=2026-03-18T08:58:43.407523803Z level=info msg="start migrating legacy resources" namespace=default orgId=1 stackId=0
grafana-1     | logger=storage.unified.migration_runner.playlists t=2026-03-18T08:58:43.407532413Z level=info msg="Migration progress" org_id=1 count=-1 message="migrating playlists..."
grafana-1     | t=2026-03-18T08:58:43.407674501Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.40766704Z msg="Using SQLite transaction from client context" logger=sql-resource-server
grafana-1     | logger=storage.unified.migration_runner.playlists t=2026-03-18T08:58:43.40776398Z level=info msg="Migration progress" org_id=1 count=-2 message="finished playlists... (0)"
grafana-1     | logger=storage.unified.migrator t=2026-03-18T08:58:43.407776398Z level=info msg="finished migrating legacy resources" namespace=default orgId=1 stackId=0
grafana-1     | t=2026-03-18T08:58:43.408025394Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.408020465Z msg="synchronize collection" key=default/playlist.grafana.app/playlists
grafana-1     | t=2026-03-18T08:58:43.408845011Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.408840001Z msg="get stats (still in transaction)" key=default/playlist.grafana.app/playlists
grafana-1     | t=2026-03-18T08:58:43.409718356Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.409711556Z msg="successfully locked RV" logger=sql-resource-server nextRV=1773824323408985 key=default/playlist.grafana.app/playlists
grafana-1     | t=2026-03-18T08:58:43.409856283Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.409851973Z msg="successfully saved RV" logger=sql-resource-server rv=1773824323408985 key=default/playlist.grafana.app/playlists
grafana-1     | logger=storage.unified.migrator t=2026-03-18T08:58:43.410041Z level=info msg="start rebuilding index for resources" namespace=default orgId=1 resources=[playlists.playlist.grafana.app]
grafana-1     | logger=storage.unified.migrator t=2026-03-18T08:58:43.410303906Z level=info msg="finished rebuilding index for resources" namespace=default orgId=1 resources=[playlists.playlist.grafana.app]
grafana-1     | logger=storage.unified.migration_runner.playlists t=2026-03-18T08:58:43.410508762Z level=info msg="Count validation" resource=playlists.playlist.grafana.app namespace=default legacy_count=0 unified_count=0 migration_summary_count=0 rejected=0 history=0
grafana-1     | logger=storage.unified.migration_runner.playlists t=2026-03-18T08:58:43.410521842Z level=info msg="Migration completed for organization" org_id=1 duration=3.01217ms processed=0 summaries=1 rejected=0
grafana-1     | logger=storage.unified.migration_runner.playlists t=2026-03-18T08:58:43.410526302Z level=info msg="Migration completed successfully for all organizations" org_count=1
grafana-1     | logger=unifiedstorage-migrator t=2026-03-18T08:58:43.410529382Z level=info msg="Migration successfully executed" id="playlists migration" duration=3.167177ms
grafana-1     | logger=unifiedstorage-migrator t=2026-03-18T08:58:43.412692964Z level=info msg="migrations completed" performed=3 skipped=0 duration=25.836398ms
grafana-1     | logger=unifiedstorage-migrator t=2026-03-18T08:58:43.413000999Z level=info msg="Unlocking database"
grafana-1     | logger=storage.unified.migrations t=2026-03-18T08:58:43.413291725Z level=info msg="Unified storage migrations completed successfully"
grafana-1     | logger=annotations t=2026-03-18T08:58:43.414811118Z level=info msg="Starting annotation dashboard_uid migration in background"
grafana-1     | logger=annotations t=2026-03-18T08:58:43.414823709Z level=info msg="Starting batched dashboard_uid migration for annotations (newest first)" batchSize=5000
grafana-1     | logger=annotations t=2026-03-18T08:58:43.415423068Z level=info msg="Completed dashboard_uid migration for annotations" totalUpdated=0
grafana-1     | logger=annotations t=2026-03-18T08:58:43.415435939Z level=info msg="Annotation dashboard_uid migration completed successfully"
grafana-1     | logger=live.push_http t=2026-03-18T08:58:43.42Z level=info msg="Live Push Gateway initialization"
grafana-1     | logger=ngalert.notifier t=2026-03-18T08:58:43.421117882Z level=info component=alertmanager orgID=1 msg="template definitions loaded" mimir=0 grafana=0 total=0 maxTemplateOutput=10485760
grafana-1     | logger=ngalert.notifier component=alertmanager orgID=1 t=2026-03-18T08:58:43.422588835Z level=info msg="Applying new configuration to Alertmanager" configHash=166dbc8552660bc83256def4ec6c992d
grafana-1     | logger=ngalert.notifier t=2026-03-18T08:58:43.422603406Z level=info component=alertmanager orgID=1 msg="template definitions loaded" mimir=0 grafana=0 total=0 maxTemplateOutput=10485760
grafana-1     | logger=ngalert.writer t=2026-03-18T08:58:43.425389628Z level=info msg="Setting up remote write using data sources" timeout=30s default_datasource_uid=
grafana-1     | logger=ngalert t=2026-03-18T08:58:43.425432747Z level=info msg="Using protobuf-based alert instance store"
grafana-1     | logger=ngalert.state.manager.persist t=2026-03-18T08:58:43.425440067Z level=info msg="Using sync rule state persister (compressed)"
grafana-1     | logger=query_data t=2026-03-18T08:58:43.42588896Z level=info msg="Query Service initialization"
grafana-1     | logger=infra.usagestats.collector t=2026-03-18T08:58:43.427318086Z level=info msg="registering usage stat providers" usageStatsProvidersLen=2
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:43.690632Z level=info msg=starting module=tracing
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:43.690700319Z level=info msg=starting module=grafana-apiserver
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.821341609Z level=info msg="Adding GroupVersion userstorage.grafana.app v0alpha1 to ResourceManager"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.821693723Z level=info msg="Adding GroupVersion preferences.grafana.app v1alpha1 to ResourceManager"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.822153894Z level=info msg="Adding GroupVersion collections.grafana.app v1alpha1 to ResourceManager"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.822344651Z level=info msg="Adding GroupVersion features.grafana.app v0alpha1 to ResourceManager"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.825053564Z level=info msg="Adding GroupVersion dashboard.grafana.app v1beta1 to ResourceManager"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.825403108Z level=info msg="Adding GroupVersion dashboard.grafana.app v0alpha1 to ResourceManager"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.825625145Z level=info msg="Adding GroupVersion dashboard.grafana.app v2beta1 to ResourceManager"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.825829332Z level=info msg="Adding GroupVersion dashboard.grafana.app v2alpha1 to ResourceManager"
grafana-1     | t=2026-03-18T08:58:43.82589416Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.825888291Z msg="Zanzana is not enabled; skipping folder propagation hooks"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.826402671Z level=info msg="Adding GroupVersion folder.grafana.app v1beta1 to ResourceManager"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.829587527Z level=info msg="Adding GroupVersion iam.grafana.app v0alpha1 to ResourceManager"
grafana-1     | t=2026-03-18T08:58:43.829937831Z level=warn caller=logger.go:224 time=2026-03-18T08:58:43.829857112Z msg="Cluster-scoped status subresource without explicit ClusterScopedStorageAuthorizerProvider. Authorization relies on API-level authorizer only." resource=playlists.playlist.grafana.app app=playlist
grafana-1     | t=2026-03-18T08:58:43.8305762Z level=warn caller=logger.go:224 time=2026-03-18T08:58:43.830567411Z msg="Cluster-scoped status subresource without explicit ClusterScopedStorageAuthorizerProvider. Authorization relies on API-level authorizer only." resource=playlists.playlist.grafana.app app=playlist
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.831364118Z level=info msg="Adding GroupVersion playlist.grafana.app v1 to ResourceManager"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.83174494Z level=info msg="Adding GroupVersion playlist.grafana.app v0alpha1 to ResourceManager"
grafana-1     | t=2026-03-18T08:58:43.831811159Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.83178711Z msg="Installed APIs for app" app=playlist
grafana-1     | t=2026-03-18T08:58:43.831879218Z level=warn caller=logger.go:224 time=2026-03-18T08:58:43.831876008Z msg="Cluster-scoped status subresource without explicit ClusterScopedStorageAuthorizerProvider. Authorization relies on API-level authorizer only." resource=metas.plugins.grafana.app app=plugins
grafana-1     | t=2026-03-18T08:58:43.831890958Z level=warn caller=logger.go:224 time=2026-03-18T08:58:43.831888578Z msg="Cluster-scoped status subresource without explicit ClusterScopedStorageAuthorizerProvider. Authorization relies on API-level authorizer only." resource=plugins.plugins.grafana.app app=plugins
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.832810653Z level=info msg="Adding GroupVersion plugins.grafana.app v0alpha1 to ResourceManager"
grafana-1     | t=2026-03-18T08:58:43.832868951Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.832865261Z msg="Installed APIs for app" app=plugins
grafana-1     | t=2026-03-18T08:58:43.832931571Z level=warn caller=logger.go:224 time=2026-03-18T08:58:43.83292852Z msg="Cluster-scoped status subresource without explicit ClusterScopedStorageAuthorizerProvider. Authorization relies on API-level authorizer only." resource=examples.example.grafana.app app=example
grafana-1     | t=2026-03-18T08:58:43.83294307Z level=warn caller=logger.go:224 time=2026-03-18T08:58:43.832939891Z msg="Cluster-scoped subresource without explicit ClusterScopedStorageAuthorizerProvider. Authorization relies on API-level authorizer only." resource=examples.example.grafana.app app=example
grafana-1     | t=2026-03-18T08:58:43.832950019Z level=warn caller=logger.go:224 time=2026-03-18T08:58:43.832947371Z msg="Cluster-scoped status subresource without explicit ClusterScopedStorageAuthorizerProvider. Authorization relies on API-level authorizer only." resource=examples.example.grafana.app app=example
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.83355048Z level=info msg="Adding GroupVersion example.grafana.app v1alpha1 to ResourceManager"
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.833856614Z level=info msg="Adding GroupVersion example.grafana.app v0alpha1 to ResourceManager"
grafana-1     | t=2026-03-18T08:58:43.833920103Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.833915994Z msg="Installed APIs for app" app=example
grafana-1     | logger=grafana-apiserver t=2026-03-18T08:58:43.835002775Z level=info msg="Adding GroupVersion notifications.alerting.grafana.app v0alpha1 to ResourceManager"
grafana-1     | t=2026-03-18T08:58:43.835077673Z level=info caller=logger.go:214 time=2026-03-18T08:58:43.835073774Z msg="Installed APIs for app" app=alerting-notifications
grafana-1     | t=2026-03-18T08:58:44.047653694Z level=info caller=logger.go:214 time=2026-03-18T08:58:44.047642825Z msg="App initialized" app=alerting-notifications
grafana-1     | t=2026-03-18T08:58:44.047731033Z level=info caller=logger.go:214 time=2026-03-18T08:58:44.047728053Z msg="App initialized" app=example
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.047739152Z level=info msg=starting module=plugins.store
grafana-1     | t=2026-03-18T08:58:44.047754512Z level=info caller=logger.go:214 time=2026-03-18T08:58:44.047735682Z msg="App initialized" app=playlist
grafana-1     | t=2026-03-18T08:58:44.047748463Z level=info caller=logger.go:214 time=2026-03-18T08:58:44.047727713Z msg="App initialized" app=plugins
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.047824751Z level=info msg=starting module=plugin.backgroundinstaller
grafana-1     | logger=plugin.backgroundinstaller t=2026-03-18T08:58:44.047839462Z level=info msg="Plugins installed" plugins=[]
grafana-1     | logger=plugin.backgroundinstaller t=2026-03-18T08:58:44.04785907Z level=info msg="Installing plugins" plugins="[{ID:grafana-metricsdrilldown-app Version: URL:} {ID:grafana-lokiexplore-app Version: URL:} {ID:grafana-pyroscope-app Version: URL:} {ID:grafana-exploretraces-app Version: URL:}]"
grafana-1     | logger=plugin.backgroundinstaller t=2026-03-18T08:58:44.04788845Z level=info msg="Installing plugin" pluginId=grafana-metricsdrilldown-app version=
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.047978488Z level=info msg=starting module=provisioning
grafana-1     | logger=provisioning.datasources t=2026-03-18T08:58:44.049228467Z level=info msg="inserting datasource from configuration" name=Prometheus uid=PBFA97CFB590B2093
grafana-1     | logger=provisioning.alerting t=2026-03-18T08:58:44.060280849Z level=warn msg="file has invalid suffix '.gitkeep' (.yaml,.yml,.json accepted), skipping"
grafana-1     | logger=provisioning.alerting t=2026-03-18T08:58:44.060294038Z level=info msg="starting to provision alerting"
grafana-1     | logger=provisioning.alerting t=2026-03-18T08:58:44.060300538Z level=info msg="finished to provision alerting"
grafana-1     | logger=dashboard-service t=2026-03-18T08:58:44.060696202Z level=info msg="not eligible for automated cleanup" reason="dashboard has no folder: Aether Voice"
grafana-1     | logger=bleve-backend namespace=default group=dashboard.grafana.app resource=dashboards size=0 reason=search t=2026-03-18T08:58:44.0620063Z level=info msg="Building index using memory"
grafana-1     | logger=bleve-backend namespace=default group=dashboard.grafana.app resource=dashboards size=0 reason=search t=2026-03-18T08:58:44.062677547Z level=info msg="Finished building index" elapsed=651.289µs listRV=1773824323399007
grafana-1     | logger=bleve-backend namespace=default group=dashboard.grafana.app resource=dashboards size=0 reason=search t=2026-03-18T08:58:44.062698528Z level=info msg="Storing index in cache" key="{Namespace:default Group:dashboard.grafana.app Resource:dashboards}" expiration=2026-03-18T09:08:44.062697907Z
grafana-1     | logger=provisioning.dashboard t=2026-03-18T08:58:44.065232384Z level=info msg="starting to provision dashboards"
grafana-1     | logger=provisioning.dashboard t=2026-03-18T08:58:44.066007681Z level=info msg="finished to provision dashboards"
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068200043Z level=info msg=starting module=*appregistry.Service
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068218283Z level=info msg=starting module=*loginattemptimpl.Service
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068233853Z level=info msg=starting module=*dynamic.KeyRetriever
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068245873Z level=info msg=starting module=*service.DashboardServiceImpl
grafana-1     | logger=app-registry t=2026-03-18T08:58:44.068248793Z level=info msg="app registry initialized"
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068259262Z level=info msg=starting module=*updatemanager.PluginsService
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068260593Z level=info msg=starting module=*anonimpl.AnonDeviceService
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068267193Z level=info msg=starting module=*dualwrite.ZanzanaReconciler
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068282422Z level=info msg=starting module=*api.HTTPServer
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068290553Z level=info msg=starting module=*migrations.SecretMigrationProviderImpl
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068296113Z level=info msg=starting module=*rendering.RenderingService
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068341081Z level=info msg=starting module=*supportbundlesimpl.Service
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.06836326Z level=info msg=starting module=*statscollector.Service
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068384271Z level=info msg=starting module=*authz.EmbeddedZanzanaService
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.06839609Z level=info msg=starting module=*manager.ServiceAccountsService
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068474928Z level=info msg=starting module=*authimpl.UserAuthTokenService
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068550137Z level=info msg=starting module=*service.DashboardUpdater
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068280762Z level=info msg=starting module=*ngalert.AlertNG
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068603686Z level=info msg=starting module=*live.GrafanaLive
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068638576Z level=info msg=starting module=*cleanup.CleanUpService
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068733564Z level=info msg=starting module=*angulardetectorsprovider.Dynamic
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068714865Z level=info msg=starting module=*notifications.NotificationService
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068199474Z level=info msg=starting module=*manager.SecretsService
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068770344Z level=info msg=starting module=*pluginexternal.Service
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068241153Z level=info msg=starting module=*ssosettingsimpl.Service
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068798933Z level=info msg=starting module=*remotecache.RemoteCache
grafana-1     | logger=ngalert t=2026-03-18T08:58:44.070069271Z level=info msg="Primary node, alert rule evaluation enabled"
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.070206929Z level=info msg=starting module=*metrics.InternalMetricsService
grafana-1     | logger=ngalert.state.manager t=2026-03-18T08:58:44.070229199Z level=info msg="Warming state cache for startup"
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.070382866Z level=info msg=starting module=*service.UsageStats
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.070426485Z level=info msg=starting module=*metric.Service
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.070447255Z level=info msg=starting module=*pushhttp.Gateway
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.070490115Z level=info msg=starting module=*updatemanager.GrafanaService
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.070554133Z level=info msg=starting module=*garbagecollectionworker.Worker
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.070564223Z level=info msg=starting module=*store.standardStorageService
grafana-1     | logger=ngalert.multiorg.alertmanager t=2026-03-18T08:58:44.070604202Z level=info msg="Starting MultiOrg Alertmanager"
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.068286713Z level=info msg=starting module=*store.dummyEntityEventsService
grafana-1     | logger=grafanaStorageLogger t=2026-03-18T08:58:44.070735591Z level=info msg="Storage starting"
grafana-1     | logger=backgroundsvcs.managerAdapter t=2026-03-18T08:58:44.070864328Z level=info msg="All modules healthy"
grafana-1     | logger=http.server t=2026-03-18T08:58:44.074701262Z level=info msg="HTTP Server Listen" address=[::]:3000 protocol=http subUrl= socket=
grafana-1     | logger=ngalert.state.manager t=2026-03-18T08:58:44.126724334Z level=info msg="State cache has been initialized" states=0 duration=56.495866ms
grafana-1     | logger=ngalert.scheduler t=2026-03-18T08:58:44.126758643Z level=info msg="Starting scheduler" tickInterval=10s maxAttempts=3
grafana-1     | logger=ngalert.scheduler t=2026-03-18T08:58:44.126795183Z level=info msg=starting component=ticker first_tick=2026-03-18T08:58:50Z
grafana-1     | logger=plugins.update.checker t=2026-03-18T08:58:44.148114999Z level=info msg="Update check succeeded" duration=79.845787ms
grafana-1     | logger=plugins.update.checker t=2026-03-18T08:58:44.148179558Z level=info msg="flag evaluation succeeded" flag="{Value:false EvaluationDetails:{FlagKey:pluginsAutoUpdate FlagType:bool ResolutionDetail:{Variant:default Reason:STATIC ErrorCode: ErrorMessage: FlagMetadata:map[]}}}" details="{Value:false EvaluationDetails:{FlagKey:pluginsAutoUpdate FlagType:bool ResolutionDetail:{Variant:default Reason:STATIC ErrorCode: ErrorMessage: FlagMetadata:map[]}}}"
grafana-1     | logger=grafana.update.checker t=2026-03-18T08:58:44.15040853Z level=info msg="Update check succeeded" duration=79.851717ms
grafana-1     | logger=plugin.angulardetectorsprovider.dynamic t=2026-03-18T08:58:44.243924983Z level=info msg="Patterns update finished" duration=95.423611ms
grafana-1     | logger=plugin.installer t=2026-03-18T08:58:44.452375524Z level=info msg="Installing plugin" pluginId=grafana-metricsdrilldown-app version=
grafana-1     | logger=installer.fs t=2026-03-18T08:58:44.517470473Z level=info msg="Downloaded and extracted grafana-metricsdrilldown-app v1.0.34 zip successfully to /var/lib/grafana/plugins/grafana-metricsdrilldown-app"
grafana-1     | logger=plugins.registration t=2026-03-18T08:58:44.54981339Z level=info msg="Plugin registered" pluginId=grafana-metricsdrilldown-app
grafana-1     | logger=plugin.backgroundinstaller t=2026-03-18T08:58:44.54983637Z level=info msg="Plugin successfully installed" pluginId=grafana-metricsdrilldown-app version= duration=501.94351ms
grafana-1     | logger=plugin.backgroundinstaller t=2026-03-18T08:58:44.54985522Z level=info msg="Installing plugin" pluginId=grafana-lokiexplore-app version=
grafana-1     | logger=plugin.installer t=2026-03-18T08:58:45.558473789Z level=info msg="Installing plugin" pluginId=grafana-lokiexplore-app version=
grafana-1     | logger=installer.fs t=2026-03-18T08:58:45.680670653Z level=info msg="Downloaded and extracted grafana-lokiexplore-app v1.0.41 zip successfully to /var/lib/grafana/plugins/grafana-lokiexplore-app"
grafana-1     | logger=plugins.registration t=2026-03-18T08:58:45.709595399Z level=info msg="Plugin registered" pluginId=grafana-lokiexplore-app
grafana-1     | logger=plugin.backgroundinstaller t=2026-03-18T08:58:45.709618698Z level=info msg="Plugin successfully installed" pluginId=grafana-lokiexplore-app version= duration=1.159758829s
grafana-1     | logger=plugin.backgroundinstaller t=2026-03-18T08:58:45.709636508Z level=info msg="Installing plugin" pluginId=grafana-pyroscope-app version=
grafana-1     | logger=plugin.installer t=2026-03-18T08:58:46.103493643Z level=info msg="Installing plugin" pluginId=grafana-pyroscope-app version=
grafana-1     | logger=installer.fs t=2026-03-18T08:58:46.160220364Z level=info msg="Downloaded and extracted grafana-pyroscope-app v1.17.0 zip successfully to /var/lib/grafana/plugins/grafana-pyroscope-app"
grafana-1     | logger=plugins.registration t=2026-03-18T08:58:46.178341645Z level=info msg="Plugin registered" pluginId=grafana-pyroscope-app
grafana-1     | logger=plugin.backgroundinstaller t=2026-03-18T08:58:46.178360435Z level=info msg="Plugin successfully installed" pluginId=grafana-pyroscope-app version= duration=468.719687ms
grafana-1     | logger=plugin.backgroundinstaller t=2026-03-18T08:58:46.178380395Z level=info msg="Installing plugin" pluginId=grafana-exploretraces-app version=
grafana-1     | logger=plugin.installer t=2026-03-18T08:58:46.536581628Z level=info msg="Installing plugin" pluginId=grafana-exploretraces-app version=
grafana-1     | logger=installer.fs t=2026-03-18T08:58:46.601371662Z level=info msg="Downloaded and extracted grafana-exploretraces-app v1.4.1 zip successfully to /var/lib/grafana/plugins/grafana-exploretraces-app"
grafana-1     | logger=plugins.registration t=2026-03-18T08:58:46.621729814Z level=info msg="Plugin registered" pluginId=grafana-exploretraces-app
grafana-1     | logger=plugin.backgroundinstaller t=2026-03-18T08:58:46.621753683Z level=info msg="Plugin successfully installed" pluginId=grafana-exploretraces-app version= duration=443.368739ms
tts-1         | INFO:     172.18.0.14:33422 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:44322 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:57,789", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:57,797", "taskName": "Task-10"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:57,820", "taskName": "Task-10"}
tts-1         | INFO:     172.18.0.11:46338 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:58:57,825", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:44122 - "GET /v1/health HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.14:60648 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:55968 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:06,863", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:06,875", "taskName": "Task-11"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:06,897", "taskName": "Task-11"}
tts-1         | INFO:     172.18.0.11:45848 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:06,903", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:48464 - "GET /v1/health HTTP/1.1" 200 OK
tts-1         | INFO:     172.18.0.14:56306 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:55980 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:12,813", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:12,822", "taskName": "Task-13"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:12,849", "taskName": "Task-13"}
tts-1         | INFO:     172.18.0.11:45856 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:12,855", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:48474 - "GET /v1/health HTTP/1.1" 200 OK
grafana-1     | logger=dashboard-service t=2026-03-18T08:59:14.075220874Z level=info msg="No last resource version found, starting from scratch" orgID=1
asr-1         | INFO:     172.18.0.14:47848 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:37882 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:21,883", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:21,892", "taskName": "Task-14"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:21,919", "taskName": "Task-14"}
tts-1         | INFO:     172.18.0.11:41502 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:21,924", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:48606 - "GET /v1/health HTTP/1.1" 200 OK
tts-1         | INFO:     172.18.0.14:55916 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:38040 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:27,805", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:27,813", "taskName": "Task-16"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:27,839", "taskName": "Task-16"}
tts-1         | INFO:     172.18.0.11:57236 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:27,845", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:42540 - "GET /v1/health HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.14:58814 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:38866 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,724", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
asr-1         | INFO:     172.18.0.11:38866 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,731", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,733", "taskName": "Task-17"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,755", "taskName": "Task-17"}
tts-1         | INFO:     172.18.0.11:50070 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,760", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:56046 - "GET /api/health HTTP/1.1" 200 OK
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,770", "taskName": "Task-18"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,792", "taskName": "Task-18"}
tts-1         | INFO:     172.18.0.11:50084 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,797", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:56060 - "GET /v1/health HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:38866 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,865", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,873", "taskName": "Task-19"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,899", "taskName": "Task-19"}
tts-1         | INFO:     172.18.0.11:50070 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:36,905", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:56070 - "GET /v1/health HTTP/1.1" 200 OK
tts-1         | INFO:     172.18.0.14:40728 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:40458 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:43,735", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:43,743", "taskName": "Task-21"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:43,771", "taskName": "Task-21"}
tts-1         | INFO:     172.18.0.11:41154 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:43,776", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:50068 - "GET /v1/health HTTP/1.1" 200 OK
grafana-1     | logger=dashboard-service t=2026-03-18T08:59:44.073057317Z level=info msg="No last resource version found, starting from scratch" orgID=1
asr-1         | INFO:     172.18.0.14:44072 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:40474 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:51,872", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:51,880", "taskName": "Task-22"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:51,909", "taskName": "Task-22"}
tts-1         | INFO:     172.18.0.11:41164 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:51,914", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:50070 - "GET /v1/health HTTP/1.1" 200 OK
tts-1         | INFO:     172.18.0.14:39158 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:37262 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:58,716", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:58,724", "taskName": "Task-24"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:58,747", "taskName": "Task-24"}
tts-1         | INFO:     172.18.0.11:36830 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 08:59:58,756", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:56098 - "GET /v1/health HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.14:47988 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:47824 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 09:00:06,881", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 09:00:06,890", "taskName": "Task-25"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 09:00:06,913", "taskName": "Task-25"}
tts-1         | INFO:     172.18.0.11:45758 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 09:00:06,918", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:38608 - "GET /v1/health HTTP/1.1" 200 OK
tts-1         | INFO:     172.18.0.14:36316 - "GET /metrics HTTP/1.1" 200 OK
asr-1         | INFO:     172.18.0.11:47870 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 09:00:13,716", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://kokoro:8026/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 09:00:13,724", "taskName": "Task-27"}
tts-1         | {"level": "INFO", "message": "HTTP Request: GET http://moss-voice-generator:8024/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 09:00:13,747", "taskName": "Task-27"}
tts-1         | INFO:     172.18.0.11:39664 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1     | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-18 09:00:13,752", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1     | INFO:     172.18.0.1:34878 - "GET /v1/health HTTP/1.1" 200 OK
grafana-1     | logger=dashboard-service t=2026-03-18T09:00:14.07232476Z level=info msg="No last resource version found, starting from scratch" orgID=1
^C
