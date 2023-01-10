from __future__ import absolute_import
import atpthings as atp
import panel as pn
import kds

from components.table import Measurements

pn.extension(sizing_mode="stretch_width")

# Load metadata
cfg = atp.dict.load("config/default.json")
metadata = atp.dict.list_to_dict(cfg["metadata"], key="name_id")

measurements = Measurements(metadata=metadata)

# Template
appName = "Measurements (development)"
panel_main = pn.template.BootstrapTemplate(title=appName)
# panel_main = kds.panel.KnaufTemplate(title=appName)
panel_main.main.append(measurements.view())


async def init():
    print("Init: Start.")
    measurements.fatch_data()
    print("Init: Done.")
    return


if __name__.startswith("bokeh"):
    pn.state.execute(init)
    panel_main.servable()
