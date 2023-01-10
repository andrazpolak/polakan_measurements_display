import atpthings as atp
import pandas as pd
import kds

print("_______________")
print("Script [start]:", __file__)
print("kds [Version]:", kds.__version__)
print("atpthings [Version]:", atp.__version__)
print("pandas [Version]:", pd.__version__)

dremio_catalog = kds.io.dremio.knauf_dremio_catalog()


sql_query = "SELECT * FROM MariaDB.dev_kds.fiberdiameter"
df = dremio_catalog.create_source(sql_query).read()
print("Dataframe", df)

print("Script [end]:", __file__)
print("_______________")
