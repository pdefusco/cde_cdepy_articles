## Managing CDE Repositories with CDEPY

CDP Data Engineering (CDE) is the only cloud-native service purpose-built for enterprise data engineering teams. Building on Apache Spark, Data Engineering is an all-inclusive data engineering toolset that enables orchestration automation with Apache Airflow, advanced pipeline monitoring, visual troubleshooting, and comprehensive management tools to streamline ETL processes across enterprise analytics teams.

Git repositories allow teams to collaborate, manage project artifacts, and promote applications from lower to higher environments. CDE supports integration with Git providers such as GitHub, GitLab, and Bitbucket in order to synchronize job runs with different versions of your code.

CDEPY is a package that allows you to do all the above with the convenience of Python. With it you can remotely connect to a Virtual Cluster from your local machine or 3rd party tool as long as it supports Python. 

In this tutorial you will use CDEPY in order to create a CDE Repository from a Git repository and create a CDE Spark Job using the PySpark script loaded in the repository.  

### Requirements

* A CDE Service with Version 1.21 or above.
* A local machine with Python and the latest version of the cdepy Python package installed.

```
pip install cdepy
```

### End to End Example

Import cdepy modules and set environment variables:

```
from cdepy import cdeconnection
from cdepy import cdeairflowpython
from cdepy import cderepositories
from cdepy import cdejob
from cdepy import cdemanager
import os
import json

#Connect via CdeConnection Object
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
json.loads(myRepoManager.listRepositories())
```

Show CDE Repository Metadata.

```
json.loads(myRepoManager.describeRepository(repoName))
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
json.loads(myRepoManager.listRepositories())
```

Create a CDE Spark Job from a CDE Repository:

```
CDE_JOB_NAME = "sparkJobFromRepo"

#Set path of PySpark script inside the CDE Repository:
applicationFilePath = "simple-pyspark-sql.py"

myCdeSparkJob = cdejob.CdeSparkJob(myCdeConnection)
myCdeSparkJobDefinition = myCdeSparkJob.createJobDefinition(CDE_JOB_NAME=CDE_JOB_NAME, \
                                                            CDE_RESOURCE_NAME=repoName, \
                                                            APPLICATION_FILE_NAME=applicationFilePath, \
                                                            executorMemory="2g", \
                                                            executorCores=2)

myCdeClusterManager = cdemanager.CdeClusterManager(myCdeConnection)
myCdeClusterManager.createJob(myCdeSparkJobDefinition)
myCdeClusterManager.runJob(CDE_JOB_NAME)
```

Optional: update code in "simple-pyspark-sql.py" in git repository.
Then pull from git repo to CDE repo in order to load code changes.

```
myRepoManager.pullRepository(repoName)
```

Describe CDE repository again. Notice changes to metadata.

```
json.loads(myRepoManager.describeRepository(repoName))
```

Download file from CDE Repository.

```
myRepoManager.downloadFileFromRepo(repoName, filePath)
```

Delete CDE Repository.

```
myRepoManager.deleteRepository(repoName)
```

Validate CDE Repository Deletion.

```
json.loads(myRepoManager.listRepositories())
```

## References

[Documentation](https://docs.cloudera.com/data-engineering/1.5.3/manage-jobs/topics/cde-git-repo.html)

[Introductory Article to CDEPY](https://community.cloudera.com/t5/Community-Articles/CDEPY-a-Python-Package-to-work-with-Cloudera-Data/ta-p/378015)

[CDEPY on PyPi](https://pypi.org/project/cdepy/)
