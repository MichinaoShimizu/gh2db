# gh2db

[![PyPI version](https://badge.fury.io/py/gh2db.svg)](https://badge.fury.io/py/gh2db)

Migrate GitHub data to database.

## Environment variables

```bash
# GitHub API
export GH2DB_GITHUB_TOKEN=
export GH2DB_GITHUB_TARGET_ORGANIZATION_NAME=
export GH2DB_GITHUB_PER_PAGE=100
export GH2DB_GITHUB_MAX_PAGE_REPOSITORIES=3
export GH2DB_GITHUB_MAX_PAGE_PULL_REQUESTS=3
export GH2DB_GITHUB_MAX_PAGE_TEAMS=3
export GH2DB_GITHUB_MAX_PAGE_TEAM_MEMBERS=3

# Database(MySQL)
export GH2DB_DB_DB_URI=mysql://root:@localhost:22/gh2db?charset=utf8
# Database(SQLite)
export GH2DB_DB_DB_URI=sqlite:///sample_db.sqlite3
# Database(SQLite Un-memory)
export GH2DB_DB_DB_URI=sqlite:///:memory:
# Database(PostgreSQL)
export GH2DB_DB_DB_URI=postgresql///?User=postgres&Password=admin&Database=postgres&Server=127.0.0.1&Port=5432
# Database(Oracle)
export GH2DB_DB_DB_URI=oracleoci///?User=myuser&Password=mypassword&Server=localhost&Port=1521
# Database(MS SQL)
export GH2DB_DB_DB_URI=sql///?User=myUser&Password=myPassword&Database=NorthWind&Server=myServer&Port=1433

export GH2DB_DB_LOG_LEVEL=ERROR
export GH2DB_APP_LOG_LEVEL=INFO
```

## Usage

```bash
$ gh2db
usage: [-h] [--update_user] [--update_org] [--create] [--drop] [--delete]
```

### Create

```bash
gh2db --create
[2021-09-27 21:26:04 INFO] Create all tables start
[2021-09-27 21:26:04 INFO] Create all tables completed
```

```bash
+----------------------------------------+
| Tables_in_gh                           |
+----------------------------------------+
| github_organization_team_members       |
| github_organization_teams              |
| github_organizations                   |
| github_repositories                    |
| github_repository_labels               |
| github_repository_pull_request_commits |
| github_repository_pull_request_labels  |
| github_repository_pull_request_reviews |
| github_repository_pull_requests        |
| github_users                           |
+----------------------------------------+
10 rows in set (0.00 sec)
```

### Drop

```bash
gh2db --drop
[2021-09-27 21:26:11 INFO] Drop all tables start
[2021-09-27 21:26:12 INFO] Drop all tables completed
```

### Delete

```bash
gh2db --delete
[2021-09-27 21:27:08 INFO] Delete all of table rows start
[2021-09-27 21:27:08 INFO] Delete all of table rows completed
```

### Update (User)

```bash
gh2db --update_user
[2021-09-27 21:28:00 INFO] ---------------------------
[2021-09-27 21:28:00 INFO] GitHub API Authorized By Personal AccessToken: OK
[2021-09-27 21:28:00 INFO] Github API Rate Limitting Information:
[2021-09-27 21:28:00 INFO] Remaining, Limit: (4441, 5000)
[2021-09-27 21:28:01 INFO] ResetTime: 2021-09-27 12:49:21
[2021-09-27 21:28:01 INFO] ---------------------------
[2021-09-27 21:28:01 INFO] User Model
[2021-09-27 21:28:01 INFO]  Repository Models (User:mshimizu)
[2021-09-27 21:28:02 INFO]   Label Models (Repository:MichinaoShimizu/anemone)
[2021-09-27 21:28:02 INFO]   Pull Request Models (Repository:MichinaoShimizu/anemone)
[2021-09-27 21:28:03 INFO]   Label Models (Repository:MichinaoShimizu/devmetrics)
[2021-09-27 21:28:03 INFO]   Pull Request Models (Repository:MichinaoShimizu/devmetrics)
[2021-09-27 21:28:05 INFO]    Pull Request Label Models (#13)
[2021-09-27 21:28:05 INFO]    Review Models (#13)
[2021-09-27 21:28:05 INFO]    Commit Models (#13)
[2021-09-27 21:28:06 INFO]    Pull Request Label Models (#10)
[2021-09-27 21:28:06 INFO]    Review Models (#10)
[2021-09-27 21:28:07 INFO]    Commit Models (#10)
[2021-09-27 21:28:08 INFO]    Pull Request Label Models (#11)
[2021-09-27 21:28:08 INFO]    Review Models (#11)
[2021-09-27 21:28:08 INFO]    Commit Models (#11)
...
[2021-09-27 21:28:45 INFO]   Label Models (Repository:MichinaoShimizu/oas_contrib)
[2021-09-27 21:28:45 INFO]   Pull Request Models (Repository:MichinaoShimizu/oas_contrib)
[2021-09-27 21:28:47 INFO] Database committed
[2021-09-27 21:28:47 INFO] Database session closed
```

### Update (Organization)

```bash
gh2db --update_org
```
