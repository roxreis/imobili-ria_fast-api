import re
from typing import Union
from fastapi import HTTPException


def validate_cpf(cpf: str) -> bool:
    cpf = re.sub(r'[^0-9]', '', cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit1 = 0 if (sum1 % 11) < 2 else 11 - (sum1 % 11)

    if int(cpf[9]) != digit1:
        return False

    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit2 = 0 if (sum2 % 11) < 2 else 11 - (sum2 % 11)

    return int(cpf[10]) == digit2


def validate_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'[^0-9]', '', cnpj)

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
    digit1 = 0 if (sum1 % 11) < 2 else 11 - (sum1 % 11)

    if int(cnpj[12]) != digit1:
        return False

    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
    digit2 = 0 if (sum2 % 11) < 2 else 11 - (sum2 % 11)

    return int(cnpj[13]) == digit2


def validate_cpf_cnpj(cpf_cnpj: str) -> str:
    """
    Valida e formata CPF ou CNPJ
    Retorna o valor limpo ou levanta HTTPException
    """
    clean_value = re.sub(r'[^0-9]', '', cpf_cnpj)

    if len(clean_value) == 11:
        if not validate_cpf(clean_value):
            raise HTTPException(
                status_code=400,
                detail="CPF inválido"
            )
        return f"{clean_value[:3]}.{clean_value[3:6]}.{clean_value[6:9]}-{clean_value[9:]}"

    elif len(clean_value) == 14:
        if not validate_cnpj(clean_value):
            raise HTTPException(
                status_code=400,
                detail="CNPJ inválido"
            )
        return f"{clean_value[:2]}.{clean_value[2:5]}.{clean_value[5:8]}/{clean_value[8:12]}-{clean_value[12:]}"

    else:
        raise HTTPException(
            status_code=400,
            detail="CPF must have 11 digits or CNPJ must have 14 digits"
        )


def get_cpf_cnpj_type(cpf_cnpj: str) -> str:
    """Retorna se é 'cpf' ou 'cnpj'"""
    clean_value = re.sub(r'[^0-9]', '', cpf_cnpj)

    if len(clean_value) == 11:
        return "cpf"
    elif len(clean_value) == 14:
        return "cnpj"
    else:
        return "invalid"