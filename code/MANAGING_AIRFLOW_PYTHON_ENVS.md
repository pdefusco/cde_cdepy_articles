## Managing Airflow Python Environments with CDEPY

To manage job dependencies, Cloudera Data Engineering (CDE) supports creating custom Python environments dedicated to Airflow using the airflow-python-env resource type. With this option, you can install custom libraries for running your Directed Acyclic Graphs (DAGs). The supported version is Python 3.8.

A resource is a named collection of files or other resources referenced by a job. The airflow-python-env resource type allows you to specify a requirements.txt file that defines an environment that you can then activate globally for airflow deployments in a virtual cluster.

You can install and use custom python packages for Airflow with Cloudera Data Engineering (CDE). Typically this feature is used in order to install third party Airflow providers in CDE. However, it can also be used to install any Python package and use it within the DAG logic.

In this example you will create a CDE Airflow Python environment with the Amazon Provider for Airflow. Then, you will deploy an Airflow DAG that creates an S3 bucket, reads a txt file from a CDE Files Resource and writes it to the S3 bucket, launches a CDE Spark Job and finally deletes the S3 bucket.

### Requirements

* A CDE Service with Version 1.21 or above.
* A local machine with Python and the latest version of the cdepy Python package installed.

```
pip install cdepy==0.1.9
```

### End to End Example

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

Instantiate a CdeAirflowPythonEnv object to manage Airflow Python Environments.

```
myAirflowPythonEnvManager = cdeairflowpython.CdeAirflowPythonEnv(myCdeConnection)
```

Create a Maintenance Session in order to perform any Airflow Python Environments related actions.

```
myAirflowPythonEnvManager.createMaintenanceSession()
```

Register a pip repository in CDE.

```
myAirflowPythonEnvManager.createPipRepository()
```

Check on Status of Maintenance Session

```
myAirflowPythonEnvManager.checkAirflowPythonEnvStatus()
```

The output should be ```{"status":"pip-repos-defined"}```.

Load requirements.txt file

```
pathToRequirementsTxt = "/resources/requirements.txt"
myAirflowPythonEnvManager.buildAirflowPythonEnv(pathToRequirementsTxt)
```

The requirements.txt file must be customized before it is uploaded.

```
myAirflowPythonEnvManager.checkAirflowPythonEnvStatus()
```

The response status should be ```{"status":"building"}```. Repeat the request in a couple of minutes. Eventually, once the response status becomes ```{"status":"built"}``` you will be ready to move on.

Validate status of Python environment.

```
myAirflowPythonEnvManager.getAirflowPythonEnvironmentDetails()
```

Explore Maintenace Session logs.

```
myAirflowPythonEnvManager.viewMaintenanceSessionLogs()
```

Activate the Python environment.

```
myAirflowPythonEnvManager.activateAirflowPythonEnv()
```

Check on Python environment build status.

```
myAirflowPythonEnvManager.checkAirflowPythonEnvStatus()
```

The response should be ```{"status":"activating"}```. The maintenance session will then end after a couple of minutes. This means that the environment has been activated.

Once the Airlfow Python environment has activated, you can create a CDE Airflow Job.

First, create pipeline resource and upload the dag to it:

```
CDE_RESOURCE_NAME = "my_pipeline_resource"
myCdeFilesResource = cderesource.CdeFilesResource(CDE_RESOURCE_NAME)
myCdeFilesResourceDefinition = myCdeFilesResource.createResourceDefinition()

LOCAL_FILE_PATH = "resources"
LOCAL_FILE_NAME = "s3BucketDag.py"

myCdeClusterManager = cdemanager.CdeClusterManager(myCdeConnection)

myCdeClusterManager.createResource(myCdeFilesResourceDefinition)
myCdeClusterManager.uploadFileToResource(CDE_RESOURCE_NAME, LOCAL_FILE_PATH, LOCAL_FILE_NAME)
```

Create files resource.

The Airflow DAG will use the S3BucketOperator and the BashOperator to read the file from the CDE Files Reosurce and write it in an S3 bucket.

```
CDE_RESOURCE_NAME = "my_file_resource"
myCdeFilesResource = cderesource.CdeFilesResource(CDE_RESOURCE_NAME)
myCdeFilesResourceDefinition = myCdeFilesResource.createResourceDefinition()

LOCAL_FILE_PATH = "resources"
LOCAL_FILE_NAME = "my_file.txt"

myCdeClusterManager.createResource(myCdeFilesResourceDefinition)
myCdeClusterManager.uploadFileToResource(CDE_RESOURCE_NAME, LOCAL_FILE_PATH, LOCAL_FILE_NAME)
```

Create a CDE Spark Job along with its resource:

```
CDE_RESOURCE_NAME = "my_script_resource"
myCdeFilesResource = cderesource.CdeFilesResource(CDE_RESOURCE_NAME)
myCdeFilesResourceDefinition = myCdeFilesResource.createResourceDefinition()

LOCAL_FILE_PATH = "resources"
LOCAL_FILE_NAME = "pysparksql.py"

myCdeClusterManager.createResource(myCdeFilesResourceDefinition)
myCdeClusterManager.uploadFileToResource(CDE_RESOURCE_NAME, LOCAL_FILE_PATH, LOCAL_FILE_NAME)
myCdeClusterManager.createJob(myCdeSparkJobDefinition)

CDE_JOB_NAME = "simple-pyspark"

myCdeSparkJob = cdejob.CdeSparkJob(myCdeConnection)
myCdeSparkJobDefinition = myCdeSparkJob.createJobDefinition(CDE_JOB_NAME, CDE_RESOURCE_NAME, APPLICATION_FILE_NAME=LOCAL_FILE_NAME, executorMemory="2g", executorCores=2)
```

Create & Run CDE Airflow Job:

```
CDE_JOB_NAME = "PythonEnvDag"
DAG_FILE = "s3BucketDag.py"
CDE_RESOURCE_NAME = "my_pipeline_resource"

myCdeAirflowJob = cdejob.CdeAirflowJob(myCdeConnection)
myCdeAirflowJobDefinition = myCdeAirflowJob.createJobDefinition(CDE_JOB_NAME, DAG_FILE, CDE_RESOURCE_NAME)

myCdeClusterManager.createJob(myCdeAirflowJobDefinition)
myCdeClusterManager.runJob(CDE_JOB_NAME)
```

Optional: Create a new Maintenance Session in order to delete the Python environment

```
myAirflowPythonEnvManager.createMaintenanceSession()
myAirflowPythonEnvManager.deleteAirflowPythonEnv()
```

Optional: End the Maintenance Session once you have deleted the Python environment

```
myAirflowPythonEnvManager.deleteMaintenanceSession()
```

### References

[Documentation](https://docs.cloudera.com/data-engineering/1.5.3/orchestrate-workflows/topics/cde-custom-python-airflow.html)
