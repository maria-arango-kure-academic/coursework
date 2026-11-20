# Run the class deployment yourself

In Windows PowerShell, run:

```powershell
& 'C:\Users\maria\Desktop\Academic\Tools & dev\vfi-simulation\deployment\Deploy.ps1'
```

This command packages local source, uploads it over your existing keeper SSH connection, and runs the uploaded deployment script on Keeper. The agent must not execute it. The script builds an isolated Docker Compose project, stores class data outside release folders, configures HTTPS at vfi.coursework.live and no-cache responses, and prints your private teacher link. Certbot may prompt for certificate terms or email settings. Keep the teacher link private.

Initial publication does not require GitHub. A dedicated one-minute updater is installed for maria-arango-kure-academic/vfi-simulation, main. It waits for /root/.ssh/vfi_simulation_deploy and an accessible private repository. Maria creates the repository, adds its read-only deploy key and pushes commits. An unavailable repository does not stop the deployed class app. Releases have separate image tags; a failed health check restores the previous application image. Session data stays in /srv/keeper/services/vfi-simulation/data.

Updater log: /var/log/vfi-simulation-update.log. To pause automatic updates, rename /etc/cron.d/vfi-simulation-update to /srv/keeper/services/vfi-simulation/update.cron.paused. To resume, move that file back. These are commands for Maria to run; home-lab access still requires three explicit approvals.

Checks performed locally: PowerShell and Bash syntax, embedded Python, archive contents, and existing application tests. No remote build, certificate issuance, deployment or live verification was performed by the agent.
