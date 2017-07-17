import salmon.lang as sal
from salmon.comp import mpc
from salmon.codegen import spark
from salmon.utils import *

@mpc
def protocol():

    # define inputs
    colsInA = [
        defCol("INTEGER", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("STRING", [1, 2, 3]),
        defCol("INTEGER", [1, 2, 3])
    ]
    inA = sal.create("inA", colsInA, set([1]))

    projA = sal.project(inA, "projA", ["inA_0", "inA_17"])
    aggA = sal.aggregate(projA, "aggA", "projA_0", "projA_1", "+")
    # dummy mult, switch to div later
    divA = sal.multiply(aggA, "divA", "aggA_1", ["aggA_1", .001])
    multA = sal.multiply(divA, "multA", "divA_0", ["divA_0", 0])
    multB = sal.multiply(multA, "multB", "multA_1", ["multA_1", 100])
    aggB = sal.aggregate(multA, "aggB", "multA_1", "multA_0", "+")
    joinA = sal.join(multB, aggB, "joinA", "multB_0", "aggB_0")
    # dummy mult
    divB = sal.multiply(joinA, "divB", "joinA_1", ["joinA_1", "joinA_2"])
    multC = sal.multiply(divB, "multC", "divB_1", ["divB_1", "divB_1"])
    aggC = sal.aggregate(multC, "aggC", "multC_1", "multC_0", "+")

    opened = sal.collect(aggC, 1)

    # return root nodes
    return set([inA])

if __name__ == "__main__":

    dag = protocol()

    cg = spark.SparkCodeGen(dag)
    cg.generate("jointest1", "/tmp")

    print("Spark code generated in /tmp/jointest1.py")