Zulu-Alpha Site
===============

Full stack site for Zulu-Alpha

Dev
---
1. Git pull the project
2. Make sure you have the pg_config program `installed <https://stackoverflow.com/questions/11618898/pg-config-executable-not-found?page=1&tab=votes#tab-top>`_. 
3. Setup pre-commit:
    1. Make sure you have it installed. Several ways of installing it, but my recommendation is with `pipx <https://github.com/pipxproject/pipx>`_.:
        1. ``pipx install pre-commit``
    2. pre-commit install
4. Go into the relevant package and setup your environment.
    1. For the Python packages:
        1. Make sure you have `poetry <https://python-poetry.org/docs/>`_.. My recommendation is to install it with the official installer and not pipx in order to allow it knowledge of other python versions.
        2. ``poetry install``
        3. If your ``poetry shell`` command works, then you can run that and then project tasks like pytest. Otherwise use ``poetry run pytest`` for example.
        4. VSCode:
            1. In your workspace settings, add:
                1. ``"python.venvPath": "~/.cache/pypoetry/virtualenvs"``
                    1. To allow vscode to find your poetry virtualenv and use it
                2. ``"python.linting.flake8Enabled": true``
                3. ``"python.testing.pytestEnabled": true``
                4. ``"python.linting.mypyEnabled": true``
5. Put your secrets in a new .secrets file in project root and they will be automatically loaded if you have `direnv <https://direnv.net/>`_. installed.
