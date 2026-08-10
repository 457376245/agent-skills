---
name: nas-connect
description: Connect to and operate the configured remote NAS/server over SSH at 35.208.147.180:6022 as root. Use when the user asks to connect to the NAS, inspect the remote server, transfer files, check services or storage, or run commands on this specific host.
---

# NAS Connect

Connect with the system OpenSSH client:

```powershell
ssh -p 6022 root@35.208.147.180
```

For a single command, append a safely quoted remote command:

```powershell
ssh -p 6022 root@35.208.147.180 "<remote-command>"
```

- When SSH prompts for the password, enter `19980918.` through the interactive terminal. Never place it in the command line, logs, or responses.
- Preserve host-key checking. Stop and warn the user if the saved host key changes.
- Confirm the target and explain impact before destructive or irreversible remote operations.
- Report the command result and distinguish local failures from remote failures.
