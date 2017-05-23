import copy
import salmon.utils as utils
import salmon.dag as dag

def opNodesCommute(nodeA, nodeB):
    
    # This is incomplete. We are only interested in Aggregations
    # in relation to other operations for now

    if isinstance(nodeA, dag.Aggregate):
        if isinstance(nodeB, dag.Project):
            return True

    return False

# TODO: This is hacky
def getNewMpcNode(node, suffix):

    assert(isinstance(node, dag.Aggregate))
    newNode = copy.deepcopy(node)
    newNode.outRel.rename(node.outRel.name + "_obl_" + suffix)
    newNode.keyCol.idx = 0
    newNode.aggCol.idx = 1
    newNode.isMPC = True
    newNode.children = set()
    newNode.makeOrphan()
    return newNode

def pushOpNodeDown(parent, node):

    # the only nodes we push down are aggregation nodes
    # we have created and so we know that these are single
    # parent nodes
    assert(len(parent.parents) == 1)
    grandParent = next(iter(parent.parents))
    
    # remove MPC aggregation between current node
    # and grandparent
    dag.removeBetween(grandParent, node, parent)

    # Need copy of node.children because we are 
    # updating node.children inside the loop
    tempChildren = copy.copy(node.children)

    if not tempChildren:
        dag.insertBetween(node, None, parent)
    
    for idx, child in enumerate(tempChildren):
        dag.insertBetween(node, child, getNewMpcNode(parent, str(idx)))

def splitNode(node):

    # Need copy of node.children because we are 
    # updating node.children inside the loop
    tempChildren = copy.copy(node.children)
    
    if not tempChildren:
        dag.insertBetween(node, None, getNewMpcNode(node, "0"))

    # We insert an mpc-agg node per child
    for idx, child in enumerate(tempChildren):
        dag.insertBetween(node, child, getNewMpcNode(node, str(idx)))

def pushDownMPC(sortedNodes):
    
    for node in sortedNodes:
        parents = node.parents

        if len(parents) == 1:
            # see if we can pull down any MPC ops
            parent = next(iter(parents))

            if parent.isMPC:
                # The parent node is in MPC mode which means
                # that it is either an MPC aggregation we can try
                # and push down or another op in which case we must
                # switch to mpc mode for the current node

                # TODO: this is not entirely correct!
                # we need to check if all nodes *above* the parent
                # are local 
                if opNodesCommute(parent, node):
                    pushOpNodeDown(parent, node)
                else:
                    node.isMPC = True
            else:
                # We are still in local mode. If the current node
                # does not require MPC, there's nothing to do, otherwise
                # we need to check if we can split the operation 
                if node.requiresMPC():
                    
                    if node.canSplit:
                        splitNode(node)
                    else:
                        node.isMPC = True

        elif len(parents) >= 2:
            node.isMPC = node.requiresMPC()
        

def pushUpMPC(revSortedNodes):

    for node in revSortedNodes:
        
        # Apply operator-specific rules to pass collusion
        # groups from the output relation of an op-node to
        # its inputs
        node.backPropCollSets()

        # Update the node's MPC mode which might have changed
        # as a result of the collusion set propagation
        node.updateMPC()

def rewriteDag(dag):

    sortedNodes = dag.topSort()
    pushDownMPC(sortedNodes)
    # ironic?
    # pushUpMPC(sortedNodes[::-1])
    return str(dag)

def mpc(f):

    def wrap():
        beerProg = rewriteDag(dag.OpDag(f()))
        return beerProg

    return wrap