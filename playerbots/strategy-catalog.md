---
type: Reference
title: PlayerBots strategy catalog
description: "Generated exhaustive generic and class strategy registration names at the pinned source commit."
tags: ["playerbots", "strategies", "catalog", "generated"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: process:playerbots-catalog-generator, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


Generated from strategy creator registrations at `172ee948e591f8bf1b53ea6389e3102186339f6e`. The scanned union contains **767 unique names**. Strategies are context-sensitive: a bot receives generic plus its class/build contexts, not this entire union. Unknown names can be silently ignored. Expansion-gated classes such as death knight are not available in the Classic build. Use [actions/strategies](actions-strategies.md) for mutation syntax and role caveats.

## Generic and shared registrations

* `accept all quests`
* `ads`
* `ai chat`
* `alterac`
* `arathi`
* `arena`
* `attack tagged`
* `avoid aoe`
* `avoid mobs`
* `battleground`
* `behind`
* `bg`
* `blackwing lair`
* `cast time`
* `chase jump`
* `chat`
* `close`
* `collision`
* `conserve mana`
* `consumables`
* `custom`
* `dead`
* `debug`
* `debug action`
* `debug equip`
* `debug grind`
* `debug llm`
* `debug log`
* `debug logname`
* `debug loot`
* `debug mount`
* `debug move`
* `debug rpg`
* `debug spell`
* `debug stuck`
* `debug threat`
* `debug travel`
* `debug xp`
* `default`
* `delayed roll`
* `dps aoe`
* `dps assist`
* `duel`
* `dungeon`
* `emote`
* `explore`
* `eye`
* `fish`
* `flee`
* `flee from adds`
* `focus heal targets`
* `focus rti targets`
* `follow`
* `follow jump`
* `food`
* `four horseman`
* `free`
* `gather`
* `glyph`
* `grind`
* `group`
* `guard`
* `guild`
* `heal interrupt`
* `isle`
* `karazhan`
* `kite`
* `lfg`
* `loot`
* `magmadar`
* `maintenance`
* `map`
* `map full`
* `mark rti`
* `molten core`
* `mount`
* `naxxramas`
* `netherspite`
* `nowar`
* `onyxia`
* `onyxia's lair`
* `passive`
* `potions`
* `preheal`
* `prince malchezaar`
* `pull back`
* `pvp`
* `quest`
* `racials`
* `ranged`
* `ready check`
* `return`
* `reveal`
* `roll`
* `rpg`
* `rpg bg`
* `rpg craft`
* `rpg explore`
* `rpg guild`
* `rpg jump`
* `rpg maintenance`
* `rpg player`
* `rpg quest`
* `rpg vendor`
* `rtsc`
* `rtsc jump`
* `runaway`
* `silent`
* `sit`
* `start duel`
* `stay`
* `suppression room`
* `tank assist`
* `tell target`
* `test`
* `tfish`
* `threat`
* `travel`
* `travel once`
* `wait for attack`
* `wander`
* `warsong`
* `wbuff`
* `wbuff travel`

## Class registrations

### deathknight (11 registrations; 11 unique)

* `bdps`
* `blood`
* `dksquest`
* `frost`
* `frost aoe`
* `nc`
* `pull`
* `react`
* `tank`
* `unholy`
* `unholy aoe`

### druid (100 registrations; 100 unique)

* `aoe`
* `aoe balance pve`
* `aoe balance pvp`
* `aoe balance raid`
* `aoe dps feral pve`
* `aoe dps feral pvp`
* `aoe dps feral raid`
* `aoe restoration pve`
* `aoe restoration pvp`
* `aoe restoration raid`
* `aoe tank feral pve`
* `aoe tank feral pvp`
* `aoe tank feral raid`
* `balance`
* `balance pve`
* `balance pvp`
* `balance raid`
* `bear`
* `boost`
* `boost balance pve`
* `boost balance pvp`
* `boost balance raid`
* `boost dps feral pve`
* `boost dps feral pvp`
* `boost dps feral raid`
* `boost restoration pve`
* `boost restoration pvp`
* `boost restoration raid`
* `boost tank feral pve`
* `boost tank feral pvp`
* `boost tank feral raid`
* `buff`
* `buff balance pve`
* `buff balance pvp`
* `buff balance raid`
* `buff dps feral pve`
* `buff dps feral pvp`
* `buff dps feral raid`
* `buff restoration pve`
* `buff restoration pvp`
* `buff restoration raid`
* `buff tank feral pve`
* `buff tank feral pvp`
* `buff tank feral raid`
* `cat`
* `cc`
* `cc balance pve`
* `cc balance pvp`
* `cc balance raid`
* `cc dps feral pve`
* `cc dps feral pvp`
* `cc dps feral raid`
* `cc restoration pve`
* `cc restoration pvp`
* `cc restoration raid`
* `cc tank feral pve`
* `cc tank feral pvp`
* `cc tank feral raid`
* `cure`
* `cure balance pve`
* `cure balance pvp`
* `cure balance raid`
* `cure dps feral pve`
* `cure dps feral pvp`
* `cure dps feral raid`
* `cure restoration pve`
* `cure restoration pvp`
* `cure restoration raid`
* `cure tank feral pve`
* `cure tank feral pvp`
* `cure tank feral raid`
* `dps feral`
* `dps feral pve`
* `dps feral pvp`
* `dps feral raid`
* `heal`
* `leveling`
* `leveling pve`
* `leveling pvp`
* `leveling raid`
* `offheal`
* `offheal pve`
* `offheal pvp`
* `offheal raid`
* `powershift`
* `pull`
* `restoration`
* `restoration pve`
* `restoration pvp`
* `restoration raid`
* `stealth`
* `stealth dps feral pve`
* `stealth dps feral pvp`
* `stealth dps feral raid`
* `stealthed`
* `tank`
* `tank feral`
* `tank feral pve`
* `tank feral pvp`
* `tank feral raid`

### hunter (85 registrations; 85 unique)

* `aoe`
* `aoe beast mastery pve`
* `aoe beast mastery pvp`
* `aoe beast mastery raid`
* `aoe marksmanship pve`
* `aoe marksmanship pvp`
* `aoe marksmanship raid`
* `aoe survival pve`
* `aoe survival pvp`
* `aoe survival raid`
* `aspect`
* `aspect beast`
* `aspect beast mastery pve`
* `aspect beast mastery pvp`
* `aspect beast mastery raid`
* `aspect cheetah`
* `aspect dragonhawk`
* `aspect hawk`
* `aspect marksmanship pve`
* `aspect marksmanship pvp`
* `aspect marksmanship raid`
* `aspect monkey`
* `aspect pack`
* `aspect survival pve`
* `aspect survival pvp`
* `aspect survival raid`
* `aspect viper`
* `aspect wild`
* `beast mastery`
* `beast mastery pve`
* `beast mastery pvp`
* `beast mastery raid`
* `boost`
* `boost beast mastery pve`
* `boost beast mastery pvp`
* `boost beast mastery raid`
* `boost marksmanship pve`
* `boost marksmanship pvp`
* `boost marksmanship raid`
* `boost survival pve`
* `boost survival pvp`
* `boost survival raid`
* `buff`
* `buff beast mastery pve`
* `buff beast mastery pvp`
* `buff beast mastery raid`
* `buff marksmanship pve`
* `buff marksmanship pvp`
* `buff marksmanship raid`
* `buff survival pve`
* `buff survival pvp`
* `buff survival raid`
* `cc`
* `cc beast mastery pve`
* `cc beast mastery pvp`
* `cc beast mastery raid`
* `cc marksmanship pve`
* `cc marksmanship pvp`
* `cc marksmanship raid`
* `cc survival pve`
* `cc survival pvp`
* `cc survival raid`
* `marksmanship`
* `marksmanship pve`
* `marksmanship pvp`
* `marksmanship raid`
* `pet`
* `pull`
* `sting`
* `sting beast mastery pve`
* `sting beast mastery pvp`
* `sting beast mastery raid`
* `sting marksmanship pve`
* `sting marksmanship pvp`
* `sting marksmanship raid`
* `sting scorpid`
* `sting serpent`
* `sting survival pve`
* `sting survival pvp`
* `sting survival raid`
* `sting viper`
* `survival`
* `survival pve`
* `survival pvp`
* `survival raid`

### mage (63 registrations; 63 unique)

* `aoe`
* `aoe arcane pve`
* `aoe arcane pvp`
* `aoe arcane raid`
* `aoe fire pve`
* `aoe fire pvp`
* `aoe fire raid`
* `aoe frost pve`
* `aoe frost pvp`
* `aoe frost raid`
* `arcane`
* `arcane pve`
* `arcane pvp`
* `arcane raid`
* `boost`
* `boost arcane pve`
* `boost arcane pvp`
* `boost arcane raid`
* `boost fire pve`
* `boost fire pvp`
* `boost fire raid`
* `boost frost pve`
* `boost frost pvp`
* `boost frost raid`
* `buff`
* `buff arcane pve`
* `buff arcane pvp`
* `buff arcane raid`
* `buff fire pve`
* `buff fire pvp`
* `buff fire raid`
* `buff frost pve`
* `buff frost pvp`
* `buff frost raid`
* `cc`
* `cc arcane pve`
* `cc arcane pvp`
* `cc arcane raid`
* `cc fire pve`
* `cc fire pvp`
* `cc fire raid`
* `cc frost pve`
* `cc frost pvp`
* `cc frost raid`
* `cure`
* `cure arcane pve`
* `cure arcane pvp`
* `cure arcane raid`
* `cure fire pve`
* `cure fire pvp`
* `cure fire raid`
* `cure frost pve`
* `cure frost pvp`
* `cure frost raid`
* `fire`
* `fire pve`
* `fire pvp`
* `fire raid`
* `frost`
* `frost pve`
* `frost pvp`
* `frost raid`
* `pull`

### paladin (104 registrations; 103 unique)

* `aoe`
* `aoe holy pve`
* `aoe holy pvp`
* `aoe holy raid`
* `aoe protection pve`
* `aoe protection pvp`
* `aoe protection raid`
* `aoe retribution pve`
* `aoe retribution pvp`
* `aoe retribution raid`
* `aura`
* `aura concentration`
* `aura crusader`
* `aura devotion`
* `aura fire`
* `aura frost`
* `aura holy pve`
* `aura holy pvp`
* `aura holy raid`
* `aura protection pve`
* `aura protection pvp`
* `aura protection raid`
* `aura retribution`
* `aura retribution pve`
* `aura retribution pvp`
* `aura retribution raid`
* `aura sanctity`
* `aura shadow`
* `blessing`
* `blessing holy pve`
* `blessing holy pvp`
* `blessing holy raid`
* `blessing kings`
* `blessing light`
* `blessing might`
* `blessing protection pve`
* `blessing protection pvp`
* `blessing protection raid`
* `blessing retribution pve`
* `blessing retribution pvp`
* `blessing retribution raid`
* `blessing salvation`
* `blessing sanctuary`
* `blessing wisdom`
* `boost`
* `boost holy pve`
* `boost holy pvp`
* `boost holy raid`
* `boost protection pve`
* `boost protection pvp`
* `boost protection raid`
* `boost retribution pve`
* `boost retribution pvp`
* `boost retribution raid`
* `buff`
* `buff holy pve`
* `buff holy pvp`
* `buff holy raid`
* `buff protection pve`
* `buff protection pvp`
* `buff protection raid`
* `buff retribution pve`
* `buff retribution pvp`
* `buff retribution raid`
* `cc`
* `cc holy pve`
* `cc holy pvp`
* `cc holy raid`
* `cc protection pve`
* `cc protection pvp`
* `cc protection raid`
* `cc retribution pve`
* `cc retribution pvp`
* `cc retribution raid`
* `cure`
* `cure holy pve`
* `cure holy pvp`
* `cure holy raid`
* `cure protection pve`
* `cure protection pvp`
* `cure protection raid`
* `cure retribution pve`
* `cure retribution pvp`
* `cure retribution raid`
* `heal`
* `holy`
* `holy pve`
* `holy pvp`
* `holy raid`
* `offheal`
* `offheal pve`
* `offheal pvp`
* `offheal raid`
* `protection`
* `protection pve`
* `protection pvp`
* `protection raid`
* `pull`
* `retribution`
* `retribution pve`
* `retribution pvp`
* `retribution raid`
* `tank`

### priest (73 registrations; 73 unique)

* `aoe`
* `aoe discipline pve`
* `aoe discipline pvp`
* `aoe discipline raid`
* `aoe holy pve`
* `aoe holy pvp`
* `aoe holy raid`
* `aoe shadow pve`
* `aoe shadow pvp`
* `aoe shadow raid`
* `boost`
* `boost discipline pve`
* `boost discipline pvp`
* `boost discipline raid`
* `boost holy pve`
* `boost holy pvp`
* `boost holy raid`
* `boost shadow pve`
* `boost shadow pvp`
* `boost shadow raid`
* `buff`
* `buff discipline pve`
* `buff discipline pvp`
* `buff discipline raid`
* `buff holy pve`
* `buff holy pvp`
* `buff holy raid`
* `buff shadow pve`
* `buff shadow pvp`
* `buff shadow raid`
* `cc`
* `cc discipline pve`
* `cc discipline pvp`
* `cc discipline raid`
* `cc holy pve`
* `cc holy pvp`
* `cc holy raid`
* `cc shadow pve`
* `cc shadow pvp`
* `cc shadow raid`
* `cure`
* `cure discipline pve`
* `cure discipline pvp`
* `cure discipline raid`
* `cure holy pve`
* `cure holy pvp`
* `cure holy raid`
* `cure shadow pve`
* `cure shadow pvp`
* `cure shadow raid`
* `discipline`
* `discipline pve`
* `discipline pvp`
* `discipline raid`
* `dps`
* `heal`
* `holy`
* `holy pve`
* `holy pvp`
* `holy raid`
* `offdps`
* `offdps pve`
* `offdps pvp`
* `offdps raid`
* `offheal`
* `offheal pve`
* `offheal pvp`
* `offheal raid`
* `pull`
* `shadow`
* `shadow pve`
* `shadow pvp`
* `shadow raid`

### rogue (87 registrations; 86 unique)

* `aoe`
* `aoe assassination pve`
* `aoe assassination pvp`
* `aoe assassination raid`
* `aoe combat pve`
* `aoe combat pvp`
* `aoe combat raid`
* `aoe subtlety pve`
* `aoe subtlety pvp`
* `aoe subtlety raid`
* `assassination`
* `assassination pve`
* `assassination pvp`
* `assassination raid`
* `boost`
* `boost assassination pve`
* `boost assassination pvp`
* `boost assassination raid`
* `boost combat pve`
* `boost combat pvp`
* `boost combat raid`
* `boost subtlety pve`
* `boost subtlety pvp`
* `boost subtlety raid`
* `buff`
* `buff assassination pve`
* `buff assassination pvp`
* `buff assassination raid`
* `buff combat pve`
* `buff combat pvp`
* `buff combat raid`
* `buff subtlety pve`
* `buff subtlety pvp`
* `buff subtlety raid`
* `cc`
* `cc assassination pve`
* `cc assassination pvp`
* `cc assassination raid`
* `cc combat pve`
* `cc combat pvp`
* `cc combat raid`
* `cc subtlety pve`
* `cc subtlety pvp`
* `cc subtlety raid`
* `combat`
* `combat pve`
* `combat pvp`
* `combat raid`
* `poison main anesthetic`
* `poison main crippling`
* `poison main deadly`
* `poison main instant`
* `poison main mind`
* `poison main wound`
* `poison off anesthetic`
* `poison off crippling`
* `poison off deadly`
* `poison off instant`
* `poison off mind`
* `poison off wound`
* `poisons`
* `poisons assassination pve`
* `poisons assassination pvp`
* `poisons assassination raid`
* `poisons combat pve`
* `poisons combat pvp`
* `poisons combat raid`
* `poisons subtlety pve`
* `poisons subtlety pvp`
* `poisons subtlety raid`
* `pull`
* `stealth`
* `stealth assassination pve`
* `stealth assassination pvp`
* `stealth assassination raid`
* `stealth combat pve`
* `stealth combat pvp`
* `stealth combat raid`
* `stealth subtlety pve`
* `stealth subtlety pvp`
* `stealth subtlety raid`
* `stealthed`
* `subtlety`
* `subtlety pve`
* `subtlety pvp`
* `subtlety raid`

### shaman (116 registrations; 104 unique)

* `aoe`
* `aoe elemental pve`
* `aoe elemental pvp`
* `aoe elemental raid`
* `aoe enhancement pve`
* `aoe enhancement pvp`
* `aoe enhancement raid`
* `aoe restoration pve`
* `aoe restoration pvp`
* `aoe restoration raid`
* `boost`
* `boost elemental pve`
* `boost elemental pvp`
* `boost elemental raid`
* `boost enhancement pve`
* `boost enhancement pvp`
* `boost enhancement raid`
* `boost restoration pve`
* `boost restoration pvp`
* `boost restoration raid`
* `buff`
* `buff elemental pve`
* `buff elemental pvp`
* `buff elemental raid`
* `buff enhancement pve`
* `buff enhancement pvp`
* `buff enhancement raid`
* `buff restoration pve`
* `buff restoration pvp`
* `buff restoration raid`
* `cc`
* `cc elemental pve`
* `cc elemental pvp`
* `cc elemental raid`
* `cc enhancement pve`
* `cc enhancement pvp`
* `cc enhancement raid`
* `cc restoration pve`
* `cc restoration pvp`
* `cc restoration raid`
* `cure`
* `cure elemental pve`
* `cure elemental pvp`
* `cure elemental raid`
* `cure enhancement pve`
* `cure enhancement pvp`
* `cure enhancement raid`
* `cure restoration pve`
* `cure restoration pvp`
* `cure restoration raid`
* `elemental`
* `elemental pve`
* `elemental pvp`
* `elemental raid`
* `enhancement`
* `enhancement pve`
* `enhancement pvp`
* `enhancement raid`
* `heal`
* `offheal`
* `offheal pve`
* `offheal pvp`
* `offheal raid`
* `pull`
* `restoration`
* `restoration pve`
* `restoration pvp`
* `restoration raid`
* `totem air grace`
* `totem air grounding`
* `totem air resistance`
* `totem air tranquil`
* `totem air windfury`
* `totem air windwall`
* `totem air wrath`
* `totem earth earthbind`
* `totem earth stoneclaw`
* `totem earth stoneskin`
* `totem earth strength`
* `totem earth tremor`
* `totem fire flametongue`
* `totem fire magma`
* `totem fire nova`
* `totem fire resistance`
* `totem fire searing`
* `totem fire wrath`
* `totem water cleansing`
* `totem water healing`
* `totem water mana`
* `totem water poison`
* `totem water resistance`
* `totembar ancestors`
* `totembar elements`
* `totembar spirits`
* `totems`
* `totems elemental pve`
* `totems elemental pvp`
* `totems elemental raid`
* `totems enhancement pve`
* `totems enhancement pvp`
* `totems enhancement raid`
* `totems restoration pve`
* `totems restoration pvp`
* `totems restoration raid`

### warlock (85 registrations; 85 unique)

* `affliction`
* `affliction pve`
* `affliction pvp`
* `affliction raid`
* `aoe`
* `aoe affliction pve`
* `aoe affliction pvp`
* `aoe affliction raid`
* `aoe demonology pve`
* `aoe demonology pvp`
* `aoe demonology raid`
* `aoe destruction pve`
* `aoe destruction pvp`
* `aoe destruction raid`
* `boost`
* `boost affliction pve`
* `boost affliction pvp`
* `boost affliction raid`
* `boost demonology pve`
* `boost demonology pvp`
* `boost demonology raid`
* `boost destruction pve`
* `boost destruction pvp`
* `boost destruction raid`
* `buff`
* `buff affliction pve`
* `buff affliction pvp`
* `buff affliction raid`
* `buff demonology pve`
* `buff demonology pvp`
* `buff demonology raid`
* `buff destruction pve`
* `buff destruction pvp`
* `buff destruction raid`
* `cc`
* `cc affliction pve`
* `cc affliction pvp`
* `cc affliction raid`
* `cc demonology pve`
* `cc demonology pvp`
* `cc demonology raid`
* `cc destruction pve`
* `cc destruction pvp`
* `cc destruction raid`
* `curse`
* `curse affliction pve`
* `curse affliction pvp`
* `curse affliction raid`
* `curse agony`
* `curse demonology pve`
* `curse demonology pvp`
* `curse demonology raid`
* `curse destruction pve`
* `curse destruction pvp`
* `curse destruction raid`
* `curse doom`
* `curse elements`
* `curse recklessness`
* `curse shadow`
* `curse tongues`
* `curse weakness`
* `demonology`
* `demonology pve`
* `demonology pvp`
* `demonology raid`
* `destruction`
* `destruction pve`
* `destruction pvp`
* `destruction raid`
* `pet`
* `pet affliction pve`
* `pet affliction pvp`
* `pet affliction raid`
* `pet demonology pve`
* `pet demonology pvp`
* `pet demonology raid`
* `pet destruction pve`
* `pet destruction pvp`
* `pet destruction raid`
* `pet felguard`
* `pet felhunter`
* `pet imp`
* `pet succubus`
* `pet voidwalker`
* `pull`

### warrior (54 registrations; 54 unique)

* `aoe`
* `aoe arms pve`
* `aoe arms pvp`
* `aoe arms raid`
* `aoe fury pve`
* `aoe fury pvp`
* `aoe fury raid`
* `aoe protection pve`
* `aoe protection pvp`
* `aoe protection raid`
* `arms`
* `arms pve`
* `arms pvp`
* `arms raid`
* `boost`
* `boost arms pve`
* `boost arms pvp`
* `boost arms raid`
* `boost fury pve`
* `boost fury pvp`
* `boost fury raid`
* `boost protection pve`
* `boost protection pvp`
* `boost protection raid`
* `buff`
* `buff arms pve`
* `buff arms pvp`
* `buff arms raid`
* `buff fury pve`
* `buff fury pvp`
* `buff fury raid`
* `buff protection pve`
* `buff protection pvp`
* `buff protection raid`
* `cc`
* `cc arms pve`
* `cc arms pvp`
* `cc arms raid`
* `cc fury pve`
* `cc fury pvp`
* `cc fury raid`
* `cc protection pve`
* `cc protection pvp`
* `cc protection raid`
* `fury`
* `fury pve`
* `fury pvp`
* `fury raid`
* `protection`
* `protection pve`
* `protection pvp`
* `protection raid`
* `pull`
* `tank`
