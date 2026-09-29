---
name: remote-power-on
description: Wake the home desktop via Wake-on-LAN through the NAS public SSH endpoint 103.73.67.112:6702. Use when the user asks to remotely power on, WOL, 远程开机, or wake this PC. Not for NAS/VPS admin, smart-plug power cycling, or shutdown.
---

# Remote Power On

Send one WOL magic packet from the NAS. Use the public SSH endpoint only.

```powershell
ssh -o BatchMode=yes -o ConnectTimeout=10 -p 6702 root@103.73.67.112 "etherwake -i br-lan -b 2C:F0:5D:25:24:5D"
```

- Target: MSI B450M MORTAR MAX desktop, MAC `2C:F0:5D:25:24:5D` (`192.168.31.205`). Do not wake any other host.
- Public endpoint is key-based (`103.73.67.112:6702`). Password login is disabled. Never put a password in a command, log, or response. Keep host-key checking on; stop if the saved host key changes.
- Success is usually empty stdout. The packet does not wait for Windows; boot may take tens of seconds. Do not retry in a loop. One extra send is enough if the first SSH call succeeded but the PC did not appear.
- Do not install packages, open extra ports, use the LAN SSH endpoint, or cut power with a smart plug. If `etherwake` is missing or SSH fails, report that and stop.
- Sending this packet is the intended action when the skill is invoked; no extra confirmation.
