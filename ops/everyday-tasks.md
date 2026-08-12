---
type: Playbook
title: Everyday tasks
description: Deployment-agnostic procedures for restart, logs, console, bot population, and backup.
tags: [ops, tasks]
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
**Related:** [Server console](/ops/console.md) · [Admin recipes via DB](/ops/admin-recipes.md) · [Hot-reload commands](/ops/reloads.md)

## Everyday tasks

The owner-supplied deployment record provides `<ssh-alias>`, `<compose-dir>`, `<docker-prefix>`, backup command, and storage destinations. Commands below assume a shell on the host inside `<compose-dir>`.

**Restart the realm and world** only after an approved config change or a diagnosis showing a restart can help:

```bash
<docker-prefix> docker compose restart realmd mangosd
```

Do not repeatedly restart a crash loop. Capture the first fatal SQL/assertion trace and resolve its cause. Completion: use the current-process health proof in [Access & status](/ops/access-status.md); the first PlayerBots boot can take several minutes.

**Watch logs:**

```bash
<docker-prefix> docker compose logs -f --tail 50 mangosd
```

**Send a server-console command** by writing exactly one line to the container-internal FIFO:

```bash
<docker-prefix> docker compose exec -T -u turtle mangosd bash -c \
  "printf '%s\n' '<console-command>' > /opt/turtle/run/mangosd.in"
```

Completion: find the command's response in current `mangosd` logs and verify its intended state through the relevant read-only query.

**Change random-bot population:** edit `AI_MIN_RANDOM_BOTS` and `AI_MAX_RANDOM_BOTS` in the private `.env`, validate the rendered Compose configuration, then recreate only `mangosd`:

```bash
<docker-prefix> docker compose config >/dev/null
<docker-prefix> docker compose up -d mangosd
```

Completion: current-process readiness succeeds and PlayerBots logs report the intended population behavior. Measure CPU, memory, and tick quality before increasing again.

**Back up safely:** use the deployment's approved backup command. A complete backup procedure must:

1. capture all realm schemas consistently, quiescing writers when nontransactional tables require it;
2. verify the compressed output and record a checksum;
3. store a redacted provenance manifest with source/image version, client build, and timestamp;
4. keep secrets in a separately protected location; and
5. periodically restore into an isolated database and prove the restored world can start.

Completion: a new checksum-verified dump exists and the restore-test schedule or latest isolated restore result is recorded in the private deployment record. A successful dump command without a restore test is not sufficient recovery evidence.
