## Managing CDE Job Logs with CDEPY

CDP Data Engineering (CDE) is the only cloud-native service purpose-built for enterprise data engineering teams. Building on Apache Spark, Data Engineering is an all-inclusive data engineering toolset that enables orchestration automation with Apache Airflow, advanced pipeline monitoring, visual troubleshooting, and comprehensive management tools to streamline ETL processes across enterprise analytics teams.

CDEPY is an open source Python wrapper to the CDE API. With it you can remotely connect to a Virtual Cluster from your local machine or 3rd party tool and perform actions such as creating and running jobs, job resources, and a lot more.

All logs are already available to you in your storage location, for example S3, and the exact location is provided in the CDE Job Runs UI. However, you can download the logs with the CDE API and a result with CDEPY. In this tutorial you will use CDEPY to download all logs from all spark jobs across multiple virtual clusters.

### Log Types in CDE Spark

* driver/stdout: The standard output stream of the Spark driver; contains logs printed via println, logging info, or System.out.

* driver/stderr: The standard error stream of the driver; includes stack traces, errors, and warnings.

* driver/k8sevents: Kubernetes events related to the driver's pod, such as scheduling, container start, or failures.

* driver/event: The Spark event log produced by the driver; used by the Spark History Server for tracking job stages and metrics.

* executor_n/stdout: The standard output of a specific executor (n is the executor number); contains logs from tasks running on that executor.

* driver/tgtloader: Logs related to target loader tasks initiated by the driver—typically seen in data loading or transformation pipelines.

* driver/workspace-init: Logs from the initialization of the driver’s runtime environment, such as downloading dependencies or setting up volumes.

* submitter/stderr: The error output of the Spark job submitter process, often including submission or API call failures.

* submitter/stdout: The standard output of the job submitter, showing job submission progress or responses.

* submitter/k8s: Kubernetes-related logs generated during job submission, often showing K8s API interactions.

* submitter/jobs_api: Logs from the internal CDE API used to submit and manage Spark jobs.

### Requirements

* A CDE Service with Version 1.24 or above with at least one previous Airflow run and Spark job run.
* A local machine with Python and the latest version of the cdepy Python package installed.
* A Python virtual environment with cdepy 0.1.19 or above installed.

```
pip install cdepy
```

### Simple Example for a Single Job Run

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

### End to End Script for All Spark Runs across multiple CDE Virtual Clusters

We now apply the same code to a Python script that will iterate through multiple CDE Virtual Clusters and download logs locally as txt files. The source code is available in this repository under `resources/logFetcher.py`.

Run the script with:

```
python logFetcher.py \
  --user <your-cdp-workload-user> \
  --password <your-cdp-workload-password> \
  --api-urls https://cluster1.example.com/dex/api/v1 https://cluster2.example.com/dex/api/v1
```

The above will retrieve and write all logs. Optionally set the type of Spark log if you'd like to retrieve just one, for example 'driver/event':

```
python logFetcher.py \
  --user <your-cdp-workload-user> \
  --password <your-cdp-workload-password> \
  --api-urls https://cluster1.example.com/dex/api/v1 https://cluster2.example.com/dex/api/v1 \
  --log-type driver/stdout
```

As an example, this command will result in the following folder structure on your local machine:

```
python logFetcher.py \
  --user pauldefusco \
  --password mypassword \
  --api-urls https://55f9q9ww.cde-jhnkv684.pdf-jul.a465-9q4k.cloudera.site/dex/api/v1 https://k5hzst9x.cde-jhnkv684.pdf-jul.a465-9q4k.cloudera.site/dex/api/v1
```

```
logs/
└── <hostname>/
    └── <job_run_id>/
        └── <log_type>/
            └── <hostname>.log
```

## References

[Documentation](https://docs.cloudera.com/data-engineering/1.5.3/manage-jobs/topics/cde-git-repo.html)

[Introductory Article to CDEPY](https://community.cloudera.com/t5/Community-Articles/CDEPY-a-Python-Package-to-work-with-Cloudera-Data/ta-p/378015)

[CDEPY on PyPi](https://pypi.org/project/cdepy/)
