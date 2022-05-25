"""
channel access server with five PVs

    CPU = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')
    MEMORY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = 'GB')
    BATTERY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')
    TIME = pvproperty(value='time unknown', read_only = True, dtype = str)
    dt = pvproperty(value=1.0, precision = 3, units = 's')

"""

