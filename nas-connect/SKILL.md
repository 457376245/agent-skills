---
name: nas-connect
description: Connect to and operate the configured NAS/server over SSH as root, preferring the LAN endpoint 192.168.31.101:22 and falling back to 103.73.67.112:6702 when the LAN endpoint is unreachable. Use when the user asks to connect to the NAS, inspect the remote server, transfer files, check services or storage, or run commands on this specific host.
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

If the LAN endpoint cannot be reached, retry through the public endpoint:

```powershell
ssh -p 6702 root@103.73.67.112
```

For a single command through the public endpoint:

```powershell
ssh -p 6702 root@103.73.67.112 "<remote-command>"
```

- Public endpoint uses key-based SSH authentication (`103.73.67.112:6702`). Password login is disabled on the public gateway.
- If connecting via LAN endpoint (`192.168.31.101:22`) prompts for password, enter `19980918.` through the interactive terminal. Never place it in the command line, logs, or responses.
- Fall back only for a LAN connection or routing failure. Do not bypass authentication failures or host-key warnings by switching endpoints.
- Preserve host-key checking. Stop and warn the user if the saved host key changes.
- Confirm the target and explain impact before destructive or irreversible remote operations.
- Report the command result and distinguish local failures from remote failures.
