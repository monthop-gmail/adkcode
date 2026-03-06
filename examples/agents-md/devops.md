# AGENTS.md — DevOps / Infrastructure

## Stack
- Docker + Docker Compose
- Kubernetes (kubectl, helm)
- Terraform
- GitHub Actions CI/CD
- Nginx / Traefik reverse proxy

## Rules
- Always explain what a command does before running it
- Never run destructive commands without asking first (rm -rf, kubectl delete, terraform destroy)
- Check current state before making changes (docker ps, kubectl get, terraform plan)
- Use `--dry-run` flags when available

## Conventions
- Use multi-stage Docker builds
- Tag images with git commit hash, not just "latest"
- Secrets go in environment variables or secret managers, never in files
- All infra changes must be in code (IaC), no manual changes

## Common Tasks
- Deploy: `kubectl apply -f k8s/`
- Rollback: `kubectl rollout undo deployment/<name>`
- Logs: `kubectl logs -f deployment/<name>`
- SSL certs: managed by cert-manager
