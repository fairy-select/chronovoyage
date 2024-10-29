# How to contribute Chronovoyage

## Reporting issues

Create an issue at GitHub.

https://github.com/fairy-select/chronovoyage/issues

The title should summarize the issue and the description should include the following information:

- Condition and operation ("given" and "when" in test structure)
- Expected behavior ("then" in test structure)
- Actual behavior

## Request source code changes

### Prerequisites

- You have a GitHub account.
- You have forked this repository.
- You have set `user.name` and `user.email` of your git config.
- You have installed Python >= 3.8.
- You have installed Docker.

### Set up your environment (first time only)

Clone your fork.

```shell
git clone https://github.com/{your account}/chronovoyage
cd chronovoyage
```

Setup pre-commit hooks.

```shell
chmod -vR a+x .githooks
git config --local core.hooksPath .githooks
```

We usually develop with [Hatch](https://hatch.pypa.io/1.13/).
Install into your python via pip or something else ([Installation Guide](https://hatch.pypa.io/1.13/install/) here).

```shell
pip install hatch
```

Install OS dependencies required for DB connectors.

- Ubuntu

```shell
sudo apt-get install libmariadb-dev  # for MariaDB
```

Then, enter the environment.
Required pip dependencies will be installed automatically.

```shell
hatch shell
```

The prompt shows the prefix if you are in the environment.

```text
(chronovoyage) you@hostname:~/path/to/chronovoyage$
```

You can leave the environment by typing `exit`.

### Code

Create your branch from `origin/main`.

```shell
git fetch origin
git checkout -b {branch name} origin/main
```

Code and commit.
We use [Conventional Commits](https://www.conventionalcommits.org/).
You should prefix a message with the following:

- `feat:` - when you add any features
- `fix:` - when you fix bugs
- `test:` - when you code only tests
- `refactor:` - when you code without the existing specification in tests.
- `docs:` - when you add/modify docs (not just in documentation but also in code)
- `ci:` - when you add/modify the config of GitHub Actions.
- `build:` - when you add/modify the config of building packages.

Then, push you code.

```shell
git push --set-upstream origin {branch name}
```

### Test your code

Create the testing database via Docker.

```shell
cd tests
docker compose up -d
```

Run tests.
The testing environment will be created automatically.

```shell
hatch test
```

### (Optional) Lint your code manually

Formatting and checking types are executed automatically when you commit.
If you want to lint your code manually, type the following:

- Format

```shell
hatch fmt
```

- Check types

```shell
hatch run types:check
```

### Create a pull request

Create a pull request at GitHub.

https://github.com/fairy-select/chronovoyage/pulls

The title should summarize the request and the description should include the following information:

- Impact on users using Chronovoyage
- Summary of the code changes
- Evidence of tests (such as operation of command, added testcases, behavior of built documentation, and so on)
