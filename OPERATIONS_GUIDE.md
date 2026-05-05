# Руководство по развертыванию кластера Corax

Данное руководство предназначено для специалистов, занимающихся развертыванием новых кластеров Corax. В нем пошагово описан процесс подготовки данных и запуска автоматизации.

---

## Предварительные требования

### Программное обеспечение

Для запуска автоматизации на управляющей машине должны быть установлены:

*   **Python 3.x** (библиотеки: `requests`, `pyyaml`, `ipaddress`).
*   **Ansible 2.10+** (коллекции: `community.general`, `ansible.posix`).
*   **Terraform 1.0+** (провайдер `cloudru/cloud` v2.0.0).
*   **Java 17 (OpenJDK)** (требуется для работы с `keytool` при генерации сертификатов).
*   **Системные утилиты**: `sshpass`, `jq`, `openssl`.

### Переменные окружения

Система требует установки ряда переменных для аутентификации в Cloud.Ru и FreeIPA. Рекомендуется экспортировать их перед началом работы:

```bash
# Cloud.Ru API Credentials
export TF_VAR_CLOUDRU_KEY_ID="ваш_key_id"
export TF_VAR_CLOUDRU_SECRET="ваш_secret"
export CLOUDRU_PROJECT_ID="id_проекта"

# Cloud.Ru Service URLs (примеры)
export CLOUDRU_COMPUTE_API_URL="https://compute.api.cloud.ru"
export CLOUDRU_VPC_API_URL="https://vpc.api.cloud.ru"
export CLOUDRU_IAM_API_URL="https://iam.api.cloud.ru"
# ... и остальные (см. ANSIBLE/roles/check_inventory/tasks/main.yaml)

# FreeIPA Credentials (для ввода в домен)
export IPA_ADDER="имя_пользователя_ipa"
export IPA_ADDER_PASSWORD="пароль_пользователя_ipa"
```

---

## Шаг 1: Подготовка данных в `INV/`

Это самый важный этап. Автоматизация считывает структуру каталогов и CSV-файлы в папке `INV/` для генерации инвентаря.

### 1.1. Создание структуры каталогов

Для нового кластера из 3 хостов создайте следующую иерархию:

```text
INV/
└── corax_<cluster_name>/          # Папка кластера (например, corax_prod)
    ├── kafka-<name>-01/           # Папка 1-го хоста
    │   ├── eth0.csv               # Настройки сети 1-го хоста
    │   └── ip                     # IP-адрес для управления (тот же, что в eth0.csv)
    ├── kafka-<name>-02/           # Папка 2-го хоста
    │   ├── eth0.csv
    │   └── ip
    └── kafka-<name>-03/           # Папка 3-го хоста
        ├── eth0.csv
        └── ip
```

### 1.2. Заполнение глобальных параметров (в корне `INV/`)

Убедитесь, что файлы в корне `INV/` содержат актуальные данные:

1.  **`vm_params.csv`**: Общие параметры ВМ.
    ```csv
    type,vm_params
    ogid,<имя_группы_в_облаке>
    project_id,<uuid_проекта>
    image_name,alt_10.2.1
    az,ru.AZ-3
    cpu,16
    ram,32
    hdd,50
    hdd_data,60
    hdd_data_device,/dev/vdb
    oversubscription,1:3
    service_id,<id_сервиса>
    cluster_type,kafka
    gis_code,<код_гис>
    stand_type,tech
    user,user1
    domain,your-domain.com
    dstr_path,/path/to/distributive/
    dstr_file,corax_fixed.tar.bz2
    ```

2.  **`net_params.csv`**: Сетевые подсети.
    ```csv
    type,net_params
    subnet,10.193.32.0/28
    gis_subnet,10.193.0.0/20
    ```

3.  **`ipa_params.csv`**: Домен FreeIPA.
    ```csv
    type,ipa_params
    domain,ipa-master-01.example.com
    ```

### 1.3. Заполнение данных хоста (в папке хоста)

Для каждого хоста (например, `INV/corax_prod/kafka-prod-01/`) создайте:

1.  **`ip`**: Текстовый файл, содержащий только IP-адрес хоста.
    *Пример:* `10.193.32.4`

2.  **`eth0.csv`**: Параметры сетевого интерфейса.
    ```csv
    type,interface
    ipaddr,10.193.32.4
    netmask,255.255.255.240
    gateway,1                  # 1 означает первый IP в подсети
    hosts,yes                  # Добавить запись в /etc/hosts
    route_target,oam           # Метка для маршрутов
    route_gateway,1            # Шлюз для статических маршрутов
    ```

---

## Шаг 2: Генерация инвентаря

После заполнения всех файлов в `INV/`, запустите скрипт для сборки `inventory.yaml`:

```bash
python3 ANSIBLE/ansible_prepare_021.py > inventory.yaml
```

*Проверьте созданный файл `inventory.yaml`, чтобы убедиться, что все хосты и переменные подтянулись корректно.*

---

## Шаг 3: Проверка и деплой

Запуск осуществляется через основной плейбук. Рекомендуется выполнять деплой поэтапно.

### 3.1. Создание инфраструктуры (Terraform)

На этом этапе создаются ВМ, диски и сети в Cloud.Ru.

```bash
ansible-playbook -i inventory.yaml ANSIBLE/playbook.yaml --tags tf_configs,tf
```

*   `tf_configs`: Генерирует `.tf` файлы на основе шаблонов.
*   `tf`: Запускает `terraform apply`.

### 3.2. Базовая настройка ОС и домена

Настройка дисков (LVM), установка базовых пакетов и ввод в FreeIPA.

```bash
ansible-playbook -i inventory.yaml ANSIBLE/playbook.yaml --tags os_config,ipadomain
```

*   `os_config`: Размечает диск данных (`hdd_data`) и монтирует его в `/pub`.
*   `ipadomain`: Регистрирует хост в FreeIPA и генерирует SSL-сертификаты (JKS).

### 3.3. Установка и настройка Corax

Распаковка дистрибутива и запуск сервисов Corax.

```bash
ansible-playbook -i inventory.yaml ANSIBLE/playbook.yaml --tags corax,corax_post
```

*   `corax`: Основная установка компонентов.
*   `corax_post`: Настройка мониторинга (JMX Exporter) и запуск служб.

---

## Полезные советы

*   **Логирование**: Если что-то пошло не так, проверьте вывод Ansible. Для повышения детализации используйте флаг `-vv`.
*   **Повторный запуск**: Большинство ролей идемпотентны. Вы можете запускать их повторно в случае сетевых сбоев.
*   **Доступ по SSH**: Убедитесь, что на управляющей машине настроен SSH-ключ, используемый для доступа к узлам. Путь к ключу настраивается в `ANSIBLE/ansible_prepare_021.py`.
