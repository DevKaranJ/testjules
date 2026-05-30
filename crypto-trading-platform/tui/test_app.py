from tui.app import run_app

def test_tui_app_import():
    # Simple test to verify import works
    assert callable(run_app)
