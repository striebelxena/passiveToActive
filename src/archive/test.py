import language_tool_python

print("test")


# Initialisieren Sie das LanguageTool
tool = language_tool_python.LanguageTool("en-US")

# Ihr Text, den Sie überprüfen möchten
text = "In order to determine whether such a controller or processor is offering goods or services to data subjects who are in the Union, one should ascertain it whether whether it is apparent that the controller or processor envisages offering services to data subjects in one or more Member States in the Union."
# Überprüfung des Textes
matches = tool.check(text)

# Ausgabe der gefundenen Fehler
print("\nGefundene Fehler:")
for match in matches:
    print(match)

# Automatische Korrektur des Textes
corrected_text = language_tool_python.utils.correct(text, matches)
print("\nKorrigierter Text:")
print(corrected_text)
