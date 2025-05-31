.PHONY: setup venv install-env create-env runserver

# Instala el entorno y dependencias
setup: venv install-env create-env

# Crea entorno virtual
venv:
	@echo "🐍 Creando entorno virtual..."
	@python3 -m venv venv

# Activa el entorno e instala dependencias
install-env:
	@echo "📦 Instalando dependencias..."
	@venv/bin/pip install --upgrade pip
	@venv/bin/pip install -r requirements.txt

# Ejecutar el servidor Django
run:
	@venv/bin/python runner.py