# Backend

`AGENTS.md` in the checkout names the types to use. If `local-backend.md` exists beside this file, read it too.

- **[project]** Follow the solution's dependency direction and its service registration paths.
- **[project]** Entities do not cross the API boundary. Map them to DTOs.
- **[project]** Use the repository's response envelope, error handling, authorization and data access layer.
- **[observed]** Follow the neighbouring code's error contract. Log with the method name and id.
- **[observed]** Seed changes are idempotent and cover every supported database. Ask before adding SQL to a bug fix.
- **[project]** Format only touched files, then run the build and test commands from `AGENTS.md`.
