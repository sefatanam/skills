---
name: act
description: Run GitHub Actions workflows locally in Docker with nektos/act. Use when the user wants to run, test or debug a workflow or CI job locally, reproduce a CI failure without pushing, or mentions `act`.
metadata:
  author: sefatanam
  version: "1.0.0"
---

# act: run GitHub Actions locally

act reads `.github/workflows/`, builds a fake event, maps each job's `runs-on` to a Docker image (`-P`), and runs the steps in containers. It is an **emulator**: a fast feedback loop that gets close to GitHub but does not match it exactly. A green run in act still needs one real CI run to confirm it.

## Steps

1. **Preflight.** Run `act --version` and `docker info`.
   - act is missing: on macOS install it with `brew install act`. For other systems see https://nektosact.com/installation.
   - Docker is not running: ask the user to start Docker Desktop, then stop here.
   - No `actrc` exists yet (`~/.actrc`, `./.actrc`, or `~/Library/Application Support/act/actrc` on macOS): act would stop to ask which image to use, which hangs a non-interactive shell. Write one before the first run:
     ```
     -P ubuntu-latest=catthehacker/ubuntu:act-latest
     -P ubuntu-24.04=catthehacker/ubuntu:act-24.04
     -P ubuntu-22.04=catthehacker/ubuntu:act-22.04
     ```
     On Apple Silicon, also add `--container-architecture linux/amd64`.

   Done when `act --version` and `docker info` both succeed and an actrc exists.

2. **Map the target.** Run `act -l <event>` (default event `push`) and pick the exact job and workflow file the user means. Read that workflow and note what it needs from outside:
   - `secrets.*`
   - `vars.*`
   - `inputs.*`
   - `github.event.*` fields
   - artifact upload/download steps
   - `macos-*` or `windows-*` runners (act cannot run these)

   Done when every external input is either matched to a value source or flagged to the user.

3. **Supply inputs.** Use the matching flag for each input from step 2:

   | Input | Flag |
   |---|---|
   | Secrets | `-s KEY` (prompts for the value, which keeps it out of shell history) or `--secret-file .secrets` |
   | `GITHUB_TOKEN` | `-s GITHUB_TOKEN="$(gh auth token)"`. act never provides it. |
   | Variables | `--var KEY=val` or `--var-file` |
   | `workflow_dispatch` inputs | `--input KEY=val` |
   | Event fields | `-e event.json`, a JSON file containing just the fields the workflow reads |
   | Artifacts | `--artifact-server-path <dir>` |

   Make sure any secret file is listed in `.gitignore`. Never write a secret's value into a file the user hasn't asked for.

4. **Dry run.** Run `act <event> -W <file> -j <job> -n`. Fix parse and plan errors here, before any containers start.

5. **Run.**
   - Run `act <event> -W <file> -j <job>`. Always scope it with `-W` and `-j`, because act applies `branches:`/`paths:` filters unreliably.
   - The first run pulls a large image and can take minutes. Run it in the background and tell the user it's downloading the image.
   - On later runs, add `--pull=false` to skip the image pull check.

   Done when the job ends with `Job succeeded` or a failure you have read.

6. **Diagnose a failure.** Decide whether the failure is a real bug or a gap between act and GitHub (see [references/REFERENCE.md](references/REFERENCE.md)). Then:
   - Rerun with `-v` to see image selection, expression values and env.
   - Rerun with `--reuse` and `docker exec -it <container> bash` to inspect the container.

   Report which kind of failure it was, and for an act gap, the workaround. Use `if: ${{ !env.ACT }}` to skip steps that can only run on GitHub (deploys, OIDC).
