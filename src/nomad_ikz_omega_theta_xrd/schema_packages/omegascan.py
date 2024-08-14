#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from datetime import datetime
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
import plotly.colors as pc
import plotly.graph_objects as go
from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.basesections import (
    Instrument,
    InstrumentReference,
    Measurement,
    MeasurementResult,
)
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import MEnum, Package, Quantity, Section, SubSection

from nomad_ikz_omega_theta_xrd.schema_packages.omegathetaxrdreader import (
    extract_data_and_metadata,
    extract_general_info,
    extract_parameter_list,
    extract_scan_data,
)
from nomad_ikz_omega_theta_xrd.schema_packages.utils import create_archive

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

m_package = Package(name='Omega Theta XRD')


class OmegaThetaXRDInstrument(Instrument, EntryData, ArchiveSection):
    """
    Class autogenerated from yaml schema.
    """

    m_def = Section()
    instrument_name = Quantity(
        type=str,
        description='Name of the instrument used.',
        default='Freiberger Omega Theta XRD',
    )
    lab_id = Quantity(
        type=str,
        description='Identifier for the instrument.',
        default='26-0019',
        label='serial_number',
    )


class OmegaThetaXRDInstrumentReference(InstrumentReference):
    """
    Class autogenerated from yaml schema.
    """

    m_def = Section()
    reference = Quantity(
        type=OmegaThetaXRDInstrument,
        a_eln={
            'component': 'ReferenceEditQuantity',
            'label': 'omega_theta_xrd_instrument',
        },
    )


