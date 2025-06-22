#Remove-Item -force -recurse $PSScriptRoot/dist/
python -m build
python -m pip install build
$item = Get-item $PSSCriptRoot\dist\*.whl
pip install $item.FullName

