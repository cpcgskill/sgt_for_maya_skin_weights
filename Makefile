export MAYA_BIN = C:\Program Files\Autodesk\Maya2022\bin
export MAYA_PY = ${MAYA_BIN}/mayapy.exe

.PHONY: clean build docs install_package publish demo_thumbnail demo

clean:
	rm -rf "build"

docs: README.md
	pandoc -f markdown -t html README.md -o README.html --css=README.css --self-contained

build: clean docs
	echo "Build Start"
	mayapy -m pyeal build -cf pyeal_maya_plugin.json
	cp README.html ./build/out/README.html
	cp "sgtkey.txt" "./build/out/sgtkey.txt"
	echo "Build End"

install_package: build
	7z -tzip a ./build/new_sgt_beta.zip ./build/out/*

