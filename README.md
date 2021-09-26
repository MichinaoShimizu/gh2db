# gh2db

## Usage

generate `.env` file.

```bash
GITHUB_TOKEN=
APPROVED_ORGANIZATION_NAME=

DB_DIALECT=mysql
DB_USERNAME=
DB_PASSWORD=
DB_HOSTNAME=localhost
DB_PORT=22
DB_NAME=gh
DB_ECHO_TYPE=0
```

```bash
$ python gh2db/gh2db/ --create_database
usage: [-h] [--update_user_repos] [--update_org_repos] [--create_all] [--drop_all] [--delete_all] [--count_all]
```
