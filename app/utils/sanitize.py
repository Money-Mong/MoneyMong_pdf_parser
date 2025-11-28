import numpy as np

def sanitize_metadata(obj):
    """
    JSON 직렬화가 가능한 타입만 남기기 위해
    numpy 타입(np.float32, np.int32 등)을 python float/int로 변환한다.
    """
    if isinstance(obj, dict):
        return {k: sanitize_metadata(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [sanitize_metadata(v) for v in obj]

    elif isinstance(obj, np.generic):   # numpy scalar (float32, int32 등)
        return obj.item()

    else:
        return obj