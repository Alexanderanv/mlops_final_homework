# импортируем переменные окружения из .env файла
-include .env
export
# построение всего дерева зависимостей с учетом заданных в pyproject.toml ограничений
deps.lock:
	@uv lock --upgrade
# установка всего дерева зависимостей в соответствии с uv.lock файлом
dev.install:
	@uv sync --locked