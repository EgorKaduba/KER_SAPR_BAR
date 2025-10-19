class DataValidator:
    @staticmethod
    def validate_bar_data(bar_data):
        """Валидация данных стержней"""
        errors = []
        if not bar_data:
            return ["Нет данных о стержнях"]

        for i, bar in enumerate(bar_data["info"]):
            # Проверка длины
            if "length" not in bar or bar["length"] <= 0:
                errors.append(f"Стержень {i + 1}: Длина должна быть больше 0")
            # Проверка площади сечения
            if "square" not in bar or bar["square"] <= 0:
                errors.append(f"Стержень {i + 1}: Площадь сечения должна быть больше 0")
            # Проверка модуля упругости
            if "modulus_elasticity" not in bar or bar["modulus_elasticity"] <= 0:
                errors.append(f"Стержень {i + 1}: Модуль упругости должен быть больше 0")
            # Проверка допускаемого напряжения
            if "voltage" not in bar or bar["voltage"] <= 0:
                errors.append(f"Стержень {i + 1}: Допускаемое напряжение должно быть больше 0")
        return errors

    @staticmethod
    def validate_loads_data(loads_data, bar_count, load_type="concentrated"):
        """Валидация данных нагрузок"""
        errors = []
        if not loads_data:
            return errors
        load_name = "сосредоточенной" if load_type == "concentrated" else "распределенной"
        for i, load in enumerate(loads_data["info"]):
            node_num = load.get("node_number")
            if node_num is None:
                errors.append(f"{load_name.capitalize()} нагрузка {i + 1}: Отсутствует номер узла")
            elif not isinstance(node_num, int) or node_num <= 0 or node_num > bar_count + 1:
                errors.append(
                    f"{load_name.capitalize()} нагрузка {i + 1}: Номер узла {node_num} не существует (должен быть от 1 до {bar_count + 1})")
            if "power" not in load:
                errors.append(f"{load_name.capitalize()} нагрузка {i + 1}: Отсутствует значение силы")

        return errors

    @staticmethod
    def validate_supports_data(supports_data):
        """Валидация данных заделок"""
        errors = []
        if not supports_data:
            return errors

        if "type" not in supports_data or supports_data["type"] != "supports":
            errors.append("Неверный тип данных заделок")

        if "left_support" not in supports_data or not isinstance(supports_data["left_support"], bool):
            errors.append("Неверное значение левой заделки")

        if "right_support" not in supports_data or not isinstance(supports_data["right_support"], bool):
            errors.append("Неверное значение правой заделки")

        return errors

    @staticmethod
    def validate_all_data(data_dict):
        """Полная валидация всех данных"""
        all_errors = []
        if "Objects" not in data_dict or len(data_dict["Objects"]) != 4:
            return ["Неверная структура файла проекта"]
        bar_data, concentrated_data, distributed_data, supports_data = data_dict["Objects"]
        bar_errors = DataValidator.validate_bar_data(bar_data)
        all_errors.extend(bar_errors)
        bar_count = bar_data["count"] if bar_data else 0
        if concentrated_data:
            concentrated_errors = DataValidator.validate_loads_data(concentrated_data, bar_count, "concentrated")
            all_errors.extend(concentrated_errors)
        if distributed_data:
            distributed_errors = DataValidator.validate_loads_data(distributed_data, bar_count, "distributed")
            all_errors.extend(distributed_errors)
        supports_errors = DataValidator.validate_supports_data(supports_data)
        all_errors.extend(supports_errors)
        return all_errors