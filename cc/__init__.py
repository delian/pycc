import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int

from parser import parse


def compile_module(parsed):
    print(parsed)

    builder = ir.IRBuilder()

    def compile(node):
        print("--->", str(node))
        match node.type:
            case "PLUS":
                left = compile(node.children[0])
                right = compile(node.children[1])
                return builder.add(left, right)
            case "MINUS":
                left = compile(node.children[0])
                right = compile(node.children[1])
                return builder.sub(left, right)
            case "MULTIPLY":
                left = compile(node.children[0])
                right = compile(node.children[1])
                return builder.mul(left, right)
            case "DIVIDE":
                left = compile(node.children[0])
                right = compile(node.children[1])
                return builder.sdiv(left, right)
            case "TERM":
                return compile(node.children[0])
            case "FACTOR":
                return compile(node.children[0])
            case "EXPRESSION":
                return compile(node.children[0])
            case "NUMBER":
                return ir.Constant(ir.IntType(32), int(node.leaf))
        return None

    triple = llvm.get_default_triple()  # Get the default triple

    module = ir.Module(
        "main"
    )  # Name of the module (we have only one module in this moment)
    # builder = ir.IRBuilder()  # Builder to create instructions
    #
    module.triple = triple

    fnty = ir.FunctionType(
        ir.IntType(32), []
    )  # Function type: int32_t foo(void), first is return type, second param is the input types
    func = ir.Function(module, fnty, name="main")  # Create a function named main

    block = func.append_basic_block("main_entry")  # Create a block in the function

    builder = ir.IRBuilder(block)  # Create a builder

    # Try to compile the module
    value = compile(parsed)
    # breakpoint()
    builder.ret(value)  # Return 33 as a test that the builder works

    # print(str(module))

    with open("out.ll", "w") as f:
        f.write(str(module))

    # Lets create an execution engine
    llvm.initialize()  # Initialize the llvm
    llvm.initialize_native_target()  # Initialize the native target
    llvm.initialize_native_asmprinter()  # Initialize the native asm printer
    # llvm.initialize_native_asmparser()  # Initialize the native asm parser if we want to support inline assembly

    llvm_parsed = llvm.parse_assembly(str(module))  # Parse the module
    llvm_parsed.verify()  # Verify the module
    print(llvm_parsed)  # Print the parsed module

    target_machine = llvm.Target.from_triple(
        triple
    ).create_target_machine()  # Create a target machine
    engine = llvm.create_mcjit_compiler(
        llvm_parsed, target_machine
    )  # Create a MCJIT compiler
    # engine.add_module(llvm_parsed)  # Add the module to the engine
    engine.finalize_object()  # Finalize the object
    engine.run_static_constructors()  # Run the static constructors

    func_ptr = engine.get_function_address("main")  # Get the function address
    cfunc = CFUNCTYPE(c_int)(func_ptr)  # Create a cfunc
    print("result of execution", cfunc())  # Print the result of the cfunc


def main():
    compile_module(parse("2*3+34-(23*2+1)"))
