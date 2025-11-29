import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import pytz
from datetime import datetime

# 🔑 BOT TOKEN (Xavfsizlik uchun Railway Secrets orqali beriladi)
BOT_TOKEN = os.getenv("BOT_TOKEN", "7872530944:AAEnjsqPfd6y_dGMQVVKdnmcKzS8e6cHkI4")

# 🌍 Barcha 195 ta davlat (to'liq ma'lumotlar)
COUNTRIES = {
    "🇦🇫 Afg'oniston": {"tz": "Asia/Kabul", "l": {"n": "Hibatulloh Ahundzoda", "b": 1961, "o": 2021, "t": "Amir"}},
    "🇦🇱 Albaniya": {"tz": "Europe/Tirane", "l": {"n": "Bajram Begaj", "b": 1967, "o": 2022, "t": "Prezident"}},
    "🇩🇿 Jazoir": {"tz": "Africa/Algiers", "l": {"n": "Abdelmadjid Tebboune", "b": 1945, "o": 2019, "t": "Prezident"}},
    "🇦🇩 Andorra": {"tz": "Europe/Andorra", "l": {"n": "Xavier Espot Zamora", "b": 1979, "o": 2019, "t": "Bosh vazir"}},
    "🇦🇴 Angola": {"tz": "Africa/Luanda", "l": {"n": "João Lourenço", "b": 1954, "o": 2017, "t": "Prezident"}},
    "🇦🇬 Antigua va Barbuda": {"tz": "America/Antigua", "l": {"n": "Gaston Browne", "b": 1967, "o": 2014, "t": "Bosh vazir"}},
    "🇦🇷 Argentina": {"tz": "America/Argentina/Buenos_Aires", "l": {"n": "Javier Milei", "b": 1970, "o": 2023, "t": "Prezident"}},
    "🇦🇲 Armaniston": {"tz": "Asia/Yerevan", "l": {"n": "Vahagn Xachaturyan", "b": 1959, "o": 2022, "t": "Prezident"}},
    "🇦🇺 Avstraliya": {"tz": "Australia/Sydney", "l": {"n": "Anthony Albanese", "b": 1963, "o": 2022, "t": "Bosh vazir"}},
    "🇦🇹 Avstriya": {"tz": "Europe/Vienna", "l": {"n": "Karl Nehammer", "b": 1972, "o": 2021, "t": "Kansler"}},
    "🇦🇿 Ozarbayjon": {"tz": "Asia/Baku", "l": {"n": "Ilhom Aliyev", "b": 1961, "o": 2003, "t": "Prezident"}},
    "🇧🇸 Bagama orollari": {"tz": "America/Nassau", "l": {"n": "Philip Davis", "b": 1951, "o": 2021, "t": "Bosh vazir"}},
    "🇧🇭 Bahrayn": {"tz": "Asia/Bahrain", "l": {"n": "Salmon bin Hamad Al Xalifa", "b": 1969, "o": 2005, "t": "Amir (de-fakto)"}},
    "🇧🇩 Bangladesh": {"tz": "Asia/Dhaka", "l": {"n": "Muhammad Shehbaz Sharif", "b": 1951, "o": 2024, "t": "Bosh vazir"}},
    "🇧🇧 Barbados": {"tz": "America/Barbados", "l": {"n": "Mia Mottley", "b": 1965, "o": 2018, "t": "Bosh vazir"}},
    "🇧🇾 Belorussiya": {"tz": "Europe/Minsk", "l": {"n": "Aleksandr Lukashenko", "b": 1954, "o": 1994, "t": "Prezident"}},
    "🇧🇪 Belgiya": {"tz": "Europe/Brussels", "l": {"n": "Alexander De Croo", "b": 1975, "o": 2020, "t": "Bosh vazir"}},
    "🇧🇿 Beliz": {"tz": "America/Belize", "l": {"n": "Johnny Briceño", "b": 1960, "o": 2020, "t": "Bosh vazir"}},
    "🇧🇯 Benin": {"tz": "Africa/Porto-Novo", "l": {"n": "Patrice Talon", "b": 1958, "o": 2016, "t": "Prezident"}},
    "🇧🇹 Butan": {"tz": "Asia/Thimphu", "l": {"n": "Lotay Tshering", "b": 1960, "o": 2018, "t": "Bosh vazir"}},
    "🇧🇴 Boliviya": {"tz": "America/La_Paz", "l": {"n": "Luis Arce", "b": 1963, "o": 2020, "t": "Prezident"}},
    "🇧🇦 Bosniya va Gertsegovina": {"tz": "Europe/Sarajevo", "l": {"n": "Željko Komšić", "b": 1964, "o": 2018, "t": "Kollektiv Prezident a'zosi"}},
    "🇧🇼 Botsvana": {"tz": "Africa/Gaborone", "l": {"n": "Mokgweetsi Masisi", "b": 1961, "o": 2018, "t": "Prezident"}},
    "🇧🇷 Braziliya": {"tz": "America/Sao_Paulo", "l": {"n": "Luiz Inácio Lula da Silva", "b": 1945, "o": 2023, "t": "Prezident"}},
    "🇧🇳 Bruney": {"tz": "Asia/Brunei", "l": {"n": "Sulton Hassanal Bolkiah", "b": 1946, "o": 1967, "t": "Sulton"}},
    "🇧🇬 Bolgariya": {"tz": "Europe/Sofia", "l": {"n": "Rumen Radev", "b": 1963, "o": 2017, "t": "Prezident"}},
    "🇧🇫 Burkina-Faso": {"tz": "Africa/Ouagadougou", "l": {"n": "Ibrahim Traoré", "b": 1988, "o": 2022, "t": "Prezident"}},
    "🇧🇮 Burundi": {"tz": "Africa/Bujumbura", "l": {"n": "Évariste Ndayishimiye", "b": 1968, "o": 2020, "t": "Prezident"}},
    "🇨🇻 Kabo-Verde": {"tz": "Atlantic/Cape_Verde", "l": {"n": "José Maria Neves", "b": 1960, "o": 2021, "t": "Bosh vazir"}},
    "🇰🇭 Kambodja": {"tz": "Asia/Phnom_Penh", "l": {"n": "Hun Manet", "b": 1977, "o": 2023, "t": "Bosh vazir"}},
    "🇨🇲 Kamerun": {"tz": "Africa/Douala", "l": {"n": "Paul Biya", "b": 1933, "o": 1982, "t": "Prezident"}},
    "🇨🇦 Kanada": {"tz": "America/Toronto", "l": {"n": "Justin Trudeau", "b": 1971, "o": 2015, "t": "Bosh vazir"}},
    "🇨🇫 Markaziy Afrika Respublikasi": {"tz": "Africa/Bangui", "l": {"n": "Faustin-Archange Touadéra", "b": 1957, "o": 2016, "t": "Prezident"}},
    "🇹🇩 Chod": {"tz": "Africa/Ndjamena", "l": {"n": "Mahamat Idriss Déby", "b": 1984, "o": 2024, "t": "Prezident"}},
    "🇨🇱 Chili": {"tz": "America/Santiago", "l": {"n": "Gabriel Boric", "b": 1986, "o": 2022, "t": "Prezident"}},
    "🇨🇳 Xitoy": {"tz": "Asia/Shanghai", "l": {"n": "Xi Jinping", "b": 1953, "o": 2013, "t": "Prezident"}},
    "🇨🇴 Kolumbiya": {"tz": "America/Bogota", "l": {"n": "Gustavo Petro", "b": 1960, "o": 2022, "t": "Prezident"}},
    "🇰🇲 Komor orollari": {"tz": "Indian/Comoro", "l": {"n": "Azali Assoumani", "b": 1959, "o": 2016, "t": "Prezident"}},
    "🇨🇬 Konga (Brazzavil)": {"tz": "Africa/Brazzaville", "l": {"n": "Denis Sassou Nguesso", "b": 1943, "o": 1997, "t": "Prezident"}},
    "🇨🇩 Kongo (Kinshasa)": {"tz": "Africa/Kinshasa", "l": {"n": "Félix Tshisekedi", "b": 1963, "o": 2019, "t": "Prezident"}},
    "🇨🇷 Kosta-Rika": {"tz": "America/Costa_Rica", "l": {"n": "Rodrigo Chaves", "b": 1961, "o": 2022, "t": "Prezident"}},
    "🇨🇮 Kot-d’Ivuar": {"tz": "Africa/Abidjan", "l": {"n": "Alassane Ouattara", "b": 1942, "o": 2010, "t": "Prezident"}},
    "🇭🇷 Xorvatiya": {"tz": "Europe/Zagreb", "l": {"n": "Zoran Milanović", "b": 1966, "o": 2020, "t": "Prezident"}},
    "🇨🇺 Kuba": {"tz": "America/Havana", "l": {"n": "Miguel Díaz-Canel", "b": 1960, "o": 2018, "t": "Prezident"}},
    "🇨🇾 Kipr": {"tz": "Asia/Nicosia", "l": {"n": "Nikos Christodoulides", "b": 1973, "o": 2023, "t": "Prezident"}},
    "🇨🇿 Chexiya": {"tz": "Europe/Prague", "l": {"n": "Petr Fiala", "b": 1964, "o": 2021, "t": "Bosh vazir"}},
    "🇩🇰 Daniya": {"tz": "Europe/Copenhagen", "l": {"n": "Mette Frederiksen", "b": 1977, "o": 2019, "t": "Bosh vazir"}},
    "🇩🇯 Jibuti": {"tz": "Africa/Djibouti", "l": {"n": "Ismaïl Omar Guelleh", "b": 1947, "o": 1999, "t": "Prezident"}},
    "🇩🇲 Dominika": {"tz": "America/Dominica", "l": {"n": "Roosevelt Skerrit", "b": 1972, "o": 2004, "t": "Bosh vazir"}},
    "🇩🇴 Dominikan Respublikasi": {"tz": "America/Santo_Domingo", "l": {"n": "Luis Abinader", "b": 1967, "o": 2020, "t": "Prezident"}},
    "🇹🇱 Sharqiy Timor": {"tz": "Asia/Dili", "l": {"n": "Xanana Gusmão", "b": 1945, "o": 2023, "t": "Bosh vazir"}},
    "🇪🇨 Ekvador": {"tz": "America/Guayaquil", "l": {"n": "Daniel Noboa", "b": 1987, "o": 2023, "t": "Prezident"}},
    "🇪🇬 Misr": {"tz": "Africa/Cairo", "l": {"n": "Abdul Fattoh al-Sisi", "b": 1954, "o": 2014, "t": "Prezident"}},
    "🇸🇻 Salvador": {"tz": "America/El_Salvador", "l": {"n": "Nayib Bukele", "b": 1981, "o": 2019, "t": "Prezident"}},
    "🇬🇶 Ekvatorial Gvineya": {"tz": "Africa/Malabo", "l": {"n": "Teodoro Obiang Nguema", "b": 1942, "o": 1979, "t": "Prezident"}},
    "🇪🇷 Eritreya": {"tz": "Africa/Asmara", "l": {"n": "Isaias Afwerki", "b": 1946, "o": 1993, "t": "Prezident"}},
    "🇪🇪 Estonya": {"tz": "Europe/Tallinn", "l": {"n": "Kaja Kallas", "b": 1977, "o": 2021, "t": "Bosh vazir"}},
    "🇸🇿 Eswatini": {"tz": "Africa/Mbabane", "l": {"n": "Mswati III", "b": 1968, "o": 1986, "t": "Qirol"}},
    "🇪🇹 Efiopiya": {"tz": "Africa/Addis_Ababa", "l": {"n": "Abiy Ahmed", "b": 1976, "o": 2018, "t": "Bosh vazir"}},
    "🇫🇯 Fidji": {"tz": "Pacific/Fiji", "l": {"n": "Sitiveni Rabuka", "b": 1948, "o": 2022, "t": "Bosh vazir"}},
    "🇫🇮 Finlandiya": {"tz": "Europe/Helsinki", "l": {"n": "Alexander Stubb", "b": 1968, "o": 2024, "t": "Prezident"}},
    "🇫🇷 Fransiya": {"tz": "Europe/Paris", "l": {"n": "Emmanuel Macron", "b": 1977, "o": 2017, "t": "Prezident"}},
    "🇬🇦 Gabon": {"tz": "Africa/Libreville", "l": {"n": "Brice Oligui Nguema", "b": 1976, "o": 2023, "t": "Prezident"}},
    "🇬🇲 Gambia": {"tz": "Africa/Banjul", "l": {"n": "Adama Barrow", "b": 1965, "o": 2017, "t": "Prezident"}},
    "🇬🇪 Gruziya": {"tz": "Asia/Tbilisi", "l": {"n": "Irakli Kobakhidze", "b": 1985, "o": 2024, "t": "Bosh vazir"}},
    "🇩🇪 Germaniya": {"tz": "Europe/Berlin", "l": {"n": "Olaf Scholz", "b": 1958, "o": 2021, "t": "Kansler"}},
    "🇬🇭 Gana": {"tz": "Africa/Accra", "l": {"n": "Nana Akufo-Addo", "b": 1944, "o": 2017, "t": "Prezident"}},
    "🇬🇷 Gretsiya": {"tz": "Europe/Athens", "l": {"n": "Kyriakos Mitsotakis", "b": 1968, "o": 2019, "t": "Bosh vazir"}},
    "🇬🇩 Grenada": {"tz": "America/Grenada", "l": {"n": "Dickon Mitchell", "b": 1983, "o": 2022, "t": "Bosh vazir"}},
    "🇬🇹 Gvatemala": {"tz": "America/Guatemala", "l": {"n": "Bernardo Arévalo", "b": 1958, "o": 2024, "t": "Prezident"}},
    "🇬🇳 Gvineya": {"tz": "Africa/Conakry", "l": {"n": "Mamady Doumbouya", "b": 1980, "o": 2021, "t": "Prezident"}},
    "🇬🇼 Gvineya-Bisau": {"tz": "Africa/Bissau", "l": {"n": "Geraldo Martins", "b": 1973, "o": 2023, "t": "Bosh vazir"}},
    "🇬🇾 Gayana": {"tz": "America/Guyana", "l": {"n": "Irfaan Ali", "b": 1980, "o": 2020, "t": "Prezident"}},
    "🇭🇹 Gaiti": {"tz": "America/Port-au-Prince", "l": {"n": "Ariel Henry", "b": 1958, "o": 2021, "t": "Bosh vazir"}},
    "🇭🇳 Gonduras": {"tz": "America/Tegucigalpa", "l": {"n": "Xiomara Castro", "b": 1959, "o": 2022, "t": "Prezident"}},
    "🇭🇺 Vengriya": {"tz": "Europe/Budapest", "l": {"n": "Viktor Orbán", "b": 1963, "o": 2010, "t": "Bosh vazir"}},
    "🇮🇸 Islandiya": {"tz": "Atlantic/Reykjavik", "l": {"n": "Bjarni Benediktsson", "b": 1970, "o": 2024, "t": "Bosh vazir"}},
    "🇮🇳 Hindiston": {"tz": "Asia/Kolkata", "l": {"n": "Narendra Modi", "b": 1950, "o": 2014, "t": "Bosh vazir"}},
    "🇮🇩 Indoneziya": {"tz": "Asia/Jakarta", "l": {"n": "Prabowo Subianto", "b": 1951, "o": 2024, "t": "Prezident"}},
    "🇮🇷 Eron": {"tz": "Asia/Tehran", "l": {"n": "Ebrahim Raisi", "b": 1960, "o": 2021, "t": "Prezident"}},
    "🇮🇶 Iroq": {"tz": "Asia/Baghdad", "l": {"n": "Mustafa al-Kadhimi", "b": 1967, "o": 2020, "t": "Bosh vazir"}},
    "🇮🇪 Irlandiya": {"tz": "Europe/Dublin", "l": {"n": "Simon Harris", "b": 1986, "o": 2024, "t": "Bosh vazir"}},
    "🇮🇱 Isroil": {"tz": "Asia/Jerusalem", "l": {"n": "Benjamin Netanyahu", "b": 1949, "o": 2022, "t": "Bosh vazir"}},
    "🇮🇹 Italiya": {"tz": "Europe/Rome", "l": {"n": "Giorgia Meloni", "b": 1977, "o": 2022, "t": "Bosh vazir"}},
    "🇯🇲 Yamayka": {"tz": "America/Jamaica", "l": {"n": "Andrew Holness", "b": 1972, "o": 2016, "t": "Bosh vazir"}},
    "🇯🇵 Yaponiya": {"tz": "Asia/Tokyo", "l": {"n": "Fumio Kishida", "b": 1957, "o": 2021, "t": "Bosh vazir"}},
    "🇯🇴 Iordaniya": {"tz": "Asia/Amman", "l": {"n": "Bisher Al-Khasawneh", "b": 1969, "o": 2020, "t": "Bosh vazir"}},
    "🇰🇿 Qozog'iston": {"tz": "Asia/Almaty", "l": {"n": "Qasim-Jomart Toqaev", "b": 1953, "o": 2019, "t": "Prezident"}},
    "🇰🇪 Keniya": {"tz": "Africa/Nairobi", "l": {"n": "William Ruto", "b": 1966, "o": 2022, "t": "Prezident"}},
    "🇰🇮 Kiribati": {"tz": "Pacific/Tarawa", "l": {"n": "Taneti Maamau", "b": 1960, "o": 2016, "t": "Prezident"}},
    "🇰🇵 Shimoliy Koreya": {"tz": "Asia/Pyongyang", "l": {"n": "Kim Jong-un", "b": 1984, "o": 2011, "t": "Rahbar"}},
    "🇰🇷 Janubiy Koreya": {"tz": "Asia/Seoul", "l": {"n": "Yoon Suk-yeol", "b": 1960, "o": 2022, "t": "Prezident"}},
    "🇰🇼 Quvayt": {"tz": "Asia/Kuwait", "l": {"n": "Shayx Mesh'al al-Ahmad al-Jobir", "b": 1940, "o": 2023, "t": "Amir"}},
    "🇰🇬 Qirg'iziston": {"tz": "Asia/Bishkek", "l": {"n": "Sadyr Japarov", "b": 1968, "o": 2021, "t": "Prezident"}},
    "🇱🇦 Laos": {"tz": "Asia/Vientiane", "l": {"n": "Sonexay Siphandone", "b": 1965, "o": 2022, "t": "Bosh vazir"}},
    "🇱🇻 Latviya": {"tz": "Europe/Riga", "l": {"n": "Evika Siliņa", "b": 1975, "o": 2023, "t": "Bosh vazir"}},
    "🇱🇧 Livan": {"tz": "Asia/Beirut", "l": {"n": "Najib Mikati", "b": 1955, "o": 2021, "t": "Bosh vazir"}},
    "🇱🇸 Lesoto": {"tz": "Africa/Maseru", "l": {"n": "Sam Matekane", "b": 1958, "o": 2022, "t": "Bosh vazir"}},
    "🇱🇷 Liberiya": {"tz": "Africa/Monrovia", "l": {"n": "Joseph Boakai", "b": 1955, "o": 2024, "t": "Prezident"}},
    "🇱🇾 Liviya": {"tz": "Africa/Tripoli", "l": {"n": "Abdul Hamid Dbeibeh", "b": 1959, "o": 2021, "t": "Bosh vazir"}},
    "🇱🇮 Lixtenshteyn": {"tz": "Europe/Vaduz", "l": {"n": "Daniel Risch", "b": 1978, "o": 2021, "t": "Bosh vazir"}},
    "🇱🇹 Litva": {"tz": "Europe/Vilnius", "l": {"n": "Ingrida Šimonytė", "b": 1974, "o": 2020, "t": "Bosh vazir"}},
    "🇱🇺 Lyuksemburg": {"tz": "Europe/Luxembourg", "l": {"n": "Luc Frieden", "b": 1963, "o": 2023, "t": "Bosh vazir"}},
    "🇲🇬 Madagaskar": {"tz": "Indian/Antananarivo", "l": {"n": "Andry Rajoelina", "b": 1974, "o": 2019, "t": "Prezident"}},
    "🇲🇼 Malavi": {"tz": "Africa/Blantyre", "l": {"n": "Lazarus Chakwera", "b": 1965, "o": 2020, "t": "Prezident"}},
    "🇲🇾 Malayziya": {"tz": "Asia/Kuala_Lumpur", "l": {"n": "Anwar Ibrahim", "b": 1947, "o": 2022, "t": "Bosh vazir"}},
    "🇲🇻 Maldiv orollari": {"tz": "Indian/Maldives", "l": {"n": "Mohamed Muizzu", "b": 1978, "o": 2023, "t": "Prezident"}},
    "🇲🇱 Mali": {"tz": "Africa/Bamako", "l": {"n": "Assimi Goïta", "b": 1983, "o": 2021, "t": "Prezident"}},
    "🇲🇹 Malta": {"tz": "Europe/Malta", "l": {"n": "Robert Abela", "b": 1977, "o": 2020, "t": "Bosh vazir"}},
    "🇲🇭 Marshall orollari": {"tz": "Pacific/Majuro", "l": {"n": "Hilda Heine", "b": 1951, "o": 2024, "t": "Prezident"}},
    "🇲🇷 Mavritaniya": {"tz": "Africa/Nouakchott", "l": {"n": "Mohamed Ould Ghazouani", "b": 1956, "o": 2019, "t": "Prezident"}},
    "🇲🇺 Mavrikiy": {"tz": "Indian/Mauritius", "l": {"n": "Pravind Jugnauth", "b": 1961, "o": 2017, "t": "Bosh vazir"}},
    "🇲🇽 Meksika": {"tz": "America/Mexico_City", "l": {"n": "Claudia Sheinbaum", "b": 1962, "o": 2024, "t": "Prezident"}},
    "🇫🇲 Mikroneziya": {"tz": "Pacific/Chuuk", "l": {"n": "Wesley Simina", "b": 1961, "o": 2023, "t": "Prezident"}},
    "🇲🇩 Moldova": {"tz": "Europe/Chisinau", "l": {"n": "Maia Sandu", "b": 1972, "o": 2020, "t": "Prezident"}},
    "🇲🇨 Monako": {"tz": "Europe/Monaco", "l": {"n": "Albert II", "b": 1958, "o": 2005, "t": "Qirol"}},
    "🇲🇳 Mongoliya": {"tz": "Asia/Ulaanbaatar", "l": {"n": "Luvsannamsrain Oyun-Erdene", "b": 1980, "o": 2021, "t": "Bosh vazir"}},
    "🇲🇪 Chernogoriya": {"tz": "Europe/Podgorica", "l": {"n": "Milojko Spajić", "b": 1987, "o": 2023, "t": "Bosh vazir"}},
    "🇲🇦 Marokash": {"tz": "Africa/Casablanca", "l": {"n": "Aziz Akhannouch", "b": 1961, "o": 2021, "t": "Bosh vazir"}},
    "🇲🇿 Mozambik": {"tz": "Africa/Maputo", "l": {"n": "Filipe Nyusi", "b": 1958, "o": 2015, "t": "Prezident"}},
    "🇲🇲 Myanma": {"tz": "Asia/Yangon", "l": {"n": "Min Aung Hlaing", "b": 1956, "o": 2021, "t": "Rahbar"}},
    "🇳🇦 Namibiya": {"tz": "Africa/Windhoek", "l": {"n": "Nangolo Mbumba", "b": 1941, "o": 2024, "t": "Prezident"}},
    "🇳🇷 Nauru": {"tz": "Pacific/Nauru", "l": {"n": "David Adeang", "b": 1969, "o": 2023, "t": "Prezident"}},
    "🇳🇵 Nepal": {"tz": "Asia/Kathmandu", "l": {"n": "Pushpa Kamal Dahal", "b": 1954, "o": 2022, "t": "Bosh vazir"}},
    "🇳🇱 Niderlandiya": {"tz": "Europe/Amsterdam", "l": {"n": "Dick Schoof", "b": 1957, "o": 2024, "t": "Bosh vazir"}},
    "🇳🇿 Yangi Zelandiya": {"tz": "Pacific/Auckland", "l": {"n": "Christopher Luxon", "b": 1970, "o": 2023, "t": "Bosh vazir"}},
    "🇳🇮 Nikaragua": {"tz": "America/Managua", "l": {"n": "Daniel Ortega", "b": 1945, "o": 2007, "t": "Prezident"}},
    "🇳🇪 Niger": {"tz": "Africa/Niamey", "l": {"n": "Abdourahamane Tchiani", "b": 1960, "o": 2023, "t": "Prezident"}},
    "🇳🇬 Nigeriya": {"tz": "Africa/Lagos", "l": {"n": "Bola Tinubu", "b": 1952, "o": 2023, "t": "Prezident"}},
    "🇳🇴 Norvegiya": {"tz": "Europe/Oslo", "l": {"n": "Jonas Gahr Støre", "b": 1960, "o": 2021, "t": "Bosh vazir"}},
    "🇴🇲 Ummon": {"tz": "Asia/Muscat", "l": {"n": "Haitham bin Tariq", "b": 1955, "o": 2020, "t": "Sulton"}},
    "🇵🇰 Pakistan": {"tz": "Asia/Karachi", "l": {"n": "Shehbaz Sharif", "b": 1951, "o": 2024, "t": "Bosh vazir"}},
    "🇵🇼 Palau": {"tz": "Pacific/Palau", "l": {"n": "Surangel Whipps Jr.", "b": 1968, "o": 2021, "t": "Prezident"}},
    "🇵🇦 Panama": {"tz": "America/Panama", "l": {"n": "José Raúl Mulino", "b": 1956, "o": 2024, "t": "Prezident"}},
    "🇵🇬 Papua – Yangi Gvineya": {"tz": "Pacific/Port_Moresby", "l": {"n": "James Marape", "b": 1971, "o": 2019, "t": "Bosh vazir"}},
    "🇵🇾 Paragvay": {"tz": "America/Asuncion", "l": {"n": "Santiago Peña", "b": 1978, "o": 2023, "t": "Prezident"}},
    "🇵🇪 Peru": {"tz": "America/Lima", "l": {"n": "Dina Boluarte", "b": 1962, "o": 2022, "t": "Prezident"}},
    "🇵🇭 Filippin": {"tz": "Asia/Manila", "l": {"n": "Bongbong Marcos", "b": 1957, "o": 2022, "t": "Prezident"}},
    "🇵🇱 Polsha": {"tz": "Europe/Warsaw", "l": {"n": "Donald Tusk", "b": 1957, "o": 2023, "t": "Bosh vazir"}},
    "🇵🇹 Portugaliya": {"tz": "Europe/Lisbon", "l": {"n": "Luís Montenegro", "b": 1973, "o": 2024, "t": "Bosh vazir"}},
    "🇶🇦 Qatar": {"tz": "Asia/Qatar", "l": {"n": "Shayx Tamim bin Hamad", "b": 1980, "o": 2013, "t": "Amir"}},
    "🇷🇴 Ruminiya": {"tz": "Europe/Bucharest", "l": {"n": "Marcel Ciolacu", "b": 1967, "o": 2023, "t": "Bosh vazir"}},
    "🇷🇺 Rossiya": {"tz": "Europe/Moscow", "l": {"n": "Vladimir Putin", "b": 1952, "o": 2012, "t": "Prezident"}},
    "🇷🇼 Ruanda": {"tz": "Africa/Kigali", "l": {"n": "Paul Kagame", "b": 1957, "o": 2000, "t": "Prezident"}},
    "🇰🇳 Sent-Kits va Nevis": {"tz": "America/St_Kitts", "l": {"n": "Terrance Drew", "b": 1976, "o": 2022, "t": "Bosh vazir"}},
    "🇱🇨 Sent-Lyusiya": {"tz": "America/St_Lucia", "l": {"n": "Philip J. Pierre", "b": 1954, "o": 2021, "t": "Bosh vazir"}},
    "🇻🇨 Sent-Vinsent va Grenadin": {"tz": "America/St_Vincent", "l": {"n": "Ralph Gonsalves", "b": 1946, "o": 2001, "t": "Bosh vazir"}},
    "🇼🇸 Samoа": {"tz": "Pacific/Apia", "l": {"n": "Fiamē Naomi Mataʻafa", "b": 1957, "o": 2021, "t": "Bosh vazir"}},
    "🇸🇲 San-Marino": {"tz": "Europe/San_Marino", "l": {"n": "Alessandro Scarano", "b": 1980, "o": 2024, "t": "Kapitan"}},
    "🇸🇹 San-Tome va Prinsipi": {"tz": "Africa/Sao_Tome", "l": {"n": "Patrice Trovoada", "b": 1962, "o": 2022, "t": "Bosh vazir"}},
    "🇸🇦 Saudiya Arabistoni": {"tz": "Asia/Riyadh", "l": {"n": "Salmon ibn Abdulaziz", "b": 1935, "o": 2015, "t": "Qirol"}},
    "🇸🇳 Senegal": {"tz": "Africa/Dakar", "l": {"n": "Bassirou Diomaye Faye", "b": 1980, "o": 2024, "t": "Prezident"}},
    "🇷🇸 Serbiya": {"tz": "Europe/Belgrade", "l": {"n": "Miloš Vučević", "b": 1975, "o": 2024, "t": "Bosh vazir"}},
    "🇸🇨 Seyshel orollari": {"tz": "Indian/Mahe", "l": {"n": "Wavel Ramkalawan", "b": 1959, "o": 2020, "t": "Prezident"}},
    "🇸🇱 Syerra-Leone": {"tz": "Africa/Freetown", "l": {"n": "Julius Maada Bio", "b": 1964, "o": 2018, "t": "Prezident"}},
    "🇸🇬 Singapur": {"tz": "Asia/Singapore", "l": {"n": "Lawrence Wong", "b": 1972, "o": 2024, "t": "Bosh vazir"}},
    "🇸🇰 Slovakiya": {"tz": "Europe/Bratislava", "l": {"n": "Robert Fico", "b": 1964, "o": 2023, "t": "Bosh vazir"}},
    "🇸🇮 Sloveniya": {"tz": "Europe/Ljubljana", "l": {"n": "Robert Golob", "b": 1967, "o": 2022, "t": "Bosh vazir"}},
    "🇸🇧 Solomon orollari": {"tz": "Pacific/Guadalcanal", "l": {"n": "Jeremiah Manele", "b": 1968, "o": 2024, "t": "Bosh vazir"}},
    "🇸🇴 Somali": {"tz": "Africa/Mogadishu", "l": {"n": "Hassan Sheikh Mohamud", "b": 1955, "o": 2022, "t": "Prezident"}},
    "🇿🇦 Janubiy Afrika": {"tz": "Africa/Johannesburg", "l": {"n": "Cyril Ramaphosa", "b": 1952, "o": 2018, "t": "Prezident"}},
    "🇸🇸 Janubiy Sudan": {"tz": "Africa/Juba", "l": {"n": "Salva Kiir", "b": 1951, "o": 2011, "t": "Prezident"}},
    "🇪🇸 Ispaniya": {"tz": "Europe/Madrid", "l": {"n": "Pedro Sánchez", "b": 1972, "o": 2018, "t": "Bosh vazir"}},
    "🇱🇰 Shri-Lanka": {"tz": "Asia/Colombo", "l": {"n": "Ranil Wickremesinghe", "b": 1949, "o": 2022, "t": "Prezident"}},
    "🇸🇩 Sudan": {"tz": "Africa/Khartoum", "l": {"n": "Abdel Fattah al-Burhan", "b": 1964, "o": 2019, "t": "Rahbar"}},
    "🇸🇷 Surinam": {"tz": "America/Paramaribo", "l": {"n": "Chan Santokhi", "b": 1959, "o": 2020, "t": "Prezident"}},
    "🇸🇪 Shvetsiya": {"tz": "Europe/Stockholm", "l": {"n": "Ulf Kristersson", "b": 1963, "o": 2022, "t": "Bosh vazir"}},
    "🇨🇭 Shveytsariya": {"tz": "Europe/Zurich", "l": {"n": "Viola Amherd", "b": 1962, "o": 2024, "t": "Prezident"}},
    "🇸🇾 Siriya": {"tz": "Asia/Damascus", "l": {"n": "Bashar al-Assad", "b": 1965, "o": 2000, "t": "Prezident"}},
    "🇹🇯 Tojikiston": {"tz": "Asia/Dushanbe", "l": {"n": "Emomali Rahmon", "b": 1952, "o": 1994, "t": "Prezident"}},
    "🇹🇿 Tanzaniya": {"tz": "Africa/Dar_es_Salaam", "l": {"n": "Samia Suluhu Hassan", "b": 1960, "o": 2021, "t": "Prezident"}},
    "🇹🇭 Tailand": {"tz": "Asia/Bangkok", "l": {"n": "Paetongtarn Shinawatra", "b": 1986, "o": 2024, "t": "Bosh vazir"}},
    "🇹🇬 Togo": {"tz": "Africa/Lome", "l": {"n": "Victoire Tomegah Dogbé", "b": 1967, "o": 2020, "t": "Bosh vazir"}},
    "🇹🇴 Tonga": {"tz": "Pacific/Tongatapu", "l": {"n": "Siaosi Sovaleni", "b": 1965, "o": 2021, "t": "Bosh vazir"}},
    "🇹🇹 Trinidad va Tobago": {"tz": "America/Port_of_Spain", "l": {"n": "Keith Rowley", "b": 1949, "o": 2015, "t": "Bosh vazir"}},
    "🇹🇳 Tunisia": {"tz": "Africa/Tunis", "l": {"n": "Kaïs Saïed", "b": 1958, "o": 2019, "t": "Prezident"}},
    "🇹🇷 Turkiya": {"tz": "Europe/Istanbul", "l": {"n": "Recep Tayyip Erdoğan", "b": 1954, "o": 2014, "t": "Prezident"}},
    "🇹🇲 Turkmaniston": {"tz": "Asia/Ashgabat", "l": {"n": "Serdar Berdimuhamedow", "b": 1981, "o": 2022, "t": "Prezident"}},
    "🇹🇻 Tuvalu": {"tz": "Pacific/Funafuti", "l": {"n": "Feleti Teo", "b": 1962, "o": 2024, "t": "Bosh vazir"}},
    "🇺🇬 Uganda": {"tz": "Africa/Kampala", "l": {"n": "Yoweri Museveni", "b": 1944, "o": 1986, "t": "Prezident"}},
    "🇺🇦 Ukraina": {"tz": "Europe/Kiev", "l": {"n": "Volodymyr Zelenskyy", "b": 1978, "o": 2019, "t": "Prezident"}},
    "🇦🇪 Birlashgan Arab Amirliklari": {"tz": "Asia/Dubai", "l": {"n": "Mohammed bin Zayed", "b": 1961, "o": 2022, "t": "Prezident"}},
    "🇬🇧 Birlashgan Qirollik": {"tz": "Europe/London", "l": {"n": "Keir Starmer", "b": 1962, "o": 2024, "t": "Bosh vazir"}},
    "🇺🇸 AQSH": {"tz": "America/New_York", "l": {"n": "Joe Biden", "b": 1942, "o": 2021, "t": "Prezident"}},
    "🇺🇾 Urugvay": {"tz": "America/Montevideo", "l": {"n": "Luis Lacalle Pou", "b": 1973, "o": 2020, "t": "Prezident"}},
    "🇺🇿 Oʻzbekiston": {"tz": "Asia/Tashkent", "l": {"n": "Shavkat Mirziyoyev", "b": 1957, "o": 2016, "t": "Prezident"}},
    "🇻🇺 Vanuatu": {"tz": "Pacific/Efate", "l": {"n": "Jotham Napat", "b": 1975, "o": 2023, "t": "Bosh vazir"}},
    "🇻🇦 Vatikan": {"tz": "Europe/Vatican", "l": {"n": "Papa Fransisk", "b": 1936, "o": 2013, "t": "Papa"}},
    "🇻🇪 Venesuela": {"tz": "America/Caracas", "l": {"n": "Nicolás Maduro", "b": 1962, "o": 2013, "t": "Prezident"}},
    "🇻🇳 Vetnam": {"tz": "Asia/Ho_Chi_Minh", "l": {"n": "Phạm Minh Chính", "b": 1958, "o": 2021, "t": "Bosh vazir"}},
    "🇾🇪 Ye'men": {"tz": "Asia/Aden", "l": {"n": "Rashad al-Alimi", "b": 1954, "o": 2022, "t": "Prezident"}},
    "🇿🇲 Zambiya": {"tz": "Africa/Lusaka", "l": {"n": "Hakainde Hichilema", "b": 1962, "o": 2021, "t": "Prezident"}},
    "🇿🇼 Zimbabwe": {"tz": "Africa/Harare", "l": {"n": "Emmerson Mnangagwa", "b": 1942, "o": 2017, "t": "Prezident"}}
}

