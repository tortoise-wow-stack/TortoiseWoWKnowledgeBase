# ops — index

* [Access & status](access-status.md) - Deployment-agnostic procedure for proving the current world-server process is alive.
* [Accounts & permissions](accounts.md) - Accounts, security levels (rank 0-6), how GM rights apply and refresh.
* [Admin recipes via DB](admin-recipes.md) - Verified SQL: who is online, kick, password reset, gold, mail items, delete characters.
* [Server console & server control](console.md) - Console command set, pending_commands DB queue, server shutdown/restart.
* [Everyday tasks](everyday-tasks.md) - Deployment-agnostic procedures for restart, logs, console, bot population, and backup.
* [Operational gotchas](gotchas.md) - Client build gate, image portability, build hygiene, migration safety, shell pipelines, and targeting.
* [Housing & character services](housing-services.md) - Guild housing (teleport bookmarks), shop-token character services (rename/race/appearance), and the variable/worldstate persistence.
* [Logs, monitoring & recovery](logs-monitoring.md) - Log files and levels, .perf, crash recovery, AutoRestart, db-init migrations, disk growth.
* [Persistence map](persistence.md) - Which config edits survive container recreates, ranked, with caveats.
* [Hot-reload commands](reloads.md) - The full .reload table list — what can change without a restart.
* [Reference topology](topology.md) - Deployment-neutral Compose services, data boundaries, network exposure, and storage preflight.