class ScanCurve(PlotSection, ArchiveSection):
    """
    Class autogenerated from yaml schema.
    """

    m_def = Section()
    name = Quantity(
        type=str,
        description='L or R',
        a_eln={'component': 'StringEditQuantity'},
        name=None,
    )
    omega = Quantity(
        type=np.float64,
        description='Omega scan values',
        # a_eln={'component': 'NumberEditQuantity'},
        shape=['*'],
        unit='\u00b0',
    )
    intensity = Quantity(
        type=np.float64,
        description='Intensity values',
        # a_eln={'component': 'NumberEditQuantity'},
        shape=['*'],
        # unit='\u00b0',
        a_plot={'x': 'omega', 'y': 'intensity'},
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        The normalizer for the `ScanCurve` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        super().normalize(archive, logger)


class ParameterList(MeasurementResult, PlotSection, ArchiveSection):
    """
    Class autogenerated from yaml schema.
    """

    m_def = Section(
        a_eln=dict()
    )  # overview=True , put back if plot table is not looking good
    name = Quantity(
        type=str,
        description='Name of the scan generated from the X-Y position',
        a_eln={'component': 'StringEditQuantity'},
    )
    x_pos = Quantity(
        type=int,
        description='XPos',
        a_eln={'component': 'NumberEditQuantity'},
    )
    y_pos = Quantity(
        type=int,
        description='YPos',
        a_eln={'component': 'NumberEditQuantity'},
    )
    tilt = Quantity(
        type=np.float64,
        description='Tilt',
        a_eln={'component': 'NumberEditQuantity'},
        unit='\u00b0',
    )
    tilt_direction = Quantity(
        type=np.float64,
        description='Tilt direction',
        a_eln={'component': 'NumberEditQuantity'},
        unit='\u00b0',
    )
    component_0 = Quantity(
        type=np.float64,
        description='Component 0',
        a_eln={'component': 'NumberEditQuantity'},
        unit='\u00b0',
    )
    component_90 = Quantity(
        type=np.float64,
        description='Component 90',
        a_eln={'component': 'NumberEditQuantity'},
        unit='\u00b0',
    )
    reference_offset = Quantity(
        type=np.float64,
        description='Reference offset',
        a_eln={'component': 'NumberEditQuantity'},
        unit='\u00b0',
    )
    reference_axis = Quantity(
        type=str,
        description='Reference axis',
        a_eln={'component': 'StringEditQuantity'},
    )
    Scan_Curves = SubSection(
        section_def=ScanCurve,
        repeats=True,
    )

    # def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
    #     """
    #     The normalizer for the `ParameterList` class.

    #     Args:
    #         archive (EntryArchive): The archive containing the section that is being
    #         normalized.
    #         logger (BoundLogger): A structlog logger.
    #     """
    #     super().normalize(archive, logger)
    #     fig = go.Figure()
    #     fig.add_trace(
    #         go.Scatter(
    #             x=self.Scan_Curves[0].omega,
    #             y=self.Scan_Curves[0].intensity,
    #             mode='lines',
    #             name='Omega R',
    #         )
    #     )
    #     fig.add_trace(
    #         go.Scatter(
    #             x=self.Scan_Curves[1].omega,
    #             y=self.Scan_Curves[1].intensity,
    #             mode='lines',
    #             name='Omega L',
    #         )
    #     )

    #     fig.update_layout(
    #         height=400,
    #         width=716,
    #         title_text='Omega Theta XRD',
    #         showlegend=True,
    #         legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
    #     )
    #     # self.figures = []
    #     self.figures.append(PlotlyFigure(label='figure 2', figure=fig.to_plotly_json()))


class SampleSpecifications(ArchiveSection):
    m_def = Section(a_eln=dict(overview=True))
    sample_preparation_status = Quantity(
        type=str,
        description='Status of the sample preparation',
        a_eln={'component': 'StringEditQuantity'},
    )
    sample_side_facing_down = Quantity(
        type=MEnum(['Al unten', 'N unten']),
        description='sample surface facing downwards',
        a_eln={'component': 'EnumEditQuantity'},
    )


class OmegaThetaXRD(Measurement, PlotSection, EntryData, ArchiveSection):
    """
    Class autogenerated from yaml schema.
    """

    m_def = Section()
    scan_recipe_name = Quantity(
        type=str,
        description='Omega scan recipe name',
        a_eln={'component': 'StringEditQuantity'},
    )
    data_file = Quantity(
        type=str,
        description='Data file *.xrd containing the XRD data.',
        a_eln={'component': 'FileEditQuantity'},
    )
    # time_stamp = Quantity(
    #     type=Datetime,
    #     a_eln={'component': 'DateTimeEditQuantity'},
    # )
    measurement_type = Quantity(
        type=MEnum(['single measurement', 'mapping']),
        description='Type of the measurement',
        a_eln={'component': 'EnumEditQuantity'},
    )

    sample_specifications = SubSection(
        section_def=SampleSpecifications,
    )
    results = SubSection(
        section_def=ParameterList,
        repeats=True,
    )
    instruments = SubSection(
        section_def=OmegaThetaXRDInstrumentReference,
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        The normalizer for the `OmegaThetaXRD` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        super().normalize(archive, logger)

        if self.data_file is not None:
            # read_function = extract_data_and_metadata
            # write_function = self.get_write_functions()
            # if read_function is None or write_function is None:
            #     logger.warn(
            #         f'No compatible reader found for the file: "{self.data_file}".'
            #     )
            # else:
            with archive.m_context.raw_file(self.data_file) as file:
                xrd_dict = extract_data_and_metadata(file.name)
                #    raman_dict = read_function(file.name)  # , logger)
                # write_function(raman_dict, archive, logger)
                if (
                    extract_general_info(xrd_dict.get('Measurement', {}))['name']
                    != None
                ):
                    info_dict = extract_general_info(xrd_dict.get('Measurement', {}))
                    paramter_dict = extract_parameter_list(
                        xrd_dict.get('Measurement', {})
                    )
                    scan_dict = extract_scan_data(xrd_dict.get('Measurement', {}))

                    self.name = info_dict.get('name').split('_')[
                        0
                    ]  # should be original_name
                    self.lab_id = self.name
                    self.datetime = datetime.strptime(
                        info_dict.get('time_stamp'), '%m/%d/%Y %H:%M:%S'
                    )
                    self.scan_recipe_name = info_dict.get('scan_recipe_name')
                    self.measurement_type = 'single measurement'
                    results = ParameterList()
                    results.name = info_dict.get('name')
                    results.x_pos = int(paramter_dict.get('xpos'))
                    results.y_pos = int(paramter_dict.get('ypos'))
                    results.tilt = float(paramter_dict.get('tilt'))
                    results.tilt_direction = float(paramter_dict.get('tilt_direction'))
                    results.component_0 = float(paramter_dict.get('component_0'))
                    results.component_90 = float(paramter_dict.get('component_90'))
                    results.reference_offset = float(
                        paramter_dict.get('reference_offset')
                    )
                    results.reference_axis = paramter_dict.get('reference_axis')
                    scan_r = ScanCurve()
                    scan_r.name = scan_dict.get('scan_r').get('name')
                    scan_r.omega = scan_dict.get('scan_r').get('omega')
                    scan_r.intensity = scan_dict.get('scan_r').get('intensity')
                    scan_l = ScanCurve()
                    scan_l.name = scan_dict.get('scan_l').get('name')
                    scan_l.omega = scan_dict.get('scan_l').get('omega')
                    scan_l.intensity = scan_dict.get('scan_l').get('intensity')
                    results.Scan_Curves = [scan_r, scan_l]
                    # results.normalize(archive, logger)
                    self.results = [results]

                    xrdinstrumentref = OmegaThetaXRDInstrumentReference()
                    xrdinstrumentref.lab_id = info_dict.get('device_serial_no')
                    # xrdinstrumentref.normalize(archive, logger)
                    if xrdinstrumentref.reference is None:
                        xrdinstrument = OmegaThetaXRDInstrument(
                            lab_id=xrdinstrumentref.lab_id
                        )
                        #    self.instruments = [ramanspectrometer]

                        xrdinstrumentref.reference = create_archive(
                            xrdinstrument,
                            archive,
                            f'Freiberger_Omega_Theta_XRD_{xrdinstrumentref.lab_id}.archive.json',
                        )
                    self.instruments = [xrdinstrumentref]

                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=self.results[0].Scan_Curves[0].omega,
                            y=self.results[0].Scan_Curves[0].intensity,
                            mode='lines',
                            name='Omega R',
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=self.results[0].Scan_Curves[1].omega,
                            y=self.results[0].Scan_Curves[1].intensity,
                            mode='lines',
                            name='Omega L',
                        )
                    )

                    fig.update_layout(
                        height=400,
                        width=716,
                        title_text='Omega Theta XRD',
                        showlegend=True,
                        legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
                    )
                    self.results[0].figures = []
                    self.results[0].figures.append(
                        PlotlyFigure(label='Omega Scans', figure=fig.to_plotly_json())
                    )

                    fig_table = go.Figure(
                        data=[
                            go.Table(
                                columnwidth=[1, 1, 1, 1.5, 1.5, 1.5, 1.5, 1.5],
                                header=dict(
                                    values=[
                                        'X Pos.',
                                        'Y Pos.',
                                        'Tilt',
                                        'Tilt Direction',
                                        'Component 0',
                                        'Component 90',
                                        'Reference Offset',
                                        'Reference Axis',
                                    ],
                                    align='center',
                                ),
                                cells=dict(
                                    values=[
                                        self.results[0].x_pos,
                                        self.results[0].y_pos,
                                        f'{self.results[0].tilt.magnitude:.3f}',
                                        f'{self.results[0].tilt_direction.magnitude:.1f}',
                                        f'{self.results[0].component_0.magnitude:.3f}',
                                        f'{self.results[0].component_90.magnitude:.3f}',
                                        f'{self.results[0].reference_offset.magnitude:.3f}',
                                        self.results[0].reference_axis,
                                    ],
                                    align='center',
                                ),
                            )
                        ]
                    )
                    fig_table.update_layout(width=1000, height=200)
                    fig_table.update_layout(
                        margin=dict(
                            l=10, r=10, t=10, b=10
                        )  # Set left, right, top, bottom margins
                    )
                    self.figures = []
                    self.figures.append(
                        PlotlyFigure(label='Table', figure=fig_table.to_plotly_json())
                    )

                elif (
                    extract_general_info(xrd_dict.get('MultiMeasurement', {}))['name']
                    != None
                ):
                    info_dict = extract_general_info(
                        xrd_dict.get('MultiMeasurement', {})
                    )

                    self.name = info_dict.get('name').split('_')[0]
                    self.lab_id = self.name
                    self.datetime = datetime.strptime(
                        info_dict.get('time_stamp'), '%m/%d/%Y %H:%M:%S'
                    )
                    self.scan_recipe_name = info_dict.get('scan_recipe_name')
                    self.measurement_type = 'mapping'
                    for measurement in (
                        xrd_dict.get('MultiMeasurement', {})
                        .get('Measurements', {})
                        .get('Measurement')
                    ):
                        info_dict = extract_general_info(measurement)
                        paramter_dict = extract_parameter_list(measurement)
                        # scan_dict = extract_scan_data(measurement)
                        results = ParameterList()
                        results.name = info_dict.get('name')
                        results.x_pos = int(paramter_dict.get('xpos'))
                        results.y_pos = int(paramter_dict.get('ypos'))
                        results.tilt = float(paramter_dict.get('tilt'))
                        results.tilt_direction = float(
                            paramter_dict.get('tilt_direction')
                        )
                        results.component_0 = float(paramter_dict.get('component_0'))
                        results.component_90 = float(paramter_dict.get('component_90'))
                        results.reference_offset = float(
                            paramter_dict.get('reference_offset')
                        )
                        results.reference_axis = paramter_dict.get('reference_axis')
                        # # scan_r = ScanCurve()
                        # # scan_r.name = scan_dict.get('scan_r').get('name')
                        # # scan_r.omega = scan_dict.get('scan_r').get('omega')
                        # # scan_r.intensity = scan_dict.get('scan_r').get('intensity')
                        # # scan_l = ScanCurve()
                        # # scan_l.name = scan_dict.get('scan_l').get('name')
                        # # scan_l.omega = scan_dict.get('scan_l').get('omega')
                        # # scan_l.intensity = scan_dict.get('scan_l').get('intensity')
                        # # results.Scan_Curves = [scan_r, scan_l]
                        # results.normalize(archive, logger)
                        self.results.append(results)

                        xrdinstrumentref = OmegaThetaXRDInstrumentReference()
                        xrdinstrumentref.lab_id = info_dict.get('device_serial_no')
                        # xrdinstrumentref.normalize(archive, logger)
                        if xrdinstrumentref.reference is None:
                            xrdinstrument = OmegaThetaXRDInstrument(
                                lab_id=xrdinstrumentref.lab_id
                            )
                            #    self.instruments = [ramanspectrometer]

                            xrdinstrumentref.reference = create_archive(
                                xrdinstrument,
                                archive,
                                f'Freiberger_Omega_Theta_XRD_{xrdinstrumentref.lab_id}.archive.json',
                            )
                        self.instruments = [xrdinstrumentref]

                    if self.results != None:
                        # Extracting data for the plots
                        x_coords = [int(point['x_pos']) for point in self.results]
                        y_coords = [int(point['y_pos']) for point in self.results]
                        tilt_values = [
                            float(point['tilt'].magnitude) for point in self.results
                        ]
                        tilt_direction_values = [
                            float(point['tilt_direction'].magnitude)
                            for point in self.results
                        ]
                        component_0_values = [
                            float(point['component_0'].magnitude)
                            for point in self.results
                        ]
                        component_90_values = [
                            float(point['component_90'].magnitude)
                            for point in self.results
                        ]
                        reference_offset_values = [
                            float(point['reference_offset'].magnitude)
                            for point in self.results
                        ]
                        # Function to normalize values and map to colors

                        def get_colors(values):
                            norm = plt.Normalize(min(values), max(values))
                            cmap = plt.cm.viridis
                            return [cmap(norm(value)) for value in values]

                        # def get_colors_pl(values):
                        #     norm = plt.Normalize(min(values), max(values))
                        #     colorscale = pc.get_colorscale('balance')
                        #     return [
                        #         pc.find_intermediate_color(
                        #             colorscale, intermed=norm(value), colortype='rgb'
                        #         )
                        #         for value in values
                        #     ]
                        def get_colors_pl(values):
                            norm = plt.Normalize(min(values), max(values))
                            colorscale = pc.get_colorscale('Picnic')

                            def get_interpolated_color(value):
                                scaled_value = norm(value)

                                for i in range(1, len(colorscale)):
                                    low_pos, low_color = colorscale[i - 1]
                                    high_pos, high_color = colorscale[i]

                                    # Ensure positions are treated as floats
                                    low_pos = float(low_pos)
                                    high_pos = float(high_pos)

                                    if low_pos <= scaled_value <= high_pos:
                                        return pc.find_intermediate_color(
                                            lowcolor=low_color,
                                            highcolor=high_color,
                                            intermed=(scaled_value - low_pos)
                                            / (high_pos - low_pos),
                                            colortype='rgb',
                                        )

                                # Return the last color if value exceeds the colorscale range
                                return colorscale[-1][1]

                            return [get_interpolated_color(value) for value in values]

                        # Function to convert RGBA to hex
                        def rgba_to_hex(rgba):
                            return f'#{int(rgba[0]*255):02x}{int(rgba[1]*255):02x}{int(rgba[2]*255):02x}'

                        # Function to create a scatter plot with text annotations and color gradient boxes
                        def create_plot(x_coords, y_coords, values, title):
                            colors = get_colors_pl(values)
                            # hex_colors = [rgba_to_hex(color) for color in colors]

                            fig = go.Figure()

                            # Define the circle's center and radius
                            circle_center_x = sum(x_coords) / len(
                                x_coords
                            )  # Center of x_coords
                            circle_center_y = sum(y_coords) / len(
                                y_coords
                            )  # Center of y_coords
                            circle_radius = (
                                3
                                + max(
                                    max(x_coords) - min(x_coords),
                                    max(y_coords) - min(y_coords),
                                )
                                / 2
                            )

                            # Add the circle to the plot
                            fig.add_shape(
                                type='circle',
                                xref='x',
                                yref='y',
                                x0=circle_center_x - circle_radius,
                                y0=circle_center_y - circle_radius,
                                x1=circle_center_x + circle_radius,
                                y1=circle_center_y + circle_radius,
                                line=dict(color='darkgrey', width=2),
                                fillcolor='grey',
                                opacity=0.3,
                            )

                            for x, y, value, color in zip(
                                x_coords,
                                y_coords,
                                values,
                                colors,  # hex_colors
                            ):
                                if title == 'Tilt Direction':
                                    text_format = f'{float(value):.1f}'
                                else:
                                    text_format = f'{float(value):.3f}'

                                # Adding box around the text with color gradient
                                fig.add_shape(
                                    type='rect',
                                    x0=x - 1.5,
                                    y0=y - 1.5,
                                    x1=x + 1.5,
                                    y1=y + 1.5,
                                    line=dict(color=color, width=2),
                                    fillcolor=color,
                                    opacity=1,
                                )
                                # fig.add_trace(
                                #     go.Scatter(
                                #         x=[x],
                                #         y=[y],
                                #         mode='text',
                                #         # marker=dict(
                                #         #    size=0,
                                #         # ),
                                #         text=text_format,  # [f'{float(value):.3f}'],
                                #         textfont=dict(
                                #             size=12,  # Font size
                                #             color='black',  # Font color
                                #             family='Arial',  # Font family
                                #             weight='bold',  # Font weight for bold text
                                #         ),
                                #         textposition='middle center',
                                #         showlegend=False,
                                #     )
                                # )
                                # Add text annotation on top of the colored box
                                fig.add_annotation(
                                    x=x,
                                    y=y,
                                    text=text_format,
                                    showarrow=False,
                                    font=dict(color='black', size=12),
                                    xanchor='center',
                                    yanchor='middle',
                                )

                            # Add color bar
                            fig.add_trace(
                                go.Scatter(
                                    x=x_coords,
                                    y=y_coords,
                                    mode='markers',
                                    opacity=0,
                                    marker=dict(
                                        size=0,  # Hide the markers
                                        color=values,
                                        colorscale='Picnic',  # Choose a colorscale
                                        colorbar=dict(
                                            title='',
                                            titleside='right',
                                        ),
                                    ),
                                    showlegend=False,
                                )
                            )
                            fig.update_layout(
                                title=title,
                                xaxis_title='X Position',
                                yaxis_title='Y Position',
                                plot_bgcolor='white',
                                xaxis=dict(
                                    showgrid=True,
                                    zeroline=False,
                                    # scaleanchor='y',
                                    # scaleratio=1,
                                ),
                                yaxis=dict(
                                    showgrid=True,
                                    zeroline=False,
                                    scaleanchor='x',
                                    scaleratio=1,
                                ),
                            )
                            return fig

                        # Creating plots for each parameter
                        fig_tilt = create_plot(x_coords, y_coords, tilt_values, 'Tilt')
                        fig_tilt_direction = create_plot(
                            x_coords, y_coords, tilt_direction_values, 'Tilt Direction'
                        )
                        fig_component_0 = create_plot(
                            x_coords, y_coords, component_0_values, 'Component 0'
                        )
                        fig_component_90 = create_plot(
                            x_coords, y_coords, component_90_values, 'Component 90'
                        )
                        fig_reference_offset = create_plot(
                            x_coords,
                            y_coords,
                            reference_offset_values,
                            'Reference Offset',
                        )
                        # Displaying the plots
                        # fig_tilt.show()
                        # fig_tilt_direction.show()
                        # fig_component_0.show()
                        self.figures = []
                        self.figures.append(
                            PlotlyFigure(
                                label='tilt', index=1, figure=fig_tilt.to_plotly_json()
                            )
                        )
                        self.figures.append(
                            PlotlyFigure(
                                label='tilt direction',
                                index=2,
                                figure=fig_tilt_direction.to_plotly_json(),
                            )
                        )
                        self.figures.append(
                            PlotlyFigure(
                                label='component 0',
                                index=3,
                                figure=fig_component_0.to_plotly_json(),
                            )
                        )
                        self.figures.append(
                            PlotlyFigure(
                                label='component 90',
                                index=4,
                                figure=fig_component_90.to_plotly_json(),
                            )
                        )
                        self.figures.append(
                            PlotlyFigure(
                                label='reference offset',
                                index=5,
                                figure=fig_reference_offset.to_plotly_json(),
                            )
                        )

        if not self.results:
            return
        # figure1 = px.line(
        #     x=self.results[0].Scan_Curves[0].omega,
        #     y=self.results[0].Scan_Curves[0].intensity,
        #     title='Raman Spectrum',
        #     labels={
        #         'x': 'Wavenumber [1/cm]',
        #         'y': 'Intensity [a.u.]',
        #         'species': 'Species of Iris',
        #     },
        # )
        # self.figures.append(
        #     PlotlyFigure(label='figure 1', index=1, figure=figure1.to_plotly_json())
        # )


m_package.__init_metainfo__()
