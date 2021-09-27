# gh2db

## Install

```bash
pip3 install git+https://github.com/MichinaoShimizu/gh2db
```

## Usage

```bash
export GH2DB_GITHUB_TOKEN=
export GH2DB_GITHUB_TARGET_ORGANIZATION_NAME=
export GH2DB_GITHUB_PER_PAGE=100
export GH2DB_GITHUB_MAX_PAGE_REPOSITORIES=3
export GH2DB_GITHUB_MAX_PAGE_PULL_REQUESTS=3
export GH2DB_GITHUB_MAX_PAGE_TEAMS=3
export GH2DB_GITHUB_MAX_PAGE_TEAM_MEMBERS=3
export GH2DB_DB_DIALECT=mysql
export GH2DB_DB_USERNAME=
export GH2DB_DB_PASSWORD=
export GH2DB_DB_HOSTNAME=localhost
export GH2DB_DB_PORT=22
export GH2DB_DB_NAME=gh
export GH2DB_DB_LOG_LEVEL=ERROR
export GH2DB_APP_LOG_LEVEL=INFO
```

```bash
$ gh2db
usage: [-h] [--update_user_repos] [--update_org_repos] [--create_all] [--drop_all] [--delete_all] [--count_all]
```

### Create Tables

```bash
gh2db --create_all
```

### Drop Tables

```bash
gh2db --drop_all
```

### Delete Rows

```bash
gh2db --delete_all
```

### Update User Repositories Data

```bash
gh2db --update_user_repos
```

### Update Organization Repositories Data

```bash
gh2db --update_org_repos
```
