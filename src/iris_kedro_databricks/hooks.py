from kedro.framework.hooks import hook_impl
from pyspark import SparkConf
from pyspark.sql import SparkSession
import os
import logging

logger = logging.getLogger(__name__)

class SparkHooks:
    @hook_impl
    def after_context_created(self, context) -> None:
        """Initialises a SparkSession using the config
        defined in project's conf folder.
        """
        # Load the spark configuration in spark.yaml using the config loader
        parameters = context.config_loader.get("spark*", "spark*/**")
        spark_conf = SparkConf().setAll(parameters.items())

        # Initialise the spark session
        if (os.environ['DATABRICKS_RUNTIME_VERSION'] is None):
          logger.info("NOT Running in databricks, setting configuration")
          spark_session_conf = (
              SparkSession.builder.appName(context._package_name)
              .enableHiveSupport()
              .config(conf=spark_conf)
          )
        else:
          logger.info("Running in databricks, skipping spark configuration")
          spark_session_conf = (
            SparkSession.builder.appName(context._package_name)
          )
        _spark_session = spark_session_conf.getOrCreate()
        _spark_session.sparkContext.setLogLevel("WARN")
  
