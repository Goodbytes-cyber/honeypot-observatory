# GoodBytes honeypot observatory

Aggregated data from an SSH and Telnet decoy (Cowrie honeypot) run by [GoodBytes](https://goodbytes.fr), updated every week, plus the Wazuh rules we use to turn Cowrie's log into alerts.

Live page: [goodbytes.fr/honeypot-attack-observatory/](https://goodbytes.fr/honeypot-attack-observatory/) · en français : [goodbytes.fr/fr/observatoire-attaques-honeypot/](https://goodbytes.fr/fr/observatoire-attaques-honeypot/)

## Contents

| Path | What | Licence |
|---|---|---|
| `data/observatoire.json` | Weekly aggregates (sessions, distinct IPs, countries, networks, credentials, commands, malware families) | CC BY 4.0 |
| `data/observatoire.csv` | Same figures, one value per row: `section, rank, label, value` | CC BY 4.0 |
| `wazuh/cowrie_rules.xml` | Wazuh rules for Cowrie's JSON log (connection, failed login, login accepted by the decoy, command) | MIT |
| `wazuh/ossec-localfile.xml` | Agent block that reads Cowrie's JSON log | MIT |

## How the figures are produced

The decoy is a [Cowrie](https://github.com/cowrie/cowrie) honeypot imitating an SSH and Telnet server. It holds no real data and every connection to it is unsolicited. Only aggregates are published: no IP address, no raw session; non-public addresses are excluded. Credentials and commands are text written by attackers: in the CSV, a cell starting with `=`, `+`, `-` or `@` is prefixed with `'` so that spreadsheets do not run it as a formula.

Limits: a single sensor, so a partial view that does not represent the whole internet. The decoy was open only on Mondays from 19 to 25 October 2026. Since 1 November 2026 its outbound traffic is limited to HTTP and HTTPS, so downloads over tftp or ftp are no longer captured. Data are cut off every Sunday at 23:59:59 UTC; all times are UTC.

The decoy accepts almost any password: a "login accepted by the decoy" is not a real compromise.

Sources: [IP Geolocation by DB-IP](https://db-ip.com) (CC BY 4.0) for countries and networks; [MalwareBazaar](https://bazaar.abuse.ch/) (abuse.ch) for malware families, by hash only. A network or country listed here is where addresses were registered, not who is behind the attacks.

## Citing these data

> GoodBytes, "Honeypot attack observatory", data from 13 September 2026 to the date in `period.end`, goodbytes.fr/honeypot-attack-observatory/, CC BY 4.0 licence.

## Using the Wazuh rules

1. Copy `wazuh/cowrie_rules.xml` to `/var/ossec/etc/rules/` on the manager (or append it to `local_rules.xml`); renumber the IDs if they collide with yours.
2. Add the block of `wazuh/ossec-localfile.xml` to the agent that can read Cowrie's `cowrie.json`, with your path.
3. Restart the manager and the agent, then check with `/var/ossec/bin/wazuh-logtest` on a line of `cowrie.json`.

These rules run in production at GoodBytes with Wazuh 4 and the official `cowrie/cowrie` Docker image.

---

## En français

Données agrégées d'un leurre SSH et Telnet (honeypot Cowrie) exploité par [GoodBytes](https://goodbytes.fr), mises à jour chaque semaine, et règles Wazuh qui transforment le journal de Cowrie en alertes.

- `data/` : agrégats en JSON et CSV, licence CC BY 4.0 (réutilisation libre, en citant GoodBytes). Aucune adresse IP ni session brute.
- `wazuh/` : règles et bloc d'agent, licence MIT.

Méthode, limites et sources : voir la page [Observatoire](https://goodbytes.fr/fr/observatoire-attaques-honeypot/), section « Comment ces chiffres sont produits ». Les pays et réseaux indiquent où les adresses sont enregistrées, pas qui est derrière les attaques.
