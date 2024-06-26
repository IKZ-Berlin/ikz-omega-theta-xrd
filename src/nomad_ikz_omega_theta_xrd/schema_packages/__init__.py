from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class MySchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_ikz_omega_theta_xrd.schema_packages.mypackage import m_package

        return m_package


mypackage = MySchemaPackageEntryPoint(
    name='MyPackage',
    description='Schema package defined using the new plugin mechanism.',
)


class OmegaThetaXRDPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_ikz_omega_theta_xrd.schema_packages.omegascan import m_package

        return m_package


omegascan = OmegaThetaXRDPackageEntryPoint(
    name='OmegaScan',
    description='Omega Theta Scan XRD.',
)
