## Downloading CDE Job Logs with CDEPY

CDP Data Engineering (CDE) is the only cloud-native service purpose-built for enterprise data engineering teams. Building on Apache Spark, Data Engineering is an all-inclusive data engineering toolset that enables orchestration automation with Apache Airflow, advanced pipeline monitoring, visual troubleshooting, and comprehensive management tools to streamline ETL processes across enterprise analytics teams.

CDEPY is a package that allows you to do all the above with the convenience of Python. With it you can remotely connect to a Virtual Cluster from your local machine or 3rd party tool as long as it supports Python.

In this tutorial you will use CDEPY in order to download all logs from all spark jobs across multiple virtual clusters.

### Requirements

* A CDE Service with Version 1.24 or above with at least one previous Airflow run and Spark job run.
* A local machine with Python and the latest version of the cdepy Python package installed.
* A Python virtual environment with cdepy 0.1.19 or above installed.

```
pip install cdepy
```

### Sample Code for a Single Job Run

Import cdepy modules and set environment variables:

```
from cdepy import cdeconnection
from cdepy import cdemanager
from cdepy import utils
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

Instantiate Cluster Manager object to interact with the CDE Virtual Cluster:

```
myCdeClusterManager = cdemanager.CdeClusterManager(myCdeConnection)
```

List all job runs:

```
allJobRuns = myCdeClusterManager.listJobRuns()
print(allJobRuns)
```

List all job runs of type Spark:

```
allSparkJobRuns = myCdeClusterManager.listJobRuns("spark")
print(allSparkJobRuns)
```

Show available Log Types for a single Spark job run:

```
jobRunId = "<jobRunId>" # obtained from allSparkJobRuns
myCdeClusterManager.showAvailableLogTypes(jobRunId)
```

Download driver/event Logs:

```
logsType = "driver/event"
sparkEventLogsClean = downloadJobRunLogs(jobRunId, logsType)
```

Parse and print out Logs:

```
sparkEventLogsClean = utils.sparkEventLogParser(sparkEventLogs)
print(sparkEventLogsClean)
```

### End to End Application for All Runs across multiple CDE Virtual Clusters

We now apply the same code to a Python script that will iterate through multiple CDE Virtual Clusters and download logs locally as txt files.

Run the script with:

```
python downloadAllLogs.py
```

```

```
