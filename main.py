import math
import random
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

units_name = {
	0: "Metric",
	1: "Imperial"
}

def roll(sides):
	return random.randint(1, sides)

month_name = {
	0: "Núzyæl",
	1: "Peónu",
	2: "Kelén",
	3: "Nólus", 
	4: "Laránè",
	5: "Ágrazhâr",
	6: "Azúra",
	7: "Halánè",
	8: "Savôr",
	9: "Ilvín",
	10: "Návek",
	11: "Morgát"
}

season_name = [ "Spring", "Summer", "Autumn", "Winter" ]

def get_season(month):
	i = 0
	if month <= 3:
		i = 0
	elif month <= 6:
		i = 1
	elif month <= 9:
		i = 2
	else:
		i = 3

	return i

def get_season_exact(day, month):
	if (month == 10 and day > 15) or month == 11 or month == 0 or (month == 1 and day <= 15):
		return 0
	elif (month == 1 and day > 15) or month == 2 or month == 3 or (month == 4 and day <= 15):
		return 1
	elif (month == 4 and day > 15) or month == 5 or month == 6 or (month == 7 and day <= 15):
		return 2
	else:
		return 3

moon_phase_name = {
	0: "🌑︎ New",
	1: "🌒︎ Waxing crecent",
	2: "🌓︎ First quater",
	3: "🌔︎ Waxing bibbous",
	4: "🌕︎ Full",
	5: "🌖︎ Waning crecent",
	6: "🌗︎ Last quater",
	7: "🌘︎ Waning bibbous"
}

def get_moon_phase(day):
	fracture = 100 / 15
	visibility = 0
	phase = 0

	if day < 15:
		visibility = int(day * fracture)
	elif day > 15:
		visibility = int(100 - ((day - 15) * fracture))

	if day < 5:
		return 1, visibility
	elif day < 10:
		return 2, visibility
	elif day < 15:
		return 3, visibility
	elif day == 15:
		return 4, 100
	elif day < 20:
		return 5, visibility
	elif day < 25:
		return 6, visibility
	elif day < 30:
		return 7, visibility
	elif day == 30:
		return 0, 0

def get_moon_phase_string(day):
	moon = get_moon_phase(day)

	return f'{moon_phase_name[moon[0]]} ({moon[1]}%)'

latitude_name = { 0: "Polar", 1: "High", 2: "Mid", 3: "Low" }

daylight_name = { 0: "Night", 1: "Twilight", 2: "Day", 3: "Twilight"}

daylight_hours = [
	[
		[ 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1 ],
		[ 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0 ]
	],
	[
		[ 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0 ]
	],
	[
		[ 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0 ]
	],
	[
		[ 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0 ]
	]
]

daylight_hours = [
	[ "00001122222222222330000", "11122222222222222222333", "00001122222222222330000", "00000001122222230000000" ],
	[ "00000122222222222300000", "00012222222222222223000", "00000122222222222300000", "00000001222222230000000" ],
	[ "00000122222222222300000", "00001222222222222230000", "00000122222222222300000", "00000012222222223000000" ],
	[ "00000022222222222000000", "00000022222222222000000", "00000022222222222000000", "00000022222222222000000" ]
]

def find_first_last(string, substring):
	first = string.find(substring)
	last = string.rfind(substring)

	if first == -1:
		return None, None

	return first, last

def find_first(string, substring):
	first = -1
	last = -1

	i = 0

	while i <= len(string) - len(substring):
		if string[i:i + len(substring)] == substring:
			if first == -1:
				first = i

			last = i

			i += len(substring)
		else:
			if not first == -1:
				break

			i += 1

	if first == -1 or last == -1:
		return None, None

	return first, last

def get_daylight(latitude, season, hour):
	return daylight[int(daylight_hours[latitude][season][hour - 1])]

def is_day(latitude, season, hour):
	return False if daylight_hours[latitude][season][hour - 1] == '2' else True

def get_dawn(latitude, season):
	string = daylight_hours[latitude][season]
	start, end = find_first(string, "1")

	if start == None or end == None:
		return None, None, 0

	length = (end + 1) - start

	return start + 1, end + 1, length

def get_dawn_string(latitude, season):
	dawn = get_dawn(latitude, season)

	if dawn[0] == None or dawn[1] == None:
		return f'Dawn: -'
	else:
		return f'Dawn: {str(dawn[0]).zfill(2)}:00'

def get_dusk(latitude, season):
	string = daylight_hours[latitude][season]
	start, end = find_first(string, "3")

	if start == None or end == None:
		return None, None, 0

	length = (end + 1) - start

	return start + 2, end + 2, length

def get_dusk_string(latitude, season):
	dusk = get_dusk(latitude, season)

	if dusk[0] == None or dusk[1] == None:
		return f'Dusk: -'
	else:
		return f'Dusk: {str(dusk[0]).zfill(2)}:00'

def get_day(latitude, season):
	string = daylight_hours[latitude][season]
	start, end = find_first_last(string, "2")

	if start == None or end == None:
		return None, None, 0

	length = string.count('2')

	return start + 1, end + 2, length

def get_day_string(latitude, season):
	day = get_day(latitude, season)

	if day[0] == None or day[1] == None:
		return f'Day: -'
	else:
		return f'Day: {str(day[0]).zfill(2)}:00'

def get_night(latitude, season):
	string = daylight_hours[latitude][season]
	length = string.count('0')

	if length == 0:
		return None, None, length

	dusk = get_dusk(latitude, season)
	dawn = get_dawn(latitude, season)
	day = get_day(latitude, season)

	start = day[1] + 1 if dusk[2] == 0 else dusk[1] + 1
	end = day[0] - 1 if dawn[2] == 0 else dawn[0] + 1

	return start, end, length

def get_night_string(latitude, season):
	night = get_night(latitude, season)

	if night[0] == None or night[1] == None:
		return f'Night: -'
	else:
		return f'Night: {str(night[0]).zfill(2)}:00'

wind_direction = [ "NW", "N", "NE", "SE", "S", "SW", "W" ]

wind_force = [ "Calm or light breeze", "Moderate breeze", "Strong wind", "Gale", "Storm" ]

wind_force_values = [
	[ "0-8 km/h", "8-24 km/h", "24-48 km/h", "48-88 km/h", ">88 km/h" ],
	[ "0-5 mph", "5-15 mph", "15-30 mph", "30-55 mph", ">55 mph" ]
]

def get_wind_force(force, is_foggy, units):
	wf = get_actual_wind_force(force) if not is_foggy else 0

	return f'{wind_force[wf]} at {wind_force_values[units][wf]}'

def get_actual_wind_force(value):
	r = roll(10)

	if value == 0:
		if r <= 4:
			return 0
		elif r <= 8:
			return 1
		else:
			return 2
	elif value == 1:
		if r <= 5:
			return 1
		elif r <= 8:
			return 2
		else:
			return 3
	else:
		if r <= 6:
			return 2
		elif r <= 9:
			return 3
		else:
			return 4

