---
type: Playbook
title: Access & status
description: Deployment-agnostic procedure for proving the current world-server process is alive.
tags: [ops, status]
resource: ssh://<server>
status: stable
generated: { by: pi/agent, at: 2026-08-12T12:00:00Z }
sources:
  - id: packaging
    resource: https://github.com/Nescabir/tortoise-docker
    title: Tortoise Docker packaging
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---
**Related:** [Everyday tasks](/ops/everyday-tasks.md) · [Logs, monitoring & recovery](/ops/logs-monitoring.md)

## Access & status

Obtain the endpoint, SSH method, Compose directory, and privilege model from the owner's private deployment record. Start read-only:

```bash
ssh <ssh-alias>
cd <compose-dir>
<docker-prefix> docker compose ps
<docker-prefix> docker compose ps -q realmd mangosd
```

`<docker-prefix>` is empty when the deployment user may access Docker directly, otherwise it is normally `sudo -n`.

Inspect the current application processes without hardcoding generated container names:

```bash
for service in realmd mangosd; do
  id=$(<docker-prefix> docker compose ps -q "$service")
  <docker-prefix> docker inspect -f \
    '{{.Name}} status={{.State.Status}} restarts={{.RestartCount}} started={{.State.StartedAt}} exit={{.State.ExitCode}}' \
    "$id"
done
```

Expected healthy state: the database service is healthy; `realmd` and `mangosd` are running; neither application service is restarting; restart counts remain stable across two observations.

Prove readiness belongs to the current process, not an old log:

```bash
id=$(<docker-prefix> docker compose ps -q mangosd)
started=$(<docker-prefix> docker inspect -f '{{.State.StartedAt}}' "$id")
<docker-prefix> docker logs --since "$started" "$id" 2>&1 \
  | grep "World server is up and running"
```

Completion: the current `mangosd` process stays `running`, its restart count does not rise, and its logs contain a readiness line emitted after its current `StartedAt`. A historical readiness line alone is not health evidence.
