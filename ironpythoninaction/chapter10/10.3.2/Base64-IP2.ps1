$base_dir_env = Get-Item env:IP2ASSEMBLIES
$base_dir = $base_dir_env.Value
$first_path = Join-Path $base_dir 'Microsoft.Scripting.dll'
$second_path = Join-Path $base_dir 'IronPython.dll'
[reflection.assembly]::LoadFrom($first_path)
[reflection.assembly]::LoadFrom($second_path)

$engine = [ironpython.hosting.python]::CreateEngine()
$global:st = [microsoft.scripting.sourcecodekind]::Statements
$global:params = @('microsoft.scripting.hosting.scriptscope')

$global:scope = $engine.CreateScope()

$init_code = $engine.CreateScriptSourceFromString(@'
import sys
sys.path.append(r'c:\Python25\lib')
import base64
'@, $st)

$src = 'result = base64.b64encode(value)'
$global:encode =$engine.CreateScriptSourceFromString($src, $st)
$src = 'result = base64.b64decode(value)'
$global:decode =$engine.CreateScriptSourceFromString($src, $st)

./Invoke-GenericMethod $init_code 'Execute' $params $scope


Function global:B64Encode ($value){
  $scope.SetVariable('value', $value)
  ./Invoke-GenericMethod $encode 'Execute' $params $scope | out-null
  [Ref] $result = $null
  $scope.TryGetVariable('result', $result) | out-null
  $result.Value
}

Function global:B64Decode ($value){
  $scope.SetVariable('value', $value)
  ./Invoke-GenericMethod $decode 'Execute' $params $scope | out-null
  [Ref] $result = $null
  $scope.TryGetVariable('result', $result) | out-null
  $result.Value
}

