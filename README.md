## Contributing

Code quality is checked on the pipeline and locally with pre-commit.
All projects in this mono-repo share the same file (`.pre-commit-config.yaml`) for configuration in the root of this project, but inside of that, when configuration differs, the same tools could have different entries for each project (for example, `mypy (for lib.environment)`).
Pre-commit is configured to run with the standard method of using remote repos for each tool that install in their own virtual environment.

1. Before committing, make sure that you have [pre-commit](https://pre-commit.com/) installed (installing via [pipx](https://pipxproject.github.io/pipx/installation/) is recommended).
2. Go into the root directory and run `pre-commit install`.
   1. (Optional) To test that the git pre-commit hooks work and to pull the relevant images, run `pre-commit run --all-files`
   2. (Optional) It's useful to occasionally update all hooks. This can be done with `pre-commit autoupdate`
