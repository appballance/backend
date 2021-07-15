APIDOC_TITLE = "Projeto Balance"
APIDOC_DESCRIPTION = "Documentação do projeto Balance"

uninstall_all:
	@python -c "$$UNINSTALL_ALL_PYSCRIPT"

define UNINSTALL_ALL_PYSCRIPT
import os
req = 'requirements.txt'
for package in [x.split('==')[0] for x in open(req).read().split('\n')]:
	if package.strip():
		os.system('pip uninstall --yes %s' % package)

endef
export UNINSTALL_ALL_PYSCRIPT

run:
	@python -c "$$RUN_APP"

define RUN_APP
import os
os.system('uvicorn main:app --reload')

endef
export RUN_APP

run_dev: run

install_dev: uninstall_all
	pip install --upgrade pip
	pip install --no-cache-dir -r requirements_dev.txt
