$full_path = Resolve-Path $cur_dir 'IronPython.dll'
[reflection.assembly]::LoadFrom($full_path)

$engine = New-Object  IronPython.Hosting.PythonEngine
$engine.Execute("print 'Hello World! from IP1'")
