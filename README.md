![GitHub Actions](https://github.com/Jazyki-Mira/langworld_db_pyramid/actions/workflows/pytest.yml/badge.svg)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Jazyki-Mira/langworld_db_pyramid/master.svg)](https://results.pre-commit.ci/latest/github/Jazyki-Mira/langworld_db_pyramid/master)
[![codecov](https://codecov.io/gh/Jazyki-Mira/langworld_db_pyramid/graph/badge.svg?token=WUYWPQ6CJ6)](https://codecov.io/gh/Jazyki-Mira/langworld_db_pyramid)

# Jazyki Mira (Languages of the World) online database

Jazyki Mira (Languages of the World) Database as a [Pyramid](https://trypyramid.com/) web app
with interactive UI components created in [React.js](https://reactjs.org/).

The data is pulled with `git subtree` from a
data repository into [*langworld_db_data*](langworld_db_data). The actual data files are in [*data*](langworld_db_data/data) subdirectory of that package.
See the [Entity Relationship Diagram](langworld_db_pyramid/dbutils/erd.png) of the relational database that was generated from the data for the web app.

The [*langworld_db_pyramid*](langworld_db_pyramid)
package contains the actual Pyramid web app. The tests
for this package are stored in a [separate directory](tests).

## Running locally

### Prerequisites
- Python 3.9
- `pipenv` (see [pipenv docs](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv) for details)

### Clone repository (and `cd` into package directory)

```bash
git clone https://github.com/Jazyki-Mira/langworld_db_pyramid/; cd langworld_db_pyramid
```

### Copy default [PasteDeploy](https://pastedeploy.readthedocs.io/en/latest/index.html) `.ini` files and edit them if necessary

Copy `.ini` files from [`/config/default/`](config/default) to [`/config/`](config). Edit if necessary (e.g. `sqlalchemy.url` for the database). 

One thing that is missing there and **must** be entered is a [MapBox](https://www.mapbox.com/) token 
(`mapbox_access_token` key in `[app:main]` section).

> Make sure you enable requests coming from URL of your deployed site in [MapBox token settings](https://console.mapbox.com/account/access-tokens).

No `.ini` files in [`/config/`](config) directory will be checked into VCS
(as per [`.gitignore`](.gitignore)).

### Create a virtual environment and install dependencies (from [`Pipfile`](Pipfile))

```bash
pipenv install
```

_Note #1: This will also automatically install `langworld_db_pyramid`  and `langworld_db_data` packages locally as they are mentioned in [`Pipfile`](Pipfile). 
There is no need to manually run `pip install -e .` (from [Pyramid docs](https://docs.pylonsproject.org/projects/pyramid/en/2.0-branch/narr/project.html#installing-your-newly-created-project-for-development)) separately._ 

_Note #2: These two packages will be installed in editable mode, which conforms to upcoming `pip` behavior that will install all local packages without copying them to the directory of the virtual environment._

To install with development dependencies (testing, linting):

```bash
pipenv install --dev
```

### Activate or use the virtual environment

Activate virtual environment...

```
pipenv shell
```

...or run all commands with `pipenv run`.


**All commands below must be run under virtual environment.**

### Run initialization script (after making it executable) 

```bash
bash_scripts/init_compile.sh
```

This [bash script](bash_scripts) applies [`alembic` migrations](langworld_db_pyramid/alembic/versions) to the database, runs the [`initialize_db` script](langworld_db_pyramid/scripts/initialize_db.py) that populates the database with data from [`langworld_db_data`](langworld_db_data) and compiles `Babel` message catalogs for the English version.

### Serve
```bash
pserve config/production.ini
```

For development, use [`development.ini`](config/development.ini) instead of [`production.ini`](config/production.ini).

Serve locally with `--reload` flag for `waitress` to reflect changes in [views](langworld_db_pyramid/views) and [templates](langworld_db_pyramid/templates) instantly:

```bash
pserve config/development.ini --reload
```

### Run [tests](tests)

```bash
pytest --cov
```

## Deployment to VPS

### Part 1: Setting up SSH Access for GitHub Actions

GitHub Actions will automatically update web app on your VPS. Do enable this, you need to let GitHub Actions ssh into your server.

#### 1.1 Generate SSH key pair for GitHub Actions

On your **local machine**, generate a new SSH key pair:

```bash
ssh-keygen -t ed25519 -C "github-actions-langworld" -f ~/.ssh/github_actions_langworld
```

This creates:
- Private key: `~/.ssh/github_actions_langworld`
- Public key: `~/.ssh/github_actions_langworld.pub`

#### 1.2 Add public key to VPS

Copy the public key to your VPS:

```bash
ssh-copy-id -i ~/.ssh/github_actions_langworld.pub -p <VPS_PORT> <VPS_USER>@<VPS_HOST>
```

Replace:
- `<VPS_PORT>`: SSH port (usually 22)
- `<VPS_USER>`: Your VPS username
- `<VPS_HOST>`: Your VPS IP address or domain

#### 1.3 Test SSH connection

Verify the key works:

```bash
ssh -i ~/.ssh/github_actions_langworld -p <VPS_PORT> <VPS_USER>@<VPS_HOST>
```

### Part 2: Initial Repository Setup on your VPS

#### 2.1 Clone the repository

SSH into your VPS and clone the repository:

```bash
cd ~
git clone https://github.com/<your-username>/langworld_db_pyramid.git
cd langworld_db_pyramid
```

#### 2.2 Install dependencies

Install pipenv if not already installed:

```bash
pip install pipenv
pipenv install
```

#### 2.3 Copy default [PasteDeploy](https://pastedeploy.readthedocs.io/en/latest/index.html) `.ini` files and edit `production.ini`

Copy `production.ini` from [`/config/default/`](config/default) to [`/config/`](config). Edit if needed (e.g. `sqlalchemy.url` for the database). 

One thing that is missing there and **must** be entered is a [MapBox](https://www.mapbox.com/) token 
(`mapbox_access_token` key in `[app:main]` section).

> Make sure you enable requests coming from URL of your deployed site in [MapBox token settings](https://console.mapbox.com/account/access-tokens).

No `.ini` files in [`/config/`](config) directory will be checked into VCS
(as per [`.gitignore`](.gitignore)).

#### 2.4 Create deployment script

Copy the sample deployment script:

```bash
cp bash_scripts/server_side_sample.sh bash_scripts/server_side.sh
chmod +x bash_scripts/server_side.sh
```

Edit `bash_scripts/server_side.sh` if you choose a different service name (not `langworld`) in Part 3 of this manual.

#### 2.5 Initial database setup

Run initial compilation and database setup:

```bash
bash_scripts/init_compile.sh
```

### Part 3: Setting up systemd Service

#### 3.1 Create systemd service file

Create a service file for your application:

```bash
sudo nano /etc/systemd/system/langworld.service
```

Example service file (adjust paths and settings as needed):

```ini
[Unit]
Description=Langworld DB Pyramid Application
After=network.target

[Service]
Type=simple
User=<VPS_USER>
WorkingDirectory=/home/<VPS_USER>/langworld_db_pyramid
ExecStart=/home/<VPS_USER>/.local/share/virtualenvs/<venv-name>/bin/pserve production.ini
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Replace:
- `<VPS_USER>`: Your VPS username
- `<venv-name>`: Your pipenv virtual environment name (find with `pipenv --venv`)

#### 3.2 Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable langworld.service
sudo systemctl start langworld.service
sudo systemctl status langworld.service
```

### Part 4: Configuring GitHub Actions

#### 4.1 Configure sudoers for passwordless service management

Allow the VPS user to restart the service without a password:

```bash
sudo visudo
```

Add this line **at the end of the file** (after the `@includedir` line):

```text
<VPS_USER> ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart langworld.service, /usr/bin/systemctl status langworld.service --no-pager
```

Replace `<VPS_USER>` with your actual VPS username.

**Important:** The commands in sudoers must match **exactly** what your deployment script calls, including the `--no-pager` flag.

Test that it works without password prompt:

```bash
ssh -p <VPS_PORT> <VPS_USER>@<VPS_HOST> "sudo systemctl status langworld.service --no-pager"
```

#### 4.2 Add GitHub Secrets

In your GitHub repository, go to **Settings → Secrets and variables → Actions** and add these secrets:

| Secret Name | Value | Description |
|------------|-------|-------------|
| `VPS_HOST` | Your VPS IP or domain | VPS hostname |
| `VPS_PORT` | SSH port (e.g., 22) | SSH port number |
| `VPS_LOGIN` | Your VPS username | VPS user account |
| `VPS_SSH_PRIVATE_KEY` | Content of `~/.ssh/github_actions_langworld` | Private key for SSH authentication |

For `VPS_SSH_PRIVATE_KEY`:

```bash
cat ~/.ssh/github_actions_langworld
```

Copy the entire output including `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----`.

#### 4.3 Clean up local private key

After setting up GitHub secrets, delete the private key from your local machine:

```bash
rm ~/.ssh/github_actions_langworld
```

The public key remains on the VPS in `~/.ssh/authorized_keys`.

#### 4.4 Create GitHub Actions workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches:
      - master

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_LOGIN }}
          key: ${{ secrets.VPS_SSH_PRIVATE_KEY }}
          port: ${{ secrets.VPS_PORT }}
          script: |
            set -e
            cd /home/${{ secrets.VPS_LOGIN }}/langworld_db_pyramid

            # BOOTSTRAP: Update the code to the latest version
            git fetch origin master
            git reset --hard origin/master

            # Make sure the script is executable
            chmod +x ${{ secrets.VPS_RELPATH_TO_SCRIPT }}

            # Execute the (now updated) script
            ./${{ secrets.VPS_RELPATH_TO_SCRIPT }}
```

Commit and push this file to your repository.

### Part 5. Test the deployment

Push a change to the `master` branch:

```bash
git add .
git commit -m "Test automated deployment"
git push origin master
```

Go to your GitHub repository → **Actions** tab to monitor the deployment.

### Troubleshooting

#### Deployment fails with "sudo: a password is required"

- Verify sudoers entry is at the **end** of `/etc/sudoers` (after `@includedir`)
- Ensure commands match **exactly**, including flags like `--no-pager`
- Test manually: `ssh -p <PORT> user@host "sudo systemctl status service --no-pager"`

#### Service fails to start

Check service logs:

```bash
sudo journalctl -u langworld.service -n 50
```

#### Git pull fails with "permission denied"

Ensure the repository was cloned by the same user configured in GitHub Actions secrets.

### Summary

Once configured, every push to the `master` branch will:

1. SSH into the VPS
2. Pull the latest code from GitHub
3. Install/update dependencies via pipenv
4. Run compilation scripts
5. Restart the systemd service
6. Display service status

No manual intervention required.

```
(works only if the project was installed in development mode)
