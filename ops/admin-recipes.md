---
type: Playbook
title: Admin recipes via DB
description: "Verified SQL: who is online, kick, password reset, gold, mail items, delete characters."
tags: ["ops", "db", "admin"]
resource: mariadb://tw_char
status: stable
generated: { by: pi/agent, at: 2026-08-18T17:00:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: live-server
    resource: <live server, read-only access>
    title: Read-only audit of a live server (DB, configs, logs)
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---
**Related:** [Console](/ops/console.md) · [Accounts & permissions](/ops/accounts.md)

## §12 — Admin recipes via DB

Use the owner-approved database access method from the private deployment record. Prefer `docker compose exec` with credentials supplied through the deployment's protected environment, and avoid placing passwords in shell history, process arguments, or documentation. Start with a read-only query and take a verified dump before writes that are difficult to reverse.

**Who is online:**

```sql
SELECT c.name, c.level, c.map, c.zone, a.username FROM tw_char.characters c
JOIN tw_logon.account a ON a.id = c.account WHERE c.online = 1;
```

**Kick:** no DB flag — console only: `.kick <name> [force]` via FIFO.

**Password reset** (SRP6 — hash = SHA1(UPPER(user)+":"+UPPER(pass))):

```sql
UPDATE tw_logon.account SET sha_pass_hash = UPPER(SHA1(CONCAT(UPPER(username),':',UPPER('<new-password>')))),
  sessionkey = NULL, v = NULL, s = NULL WHERE username = '<account-name>';
```

(no restart; player relogs)

**Gold:** `characters.money` is copper — `UPDATE tw_char.characters SET money = money + 100000 WHERE guid = <guid>;` (relog required).

**Mail an item (system mail, instant):**

```sql
INSERT INTO tw_char.item_instance (guid, itemEntry, owner_guid, creatorGuid, giftCreatorGuid, count,
  duration, charges, flags, enchantments, randomPropertyId, transmogrifyId, durability, text, generated_loot)
  VALUES ((SELECT MAX(guid)+1 FROM tw_char.item_instance), <entry>, <char_guid>, 0, 0, 1, 0, '', 0, '', 0, 0, 0, 0, 0);
INSERT INTO tw_char.mail (id, messageType, stationery, mailTemplateId, sender, receiver, subject, itemTextId,
  has_items, expire_time, deliver_time, money, cod, checked, isDeleted)
  VALUES (NULL, 0, 41, 0, 0, <char_guid>, 'Subject', 0, 1, UNIX_TIMESTAMP()+259200, UNIX_TIMESTAMP(), 0, 0, 0, 0);
INSERT INTO tw_char.mail_items (mail_id, item_guid, item_template, receiver)
  VALUES (LAST_INSERT_ID(), <item_instance_guid>, <entry>, <char_guid>);
```

**Delete a character** — the core's soft delete: `UPDATE tw_char.characters SET deleteInfos_Name=name, deleteInfos_Account=account, deleteDate=UNIX_TIMESTAMP(), name='', account=0 WHERE guid=<g>;` (restorable: clear those columns). Hard wipe = delete child rows yourself (`character_inventory`, `item_instance` by owner_guid, `character_aura/skills/spell/queststatus/reputation/action/social/titles/homebind/instance/pet/transmogs`, `mail` by receiver, `guild_member`, `corpse`, then `characters`). **No FK cascades anywhere — manual deletes must clean children.**

**Inventory internals:** `character_inventory` (guid, bag, slot, item→item_instance.guid, item_template); slots: 0–18 equipped, 19–22 bags, 23–38 backpack. Item add via DB = `item_instance` + `character_inventory` row; easier: `.additem` in-game or mail recipe above.

**Guilds:** vanilla-style — buy Guild Charter (item 5863), 9 signatures (`petition`/`petition_sign`), turn in; GM shortcut: console `.guild create <name> <leader>`. Bot guilds draw names from `ai_playerbot_guild_names` (400 candidates).

**Reset the random-bot pool to a fresh level-1 start** (verified on a live deployment):

1. Take a verified dump first (see the private record's backup procedure; `mariadb-dump` on MariaDB 11+, not `mysqldump`).
2. In the bot conf: `AiPlayerbot.DisableRandomLevels = 1`, `AiPlayerbot.randombotStartingLevel = 1`, `AiPlayerbot.RandomBotMaxLevelChance = 0` (without this, ~15% of the "level-1" pool spawns at max level), and `AiPlayerbot.DeleteRandomBotAccounts = 1` — the built-in one-shot reset: at next startup the core deletes all RNDBOT accounts and `RandomBotAutoCreate` rebuilds the pool with the current level settings.
3. Restart, wait for account/character creation to finish, then verify the pool is all at the starting level:

```sql
SELECT level, COUNT(*) FROM tw_char.characters
WHERE account IN (SELECT id FROM tw_logon.account WHERE username LIKE 'RNDBOT%')
GROUP BY level;
```

4. Set `DeleteRandomBotAccounts` back to 0 and restart again — leaving it at 1 wipes the pool on every boot.

Notes: the offline pool does not progress while logged out; with a wide pool and a small online target, rotation dilutes per-character leveling (a 4,500-character pool with 500 online puts each character online ~10% of the time). Shrink the pool (`RandomBotAccountCount`) to concentrate progression on the online set. Fresh level-1 pools crowd into the six racial starting zones until the curve grows (see [PlayerBots config](/playerbots/config.md#fresh-level-1-starts)); custom-race bots may be placed at classic starting spawns rather than their own zones.

**Gotchas:** all money in copper; inventory/money edits need the char offline + relog; `mail.id` auto_increment, `auction.id` not; `characters.name` unique (deleted chars renamed to `''`); `character_bck` table = schema-only backup copy (empty).
