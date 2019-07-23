import logging

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'
    
    # https://dataedo.com/kb/query/amazon-redshift/find-tables-without-primary-keys
    no_pkey_sql="""
    select tab.table_schema, tab.table_name
    from information_schema.tables tab
    left join information_schema.table_constraints tco 
        on tab.table_schema = tco.table_schema
        and tab.table_name = tco.table_name 
        and tco.constraint_type = 'PRIMARY KEY'
    where tab.table_type = 'BASE TABLE'
        and tab.table_schema not in ('pg_catalog', 'information_schema')
        and tco.constraint_name is null
    order by table_schema, table_name;
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        """
        checks for the number of user-defined tables that contain no primary keys,
        which should be 2, namely staging_songs and staging_events
        """
        redshift_hook = PostgresHook(self.redshift_conn_id)
        records = redshift_hook.get_records(DataQualityOperator.no_pkey_sql)
        if len(records) > 2:
            raise ValueError("Data quality check failed. Too many tables contain no primary keys")
        logging.info("Data quality check passed")
