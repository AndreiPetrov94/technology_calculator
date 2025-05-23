def validate_float(value):

    if value == "":
        return True
    try:
        val = float(value.replace(',', '.'))
        return 0 <= val <= 32000
    except ValueError:
        return False


def to_float(value):

    try:
        return float(value.replace(' ', '').replace(',', '.'))
    except (ValueError, AttributeError):
        return 0.0


def to_str(value, precision=2, grouping=False):
    """
    Преобразует float в строку с запятой (например, 1234.56 → '1 234,56').
    """
    s = f"{value:,.{precision}f}" if grouping else f"{value:.{precision}f}"
    return s.replace(',', ' ').replace('.', ',')
