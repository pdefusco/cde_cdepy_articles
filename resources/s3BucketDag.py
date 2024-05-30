#****************************************************************************
# (C) Cloudera, Inc. 2020-2024
#  All rights reserved.
#
#  Applicable Open Source License: GNU Affero General Public License v3.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# #  Author(s): Paul de Fusco
#***************************************************************************/

from dateutil import parser
from datetime import datetime, timedelta
from datetime import timezone
from airflow import DAG
from cloudera.cdp.airflow.operators.cde_operator import CDEJobRunOperator
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator, S3CreateBucketOperator, S3CreateObjectOperator, S3DeleteBucketOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
import pendulum

username = "pdefusco-051224-v1"
bucket_name = "eastbucket-" + username
cde_job_name = "simple-pyspark"

print("Running as Username: ", username)

#DAG instantiation
default_args = {
        'owner': 'pauldefusco',
        'retry_delay': timedelta(seconds=5),
        'depends_on_past': False,
        'start_date': datetime(2023,9,20,0),
        'schedule_interval':'@hourly',
        'end_date': datetime(2024,9,30,8)
        }

dag_name = '{}-aws-prvdrs'.format(username)

custom_airflow_dag = DAG(
    dag_name,
    default_args=default_args,
    catchup=False,
    is_paused_upon_creation=False
)

start = DummyOperator(
    task_id="start",
    dag=custom_airflow_dag
)

create_bucket = S3CreateBucketOperator(
    task_id='create_bucket',
    bucket_name=bucket_name,
    dag=custom_airflow_dag,
    aws_conn_id='s3_default',
    region_name='us-east-2'
)

list_bucket  = S3ListOperator(
    task_id="list_keys",
    bucket=bucket_name,
    dag=custom_airflow_dag,
    aws_conn_id = 's3_default'
)

read_conf = BashOperator(
    	task_id="read_conf",
    	bash_command="cat /app/mount/my_file_resource/my_file.txt",
        do_xcom_push=True,
        dag=custom_airflow_dag
	)

create_object = S3CreateObjectOperator(
    task_id="create_object",
    s3_bucket=bucket_name,
    s3_key="my_file.txt",
    data="{{ ti.xcom_pull(task_ids=[\'read_conf\'])}}",
    replace=True,
    dag=custom_airflow_dag,
    aws_conn_id = 's3_default'
)

#Using the CDEJobRunOperator
etl = CDEJobRunOperator(
  task_id='etl',
  dag=custom_airflow_dag,
  job_name=cde_job_name #job_name needs to match the name assigned to the Spark CDE Job in the CDE UI
)

delete_bucket = S3DeleteBucketOperator(
    task_id='delete_bucket',
    bucket_name=bucket_name,
    force_delete=True,
    dag=custom_airflow_dag,
    aws_conn_id = 's3_default'
)

end = DummyOperator(
    task_id="end",
    dag=custom_airflow_dag
)
#Execute tasks in the below order

# step6c only executes when both step6a and step6b have completed
start >> create_bucket >> list_bucket >> read_conf >> create_object >> etl >> delete_bucket>> end
