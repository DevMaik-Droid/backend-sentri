

def limpiar_nulls(objeto):
    return [x.model_dump(exclude_none=True) for x in objeto]