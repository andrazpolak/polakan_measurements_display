import panel as pn
import pandas as pd
import kds
from bokeh.models.widgets.tables import NumberFormatter

import atpthings as atp


class Measurements:
    def __init__(self, metadata):

        self.metadata = metadata
        self.dataset = pd.DataFrame()
        self.panel = self._init_panel()
        self.dremio = kds.io.dremio.knauf_dremio_catalog()

    def _init_panel(self):
        self.button_refresh = pn.widgets.Button(name="Refresh", button_type="primary")
        self.button_refresh.on_click(self.fatch_data)

        # tabulator
        tabulator_formatters = {
            "fiberdiameter_mean": NumberFormatter(format="0.000"),
            "fiberdiameter_median": NumberFormatter(format="0.000"),
            "fiberdiameter_geometricmean": NumberFormatter(format="0.000"),
            "fiberdiameter_std": NumberFormatter(format="0.000"),
            "fiberdiameter_min": NumberFormatter(format="0.000"),
            "fiberdiameter_max": NumberFormatter(format="0.000"),
        }
        self.columns_rename = {
            "sample_id": "Sample ID",
            "measurement_id": "Measurement ID",
            "division": "Division",
            "plant": "Plant",
            "label": "Label",
            "fiberdiameter_mean": "Fiber diameter (mean) [μm]",
            "fiberdiameter_median": "Fiber diameter (median) [μm]",
            "fiberdiameter_geometricmean": "Fiber diameter (geometric mean) [μm]",
            "fiberdiameter_std": "Fiber diameter (std) [μm]",
            "fiberdiameter_min": "Fiber diameter (min) [μm]",
            "fiberdiameter_max": "Fiber diameter (max) [μm]",
            "fiberdiameter_count": "Fiber diameter (count) ",
        }
        columns_filters = {
            "sample_id": {"type": "input", "func": "like"},
            "division": {"type": "input", "func": "like"},
            "plant": {"type": "input", "func": "like"},
            "label": {"type": "input", "func": "like"},
        }

        self.tabulator_measurements = pn.widgets.Tabulator(
            self.dataset,
            # name="Measurements",
            configuration={
                "clipboard": True,
                "clipboardCopyHeader": True,
            },
            titles=self.columns_rename,
            formatters=tabulator_formatters,
            header_filters=columns_filters,
            # pagination="remote",
            # page_size=1,
            sorters=[
                # {"field": "sample_fiber_diameter_tag", "dir": "asc"},
                {"field": "sample_id", "dir": "asc"},
            ],
        )

        return pn.Column(self.button_refresh, self.tabulator_measurements)

    def fatch_data(self, event=None):
        sql_query = "SELECT * FROM MariaDB.dev_kds.fiberdiameter"
        self.dataset = self.dremio.create_source(sql_query).read()
        self.dataset.set_index("sample_id", inplace=True)

        # convert units
        const_m_to_um = 10**6
        dataset = self.dataset.copy()
        # dataset["fiberdiameter_min"] *= const_m_to_um
        # dataset["fiberdiameter_max"] *= const_m_to_um
        # dataset["fiberdiameter_std"] *= const_m_to_um
        dataset["fiberdiameter_mean"] *= const_m_to_um
        dataset["fiberdiameter_median"] *= const_m_to_um
        dataset["fiberdiameter_geometricmean"] *= const_m_to_um

        # write data to dataset
        self.tabulator_measurements.value = dataset
        self.tabulator_measurements.hidden_columns = list(
            set(self.dataset.columns)
            - set(atp.dict.get_keys_as_list(self.columns_rename))
        )
        print("Dataframe", self.dataset)
        return self

    def view(self):
        return self.panel