cloud_precipitation = [ "Clear and dry", "Cloudy but dry", "Cloudy with showers", "Overcast but dry", "Overcast with snow or hail showers", "Overcast with continuous snow", "Overcast with showers", "Overcast with continuous rain", "Foggy or misty", "Cloudy with thunderstorm" ]

subjective_temperature = [ "Sweltering", "Hot", "Warm", "Cool", "Cold", "Freezing" ]

subjective_temperature_values = [
	[ ">35°C", "26°C-35°C", "16°C-25°C", "10°C-15°C", "1°C-10°C", "≤0°C" ],
	[ ">95°F", "79°F-95°F", "61°F-77°F", "50°F-59°F", "34°F-50°F", "≤32°F" ]
]

def get_subjective_temperature(temperature, units):
	return f'{subjective_temperature[temperature]} at {subjective_temperature_values[units][temperature]}'

def get_weather_hazard(temperature):
	return subjective_temperature[temperature] in {"Sweltering", "Hot", "Freezing"}

climate_zone = {
	0: "Subpolar",
	1: "Cool Temperate",
	2: "Warm Temperate",
	3: "Subtropical",
	4: "Tropical (Dry)",
	5: "Tropical (Wet)",
	6: "Ázadmêre, Hârn",
	7: "Énselet, Shôrkýne",
	8: "Isýnen, Northern Hèpekéria",
	9: "Ubárian, Central Tríerzòn"
}

climate_zone_start = {
	0: [ 16, 6, 8, 1 ],
	1: [ 16, 9, 17, 19 ],
	2: [ 7, 15, 17, 19 ],
	3: [ 4, 14, 10, 19 ],
	4: [ 11, 10, 1, 8 ],
	5: [ 8, 6, 8, 9 ],
	6: [ 8, 9, 8, 8 ],
	7: [ 9, 16, 1, 8 ],
	8: [ 3, 3, 1, 8 ],
	9: [ 7, 4, 17, 19 ]
}

def get_weather_index_start(climate_zone, season):
	r = roll(100)

	return climate_zone_start[climate_zone][season] if r <= 50 else roll(20)

def get_weather_index_change(index, dice):
	r = roll(dice)
	m = 0

	if r == 1:
		m = 1
	elif r == 2:
		m = -2
	elif r <= 4:
		m = -1
	else:
		m = 0

	index = 1 + ((index + m) - 1) % (20 - 1)

	return index

class weather:
	subjective_temperature = []
	cloud_precipitation = 0
	wind_direction = 0
	wind_force = 0
	change = 0

	def __init__(self, subjective_temperature_day, subjective_temperature_night, wind_direction, wind_force, cloud_precipitation, change):
		self.subjective_temperature = [subjective_temperature_day, subjective_temperature_night]
		self.wind_direction = wind_direction
		self.wind_force = wind_force
		self.cloud_precipitation = cloud_precipitation
		self.change = change

