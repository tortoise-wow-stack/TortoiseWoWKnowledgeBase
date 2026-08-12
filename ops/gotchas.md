---
type: Reference
title: Operational gotchas
description: Client build gate, image portability, build hygiene, migration safety, shell pipelines, and command targeting.
tags: [ops, gotchas]
status: stable
generated: { by: pi/agent, at: 2026-08-12T12:00:00Z }
sources:
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
  - id: packaging
    resource: https://github.com/Nescabir/tortoise-docker
    title: Tortoise Docker packaging
---
**Related:** [Persistence map](/ops/persistence.md) · [Project history](/history/implementation-plan.md)

## Operational gotchas

- **Client build gate:** `RealmList.cpp` defines accepted builds through `ExpectedRealmdClientBuilds`; this fork's lower bound is build 7272. A build 7234 client is rejected with “Unable to validate game version.” Changing the gate requires a source change, rebuild, and compatibility test—it is not a `realmlist.wtf` setting.
- **Prebuilt-image portability:** validate a prebuilt image on the target CPU. If `realmd` or `mangosd` exits with `SIGILL`, preserve the exact failure evidence and image provenance, avoid asserting an unproved ISA cause, and use a reproducible local build as the fallback. Promote an image only after boot and in-game tests.
- **Build provenance:** record packaging commit/status, resolved source commit, build arguments, toolchain/base image, and resulting image digest. Pin the tested source/image and retain the last known-good image for rollback.
- **Build-context hygiene:** use `.dockerignore` to exclude `.env`, credentials, logs, database dumps, client archives, and unrelated workspaces. Remove large build trees in the same Dockerfile layer that creates them; deleting them in a later layer does not reclaim the earlier layer's space.
- **Disk and DNS preflight:** check available space, inode use, and name resolution before a long build. Record any temporary resolver workaround only in the private deployment record and restore the host's normal policy afterward.
- **`pipefail` and `grep -q`:** under `set -o pipefail`, `producer | grep -q pattern` may return failure when an early successful match closes the pipe and the producer exits with SIGPIPE/141. Fully consume the stream or explicitly handle `PIPESTATUS` in readiness gates.
- **DB re-initialization:** database data and its initialization marker form one consistency boundary. Reset them together only after a verified dump; never reset one while retaining the other.
- **Initializer false success:** error-tolerant SQL execution can continue after a failed statement. Preserve the full initializer log, inspect SQL errors, assert required schema/migration state, and prove current-process world readiness.
- **MMAP generation:** this fork may return a nonzero completion code in silent mode. Accept it only with independent completeness checks: expected map coverage, non-empty required GameObject navmeshes, and no failure lines.
- **`.additem` targeting:** `.additem` acts on the current target. Clear the target before giving an item to yourself; with a bot targeted, the item can land in the bot's bags.
