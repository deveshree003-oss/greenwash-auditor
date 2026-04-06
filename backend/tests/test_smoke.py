def test_health_endpoint_importable():
    # import the backend main module to ensure package structure is importable
    import importlib
    m = importlib.import_module('backend.main')
    assert hasattr(m, 'app') or hasattr(m, 'health')
