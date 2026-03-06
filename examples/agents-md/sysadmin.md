# AGENTS.md — System Administration

## Environment
- Ubuntu 22.04 / Debian 12
- Systemd services
- UFW firewall
- Nginx web server

## Rules
- NEVER run commands that could cause downtime without asking first
- Always check service status before restarting
- Take backups before modifying config files
- Show `diff` before applying config changes
- Use `sudo` only when necessary, explain why root is needed

## Safety
- Destructive commands require confirmation: rm, mkfs, dd, iptables -F
- Always use `--dry-run` or `--check` when available
- Test config before reload: `nginx -t`, `sshd -t`, `named-checkconf`
- Check disk space before large operations: `df -h`

## Logging
- System logs: `journalctl -u <service>`
- Nginx: `/var/log/nginx/`
- Auth: `/var/log/auth.log`
- Always check logs after making changes

## Common Tasks
- Service management: `systemctl start|stop|restart|status <service>`
- Firewall: `ufw status`, `ufw allow <port>`
- Disk: `df -h`, `du -sh *`, `ncdu`
- Network: `ss -tlnp`, `curl -I`, `dig`
- Process: `htop`, `ps aux`, `kill -15` (never -9 first)
