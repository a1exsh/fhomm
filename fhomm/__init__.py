def asdict(m):
    return {
        k: asdict(v) if isinstance(v, dict) else v._asdict()
        for k, v in m.items()
    }
