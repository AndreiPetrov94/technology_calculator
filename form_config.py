data_applicant = {
    "applicant_name": {
        "label": "Наименование заявителя:",
        "type": "entry"
    },
    "request_number": {
        "label": "Номер заявки ТП:",
        "type": "entry"
    },
    "request_date": {
        "label": "Дата заявки ТП:",
        "type": "date"
    },
    "object_address": {
        "label": "Адрес местоположения объекта ТП:",
        "type": "entry"
    }
}

data_connection_parameters = {
    "applicant_type": {
        "label": "Тип Заявителя",
        "type": "combobox",
        "values": [
            "Физическое лицо",
            "Юридическое лицо",
            "Индивидуальный предприниматель"
        ]
    },
    "location": {
        "label": "Расположение",
        "type": "combobox",
        "values": [
            "Город",
            "Поселок городского типа",
            "Сельская местность"
        ]
    },
    "power_prev": {
        "label": "Ранее присоединенная мощность, кВт",
        "type": "float_entry"
    },
    "power_new": {
        "label": "Присоединяемая мощность, кВт",
        "type": "float_entry"
    },
    "power_total": {
        "label": "Максимальная мощность, кВт",
        "type": "readonly"
    },
    "category_result": {
        "label": "Категория присоединения",
        "type": "readonly"
    },
    "voltage": {
        "label": "Напряжение",
        "type": "combobox",
        "values": [
            "0,4 кВ и ниже",
            "1-20 кВ"
        ]
    },
    "reliability_category": {
        "label": "Категория надежности",
        "type": "combobox",
        "values": [
            "I",
            "II",
            "III"
        ]
    },
    "distance": {
        "label": "Расстояние от границ участка заявителя до ближайшего объекта СО",
        "type": "combobox",
        "values": []  # будет заполняться динамически
    },
    "privileged_group": {
        "label": "Льготная группа заявителей (861 постановление п.17 абзацы 11-19)",
        "type": "combobox",
        "values": [
            "да",
            "нет"
        ]
    },
    "rate_option": {
        "label": "Выбор ставки C1.2.1 / C1.2.2",
        "type": "combobox",
        "values": [
            "C1.2.1 - выдача уведомления",
            "C1.2.2 - проверку выполнения ТУ"
        ]
    }
}
