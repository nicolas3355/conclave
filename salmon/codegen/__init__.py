from salmon.dag import *

class CodeGenConfig:

    def __init__(self):
        self.inited = True
        self.delimiter = ','
        self.input_path = '/tmp'
        self.output_path = '/tmp'
        self.pid = 1

    def with_pid(self, pid):
        if not self.inited:
            self.__init__()
        self.sharemind_pid = pid

    def with_delimiter(self, delimiter):
        if not self.inited:
            self.__init__()
        self.delimiter = delimiter

    def from_dict(cfg):
        ccfg = CodeGenConfig()

        ccfg.delimiter = cfg['delimiter']
        ccfg.input_path = cfg['input_path']
        ccfg.output_path = cfg['output_path']

        ccfg.sharemind_pid = cfg['sharemind_pid']

        return ccfg


class CodeGen:

    # initialize code generator for DAG passed
    def __init__(self, config, dag):
        self.config = config
        self.dag = dag

    # generate code for the DAG stored
    def generate(self, job_name, output_directory):
        job, code = self._generate(job_name, output_directory)
        # store the code in type-specific files
        self._writeCode(code, output_directory, job_name)
        # return job object
        return job

    # generate code for the DAG stored
    def _generate(self, job_name, output_directory):
        op_code = ""

        # topological traversal
        nodes = self.dag.topSort()

        # for each op
        for node in nodes:
            if isinstance(node, Aggregate):
                op_code += self._generateAggregate(node)
            elif isinstance(node, Concat):
                op_code += self._generateConcat(node)
            elif isinstance(node, Create):
                op_code += self._generateCreate(node)
            elif isinstance(node, Close):
                op_code += self._generateClose(node)
            elif isinstance(node, IndexJoin):
                op_code += self._generateIndexJoin(node)
            elif isinstance(node, RevealJoin):
                op_code += self._generateRevealJoin(node)
            elif isinstance(node, HybridJoin):
                op_code += self._generateHybridJoin(node)
            elif isinstance(node, Join):
                op_code += self._generateJoin(node)
            elif isinstance(node, Open):
                op_code += self._generateOpen(node)
            elif isinstance(node, Filter):
                op_code += self._generateFilter(node)
            elif isinstance(node, Project):
                op_code += self._generateProject(node)
            elif isinstance(node, Persist):
                op_code += self._generatePersist(node)
            elif isinstance(node, Multiply):
                op_code += self._generateMultiply(node)
            elif isinstance(node, Divide):
                op_code += self._generateDivide(node)
            elif isinstance(node, Index):
                op_code += self._generateIndex(node)
            elif isinstance(node, Shuffle):
                op_code += self._generateShuffle(node)
            else:
                print("encountered unknown operator type", repr(node))

        # expand top-level job template and return code
        return self._generateJob(job_name, output_directory, op_code)

    def _writeCode(self, code, output_directory, job_name):

        # overridden in subclasses
        pass