PAGE_SIZE = 25

def build_country_menu(context: ContextTypes.DEFAULT_TYPE):
    country_names = sorted(COUNTRIES.keys())
    page = context.user_data.get("page", 0)
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    current_countries = country_names[start:end]

    mid = (len(current_countries) + 1) // 2
    left_col = current_countries[:mid]
    right_col = current_countries[mid:]

    buttons = []
    for i in range(max(len(left_col), len(right_col))):
        row = []
        if i < len(left_col):
            row.append(InlineKeyboardButton(left_col[i], callback_data=f"country:{left_col[i]}"))
        else:
            row.append(InlineKeyboardButton(" ", callback_data="noop"))
        if i < len(right_col):
            row.append(InlineKeyboardButton(right_col[i], callback_data=f"country:{right_col[i]}"))
        else:
            row.append(InlineKeyboardButton(" ", callback_data="noop"))
        buttons.append(row)

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Oldingi", callback_data="prev"))
    if end < len(country_names):
        nav_row.append(InlineKeyboardButton("➡️ Keyingi", callback_data="next"))
    if nav_row:
        buttons.append(nav_row)

    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["page"] = 0
    reply_markup = build_country_menu(context)
    await update.message.reply_text("🌍 Davlatni tanlang:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "noop":
        return

    if data == "prev":
        context.user_data["page"] = max(0, context.user_data.get("page", 0) - 1)
        reply_markup = build_country_menu(context)
        await query.edit_message_text("🌍 Davlatni tanlang:", reply_markup=reply_markup)
    elif data == "next":
        context.user_data["page"] = context.user_data.get("page", 0) + 1
        reply_markup = build_country_menu(context)
        await query.edit_message_text("🌍 Davlatni tanlang:", reply_markup=reply_markup)
    elif data.startswith("country:"):
        name = data.split(":", 1)[1]
        c = COUNTRIES.get(name)
        if not c:
            await query.edit_message_text("❌ Ma'lumot topilmadi.")
            return

        try:
            tz = pytz.timezone(c["tz"])
            now = datetime.now(tz)
        except Exception:
            now = datetime.now(pytz.utc)

        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        weekday = now.strftime("%A")
        weekdays_uz = {
            "Monday": "Dushanba", "Tuesday": "Seshanba", "Wednesday": "Chorshanba",
            "Thursday": "Payshanba", "Friday": "Juma", "Saturday": "Shanba", "Sunday": "Yakshanba"
        }
        weekday_uz = weekdays_uz.get(weekday, weekday)

        leader = c["l"]
        current_year = datetime.now().year
        age = current_year - leader["b"]

        msg = (
            f"📅 **Sana**: {date_str}\n"
            f"⏰ **Vaqt**: {time_str}\n"
            f"📆 **Kun**: {weekday_uz}\n\n"
            f"**{leader['t']}**: {leader['n']}\n"
            f"**Yoshi**: {age}\n"
            f"**Tug'ilgan yili**: {leader['b']}\n"
            f"**Lavozimga kirgan yili**: {leader['o']}"
        )
        await query.edit_message_text(msg, parse_mode="Markdown")

def main():
    logging.basicConfig(level=logging.INFO)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("✅ Bot ishga tushdi! 2 ustunli sahifalangan rejim.")
    app.run_polling()

if __name__ == "__main__":
    main()
