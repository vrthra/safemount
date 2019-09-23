build:
	python3 setup.py bdist_wheel

upload:
	python -m twine upload dist/*

clean:
	rm -rf build
