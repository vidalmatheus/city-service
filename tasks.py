import inspect
from functools import wraps

from invoke import task


def projtask(func):
    """
    Task to be executed at the project's root.
    """

    @wraps(func)
    def wrapper(c, *args, **kwargs):
        with c.cd(c.config._project_prefix):
            return func(c, *args, **kwargs)

    wrapper.__signature__ = inspect.signature(func)
    return task(wrapper)


def _pipcompile(c, *, upgrade=None):
    upgrades = ""
    if upgrade:
        if upgrade == "ALL":
            upgrades = " --upgrade"
        else:
            for package in upgrade.split():
                upgrades += f' --upgrade-package "{package}"'

    output_file = "requirements.txt"
    input_files = "requirements.in"
    cmd = f"pip-compile --generate-hashes --allow-unsafe {upgrades} -o {output_file} {input_files}"
    print(cmd)
    c.run(cmd)


@projtask
def requirements(c, upgrade=None):
    _pipcompile(c, upgrade=upgrade)


@projtask
def lint(c):
    c.run("isort --profile black --line-length 120 --check .")
    c.run("black --line-length 120 --check .")


@projtask
def format(c):
    c.run("autoflake --remove-all-unused-imports --in-place -r .")
    c.run("isort --profile black --line-length 120 .")
    c.run("black --line-length 120 .")


@projtask
def dkbuild(c):
    c.run("docker build -t city-service .")


@projtask
def dkrun(c):
    c.run("docker rm city-service")
    c.run("docker run -p 8000:8000 --name city-service city-service")
