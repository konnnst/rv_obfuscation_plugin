## Модуль обфускации для архитектуры RISC-V
Зависит от https://gitlab.softcom.su/obfuscation/core-ng
## Использование
Предоставляет точку входа risc-v типа arch для ядра обфускатора
Для запуска обфускатора для платформы RISC-V требуется:
- Обновить setuptools
- Клонировать репозиторий с ядром обфускатора (`git clone https://gitlab.softcom.su/obfuscation/core-ng`)
- Клонировать репозиторий с плагином обфускатора (`git clone https://gitlab.softcom.su/obfuscation/risc-v`)
- В репозитории `core-ng` перейти на ветку, в которой ведётся работа с плагином (`git checkout 23-RISCV-arch-support`)
- Установить пакет с ядром обфускатора (`pip install core-ng`)
- В репозитории `risc-v` перейти на рабочую ветку ('git checkout working')
- Установить пакет с плагином обфускатора (`pip install risc-v`)
- Пример команды для запуска обфускатора для работы с файлом bubble.s (`obfuscator -t risc-v --linear-mix --max-ls-length 3 bubble.s`)
## Разработка
Для установки зависимости `obfuscator-core` необходимо 
- выпустить собственный токен доступа
- Установить последнюю версию зависимости командой `python -m pip install obfuscator-core --index-url https://__token__:<Токен доступа>@gitlab.softcom.su/api/v4/projects/480/packages/pypi/simple` либо расположить репозиторий с проектом core-ng и указать пути к нему в настройках рабочей области ("python.analysis.extraPaths")
## Тестирование
    - Разрешить зависимость core-ng одним из следующих сопособов:
        - установить `core-ng` в систему
        - указать расположение исходников проекта в файле `pytest.ini`
## Выгрузка изменений
После окончания работы перед снятием опции Draft MR рекомендуется запустить форматтер `black` (`python -m pip install black`) выполнив две команды
- `black src`
- `black tests`