weather_chart = [
	[
		[ weather(4, 5, 1, 1, 4, 4), weather(3, 4, 2, 1, 1, 4), weather(2, 3, 3, 0, 0, 8), weather(3, 3, 5, 1, 1, 10), weather(4, 4, 0, 2, 4, 4), weather(4, 5, 0, 2, 2, 4), weather(4, 5, 5, 2, 0, 8), weather(3, 4, 5, 1, 0, 10), weather(4, 5, 0, 1, 0, 8), weather(5, 5, 1, 0, 8, 8), weather(4, 5, 1, 1, 1, 6), weather(3, 5, 2, 1, 6, 4), weather(2, 3, 3, 0, 2, 6), weather(2, 3, 4, 0, 6, 8), weather(2, 3, 4, 0, 2, 8), weather(3, 4, 5, 0, 0, 12), weather(3, 4, 5, 2, 6, 6), weather(4, 5, 5, 2, 2, 6), weather(4, 5, 0, 2, 0, 6), weather(4, 4, 0, 1, 1, 8) ],
		[ weather(3, 4, 1, 0, 0, 8), weather(2, 3, 2, 0, 0, 6), weather(1, 2, 3, 0, 0, 8), weather(2, 2, 4, 0, 6, 8), weather(3, 3, 5, 0, 2, 10), weather(3, 3, 4, 0, 0, 10), weather(3, 3, 5, 1, 0, 10), weather(2, 3, 0, 2, 6, 4), weather(3, 3, 5, 1, 1, 10), weather(2, 3, 0, 1, 0, 8), weather(2, 4, 1, 1, 2, 4), weather(3, 4, 2, 0, 6, 4), weather(2, 3, 3, 0, 2, 6), weather(1, 3, 4, 0, 1, 10), weather(2, 2, 5, 1, 6, 8), weather(2, 3, 4, 0, 2, 8), weather(3, 3, 5, 2, 1, 8), weather(3, 3, 5, 1, 0, 10), weather(3, 4, 5, 1, 0, 10), weather(4, 4, 0, 0, 2, 8) ],
		[ weather(3, 5, 1, 0, 1, 8), weather(3, 4, 1, 0, 6, 6), weather(2, 3, 2, 0, 2, 4), weather(1, 3, 3, 0, 0, 8), weather(2, 3, 4, 0, 8, 10), weather(2, 3, 5, 0, 6, 10), weather(3, 4, 0, 1, 0, 8), weather(3, 3, 5, 1, 3, 10), weather(4, 4, 0, 2, 4, 4), weather(4, 4, 0, 1, 1, 8), weather(4, 5, 1, 2, 0, 4), weather(3, 4, 2, 1, 1, 4), weather(2, 3, 3, 0, 2, 6), weather(3, 3, 4, 1, 2, 6), weather(3, 4, 5, 2, 6, 6), weather(3, 3, 4, 1, 6, 6), weather(2, 3, 5, 1, 0, 10), weather(3, 4, 0, 2, 2, 4), weather(4, 5, 5, 2, 3, 8), weather(5, 5, 0, 1, 1, 8) ],
		[ weather(4, 5, 1, 0, 2, 10), weather(5, 5, 0, 1, 0, 8), weather(5, 5, 1, 2, 0, 8), weather(4, 5, 2, 1, 2, 6), weather(5, 5, 3, 0, 8, 8), weather(4, 5, 4, 0, 2, 4), weather(3, 4, 5, 1, 0, 6), weather(4, 5, 0, 0, 2, 8), weather(4, 5, 1, 1, 4, 8), weather(4, 5, 2, 1, 1, 8), weather(4, 5, 3, 2, 4, 4), weather(5, 5, 2, 1, 0, 8), weather(4, 5, 2, 2, 5, 4), weather(4, 5, 3, 1, 2, 4), weather(3, 4, 4, 1, 0, 4), weather(2, 3, 5, 2, 0, 4), weather(3, 4, 4, 1, 2, 4), weather(3, 4, 5, 2, 6, 4), weather(4, 5, 5, 1, 4, 4), weather(4, 5, 0, 1, 5, 4) ]
	],
	[
		[ weather(4, 4, 1, 1, 4, 4), weather(3, 3, 2, 1, 1, 4), weather(2, 3, 0, 3, 8, 8), weather(2, 2, 4, 1, 1, 8), weather(3, 3, 5, 2, 6, 6), weather(4, 4, 0, 2, 4, 4), weather(4, 5, 5, 1, 1, 10), weather(3, 3, 5, 1, 2, 8), weather(4, 4, 0, 1, 1, 8), weather(5, 5, 1, 0, 1, 8), weather(4, 5, 1, 1, 0, 6), weather(3, 5, 2, 1, 6, 4), weather(2, 3, 3, 0, 6, 6), weather(1, 2, 4, 0, 8, 10), weather(2, 2, 4, 0, 9, 6), weather(3, 4, 5, 0, 0, 12), weather(3, 3, 3, 1, 2, 4), weather(3, 3, 5, 2, 7, 4), weather(4, 4, 0, 2, 4, 4), weather(4, 4, 0, 1, 4, 6) ],
		[ weather(3, 3, 1, 0, 2, 6), weather(2, 2, 2, 0, 2, 4), weather(1, 3, 3, 0, 0, 8), weather(1, 2, 4, 0, 0, 10), weather(2, 2, 5, 0, 9, 8), weather(2, 3, 5, 0, 2, 8), weather(3, 3, 5, 1, 6, 8), weather(3, 3, 0, 2, 6, 4), weather(2, 3, 5, 1, 1, 10), weather(2, 3, 0, 1, 0, 8), weather(2, 3, 1, 1, 0, 6), weather(1, 3, 2, 0, 8, 6), weather(1, 2, 3, 0, 6, 6), weather(1, 2, 3, 0, 1, 8), weather(2, 2, 4, 0, 1, 10), weather(2, 3, 5, 1, 1, 10), weather(2, 2, 0, 2, 6, 4), weather(3, 3, 5, 1, 6, 8), weather(3, 3, 0, 1, 6, 6), weather(3, 3, 1, 0, 3, 8) ],
		[ weather(3, 4, 1, 0, 8, 8), weather(3, 4, 1, 0, 2, 6), weather(2, 3, 2, 0, 8, 6), weather(1, 3, 3, 0, 2, 6), weather(1, 3, 4, 0, 8, 10), weather(2, 3, 5, 0, 9, 8), weather(3, 3, 0, 1, 7, 4), weather(3, 3, 5, 1, 6, 8), weather(3, 4, 0, 2, 3, 6), weather(4, 4, 1, 1, 1, 6), weather(4, 4, 2, 2, 4, 4), weather(3, 4, 3, 1, 6, 4), weather(2, 3, 3, 0, 1, 8), weather(3, 3, 4, 1, 7, 4), weather(3, 3, 5, 2, 6, 6), weather(3, 4, 4, 1, 1, 8), weather(2, 4, 5, 1, 0, 10), weather(3, 4, 0, 2, 1, 6), weather(4, 5, 5, 2, 4, 6), weather(5, 5, 0, 1, 1, 8) ],
		[ weather(4, 5, 1, 0, 5, 4), weather(5, 5, 1, 1, 3, 6), weather(4, 4, 2, 2, 4, 4), weather(3, 4, 3, 1, 2, 4), weather(2, 4, 3, 0, 8, 8), weather(3, 4, 4, 0, 2, 8), weather(3, 4, 5, 1, 7, 6), weather(4, 4, 0, 0, 3, 10), weather(3, 3, 5, 1, 6, 8), weather(4, 4, 0, 1, 4, 6), weather(4, 4, 1, 2, 3, 4), weather(5, 5, 2, 2, 4, 4), weather(3, 5, 3, 1, 0, 6), weather(3, 4, 4, 1, 1, 8), weather(3, 5, 4, 1, 0, 8), weather(3, 4, 5, 2, 2, 6), weather(4, 5, 0, 1, 4, 6), weather(4, 4, 5, 2, 4, 6), weather(4, 4, 5, 1, 1, 10), weather(4, 4, 0, 1, 2, 6) ]
	],
	[
		[ weather(3, 3, 1, 1, 6, 4), weather(3, 3, 2, 1, 2, 4), weather(2, 3, 3, 0, 8, 8), weather(2, 2, 4, 1, 1, 8), weather(3, 3, 5, 2, 6, 6), weather(4, 4, 0, 2, 3, 6), weather(3, 3, 5, 1, 1, 10), weather(3, 3, 5, 1, 2, 8), weather(4, 4, 0, 1, 2, 6), weather(3, 3, 1, 0, 1, 8), weather(4, 4, 1, 1, 0, 6), weather(3, 4, 2, 1, 1, 4), weather(2, 3, 3, 0, 8, 8), weather(1, 2, 4, 0, 8, 10), weather(2, 2, 4, 0, 9, 6), weather(3, 4, 5, 0, 0, 12), weather(3, 3, 3, 1, 2, 4), weather(3, 3, 5, 2, 7, 4), weather(3, 3, 0, 2, 2, 4), weather(3, 3, 0, 1, 6, 6) ],
		[ weather(3, 3, 2, 0, 2, 6), weather(2, 2, 1, 0, 1, 6), weather(1, 3, 2, 0, 0, 8), weather(1, 2, 3, 0, 0, 10), weather(2, 2, 4, 1, 6, 8), weather(2, 3, 5, 0, 1, 10), weather(2, 2, 3, 1, 9, 4), weather(1, 1, 4, 0, 3, 12), weather(2, 2, 5, 0, 2, 8), weather(1, 2, 0, 1, 0, 6), weather(2, 3, 1, 0, 0, 6), weather(1, 3, 2, 0, 8, 8), weather(2, 2, 2, 1, 6, 4), weather(0, 2, 3, 0, 0, 10), weather(1, 1, 4, 0, 1, 12), weather(2, 2, 5, 2, 2, 4), weather(2, 2, 0, 1, 1, 6), weather(1, 2, 1, 0, 1, 6), weather(3, 3, 0, 0, 6, 6), weather(3, 3, 1, 0, 6, 4) ],
		[ weather(2, 3, 1, 0, 8, 8), weather(2, 2, 1, 0, 2, 6), weather(2, 3, 2, 0, 8, 6), weather(1, 2, 3, 0, 8, 8), weather(1, 2, 4, 0, 6, 8), weather(2, 2, 5, 0, 9, 8), weather(2, 2, 0, 1, 3, 8), weather(2, 2, 5, 1, 6, 8), weather(2, 3, 0, 2, 7, 4), weather(3, 3, 1, 1, 3, 6), weather(3, 3, 2, 2, 6, 4), weather(3, 3, 3, 1, 6, 4), weather(2, 3, 3, 0, 1, 8), weather(3, 3, 4, 1, 7, 4), weather(3, 3, 5, 2, 3, 8), weather(2, 3, 4, 1, 2, 6), weather(2, 3, 5, 1, 0, 10), weather(3, 4, 0, 2, 1, 6), weather(3, 3, 5, 2, 6, 6), weather(4, 4, 0, 1, 1, 8) ],
		[ weather(4, 4, 1, 0, 4, 6), weather(4, 4, 1, 1, 4, 4), weather(4, 4, 2, 2, 4, 4), weather(3, 4, 3, 1, 2, 4), weather(3, 4, 3, 0, 8, 8), weather(3, 5, 4, 0, 2, 8), weather(3, 3, 5, 1, 7, 6), weather(3, 3, 0, 0, 3, 10), weather(2, 2, 5, 1, 6, 8), weather(3, 3, 0, 1, 7, 4), weather(3, 3, 1, 2, 6, 4), weather(4, 4, 2, 2, 3, 4), weather(3, 5, 3, 1, 0, 6), weather(3, 4, 4, 1, 2, 6), weather(3, 5, 4, 1, 0, 8), weather(3, 4, 5, 2, 2, 6), weather(4, 5, 0, 1, 4, 6), weather(4, 4, 5, 2, 3, 8), weather(4, 4, 5, 1, 1, 10), weather(3, 3, 0, 1, 3, 8) ]
	],
	[
		[ weather(2, 2, 2, 0, 3, 10), weather(2, 3, 1, 1, 2, 4), weather(2, 3, 2, 0, 8, 10), weather(2, 3, 3, 0, 0, 12), weather(2, 3, 4, 1, 0, 8), weather(1, 3, 5, 0, 0, 8), weather(3, 3, 0, 0, 1, 6), weather(2, 2, 1, 0, 2, 6), weather(2, 2, 0, 1, 1, 4), weather(2, 3, 1, 0, 0, 8), weather(2, 3, 2, 1, 0, 8), weather(2, 3, 3, 0, 1, 12), weather(2, 2, 2, 0, 2, 8), weather(2, 3, 3, 0, 8, 12), weather(1, 2, 3, 0, 9, 8), weather(2, 3, 4, 0, 0, 10), weather(3, 3, 4, 1, 2, 6), weather(2, 3, 5, 0, 0, 8), weather(2, 3, 5, 0, 2, 6), weather(3, 3, 0, 0, 6, 4) ],
		[ weather(1, 2, 2, 1, 1, 10), weather(1, 2, 2, 1, 2, 8), weather(0, 2, 2, 1, 0, 10), weather(1, 2, 3, 0, 0, 10), weather(1, 2, 3, 1, 2, 6), weather(2, 3, 4, 0, 1, 8), weather(2, 2, 5, 0, 6, 4), weather(1, 1, 0, 0, 6, 6), weather(1, 2, 1, 1, 2, 6), weather(1, 2, 1, 1, 0, 8), weather(2, 3, 2, 1, 0, 10), weather(1, 3, 2, 0, 8, 12), weather(1, 2, 2, 2, 9, 4), weather(1, 2, 2, 1, 0, 10), weather(0, 1, 2, 1, 0, 10), weather(1, 2, 3, 2, 2, 4), weather(2, 2, 4, 1, 2, 4), weather(1, 2, 5, 0, 0, 6), weather(2, 3, 0, 0, 1, 8), weather(3, 3, 1, 1, 6, 6) ],
		[ weather(2, 3, 2, 0, 8, 8), weather(2, 2, 1, 0, 2, 8), weather(2, 2, 2, 0, 8, 8), weather(1, 3, 3, 0, 8, 6), weather(1, 2, 4, 1, 2, 4), weather(2, 3, 5, 0, 2, 8), weather(2, 2, 0, 1, 1, 10), weather(1, 2, 5, 0, 2, 8), weather(1, 2, 0, 0, 1, 12), weather(2, 3, 1, 0, 0, 10), weather(3, 3, 1, 0, 1, 10), weather(2, 3, 2, 1, 2, 4), weather(2, 3, 2, 0, 0, 8), weather(1, 2, 3, 0, 0, 6), weather(1, 2, 3, 2, 9, 4), weather(2, 3, 4, 1, 0, 6), weather(2, 3, 4, 0, 0, 8), weather(2, 3, 5, 0, 1, 10), weather(3, 3, 0, 0, 6, 10), weather(3, 3, 1, 1, 1, 8) ],
		[ weather(3, 3, 1, 0, 3, 8), weather(3, 3, 1, 1, 1, 6), weather(3, 3, 2, 1, 6, 4), weather(2, 4, 3, 1, 2, 4), weather(3, 3, 3, 0, 8, 8), weather(2, 3, 4, 0, 2, 8), weather(3, 3, 5, 1, 6, 8), weather(2, 3, 0, 0, 3, 10), weather(2, 2, 5, 2, 7, 4), weather(3, 4, 0, 1, 2, 6), weather(3, 3, 1, 2, 6, 4), weather(3, 3, 2, 2, 3, 4), weather(2, 3, 3, 1, 0, 6), weather(2, 3, 4, 1, 2, 6), weather(2, 3, 4, 1, 0, 8), weather(3, 4, 5, 2, 1, 8), weather(3, 3, 5, 1, 6, 8), weather(3, 3, 0, 2, 3, 6), weather(3, 3, 5, 1, 1, 10), weather(3, 3, 0, 1, 6, 6) ]
	],
	[
		[ weather(2, 2, 2, 1, 3, 10), weather(1, 2, 2, 1, 2, 8), weather(1, 2, 2, 0, 8, 12), weather(0, 2, 3, 0, 0, 10), weather(1, 2, 3, 1, 2, 6), weather(2, 2, 4, 0, 6, 6), weather(1, 2, 5, 0, 1, 6), weather(1, 2, 0, 1, 0, 6), weather(1, 2, 1, 1, 2, 6), weather(0, 2, 1, 0, 0, 10), weather(0, 2, 2, 1, 0, 10), weather(0, 2, 2, 0, 0, 12), weather(0, 1, 2, 1, 1, 10), weather(1, 2, 2, 1, 2, 8), weather(1, 1, 2, 1, 2, 8), weather(0, 2, 3, 1, 0, 8), weather(0, 2, 4, 1, 0, 6), weather(1, 1, 5, 2, 6, 4), weather(2, 2, 0, 2, 9, 4), weather(1, 2, 1, 1, 0, 8) ],
		[ weather(1, 2, 2, 1, 2, 8), weather(0, 2, 2, 1, 0, 10), weather(0, 2, 2, 1, 0, 10), weather(0, 2, 2, 0, 0, 12), weather(1, 2, 3, 1, 1, 8), weather(1, 2, 4, 0, 2, 6), weather(2, 2, 3, 0, 6, 8), weather(1, 1, 2, 0, 1, 12), weather(1, 2, 2, 1, 2, 8), weather(0, 2, 2, 1, 0, 10), weather(1, 2, 2, 1, 0, 10), weather(1, 2, 1, 0, 8, 10), weather(0, 1, 2, 0, 2, 10), weather(1, 2, 2, 1, 0, 10), weather(0, 1, 3, 1, 0, 8), weather(0, 1, 3, 1, 0, 8), weather(0, 1, 4, 1, 1, 6), weather(1, 1, 5, 2, 9, 4), weather(2, 3, 0, 2, 2, 4), weather(2, 2, 1, 1, 6, 6) ],
		[ weather(1, 2, 2, 1, 0, 10), weather(1, 1, 2, 1, 2, 8), weather(0, 2, 2, 0, 0, 12), weather(1, 2, 3, 0, 8, 10), weather(1, 2, 3, 1, 2, 6), weather(1, 2, 4, 0, 2, 6), weather(1, 1, 5, 0, 3, 6), weather(1, 2, 0, 1, 2, 4), weather(1, 2, 1, 0, 0, 10), weather(0, 2, 1, 0, 0, 10), weather(1, 2, 2, 1, 1, 10), weather(2, 2, 2, 1, 2, 8), weather(0, 2, 2, 1, 0, 10), weather(0, 2, 2, 1, 0, 10), weather(0, 2, 2, 1, 0, 10), weather(0, 1, 3, 1, 0, 8), weather(0, 1, 4, 1, 1, 6), weather(1, 1, 5, 2, 9, 4), weather(2, 3, 0, 1, 2, 4), weather(2, 2, 1, 1, 6, 6) ],
		[ weather(2, 2, 2, 0, 3, 10), weather(1, 1, 1, 0, 1, 12), weather(0, 2, 2, 0, 0, 10), weather(2, 2, 3, 0, 8, 8), weather(1, 2, 4, 1, 2, 4), weather(1, 2, 5, 0, 0, 8), weather(1, 2, 0, 1, 2, 6), weather(1, 2, 1, 0, 1, 12), weather(1, 2, 0, 0, 0, 10), weather(0, 1, 1, 0, 1, 12), weather(1, 2, 2, 1, 2, 6), weather(2, 2, 3, 0, 3, 8), weather(0, 2, 2, 0, 0, 10), weather(1, 2, 3, 0, 2, 6), weather(0, 2, 3, 0, 0, 8), weather(0, 2, 4, 0, 0, 6), weather(1, 2, 4, 1, 1, 4), weather(1, 1, 5, 2, 9, 4), weather(2, 3, 0, 1, 1, 8), weather(2, 2, 1, 0, 2, 10) ]
	],
	[
		[ weather(2, 2, 2, 1, 7, 4), weather(1, 2, 1, 1, 2, 6), weather(1, 2, 2, 0, 8, 8), weather(0, 2, 2, 0, 3, 8), weather(1, 2, 3, 1, 2, 4), weather(2, 2, 4, 0, 0, 8), weather(1, 2, 5, 0, 2, 8), weather(1, 2, 0, 1, 6, 8), weather(1, 2, 1, 1, 2, 6), weather(0, 2, 2, 0, 0, 8), weather(0, 2, 3, 1, 0, 4), weather(0, 2, 2, 0, 2, 6), weather(0, 1, 3, 1, 7, 4), weather(1, 2, 4, 1, 2, 4), weather(1, 1, 3, 1, 0, 4), weather(0, 2, 3, 1, 1, 4), weather(0, 2, 4, 1, 2, 4), weather(1, 1, 5, 2, 9, 4), weather(2, 2, 0, 2, 7, 4), weather(1, 2, 1, 1, 1, 8) ],
		[ weather(1, 2, 2, 0, 7, 4), weather(0, 2, 1, 1, 0, 6), weather(0, 2, 2, 1, 1, 4), weather(0, 2, 3, 0, 7, 4), weather(1, 2, 4, 1, 0, 8), weather(1, 2, 5, 0, 2, 10), weather(2, 2, 0, 0, 8, 10), weather(1, 1, 1, 0, 2, 6), weather(1, 2, 0, 1, 6, 6), weather(0, 2, 1, 1, 0, 6), weather(1, 2, 2, 1, 2, 4), weather(1, 2, 3, 0, 2, 6), weather(0, 1, 4, 0, 6, 8), weather(1, 2, 3, 1, 0, 6), weather(0, 1, 4, 1, 2, 6), weather(0, 1, 4, 1, 0, 8), weather(0, 1, 5, 1, 1, 10), weather(1, 1, 5, 2, 9, 4), weather(2, 3, 0, 1, 7, 4), weather(2, 2, 1, 1, 6, 4) ],
		[ weather(1, 2, 1, 1, 1, 8), weather(1, 1, 2, 1, 2, 4), weather(0, 2, 2, 0, 8, 8), weather(1, 2, 2, 0, 7, 4), weather(1, 2, 3, 1, 2, 4), weather(1, 2, 4, 0, 0, 8), weather(1, 1, 5, 0, 2, 8), weather(1, 2, 0, 1, 6, 8), weather(1, 2, 1, 0, 2, 8), weather(0, 2, 2, 0, 0, 8), weather(1, 2, 3, 1, 2, 4), weather(2, 2, 2, 1, 1, 6), weather(0, 2, 3, 1, 2, 4), weather(0, 2, 3, 1, 0, 4), weather(0, 2, 3, 1, 2, 4), weather(0, 1, 4, 1, 2, 4), weather(0, 1, 4, 1, 6, 4), weather(1, 1, 5, 2, 9, 4), weather(2, 3, 0, 1, 7, 6), weather(2, 2, 1, 1, 6, 6) ],
		[ weather(2, 2, 2, 1, 6, 4), weather(1, 1, 2, 1, 1, 6), weather(0, 2, 2, 0, 0, 8), weather(2, 2, 3, 0, 8, 6), weather(1, 2, 3, 1, 2, 4), weather(1, 2, 4, 0, 0, 8), weather(1, 2, 5, 1, 0, 8), weather(1, 2, 0, 1, 2, 8), weather(1, 2, 1, 0, 0, 10), weather(0, 1, 1, 0, 0, 10), weather(1, 2, 2, 1, 0, 6), weather(2, 2, 2, 1, 2, 4), weather(0, 2, 2, 1, 6, 4), weather(1, 2, 3, 1, 2, 4), weather(0, 2, 2, 1, 0, 6), weather(0, 2, 3, 1, 0, 4), weather(1, 2, 4, 1, 2, 4), weather(1, 1, 5, 2, 9, 4), weather(2, 3, 0, 1, 6, 8), weather(2, 2, 1, 1, 2, 6) ]
	],
	[
		[ weather(4, 5, 1, 1, 4, 4), weather(3, 4, 2, 1, 1, 4), weather(2, 4, 3, 0, 0, 8), weather(2, 3, 4, 1, 0, 8), weather(3, 4, 5, 2, 1, 6), weather(4, 5, 0, 2, 4, 4), weather(5, 5, 5, 1, 0, 10), weather(3, 4, 5, 1, 0, 8), weather(4, 5, 0, 1, 1, 8), weather(5, 5, 1, 0, 1, 8), weather(5, 5, 1, 1, 0, 6), weather(4, 5, 2, 1, 4, 4), weather(2, 4, 3, 0, 2, 6), weather(1, 3, 4, 0, 0, 10), weather(2, 3, 4, 0, 9, 6), weather(3, 5, 5, 0, 0, 12), weather(3, 4, 3, 1, 1, 4), weather(3, 4, 5, 2, 2, 4), weather(4, 5, 0, 2, 4, 4), weather(4, 5, 0, 1, 4, 6) ],
		[ weather(3, 4, 1, 0, 2, 6), weather(2, 3, 2, 0, 2, 4), weather(2, 3, 3, 0, 0, 8), weather(1, 3, 4, 0, 0, 10), weather(2, 3, 5, 0, 9, 8), weather(2, 4, 4, 0, 0, 8), weather(3, 4, 5, 1, 1, 8), weather(3, 4, 0, 2, 2, 4), weather(2, 4, 5, 1, 0, 10), weather(2, 4, 0, 1, 0, 8), weather(2, 4, 1, 1, 0, 6), weather(2, 3, 2, 0, 8, 6), weather(1, 3, 3, 0, 2, 6), weather(1, 3, 3, 0, 0, 8), weather(2, 3, 4, 0, 0, 10), weather(2, 4, 5, 1, 0, 10), weather(2, 3, 0, 2, 2, 4), weather(3, 4, 5, 1, 1, 8), weather(3, 4, 0, 1, 2, 6), weather(3, 4, 1, 0, 3, 8) ],
		[ weather(3, 5, 1, 0, 8, 8), weather(3, 5, 1, 0, 2, 6), weather(2, 4, 2, 0, 8, 6), weather(2, 3, 3, 0, 1, 6), weather(2, 3, 4, 0, 0, 10), weather(2, 4, 5, 0, 9, 8), weather(3, 4, 0, 1, 6, 4), weather(3, 4, 5, 1, 1, 8), weather(3, 5, 0, 2, 1, 6), weather(4, 5, 1, 1, 1, 6), weather(4, 5, 2, 2, 4, 4), weather(3, 5, 3, 1, 2, 4), weather(2, 4, 3, 0, 0, 8), weather(3, 4, 4, 1, 2, 4), weather(3, 4, 5, 2, 1, 6), weather(3, 5, 4, 1, 0, 8), weather(3, 4, 5, 1, 0, 10), weather(3, 5, 0, 2, 0, 6), weather(5, 5, 5, 2, 3, 6), weather(5, 5, 0, 1, 1, 8) ],
		[ weather(5, 5, 1, 0, 5, 4), weather(5, 5, 1, 1, 3, 6), weather(4, 5, 2, 2, 4, 4), weather(3, 5, 3, 1, 1, 4), weather(3, 4, 3, 0, 0, 8), weather(3, 5, 4, 0, 0, 8), weather(3, 5, 5, 1, 2, 6), weather(4, 5, 0, 0, 3, 10), weather(3, 4, 5, 1, 1, 8), weather(4, 5, 0, 1, 4, 6), weather(4, 5, 1, 2, 3, 4), weather(5, 5, 2, 2, 4, 4), weather(4, 5, 3, 1, 0, 6), weather(3, 5, 4, 1, 0, 8), weather(4, 5, 4, 1, 0, 8), weather(3, 5, 5, 2, 0, 6), weather(5, 5, 0, 1, 4, 6), weather(4, 5, 5, 2, 3, 6), weather(4, 5, 5, 1, 0, 10), weather(4, 5, 0, 1, 2, 6) ]
	],
	[
		[ weather(4, 4, 1, 1, 4, 6), weather(3, 3, 2, 1, 1, 6), weather(2, 3, 4, 1, 0, 6), weather(2, 2, 3, 0, 0, 6), weather(3, 3, 5, 2, 1, 4), weather(4, 4, 0, 2, 3, 6), weather(4, 5, 5, 1, 0, 8), weather(3, 3, 5, 1, 0, 6), weather(4, 4, 0, 1, 0, 10), weather(5, 5, 1, 0, 1, 10), weather(4, 5, 1, 1, 0, 8), weather(3, 5, 2, 1, 6, 4), weather(2, 3, 3, 0, 2, 4), weather(1, 2, 4, 0, 0, 8), weather(2, 2, 4, 0, 9, 4), weather(3, 4, 5, 0, 0, 10), weather(3, 3, 3, 1, 1, 4), weather(3, 3, 5, 2, 2, 4), weather(4, 4, 0, 2, 3, 6), weather(4, 4, 0, 1, 3, 8) ],
		[ weather(3, 3, 1, 0, 1, 6), weather(2, 2, 2, 0, 2, 4), weather(1, 3, 3, 0, 0, 8), weather(1, 2, 4, 0, 0, 10), weather(2, 2, 5, 0, 9, 8), weather(2, 3, 4, 0, 0, 8), weather(3, 3, 5, 1, 1, 8), weather(3, 3, 0, 2, 1, 4), weather(2, 3, 5, 1, 0, 10), weather(2, 3, 0, 1, 0, 8), weather(2, 3, 1, 1, 0, 6), weather(1, 3, 2, 0, 8, 6), weather(1, 2, 3, 0, 2, 6), weather(1, 2, 3, 0, 0, 8), weather(2, 2, 4, 0, 0, 10), weather(2, 3, 5, 1, 0, 10), weather(2, 2, 0, 2, 1, 4), weather(3, 3, 5, 1, 1, 8), weather(3, 3, 0, 1, 1, 6), weather(3, 3, 1, 0, 1, 8) ],
		[ weather(3, 4, 1, 0, 0, 10), weather(3, 4, 1, 0, 1, 8), weather(2, 3, 2, 0, 8, 8), weather(1, 3, 3, 0, 1, 4), weather(1, 3, 4, 0, 0, 8), weather(2, 3, 5, 0, 9, 6), weather(3, 3, 0, 1, 2, 6), weather(3, 3, 5, 1, 1, 6), weather(3, 4, 0, 2, 0, 8), weather(4, 4, 1, 1, 1, 8), weather(4, 4, 2, 2, 4, 4), weather(3, 4, 3, 1, 2, 4), weather(2, 3, 3, 0, 0, 6), weather(3, 3, 4, 1, 2, 4), weather(3, 3, 5, 2, 1, 4), weather(3, 4, 4, 1, 0, 6), weather(2, 4, 5, 1, 0, 8), weather(3, 4, 0, 2, 0, 8), weather(4, 5, 5, 2, 3, 4), weather(5, 5, 0, 1, 0, 10) ],
		[ weather(4, 5, 1, 0, 4, 6), weather(5, 5, 1, 1, 3, 8), weather(4, 4, 2, 2, 4, 4), weather(3, 4, 3, 1, 1, 4), weather(2, 4, 3, 0, 0, 6), weather(3, 4, 4, 0, 0, 6), weather(3, 4, 5, 1, 2, 4), weather(4, 4, 0, 0, 1, 12), weather(3, 3, 5, 1, 1, 6), weather(4, 4, 0, 1, 3, 8), weather(4, 4, 1, 2, 3, 6), weather(5, 5, 2, 2, 4, 4), weather(3, 5, 3, 1, 0, 4), weather(3, 4, 4, 1, 0, 6), weather(3, 5, 4, 1, 0, 6), weather(3, 4, 5, 2, 0, 4), weather(4, 5, 0, 1, 3, 8), weather(4, 4, 5, 2, 3, 4), weather(4, 4, 5, 1, 0, 8), weather(4, 4, 0, 1, 1, 8) ]
	],
	[
		[ weather(2, 2, 2, 0, 3, 12), weather(2, 3, 1, 1, 2, 6), weather(2, 3, 2, 0, 8, 12), weather(2, 3, 3, 0, 0, 10), weather(2, 3, 4, 1, 0, 6), weather(1, 3, 5, 0, 0, 6), weather(3, 3, 0, 0, 1, 8), weather(2, 2, 1, 0, 2, 8), weather(2, 2, 0, 0, 1, 6), weather(2, 3, 1, 0, 0, 10), weather(2, 3, 2, 1, 0, 10), weather(2, 3, 3, 0, 0, 10), weather(2, 2, 2, 0, 2, 10), weather(2, 3, 3, 0, 0, 10), weather(1, 2, 3, 0, 9, 6), weather(2, 3, 4, 0, 0, 8), weather(3, 3, 4, 1, 0, 4), weather(2, 3, 5, 0, 0, 6), weather(2, 3, 5, 0, 1, 4), weather(3, 3, 0, 0, 6, 6) ],
		[ weather(1, 2, 2, 1, 1, 10), weather(1, 2, 2, 1, 2, 8), weather(0, 2, 2, 1, 0, 10), weather(1, 2, 3, 0, 0, 10), weather(1, 2, 3, 1, 1, 6), weather(2, 3, 4, 0, 0, 8), weather(2, 2, 5, 0, 2, 4), weather(1, 1, 0, 0, 6, 6), weather(1, 2, 1, 1, 2, 6), weather(1, 2, 1, 1, 0, 8), weather(2, 3, 2, 1, 0, 10), weather(1, 3, 2, 0, 8, 12), weather(1, 2, 2, 2, 9, 4), weather(1, 2, 2, 1, 0, 10), weather(0, 1, 2, 1, 0, 10), weather(1, 2, 3, 2, 1, 4), weather(2, 2, 4, 1, 0, 4), weather(1, 2, 5, 0, 0, 6), weather(2, 3, 0, 0, 1, 8), weather(3, 3, 1, 1, 6, 6) ],
		[ weather(2, 3, 2, 0, 8, 12), weather(2, 2, 1, 0, 2, 8), weather(2, 2, 2, 0, 8, 12), weather(1, 3, 3, 0, 0, 10), weather(1, 2, 4, 1, 0, 4), weather(2, 3, 5, 0, 1, 4), weather(2, 2, 0, 0, 1, 6), weather(1, 2, 5, 0, 1, 4), weather(1, 2, 0, 0, 1, 8), weather(2, 3, 1, 0, 0, 10), weather(3, 3, 1, 0, 1, 10), weather(2, 3, 2, 1, 2, 8), weather(2, 3, 2, 0, 0, 12), weather(1, 2, 3, 0, 0, 10), weather(1, 2, 3, 2, 9, 4), weather(2, 3, 4, 1, 0, 6), weather(2, 3, 4, 0, 0, 8), weather(2, 3, 5, 0, 0, 6), weather(3, 3, 0, 0, 6, 6), weather(3, 3, 1, 1, 1, 8) ],
		[ weather(3, 3, 1, 0, 3, 10), weather(3, 3, 1, 1, 1, 8), weather(3, 3, 2, 1, 6, 4), weather(2, 4, 3, 1, 1, 4), weather(3, 3, 3, 0, 0, 6), weather(2, 3, 4, 0, 0, 6), weather(3, 3, 5, 1, 2, 6), weather(2, 3, 0, 0, 3, 12), weather(2, 2, 5, 2, 6, 4), weather(3, 4, 0, 0, 2, 8), weather(3, 3, 1, 2, 6, 4), weather(3, 3, 2, 2, 3, 4), weather(2, 3, 3, 1, 0, 4), weather(2, 3, 4, 1, 0, 4), weather(2, 3, 4, 1, 0, 6), weather(3, 4, 5, 2, 0, 6), weather(3, 3, 5, 1, 2, 6), weather(3, 3, 0, 1, 3, 8), weather(3, 3, 5, 1, 0, 8), weather(3, 3, 0, 0, 6, 8) ]
	],
	[
		[ weather(3, 3, 1, 1, 1, 4), weather(3, 3, 2, 1, 0, 4), weather(2, 3, 3, 0, 0, 8), weather(2, 2, 4, 1, 1, 8), weather(3, 3, 5, 2, 2, 6), weather(4, 4, 0, 2, 1, 6), weather(3, 3, 5, 1, 0, 10), weather(3, 3, 5, 1, 1, 8), weather(4, 4, 0, 1, 1, 6), weather(3, 3, 1, 0, 0, 8), weather(4, 4, 1, 1, 0, 6), weather(3, 4, 2, 1, 0, 4), weather(2, 3, 3, 0, 0, 8), weather(1, 2, 4, 0, 8, 10), weather(2, 2, 4, 0, 9, 6), weather(3, 4, 5, 0, 0, 12), weather(3, 3, 3, 1, 1, 4), weather(3, 3, 5, 2, 6, 4), weather(3, 3, 0, 2, 0, 4), weather(3, 3, 0, 1, 1, 6) ],
		[ weather(3, 3, 2, 0, 0, 6), weather(2, 2, 1, 0, 0, 6), weather(1, 3, 2, 0, 0, 8), weather(1, 2, 3, 0, 0, 10), weather(2, 2, 4, 1, 6, 8), weather(2, 3, 5, 0, 0, 10), weather(2, 2, 3, 1, 9, 4), weather(1, 1, 4, 0, 3, 12), weather(2, 2, 5, 0, 1, 8), weather(1, 2, 0, 1, 0, 6), weather(2, 3, 1, 0, 0, 6), weather(1, 3, 2, 0, 0, 8), weather(2, 2, 2, 1, 1, 4), weather(0, 2, 3, 0, 0, 10), weather(1, 1, 4, 0, 1, 12), weather(2, 2, 5, 2, 1, 4), weather(2, 2, 0, 1, 0, 6), weather(1, 2, 1, 0, 0, 6), weather(3, 3, 0, 0, 1, 6), weather(3, 3, 1, 0, 1, 4) ],
		[ weather(2, 3, 1, 0, 0, 8), weather(2, 2, 1, 0, 0, 6), weather(2, 3, 2, 0, 0, 6), weather(1, 2, 3, 0, 0, 8), weather(1, 2, 4, 0, 6, 8), weather(2, 2, 5, 0, 9, 8), weather(2, 2, 0, 1, 0, 8), weather(2, 2, 5, 1, 2, 8), weather(2, 3, 0, 2, 2, 4), weather(3, 3, 1, 1, 0, 6), weather(3, 3, 2, 2, 1, 4), weather(3, 3, 3, 1, 2, 4), weather(2, 3, 3, 0, 0, 8), weather(3, 3, 4, 1, 7, 4), weather(3, 3, 5, 2, 1, 8), weather(2, 3, 4, 1, 2, 6), weather(2, 3, 5, 1, 0, 10), weather(3, 4, 0, 2, 0, 6), weather(3, 3, 5, 2, 2, 6), weather(4, 4, 0, 1, 0, 8) ],
		[ weather(4, 4, 1, 0, 3, 6), weather(4, 4, 1, 1, 3, 4), weather(4, 4, 2, 2, 3, 4), weather(3, 4, 3, 1, 1, 4), weather(3, 4, 3, 0, 0, 8), weather(3, 5, 4, 0, 2, 8), weather(3, 3, 5, 1, 6, 6), weather(3, 3, 0, 0, 0, 10), weather(2, 2, 5, 1, 2, 8), weather(3, 3, 0, 1, 2, 4), weather(3, 3, 1, 2, 1, 4), weather(3, 4, 2, 2, 1, 4), weather(3, 5, 3, 1, 0, 6), weather(3, 4, 4, 1, 2, 6), weather(3, 5, 4, 1, 0, 8), weather(3, 4, 5, 2, 1, 6), weather(4, 5, 0, 1, 3, 6), weather(4, 4, 5, 2, 3, 8), weather(4, 4, 5, 1, 1, 10), weather(3, 3, 0, 1, 0, 8) ]
	]
]

