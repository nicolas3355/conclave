from salmon import *

if __name__ == "__main__":

    # define inputs
    colsInA = [
        ("int", set([1, 2, 3])), 
        ("int", set([1, 2, 3])), 
        ("int", set([1, 2, 3]))
    ]
    inA = create("inA", colsInA)

    # specify the workflow
    agg = aggregate(inA, "agg", "inA_0", "inA_1", "+")
    projA = project(agg, "projA", None)
    projB = project(projA, "projB", None)

    # create dag with root nodes
    dag = OpDag(set([inA]))
    rewriteDag(dag)