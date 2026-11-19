# act reference: gaps between act and GitHub

Run `act --help` for the full flag list. This file covers what the help output doesn't.

## How act differs from GitHub

| Area | GitHub | act |
|---|---|---|
| Runner | Full VM, `runner` user | Docker container, root user |
| macOS / Windows runners | Yes | No. Either skip them, or use `-P macos-latest=-self-hosted` to run directly on the host machine (this is not sandboxed). |
| `GITHUB_TOKEN` | Provided automatically | You must pass it with `-s` |
| Preinstalled tools | Many | Only what the image has. The medium `act-*` image has far fewer. |
| `branches:` / `paths:` filters | Exact | Unreliable, so scope runs with `-W` / `-j` |
| `actions/checkout` | Clones from GitHub | Uses the local working copy, including uncommitted changes |
| Artifacts | Built in | Needs `--artifact-server-path` |
| `actions/cache` | Built in | Built-in cache server, usually works |
| `concurrency`, environment protection rules | Enforced | Ignored |
| OIDC (`id-token: write`) | Yes | No |
| Event payload | Full | Nearly empty unless you pass `-e event.json` |
| `ACT` env var | Not set | `ACT=true` |

## Failures and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker is not running | Start Docker Desktop |
| `command not found` (`gh`, `aws`, ...) | The medium image lacks the tool | Install the tool in a step, or map the runner to `catthehacker/ubuntu:full-latest` (about 20GB) |
| The run hangs at start | No actrc, so act is waiting at the image-size prompt | Write an actrc (SKILL.md step 1) |
| Slow on Apple Silicon | amd64 emulation | Remove `--container-architecture linux/amd64` if nothing needs x86 |
| `Bad credentials`, 401 | No token | `-s GITHUB_TOKEN="$(gh auth token)"` |
| `upload-artifact` fails | No artifact server | `--artifact-server-path /tmp/act-artifacts` |
| No jobs run | The event doesn't match | Run `act -l <event>` and pass the right event name |
| `github.event.X` is empty | Default payload | `-e event.json` |
| Fails offline | act re-fetches actions and images | `--action-offline-mode --pull=false` |
| Matrix runs too many combinations | Every combination runs | `--matrix key:val` to pick one |

## Image sizes (`-P`)

| Size | Image | Approx. size |
|---|---|---|
| Micro | `node:16-buster-slim` | 200MB |
| Medium | `catthehacker/ubuntu:act-<ver>` | 0.5–1GB |
| Large | `catthehacker/ubuntu:full-<ver>` | 20GB+ |
