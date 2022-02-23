# Zulu-Alpha Site

Repo for the Zulu-Alpha site

## Environmental configuration

In development, environmental variables are read from the `.env` and `.secrets.env`, with the latter's variables taking precedence.
The `.env` file is considered safe and in version control, however `.secrets.env` is not, and requires the following variables:

### Discord

- **DISCORD_OAUTH_CLIENT_ID**: The Discord OAuth client ID.
- **DISCORD_OAUTH_CLIENT_SECRET**: The discord OAuth client secret
- **DISCORD_BOOTSTRAP_ADMIN_UID**: The discord UID of the user who should automatically be made an admin on first login. Note that you can leave this blank to disable bootstrapping (useful after doing it the first time).

## Contributing

### Pre-commit

Code quality is checked on the pipeline and locally with pre-commit.
Pre-commit is configured to run with the standard method of using remote repos for each tool that install in their own virtual environment.

1. Before committing, make sure that you have [pre-commit](https://pre-commit.com/) installed.
2. Go into the root directory and run `pre-commit install`.
   1. (Optional) To test that the git pre-commit hooks work and to pull the relevant images, run `pre-commit run --all-files`
   2. (Optional) It's useful to occasionally update all hooks. This can be done with `pre-commit autoupdate`

### Django-extensions

[django-extensions](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html) is installed in the dev environment, and it's options can be accessed with the Makefile commands:

- **make shell**: IPython django shell

## Authors

- [@adampiskorski](https://github.com/adampiskorski)

## Badges

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

## Local dev

Install packages using [poetry](https://python-poetry.org/) with `poetry install`

## Test

Just run pytest
