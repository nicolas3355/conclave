import os
import sys

import conclave.lang as cc
from conclave import generate_code, dispatch_jobs
from conclave.config import CodeGenConfig, SharemindCodeGenConfig
from conclave.utils import defCol


def protocol():
    input_columns_left = [
        defCol("column_a", "INTEGER", [1]),
        defCol("column_b", "INTEGER", [1])
    ]
    left = cc.create("left", input_columns_left, {1})
    input_columns_right = [
        defCol("column_a", "INTEGER", [2]),
        defCol("column_b", "INTEGER", [2])
    ]
    right = cc.create("right", input_columns_right, {2})
    rel = cc.concat([left, right], "rel")
    filtered = cc.cc_filter(rel, "filtered", "column_b", "==", scalar=1)
    in_order = cc.sort_by(filtered, "in_order", "column_a")
    actual = cc.distinct_count(in_order, "actual", "column_a")
    cc.collect(actual, 1)
    return {left, right}


if __name__ == "__main__":
    pid = sys.argv[1]
    # define name for the workflow
    workflow_name = "real-distinct-count-test-" + pid
    # configure conclave
    conclave_config = CodeGenConfig(workflow_name, int(pid))
    conclave_config.all_pids = [1, 2, 3]
    sharemind_conf = SharemindCodeGenConfig("/mnt/shared",
                                            use_docker=True,
                                            use_hdfs=False)
    conclave_config.with_sharemind_config(sharemind_conf)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # point conclave to the directory where the generated code should be stored/ read from
    conclave_config.code_path = os.path.join("/mnt/shared", workflow_name)
    # point conclave to directory where data is to be read from...
    conclave_config.input_path = os.path.join(current_dir, "data")
    # and written to
    conclave_config.output_path = os.path.join(current_dir, "data")
    # define this party's unique ID (in this demo there is only one party)
    job_queue = generate_code(protocol, conclave_config, ["sharemind"], ["python"], apply_optimizations=True)
    dispatch_jobs(job_queue, conclave_config)
