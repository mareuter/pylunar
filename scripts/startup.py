from pylunar import MoonInfo
location = ((35, 58, 10), (-84, 19, 0))
obs_datetime = (2013, 10, 18, 22, 0, 0)
mi = MoonInfo(location[0], location[1])
mi.update(obs_datetime)
