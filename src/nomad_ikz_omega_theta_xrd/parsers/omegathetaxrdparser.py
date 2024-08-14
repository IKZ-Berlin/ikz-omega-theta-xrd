from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Quantity
from nomad.parsing.parser import MatchingParser

from nomad_ikz_omega_theta_xrd.schema_packages.omegascan import OmegaThetaXRD
from nomad_ikz_omega_theta_xrd.schema_packages.utils import create_archive

configuration = config.get_plugin_entry_point(
    'nomad_ikz_omega_theta_xrd.parsers:omegathetaxrdparser'
)


class RawFileOmegaThetaXRDData(EntryData):
    """
    Section for a Omega Theta XRD data file.
    """

    measurement = Quantity(
        type=OmegaThetaXRD,
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
        ),
    )


class OmegaThetaXRDParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        logger.info('OmegaThetaXRDParser.parse', parameter=configuration.parameter)
        data_file = mainfile.split('/')[-1]
        entry = OmegaThetaXRD()  # .m_from_dict(Ramanspectroscopy.m_def.a_template)
        entry.data_file = data_file
        entry.name = ''.join(data_file.split('.')[:-1])
        file_name = f'{"".join(data_file.split(".")[:-1])}.archive.json'
        archive.data = RawFileOmegaThetaXRDData(
            measurement=create_archive(entry, archive, file_name)
        )
        archive.metadata.entry_name = f'{data_file} data file'
