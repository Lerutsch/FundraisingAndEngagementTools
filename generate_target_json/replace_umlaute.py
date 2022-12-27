main_folder = r"C:\Users\OleksiiMakarenko\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK Finance " \
              r"- Documents\Integration"
# folder = "Paypal"
# file_name = '20221223_20221226_paypal_export.csv'
folder = "Bank"
file_name = '20221001-20221226-umsatz.csv'
file_path = main_folder + '\\' + folder + '\\' + file_name

# x = open(file_path, "r", encoding='utf-8')
x = open(file_path, "r", encoding='ansi')
special_char_map = {ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('ß'): 'ss'}

s = x.read()
s = s.translate(special_char_map)
print(s)
x.close()

x = open(file_path, "w", encoding="utf-8")
x.write(s)
x.close()