def get_weather_per_watch(watch, climate_zone, season, latitude, index):
	weather = weather_chart[climate_zone][season][index - 1]

	return weather, get_weather_index_change(index, weather.change)

def get_watch_times(watch):
	return f'{str(watch * 4).zfill(2)}:00-{str(watch * 4 + 4).zfill(2)}:00'

with ui.row():
	ui.image('chart.webp').props(f"width=983px height=654px")

with ui.row():
	latitude_input = ui.select(latitude_name, label = "Latitude", value = 1)
	climate_zone_input = ui.select(climate_zone, label = "Climate Zone", value = 6)

	ui.space()
	ui.space()

	day_input = ui.number(label = "Day", value = 1, format = '%d', min = 1, max = 30)
	month_input = ui.select(month_name, label = "Month", value = 0)
	year_input = ui.number(label = "Year", value = 720, format = '%d')

	ui.space()
	ui.space()

	duration_input = ui.number(label = "Number of Days", value = 1, format = '%d', min = 1)

	ui.space()
	ui.space()

	units_input = ui.select(units_name, label = "Units", value = 0)

	with ui.scroll_area().classes("border"):
		markdown_output = ui.markdown()

def on_click_generate():
	markdown_content = markdown_output.content

	for d in range(int(duration_input.value)):
		season = get_season_exact(day_input.value, month_input.value)
		index = get_weather_index_start(climate_zone_input.value, season)
		moon = get_moon_phase(day_input.value)

		markdown_content += f'**{day_input.value} {month_name[month_input.value]} TR {year_input.value} - {get_dawn_string(latitude_input.value, season)}, {get_day_string(latitude_input.value, season)}, {get_dusk_string(latitude_input.value, season)}, {get_night_string(latitude_input.value, season)}, Moon: {get_moon_phase_string(day_input.value)}**<br>'

		for watch in range(0, 6, 1):
			daylight = is_day(latitude_input.value, season, watch * 4)
			weather, index = get_weather_per_watch(watch, climate_zone_input.value, season, latitude_input.value, index)
			is_foggy = True if weather.cloud_precipitation == 8 else False
			hazard = " ⚠" if get_weather_hazard(weather.subjective_temperature[daylight]) else ""

			markdown_content += f'- *{get_watch_times(watch)}:* {get_subjective_temperature(weather.subjective_temperature[daylight], units_input.value)}, {cloud_precipitation[weather.cloud_precipitation]}, {get_wind_force(weather.wind_force, is_foggy, units_input.value)} from {wind_direction[weather.wind_direction]}{hazard}<br>'

		day_input.value = day_input.value + 1

		if day_input.value > 30:
			day_input.value = 1

			if month_input.value + 1 > 11:
				month_input.value = 0
				year_input.value = year_input.value + 1
			else:
				month_input.value = month_input.value + 1

		markdown_content += f'<br>'
	
	markdown_output.content = markdown_content

