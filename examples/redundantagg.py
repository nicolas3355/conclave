import salmon.lang as sal 
from salmon.comp import mpc

@mpc
def protocol():
    # define inputs
    colsInA = [
        ("int", set([1, 2, 3])), 
        ("int", set([1, 2, 3]))
    ]
    inA = sal.create("inA", colsInA)

    # specify the workflow
    agg = sal.aggregate(inA, "agg", "inA_0", "inA_1", "+")
    projA = sal.project(agg, "projA", None)
    projB = sal.project(projA, "projB", None)
    projC = sal.project(projA, "projC", None)
    otherAgg = sal.aggregate(agg, "otherAgg", "agg_0", "agg_1", "+")

    # create dag with root nodes
    return set([inA])
    
if __name__ == "__main__":

    print(protocol())