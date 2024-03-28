pyinstaller -i HDZeroIcon.ico  hdzero_programmer.py
xcopy /E /I /Y "resource" "dist/hdzero_programmer/resource"
xcopy /E /I /Y "driver" "dist/hdzero_programmer/driver"