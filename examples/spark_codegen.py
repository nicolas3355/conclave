import salmon.lang as sal
from salmon.comp import dagonly
from salmon.codegen import spark, viz
from salmon.utils import *

@dagonly
def simple_div():

    colsInA = [
        defCol("a", "INTEGER", [1, 2, 3]),
        defCol("b", "INTEGER", [1, 2, 3]),
        defCol("c", "INTEGER", [1, 2, 3])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    div1 = sal.divide(in1, "div1", "a", ["a", "b"])

    opened = sal.collect(div1, 1)

    # return root nodes
    return set([in1])


@dagonly
def comp_div():

    colsInA = [
        defCol("a", "INTEGER", [1, 2, 3]),
        defCol("b", "INTEGER", [1, 2, 3]),
        defCol("c", "INTEGER", [1, 2, 3])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    # divide column 0 by columns 1 & 2, then divide by 5 (scalar)
    div1 = sal.divide(in1, "div1", "a", ["a", "b", "c", 5])

    opened = sal.collect(div1, 1)

    # return root nodes
    return set([in1])


@dagonly
def simple_mult():

    colsInA = [
        defCol("a", "INTEGER", [1, 2, 3]),
        defCol("b", "INTEGER", [1, 2, 3]),
        defCol("c", "INTEGER", [1, 2, 3])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    mult1 = sal.multiply(in1, "mult1", "a", ["a", "b"])

    opened = sal.collect(mult1, 1)

    # return root nodes
    return set([in1])


@dagonly
def comp_mult():
    colsInA = [
        defCol("a", "INTEGER", [1, 2, 3]),
        defCol("b", "INTEGER", [1, 2, 3]),
        defCol("c", "INTEGER", [1, 2, 3])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    # multiply column 0 by columns 1 & 2, then multiply by 5 (scalar)
    mult1 = sal.multiply(in1, "mult1", "a", ["a", "b", "c", 5])

    opened = sal.collect(mult1, 1)

    # return root nodes
    return set([in1])


@dagonly
def create_col_mult():
    colsInA = [
        defCol("a", "INTEGER", [1, 2, 3]),
        defCol("b", "INTEGER", [1, 2, 3]),
        defCol("c", "INTEGER", [1, 2, 3])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    mult1 = sal.multiply(in1, "mult1", "d", ["a", "b"])

    opened = sal.collect(mult1, 1)

    return set([in1])


if __name__ == "__main__":

    simple_mult_dag = simple_mult()
    comp_mult_dag = comp_mult()
    simple_div_dag = simple_div()
    comp_div_dag = comp_div()
    create_mult_dag = create_col_mult()

    simple_mult = spark.SparkCodeGen(simple_mult_dag)
    simple_mult.generate("simple_mult", "/tmp")

    comp_mult = spark.SparkCodeGen(comp_mult_dag)
    comp_mult.generate("comp_mult", "/tmp")

    simple_div = spark.SparkCodeGen(simple_div_dag)
    simple_div.generate("simple_div", "/tmp")

    comp_div = spark.SparkCodeGen(comp_div_dag)
    comp_div.generate("comp_div", "/tmp")

    create_mult = spark.SparkCodeGen(create_mult_dag)
    create_mult.generate("create_mult", "/tmp")

    print("Spark code generated in /tmp/")