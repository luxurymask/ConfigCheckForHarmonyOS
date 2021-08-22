# ConfigCheckForHarmonyOS
A python project for check the configs for HarmonyOS app.

Usage:
python3 ReadFromConfigJson.py [your_harmony.app]

Then check app_table.html and app_image.html, which are generated on the same path of the script.

![image](https://github.com/luxurymask/ConfigCheckForHarmonyOS/blob/main/example_image/example_imagehtml.png)
![image](https://github.com/luxurymask/ConfigCheckForHarmonyOS/blob/main/example_image/example_tablehtml.png)

Note that I cannot find strings.json from the app package, so for now the description may not be correct. I guess the "$string:xxx" is processed with runtime parsing, i'll check it out.
