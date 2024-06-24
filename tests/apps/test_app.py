def test_importing_app():
    # this will raise an exception if pydantic model validation fails for th app
    from nomad_ikz_omega_theta_xrd.apps import myapp

    assert myapp.app.label == 'MyApp'

