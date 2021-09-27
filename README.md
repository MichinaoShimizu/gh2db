# gh2db

Migrate GitHub data to database.

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


### Create

```bash
$ gh2db --create_all
[2021-09-27 21:26:04 INFO] Create all tables start
[2021-09-27 21:26:04 INFO] Create all tables completed
```

```
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
$ gh2db --drop_all
[2021-09-27 21:26:11 INFO] Drop all tables start
[2021-09-27 21:26:12 INFO] Drop all tables completed
```

### Delete

```bash
$ gh2db --delete_all
[2021-09-27 21:27:08 INFO] Delete all of table rows start
[2021-09-27 21:27:08 INFO] Delete all of table rows completed
```

### Update (User)

```bash
$ gh2db --update_user_repos
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
$ gh2db --update_org_repos
```
