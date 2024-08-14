import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int

from distutils.command import build
from parser import parse


class Compiler:
    def __init__(self, source):
        self.source = source
        self.parsed = parse(source)
        self.builder = []
        self.triple = llvm.get_default_triple()
        self.module = {}
        self.func = []
        self.block = []
        self.var = {}  # Needs to be made function unique

    def compile(self, node, name=""):
        print("--->", str(node))

        match node.type:
            case "PROGRAM":
                return self.compile(node.children[0])
            case "FUNCTIONS":
                for child in node.children:
                    self.compile(child)
            case "FUNCTION":
                fnty = ir.FunctionType(ir.IntType(32), [])
                self.func.append(ir.Function(self.module, fnty, name=node.leaf))
                self.compile(node.children[0])
            case "BLOCK":
                self.block.append(self.func[-1].append_basic_block())
                self.builder.append(ir.IRBuilder(self.block[-1]))
                self.compile(node.children[0])
                self.builder[-1].ret(
                    ir.Constant(ir.IntType(32), 33)
                )  # I need to find a way to find the last expression for return value
                self.builder.pop()
                self.block.pop()
            case "STATEMENTS":
                for child in node.children:
                    self.compile(child)
            case "STATEMENT":
                self.compile(node.children[0])
            case "VAR_DECLARE":
                self.var[node.leaf] = self.builder[-1].alloca(
                    ir.IntType(32), name=node.leaf
                )
                self.compile(node.children[0])
            case "VAR_ASSIGN":
                self.builder[-1].store(
                    self.compile(node.children[0]), self.var[node.leaf]
                )
            case "PLUS":
                left = self.compile(node.children[0])
                right = self.compile(node.children[1])
                return self.builder[-1].add(left, right)
            case "MINUS":
                left = self.compile(node.children[0])
                right = self.compile(node.children[1])
                return self.builder[-1].sub(left, right)
            case "MULTIPLY":
                left = self.compile(node.children[0])
                right = self.compile(node.children[1])
                return self.builder[-1].mul(left, right)
            case "DIVIDE":
                left = self.compile(node.children[0])
                right = self.compile(node.children[1])
                return self.builder[-1].sdiv(left, right)
            case "TERM":
                return self.compile(node.children[0])
            case "FACTOR":
                return self.compile(node.children[0])
            case "EXPRESSION":
                return self.compile(node.children[0])
            case "NUMBER":
                return ir.Constant(ir.IntType(32), int(node.leaf))

    def compile_module(self, parsed, name="main"):
        print(parsed)

        self.module[name] = ir.Module(name)
        self.compile(parsed)

        print(str(self.module[name]))
        with open("name.ll", "w") as f:
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


s = "main() { a = 1 + 3 }"


def main():
    c = Compiler(s)
    c.compile_module
    c.compile_module(parse(s))
