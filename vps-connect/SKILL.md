---
name: vps-connect
description: Connect to and inspect the configured HK VPS (v58, frps server) over SSH at hknew.khanwebhost.com:6721 as root. Use when the user asks to connect to the VPS, inspect frps logs or services, or operate this specific host; not for the NAS.
---

# VPS Connect

Connect with the system OpenSSH client:

```powershell
ssh -i ~/.ssh/id_ed25519_vps_hknew -o IdentitiesOnly=yes -p 6721 root@hknew.khanwebhost.com
```

For one read-only command:

```powershell
ssh -i ~/.ssh/id_ed25519_vps_hknew -o IdentitiesOnly=yes -p 6721 root@hknew.khanwebhost.com "<remote-command>"
```

- The host's ED25519 fingerprint was verified from its console: `SHA256:v1Vsdgdl4lQQI4J7+vuj8IdriBNvFN6HoDF23+EKnH0`. Keep SSH host-key checking enabled; stop on a changed key. For a new client, verify the fingerprint independently before trusting it.
- Use the dedicated local key above after its public half has been added to `/root/.ssh/authorized_keys` on the VPS. Keep the private half in the local SSH directory, never copy it to the VPS or a synced config repository. If key authentication is unavailable, use a secure interactive terminal; never put a password in commands, tool arguments, files, logs, or responses. Never reuse NAS credentials or keys for VPS access.
- The VPS uses UTC; correlate frps journal entries with NAS timestamps by converting the timezone. Check whether frps runs under systemd before using `journalctl -u frps`; do not assume every service uses the same manager.
- Confirm target and impact before destructive or service-disrupting operations. Do not restart frps, modify its configuration, deploy, or alter firewall rules without explicit user authorization. Report command results and distinguish SSH/authentication failures from remote command failures.
