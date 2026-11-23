---
name: nas-connect
description: Connect to and operate the configured NAS/server over SSH as root, preferring the LAN endpoint 192.168.31.101:22 and falling back to the Osaka VPS ProxyJump gateway (vps -> 127.0.0.1:6702) when the LAN endpoint is unreachable. Use when the user asks to connect to the NAS, inspect the remote server, transfer files, check services or storage, or run commands on this specific host.
---

# NAS Connect

Connect to the LAN endpoint first with the system OpenSSH client:

```powershell
ssh root@192.168.31.101
```

For a single command, append a safely quoted remote command:

```powershell
ssh root@192.168.31.101 "<remote-command>"
```

If the LAN endpoint cannot be reached, retry directly through the Osaka VPS `ProxyJump` gateway (without the local proxy):

```powershell
ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes -o ProxyJump=vps -o HostKeyAlias=nas-osaka-frp -o StrictHostKeyChecking=yes -p 6702 root@127.0.0.1
```

For a single command through the public endpoint:

```powershell
ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes -o ProxyJump=vps -o HostKeyAlias=nas-osaka-frp -o StrictHostKeyChecking=yes -p 6702 root@127.0.0.1 "<remote-command>"
```

- Public endpoint uses key-based SSH authentication via the Osaka VPS `ProxyJump` (`vps` -> `127.0.0.1:6702`, `HostKeyAlias nas-osaka-frp`), connecting directly without a local HTTP proxy. Password login is disabled on the public gateway.
- Prefer key-based SSH authentication. Never store, request, print, or place a password in a command, log, skill, or response. If interactive authentication is required, ask the user to complete it directly in their terminal.
- Fall back only for a LAN connection or routing failure. Do not bypass authentication failures or host-key warnings by switching endpoints.
- Preserve host-key checking. Stop and warn the user if the saved host key changes.
- Remote writes, restarts, deletions, deployments, and other external changes require explicit authorization in the current request.
- Report the command result and distinguish local failures from remote failures.
