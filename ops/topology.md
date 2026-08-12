---
type: Reference
title: Reference topology
description: Deployment-agnostic Compose services, data boundaries, network exposure, and storage preflight.
tags: [ops, topology]
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

## Reference topology

```text
host
├── Compose checkout
│   ├── private .env                 secrets and deployment values
│   └── packaging / render scripts
├── Compose services
│   ├── db                           MariaDB, private to the Compose network
│   ├── db-init                      one-shot base-schema and migration initializer
│   ├── realmd                       authentication and realm-list service
│   └── mangosd                      world service and PlayerBots
├── persistent Docker volumes
│   ├── database data
│   ├── initialization marker
│   └── world logs
└── client-derived data mount
    ├── dbc/
    ├── maps/
    ├── vmaps/
    └── mmaps/
```

The world console FIFO is a container-runtime invariant at `/opt/turtle/run/mangosd.in`. Host checkout, storage, backup, network, and credential paths are deployment choices and belong only in the owner's private record.

## Network boundary

- Publish only the realm and world endpoints needed by trusted clients.
- Keep MariaDB private to the Compose network unless an explicit secured administration design requires otherwise.
- Bind or firewall game endpoints to the intended LAN/VPN boundary rather than exposing them generally.
- Audit existing listeners and co-tenants before changing ports, firewall rules, CPU/RAM allocation, storage, or container runtime settings.

## Storage preflight

Before formatting, mounting, moving, or pruning storage:

1. positively identify each filesystem by stable attributes and existing contents;
2. obtain owner approval for destructive or service-affecting changes;
3. verify persistent mount configuration and service-account permissions;
4. keep latency-sensitive database/log data on suitable storage;
5. place bulky extracted client data and backups according to measured capacity and recovery needs; and
6. preserve the only copy of source/client data until a login and restart-persistence test succeeds.

Do not infer a deployment's hostnames, addresses, capacities, devices, paths, services, or image tags from this reference topology.