def on_click_reset():
	month_input.value = 0
	day_input.value = 1
	year_input.value = 720
	latitude_input.value = 1
	climate_zone_input.value = 6
	markdown_output.content = ''

def on_click_copy_to_clipboard():
	ui.clipboard.write(markdown_output.content.replace("<br>", "\n"))

def on_click_export_to_pdf():
	ui.notify("This feature is currently not implemented!")

with ui.row():
	ui.button("Generate", on_click = on_click_generate)
	ui.button("Reset", on_click = on_click_reset)
	ui.button("Copy To Clipboard", on_click = on_click_copy_to_clipboard)
	ui.button("Export To PDF", on_click = on_click_export_to_pdf)

with ui.row():
	ui.html('<small>Knocked together with ❤️ in 2025 by Marc André Uebereall (www.marcueberall.com).</br>This is unofficial Hârn fan material. Hârn®, HârnWorld®, and HârnMaster® are registered trademarks of Arien Crossby, licensed by Keléstia Productions Ltd (<a href="www.kelestia.com">www.kelestia.com</a>).</br>All related concepts and material are the property of Arien Crossby and Keléstia Productions Ltd (<a href="www.kelestia.com">www.kelestia.com</a>). Used with permission.</small>')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='HârnMaster Venârivè Weather', favicon='⛅')