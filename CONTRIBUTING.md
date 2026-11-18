# Contributing to Verity

Everyone works in their **own fork** and sends changes to the shared **upstream** repository through pull requests. Nobody pushes directly to upstream `main`.

Throughout this guide:

- **upstream** = the shared team repository: `https://github.com/<org-or-owner>/verity`
- **origin** = your personal fork: `https://github.com/<your-username>/verity`

## 1. One-time setup

1. Fork the upstream repository on GitHub (the **Fork** button).
2. Clone **your fork**:

```bash
git clone https://github.com/<your-username>/verity.git
```

3. Move into the folder and add the upstream repository as a second remote:

```bash
cd verity
```

```bash
git remote add upstream https://github.com/<org-or-owner>/verity.git
```

4. Check that both remotes are there (`origin` = your fork, `upstream` = the team repo):

```bash
git remote -v
```

5. Set up the service you will work on (ingestion shown here; see its README for details):

```bash
cd ingestion && uv sync && cp .env.example .env && docker compose up -d
```

## 2. Start every piece of work from a fresh `main`

Always sync with upstream before you begin, so your branch starts from the latest code.

```bash
git checkout main
```

```bash
git fetch upstream
```

```bash
git merge --ff-only upstream/main
```

```bash
git push origin main
```

`--ff-only` keeps your `main` identical to upstream. If it refuses, your `main` has stray commits: never commit on `main`, only on branches.

## 3. Create a branch

One branch per task. Name it `<type>/<short-description>`:

```bash
git checkout -b feat/markdown-parser
```

| Type | Use for | Example |
| --- | --- | --- |
| `feat/` | new functionality | `feat/pdf-page-ocr-fallback` |
| `fix/` | bug fix | `fix/duplicate-chunks-on-retry` |
| `test/` | tests only | `test/corrupt-pdf-fixtures` |
| `refactor/` | no behaviour change | `refactor/job-claim-query` |
| `chore/` | tooling, config, dependencies | `chore/add-openpyxl` |

Keep a branch small and focused: one task, reviewable in about 30 minutes. Large changes go in several PRs.

## 4. Make your changes

- Read the service's `CLAUDE.md` first. Its **rules that must not be broken** (idempotency, atomic activation, never deleting versions, ACLs from the source system, and so on) apply to every change.
- Add or update tests with the code. A parser comes with a test using a small sample file; a bug fix comes with a test that fails without the fix.
- Add dependencies with `uv add <package>` (or `uv add --dev <package>`), and commit both `pyproject.toml` and `uv.lock`.
- Never commit secrets, `.env` files, large data files, or your personal notes. `notes/`, `docs/` and `.env` are already gitignored.

Before every push, from the service folder (`ingestion/`):

```bash
uv run ruff check . && uv run ruff format --check . && uv run pytest
```

All three must pass.

## 5. Commit

Make small commits with clear messages: a short summary in the imperative, a blank line, and a longer explanation if the *why* is not obvious.

```bash
git add <files>
```

```bash
git commit -m "Add Markdown parser with front matter metadata"
```

Prefer adding specific files over `git add .`, so nothing unintended is included.

## 6. Keep your branch up to date

If upstream `main` moved while you were working, bring your branch up to date **before** opening or while updating a PR:

```bash
git fetch upstream
```

```bash
git rebase upstream/main
```

Resolve any conflicts, run the checks again, then update your fork. After a rebase the history changed, so use the safe force option on **your own branch only**:

```bash
git push --force-with-lease origin feat/markdown-parser
```

Never force-push `main`.

## 7. Push and open the pull request

First push of a new branch:

```bash
git push -u origin feat/markdown-parser
```

Then on GitHub, open a pull request:

- **base repository:** the upstream repo, **base branch:** `main`
- **head repository:** your fork, **compare branch:** your branch

Or with the GitHub CLI:

```bash
gh pr create --repo <org-or-owner>/verity --base main --title "Add Markdown parser" --body "What and why"
```

A good PR description answers:

1. **What** changed, in a few lines.
2. **Why** (the problem or milestone it belongs to).
3. **How to test** it (commands, or the sample file to use).
4. **Anything risky** or deliberately left out.

Checklist before you click **Create**:

- [ ] Branch is up to date with `upstream/main`
- [ ] `ruff check`, `ruff format --check` and `pytest` pass
- [ ] New behaviour has tests
- [ ] No secrets, `.env`, `notes/`, `docs/` or large data files in the diff
- [ ] The PR does one thing

## 8. Review

- At least **one teammate** reviews and approves before a PR is merged.
- Reply to every comment: make the change, or explain why not. Push fixes to the same branch and the PR updates itself.
- Reviewers: check the project rules in `CLAUDE.md`, correctness on failure paths (retries, partial failures), and that tests would catch a regression. Be specific and kind.
- Do not merge your own PR without a review, unless the team agreed otherwise for a trivial change.

## 9. After your PR is merged

Sync your fork and clean up:

```bash
git checkout main
```

```bash
git fetch upstream
```

```bash
git merge --ff-only upstream/main
```

```bash
git push origin main
```

```bash
git branch -d feat/markdown-parser
```

```bash
git push origin --delete feat/markdown-parser
```

Then start the next task from section 2.

## Working together

- **Claim work before starting**: say in the team chat or on the issue which task or milestone you are taking, so two people do not build the same thing.
- **Avoid editing the same files** at the same time. Shared files (`models.py`, `pyproject.toml`, migrations) cause most conflicts: merge small changes to them quickly.
- **Migrations**: only one pending migration per person at a time. If two migrations collide, the later PR rebases and renumbers.
- **Stuck for more than an hour?** Ask. A quick question beats a long detour.
