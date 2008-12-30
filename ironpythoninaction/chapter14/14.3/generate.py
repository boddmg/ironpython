from System.Environment import CurrentDirectory
from System.IO import Path, Directory

from System.CodeDom import Compiler
from Microsoft.CSharp import CSharpCodeProvider
from Microsoft.VisualBasic import VBCodeProvider


def Generate(code, name, references=None, outputDir=None,
             inMemory=False, csharp=True):
    params = Compiler.CompilerParameters()

    if not inMemory:
        if outputDir is None:
            outputDir = Directory.GetCurrentDirectory()
        asmPath = Path.Combine(outputDir, name + '.dll')
        params.OutputAssembly = asmPath
        params.GenerateInMemory = False
    else:
        params.GenerateInMemory = True

    params.TreatWarningsAsErrors = False
    params.GenerateExecutable = False
    params.CompilerOptions = "/optimize"

    for reference in references or []:
        params.ReferencedAssemblies.Add(reference)

    if csharp:
        provider = CSharpCodeProvider()
    else:
        provider = VBCodeProvider()
    compile = provider.CompileAssemblyFromSource(params, code)

    if compile.Errors.HasErrors:
        errors = list(compile.Errors.List)
        raise Exception("Compile error: %r" % errors)

    if inMemory:
        return compile.CompiledAssembly
    return compile.PathToAssembly