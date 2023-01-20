.PHONY: setup
setup:
	@which python3
	python3 -m pip install virtualenv
	python3 -m virtualenv restpods-env
	./restpods-env/bin/pip install -r requirements.txt

.PHONY: install
install:
	@echo  "${PWD}/restpods-env/bin/python3 ${PWD}/src/restpods.py \$$@" > restpods
	@chmod +x restpods
	@cp restpods ${HOME}/bin/
	@echo "\nYou can add restpods to your path running"
	@echo "$$ export PATH="\$${PATH}:\$${HOME}/bin""
