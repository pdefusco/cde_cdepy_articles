## Managing Airflow Python Environments with CDEPY

To manage job dependencies, Cloudera Data Engineering (CDE) supports creating custom Python environments dedicated to Airflow using the airflow-python-env resource type. With this option, you can install custom libraries for running your Directed Acyclic Graphs (DAGs). The supported version is Python 3.8.

A resource is a named collection of files or other resources referenced by a job. The airflow-python-env resource type allows you to specify a requirements.txt file that defines an environment that you can then activate globally for airflow deployments in a virtual cluster.

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
pathToRequirementsTxt = "/examples/requirements.txt"
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

Optional: Create a new session and then delete the Python environment

```
myAirflowPythonEnvManager.deleteAirflowPythonEnv()
```

Optional: End the Maintenance Session once you have deleted the Python environment
```
myAirflowPythonEnvManager.deleteMaintenanceSession()
```

## References

[Documentation](https://docs.cloudera.com/data-engineering/1.5.3/orchestrate-workflows/topics/cde-custom-python-airflow.html)
