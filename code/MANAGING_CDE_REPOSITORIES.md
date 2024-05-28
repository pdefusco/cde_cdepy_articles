## Managing CDE Repositories with CDEPY

Git repositories allow teams to collaborate, manage project artifacts, and promote applications from lower to higher environments. Cloudera currently supports Git providers such as GitHub, GitLab, and Bitbucket. Learn how to use Cloudera Data Engineering (CDE) with version control service.

## End to End Example

Install CDEPY==0.1.9 or above in your machine.

```
pip install cdepy==0.1.9
```

Import cdepy modules and set environment variables:

```
from cdepy import cdeconnection
from cdepy import cdeairflowpython
import os
import json

Connect via CdeConnection Object
JOBS_API_URL = "<myJobsAPIurl>"
WORKLOAD_USER = "<myusername>"
WORKLOAD_PASSWORD = "<mypwd>"
```

Instantiate a CdeConnection object in order to be able to connect to the CDE Virtual Cluster.

```
myCdeConnection = cdeconnection.CdeConnection(JOBS_API_URL, WORKLOAD_USER, WORKLOAD_PASSWORD)
myCdeConnection.setToken()
```

Instantiate a CdeRepositoryManager obect in order to be able to interact with CDE repositories.

```
myRepoManager = cderepositories.CdeRepositoryManager(myCdeConnection)
```

Provide git repository information. Use the provided git repository for testing purposes.

```
repoName = "exampleGitRepository"
repoPath = "https://github.com/pdefusco/cde_git_repo.git"
```

Create CDE Repository from Git Repository.

```
myRepoManager.createRepository(repoName, repoPath, repoBranch="main")
```

Show available CDE repositories.

```
myRepoManager.listRepositories()
```

Show CDE Repository Metadata.

```
myRepoManager.describeRepository(repoName)
```

Download file from CDE Repository.

```
filePath = "simple-pyspark-sql.py"
myRepoManager.downloadFileFromRepo(repoName, filePath)
```

Delete CDE Repository.

```
myRepoManager.deleteRepository(repoName)
```

Validate CDE Repository Deletion.

```
myRepoManager.listRepositories()
```

## References

[Documentation](https://docs.cloudera.com/data-engineering/1.5.3/manage-jobs/topics/cde-git-repo.html)
