import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int
from parser import parse
import history


class Compiler:
    def __init__(self, source):
        self.source = source
        self.parsed = parse(source)
        self.builder = []
        self.triple = llvm.get_default_triple()
        self.module = {}
        self.func = []
        self.f = {}
        self.block = []
        self.var = {}  # Needs to be made function unique

    def compile(self, node, module=None, name=""):
        print("--->", str(node))

        match node.type:
            case "PROGRAM":
                return self.compile(node.children[0], module=module)
            case "FUNCTIONS":
                for child in node.children:
                    self.compile(child, module=module)
            case "FUNCTION":
                fnty = ir.FunctionType(ir.IntType(32), [])
                self.func.append(ir.Function(module, fnty, name=node.leaf))
                self.f[node.leaf] = self.func[-1]
                self.compile(node.children[0], module=module)
            case "BLOCK":
                self.block.append(self.func[-1].append_basic_block())
                self.builder.append(ir.IRBuilder(self.block[-1]))
                self.compile(node.children[0], module=module)
                self.builder[-1].ret(
                    ir.Constant(ir.IntType(32), 33)
                )  # I need to find a way to find the last expression for return value
                self.builder.pop()
                self.block.pop()
            case "STATEMENTS":
                for child in node.children:
                    self.compile(child, module=module)
            case "STATEMENT":
                self.compile(node.children[0], module=module)
            case "VAR_DECLARE":
                self.var[node.leaf] = self.builder[-1].alloca(
                    ir.IntType(32), name=node.leaf
                )
                if len(node.children) > 0:
                    expr = self.compile(node.children[0], module=module)
                    self.builder[-1].store(expr, self.var[node.leaf])
            case "VAR_ASSIGN":
                expr = self.compile(node.children[0], module=module)
                self.builder[-1].store(expr, self.var[node.leaf])
                return expr
            case "PLUS":
                left = self.compile(node.children[0], module=module)
                right = self.compile(node.children[1], module=module)
                return self.builder[-1].add(left, right)
            case "MINUS":
                left = self.compile(node.children[0], module=module)
                right = self.compile(node.children[1], module=module)
                return self.builder[-1].sub(left, right)
            case "MULTIPLY":
                left = self.compile(node.children[0], module=module)
                right = self.compile(node.children[1], module=module)
                return self.builder[-1].mul(left, right)
            case "DIVIDE":
                left = self.compile(node.children[0], module=module)
                right = self.compile(node.children[1], module=module)
                return self.builder[-1].sdiv(left, right)
            case "TERM":
                return self.compile(node.children[0], module=module)
            case "FACTOR":
                return self.compile(node.children[0], module=module)
            case "EXPRESSION":
                return self.compile(node.children[0], module=module)
            case "FUNCTION_CALL":
                return self.builder[-1].call(self.f[node.leaf], [], tail="tail")
            case "NUMBER":
                # breakpoint()
                return ir.Constant(ir.IntType(32), int(node.leaf))

    def compile_module(self, parsed, name="main"):
        print(parsed)

        self.module[name] = ir.Module(name)
        self.compile(parsed, module=self.module[name])

        print(str(self.module[name]))
        with open(f"{name}.ll", "w") as f:
            f.write(str(self.module[name]))

    def run_module(self, name="main"):
        # Lets create an execution engine
        llvm.initialize()  # Initialize the llvm
        llvm.initialize_native_target()  # Initialize the native target
        llvm.initialize_native_asmprinter()  # Initialize the native asm printer
        # llvm.initialize_native_asmparser()  # Initialize the native asm parser if we want to support inline assembly

        llvm_parsed = llvm.parse_assembly(str(self.module[name]))  # Parse the module
        llvm_parsed.verify()  # Verify the module
        # print(llvm_parsed)  # Print the parsed module

        target_machine = llvm.Target.from_triple(
            self.triple
        ).create_target_machine()  # Create a target machine
        engine = llvm.create_mcjit_compiler(
            llvm_parsed, target_machine
        )  # Create a MCJIT compiler
        # engine.add_module(llvm_parsed)  # Add the module to the engine
        engine.finalize_object()  # Finalize the object
        engine.run_static_constructors()  # Run the static constructors

        func_ptr = engine.get_function_address(
            name
        )  # Get the function address, assuming the function name is the same as module name
        cfunc = CFUNCTYPE(c_int)(func_ptr)  # Create a cfunc
        print("result of execution", cfunc())  # Print the result of the cfunc


def main():
    while True:
        try:
            s = input("compile > ")
        except EOFError:
            break
        if not s:
            continue
        c = Compiler(s)
        c.compile_module(parse(s))
