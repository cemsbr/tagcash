update-deps:
	pip-compile -Uo requirements-dev.txt requirements-dev.in >/dev/null
	@sed -i -e 's/^-e file.*/-e ./' requirements-dev.txt
	git diff requirements-dev.txt
