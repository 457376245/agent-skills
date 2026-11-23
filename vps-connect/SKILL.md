---
name: vps-connect
description: Connect directly to the Osaka Google Cloud VPS (frps-osaka, 35.217.130.39:22) over SSH as osaka. Use when the user asks to connect to the VPS or inspect its frps, Nginx HTTPS entry, logs, or certificate renewal; use nas-connect for NAS administration.
---

# VPS Connect

Default target: `frps-osaka` in `asia-northeast2-a`, with fixed Standard-tier IPv4 `35.217.130.39`. Connect directly with the system OpenSSH client, without the local proxy:

```powershell
ssh -i ~/.ssh/id_ed25519_vps_osaka -o IdentitiesOnly=yes -o ProxyCommand=none -o StrictHostKeyChecking=yes -p 22 osaka@35.217.130.39
```

For one read-only command:

```powershell
ssh -i ~/.ssh/id_ed25519_vps_osaka -o IdentitiesOnly=yes -o ProxyCommand=none -o StrictHostKeyChecking=yes -p 22 osaka@35.217.130.39 "<remote-command>"
```

- The recorded ED25519 host fingerprint is `SHA256:yVPen5u/byyoj6J70U7pK6vlPewUfeRBGmogOT+huCk`. Keep SSH host-key checking enabled; stop on a changed key. Before trusting this fingerprint on a new client, independently verify it through Google Cloud Console or another trusted management channel; ssh-keyscan alone is not verification.
- Use the dedicated Osaka key above; its public half is configured for `osaka` through per-instance Google Cloud SSH metadata. The login user is not root: use `sudo -n` for privileged inspection. Keep the private half in the local SSH directory, never copy it to the VPS or a synced config repository. If key authentication is unavailable, stop and report it; never put a password in commands, tool arguments, files, logs, or responses. Never reuse NAS SSH keys for Osaka access.
- The VPS uses UTC; correlate journal entries with NAS timestamps by converting the timezone. Known systemd units are `frps`, `nginx`, and `omp-acme-renew.timer`; confirm their state before inspecting logs with commands such as `sudo -n journalctl -u frps -n 100 --no-pager`.
- Public HTTPS is `https://*.blackandw.cloud:6704`; Nginx forwards to local-only `127.0.0.1:6703`, and frps accepts authenticated TLS clients on `7000/TCP`. Configurations are `/etc/nginx/conf.d/omp-frp-https.conf` and `/etc/frp/frps.toml`; certificate renewal uses acme.sh with `dns_ali`. Do not dump authentication tokens, private keys, or `/root/.acme.sh/account.conf`.
- The local `ssh vps` alias also connects directly to Osaka and serves as the `ProxyJump` host for the NAS SSH gateway (`127.0.0.1:6702` on Osaka). Use `nas-connect` for NAS administration.
- Confirm target and impact before destructive or service-disrupting operations. Do not restart or reload frps/Nginx, run certificate renewal, modify configuration or DNS, deploy, or alter firewall rules without explicit user authorization. Report command results and distinguish SSH/authentication failures from remote command failures.
