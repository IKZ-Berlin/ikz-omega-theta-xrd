from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class MyParserEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_ikz_omega_theta_xrd.parsers.myparser import MyParser

        return MyParser(**self.dict())


myparser = MyParserEntryPoint(
    name='MyParser',
    description='Parser defined using the new plugin mechanism.',
    mainfile_name_re='.*\.myparser',
)


class OmegaThetaXRDParserEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_ikz_omega_theta_xrd.parsers.omegathetaxrdparser import (
            OmegaThetaXRDParser,
        )

        return OmegaThetaXRDParser(**self.dict())


omegathetaxrdparser = OmegaThetaXRDParserEntryPoint(
    name='OmegaThetaXRDParser',
    description='Parser defined using the new plugin mechanism for *.xrd files from Freiberger Instruments.',
    mainfile_name_re='.*\.xrd',
)
