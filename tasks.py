from invoke import task

packages = ['fling-core', 'fling-client', 'fling-cli', 'fling-web', 'fling-api']

@task
def clean(c, docs=False, bytecode=False, extra=''):
    print("Cleaning build artifacts...")
    patterns = ['dist']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))


@task(pre=[clean])
def build(c, docs=False):
    c.run("mkdir -p dist")
    for package in packages:
        with c.cd(package):
            c.run("poetry build")
            c.run("mv dist/* ../dist/")


@task
def install(c):
    for package in packages:
        with c.cd(package):
            c.run("pip install -r requirements.txt")
