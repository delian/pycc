import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int


def compile_module():
    module = ir.Module(
        "main"
    )  # Name of the module (we have only one module in this moment)
    # builder = ir.IRBuilder()  # Builder to create instructions

    fnty = ir.FunctionType(
        ir.IntType(32), []
    )  # Function type: int32_t foo(void), first is return type, second param is the input types
    func = ir.Function(module, fnty, name="main")  # Create a function named main

    block = func.append_basic_block("main_entry")  # Create a block in the function

    builder = ir.IRBuilder(block)  # Create a builder

    builder.ret(
        ir.Constant(ir.IntType(32), 33)
    )  # Return 33 as a test that the builder works

    triple = llvm.get_default_triple()  # Get the default triple
    # print(str(module))  # Print the module
    # print(str(triple))  # Check triple

    llvm.initialize()  # Initialize the llvm
    llvm.initialize_native_target()  # Initialize the native target
    llvm.initialize_native_asmprinter()  # Initialize the native asm printer
    llvm.initialize_native_asmparser()  # Initialize the native asm parser
    
    llvm_parsed = llvm.parse_assembly(str(module))  # Parse the module
    llvm_parsed.verify()  # Verify the module
    print(llvm_parsed)  # Print the parsed module
    
    target_machine = llvm.Target.from_triple(triple).create_target_machine()  # Create a target machine
    engine = llvm.create_mcjit_compiler(llvm_parsed, target_machine)  # Create a MCJIT compiler
    # engine.add_module(llvm_parsed)  # Add the module to the engine
    engine.finalize_object()  # Finalize the object
    engine.run_static_constructors()  # Run the static constructors
    
    func_ptr = engine.get_function_address("main")  # Get the function address
    cfunc = CFUNCTYPE(c_int)(func_ptr)  # Create a cfunc
    print(cfunc())  # Print the result of the cfunc
    

def main():
    compile_module()
