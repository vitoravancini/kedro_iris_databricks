# Databricks notebook source
# MAGIC %sh
# MAGIC pip install -r ../src/requirements.txt

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

import importlib
from pathlib import Path
from kedro.framework.project import configure_project
from kedro.framework.session import KedroSession
from pathlib import Path
from kedro.utils import load_obj
from kedro.framework.startup import bootstrap_project
from pathlib import Path

import os

def main(*args, **kwargs):
    env = None
    params = None
    bootstrap_project(str(Path('.').absolute()))
    tag = None
    is_async= None
    runner = load_obj("SequentialRunner", "kedro.runner")
    tag = _get_values_as_tuple(tag) if tag else tag
    node_names = []
    from_nodes = None
    to_nodes = None
    from_inputs = None
    to_outputs = None
    load_version = None
    pipeline = None

    with KedroSession.create(env=env, extra_params=params) as session:
        session.run(
            tags=tag,
            runner=runner(is_async=is_async),
            node_names=node_names,
            from_nodes=from_nodes,
            to_nodes=to_nodes,
            from_inputs=from_inputs,
            to_outputs=to_outputs,
            load_versions=load_version,
            pipeline_name=pipeline,
        )

if __name__ == "__main__":
  try:
    os.chdir('..')
    main()
  except Exception as e:
    print(str(e))
    raise e
  finally:
    os.chdir('notebooks')
