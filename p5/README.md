# Project 5: Data Pipelines with Airflow

### Summary

In this project I use Apache Airflow in order to introduce automation to scheduling data pipelines and monitoring data quality.  After writing operators to stage the data, load facts and dimension tables, and perform data quality checks, I configure the task dependencies so as to create the following DAG (directed acyclic graph).

![example dag](example-dag.png)

### Files

In order to see the graph and related tasks, a local Airflow installation is required.  I recommend this Docker image with LocalExecutor option https://github.com/puckel/docker-airflow.

The `airflow` directory must be accessible from within Docker, either as a bind mount or volume.  It contains the following sub-directories
- `dags`: contains the Python files to define task dependencies and call operators (note that the actual Python script is not run, but parsed by Airflow to run the defined DAG)
- `plugins`: defines operators and SQL queries to run the tasks in the DAG

Creating the tables initially in Redshift is outside of the pipeline defined by the DAG and can be performed with the provided `create_tables.sql` file.

Even though for the sake of this project the DAG is run only once, I have included additional functionality by way of operator parameters, such as distinguishing between JSON/CSV formats during staging, and append vs delete/load functionality while loading dimension tables during backfilling. 