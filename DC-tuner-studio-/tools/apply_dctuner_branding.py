from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]

# Fail closed: this script is limited to branding/configuration files.
def replace_exact(path: Path, old: str, new: str, expected: int = 1):
    text = path.read_text()
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} occurrences, found {count} for {old!r}")
    path.write_text(text.replace(old, new))

# Root/module naming only; no firmware or protocol files are touched.
replace_exact(ROOT / "settings.gradle", "include ':version'", "rootProject.name = 'DCtuneRstudio'\ninclude ':java_console'\nproject(':java_console').projectDir = new File(rootRelativePath + 'java_console')\ninclude ':version'")
(ROOT / "java_console" / "build.gradle").write_text("""// Compatibility aggregator: the functional console remains the :ui module.\ntasks.named('build') {\n    dependsOn ':ui:build'\n}\n""")
replace_exact(ROOT / "java_console/ui/build.gradle", "archiveFileName = 'rusefi_console.jar'", "archiveFileName = 'DCtuneRstudio.jar'")
replace_exact(ROOT / "java_console/ui/build.gradle", "destinationDirectory = file(\"${rootDir}/console\")", "destinationDirectory = file(\"${rootDir}/java_console/build/libs\")")

# Branding API keeps copy centralized and leaves technical package names intact.
brand_java = ROOT / "java_console/ui/src/main/java/com/rusefi/DCtuneRstudioBrand.java"
brand_java.parent.mkdir(parents=True, exist_ok=True)
brand_java.write_text("""package com.rusefi;\n\nimport javax.swing.*;\nimport javax.swing.border.LineBorder;\nimport java.awt.*;\n\n/** Visual identity constants only; ECU behavior and communication remain unchanged. */\npublic final class DCtuneRstudioBrand {\n    public static final String APP_NAME = \"DCtuneRstudio\";\n    public static final String COMPANY = \"DC Laboratory\";\n    public static final String STARTUP_TITLE = APP_NAME + \" — Diagnóstico y Sintonización Automotriz\";\n    public static final String STARTUP_SUBTITLE = COMPANY + \" — Versión PC\";\n    public static final String ABOUT_URL = \"https://github.com/dcg0/DC-tuner-studio-\";\n    public static final Color NEON_BLUE = Color.decode(\"#00ccff\");\n    public static final Color NEON_BLUE_DARK = Color.decode(\"#0099ff\");\n    public static final Color NEON_RED = Color.decode(\"#ff2244\");\n    public static final Color NEON_RED_LIGHT = Color.decode(\"#ff4466\");\n    public static final Color BACKGROUND = Color.decode(\"#050508\");\n    public static final Color SURFACE = Color.decode(\"#0f0f1a\");\n    public static final Color TEXT = Color.decode(\"#e8e8f0\");\n    public static final Color HIGHLIGHT = Color.decode(\"#00ff99\");\n    public static final Color BORDER = Color.decode(\"#1a1a2e\");\n\n    private DCtuneRstudioBrand() {}\n\n    public static void applyTheme() {\n        UIManager.put(\"Panel.background\", SURFACE);\n        UIManager.put(\"OptionPane.background\", SURFACE);\n        UIManager.put(\"MenuBar.background\", BACKGROUND);\n        UIManager.put(\"Menu.background\", BACKGROUND);\n        UIManager.put(\"MenuItem.background\", SURFACE);\n        UIManager.put(\"Menu.foreground\", TEXT);\n        UIManager.put(\"MenuItem.foreground\", TEXT);\n        UIManager.put(\"Button.background\", NEON_BLUE_DARK);\n        UIManager.put(\"Button.foreground\", Color.WHITE);\n        UIManager.put(\"Button.focusedBorderColor\", NEON_RED);\n        UIManager.put(\"Component.borderColor\", BORDER);\n        UIManager.put(\"TitlePane.background\", BACKGROUND);\n        UIManager.put(\"TitlePane.foreground\", TEXT);\n        UIManager.put(\"TabbedPane.selectedBackground\", NEON_RED);\n        UIManager.put(\"TabbedPane.underlineColor\", NEON_BLUE);\n        UIManager.put(\"TabbedPane.selectedUnderlineColor\", NEON_RED_LIGHT);\n    }\n\n    public static Border themedBorder() {\n        return new LineBorder(NEON_BLUE, 1, true);\n    }\n}\n""")

# Startup/main window visible copy and title behavior.
replace_exact(ROOT / "java_console/ui/src/main/java/com/rusefi/Launcher.java", "log.info(\"rusEFI UI console \" + UiVersion.CONSOLE_VERSION);", "log.info(DCtuneRstudioBrand.APP_NAME + \" UI console \" + UiVersion.CONSOLE_VERSION);")
replace_exact(ROOT / "java_console/ui/src/main/java/com/rusefi/Launcher.java", '"Java 11 or newer is required to run rusEFI console\\n"', '"Java 11 or newer is required to run DCtuneRstudio\\n"')
replace_exact(ROOT / "java_console/ui/src/main/java/com/rusefi/StartupFrame.java", 'String title = UiProperties.getWhiteLabel() + " console " + Launcher.CONSOLE_VERSION;', 'String title = DCtuneRstudioBrand.STARTUP_TITLE;')
replace_exact(ROOT / "java_console/ui/src/main/java/com/rusefi/StartupFrame.java", 'String projectName = PropertiesHolder.getProperty("default_project_name", "rusEFI");', 'String projectName = PropertiesHolder.getProperty("default_project_name", DCtuneRstudioBrand.APP_NAME);')
replace_exact(ROOT / "java_console/ui/src/main/java/com/rusefi/ui/console/MainFrame.java", 'String consoleVersion = "Console " + Launcher.CONSOLE_VERSION;', 'String consoleVersion = DCtuneRstudioBrand.APP_NAME + " " + Launcher.CONSOLE_VERSION;')
# MainFrame shares com.rusefi package import via existing package hierarchy; add explicit import.
main = ROOT / "java_console/ui/src/main/java/com/rusefi/ui/console/MainFrame.java"
text = main.read_text()
if "import com.rusefi.DCtuneRstudioBrand;" not in text:
    text = text.replace("import com.rusefi.ConsoleUI;", "import com.rusefi.ConsoleUI;\nimport com.rusefi.DCtuneRstudioBrand;")
main.write_text(text)

# Add About to the primary menu; rusEFI is intentionally confined to this dialog.
needle = '        menuBar.add(shortcutsItem);\n\n        frame.getFrame().setJMenuBar(menuBar);'
replacement = '''        menuBar.add(shortcutsItem);\n\n        JMenuItem aboutItem = new JMenuItem("Acerca de");\n        aboutItem.addActionListener(e -> JOptionPane.showMessageDialog(\n                frame.getFrame(),\n                DCtuneRstudioBrand.APP_NAME + "\\n" + DCtuneRstudioBrand.COMPANY +\n                        "\\nBasado en rusEFI — Código abierto GPL v3\\n" + DCtuneRstudioBrand.ABOUT_URL,\n                "Acerca de " + DCtuneRstudioBrand.APP_NAME,\n                JOptionPane.INFORMATION_MESSAGE));\n        menuBar.add(aboutItem);\n\n        frame.getFrame().setJMenuBar(menuBar);'''
if needle not in text:
    raise RuntimeError("MainFrame menu insertion point not found")
main.write_text(text.replace(needle, replacement))

# Global theme hook.
replace_exact(ROOT / "java_console/ui/src/main/java/com/rusefi/ui/basic/UiHelper.java", "        UIManager.put(\"TitlePane.buttonSize\", new Dimension(45, 30));", "        com.rusefi.DCtuneRstudioBrand.applyTheme();\n        UIManager.put(\"TitlePane.buttonSize\", new Dimension(45, 30));")

# Shared visible default only; ECU signatures and internal identifiers are untouched.
replace_exact(ROOT / "java_console/shared_io/src/main/resources/shared_io.properties", "default_project_name=rusEFI", "default_project_name=DCtuneRstudio")

# Static web-facing brand shell, intentionally separate from ECU communication code.
ui = ROOT / "ui"
(ui / "public").mkdir(parents=True, exist_ok=True)
(ui / "public/index.html").write_text("""<!doctype html>\n<html lang=\"es\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>DCtuneRstudio</title><link rel=\"stylesheet\" href=\"styles.css\"></head>\n<body><header><div class=\"brand\"><span>DC</span><strong>tuneR</strong><small>studio</small></div><div class=\"company\">DC Laboratory</div></header><main><p class=\"eyebrow\">Diagnóstico y Sintonización Automotriz</p><h1>DCtuneRstudio</h1><p class=\"lead\">Interfaz de escritorio para conectar, diagnosticar y ajustar tu ECU.</p><a class=\"button\" href=\"#conectar\">Conectar ECU</a><section id=\"conectar\"><article><h2>Panel de conexión</h2><p>La lógica de comunicación permanece en la consola Java oficial de esta distribución.</p></article><article><h2>Gráficas en tiempo real</h2><div class=\"chart\"><i></i><b></b></div></article></section></main><footer>© 2026 DC Laboratory</footer></body></html>\n""")
(ui / "public/styles.css").write_text(""":root{--blue:#00ccff;--blue2:#0099ff;--red:#ff2244;--red2:#ff4466;--bg:#050508;--surface:#0f0f1a;--text:#e8e8f0;--green:#00ff99;--line:#1a1a2e}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(circle at 20% 0%,#102332 0,#050508 45%);color:var(--text);font:16px Inter,system-ui,sans-serif}header{height:74px;padding:0 6vw;display:flex;align-items:center;justify-content:space-between;background:linear-gradient(100deg,var(--blue2),var(--red));box-shadow:0 0 30px #00ccff55}.brand{font-size:28px;font-weight:800;letter-spacing:-1px}.brand span{color:var(--blue);text-shadow:0 0 12px #00ccff}.brand strong{color:var(--red2);text-shadow:0 0 12px #ff2244}.brand small{color:white;font-size:13px;margin-left:3px}.company{font-size:13px;letter-spacing:.14em;text-transform:uppercase}main{max-width:1080px;margin:0 auto;padding:11vh 6vw}h1{font-size:clamp(44px,8vw,92px);margin:12px 0;background:linear-gradient(90deg,var(--blue),var(--red2));-webkit-background-clip:text;color:transparent}.eyebrow{color:var(--green);text-transform:uppercase;letter-spacing:.14em}.lead{max-width:560px;font-size:21px;color:#b5b6c4}.button{display:inline-block;margin:26px 0;padding:13px 22px;background:var(--blue2);border:1px solid transparent;border-radius:8px;color:#fff;text-decoration:none;font-weight:700;transition:.2s}.button:hover{border-color:var(--red2);box-shadow:0 0 20px #ff224477}section{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:50px}article{padding:22px;background:var(--surface);border:1px solid var(--blue);border-radius:12px;box-shadow:0 0 18px #00ccff18}h2{margin-top:0}.chart{height:130px;border-bottom:1px solid var(--line);position:relative;overflow:hidden;background:repeating-linear-gradient(0deg,transparent 0 31px,#1a1a2e 32px)}.chart i,.chart b{position:absolute;inset:50% 0 auto;height:3px;display:block;transform:skewY(-13deg) rotate(-8deg);background:var(--blue);box-shadow:0 0 9px var(--blue)}.chart b{top:72%;background:var(--red2);box-shadow:0 0 9px var(--red2);transform:skewY(16deg) rotate(5deg)}footer{text-align:center;padding:28px;color:#8b8c9b;border-top:1px solid var(--line)}@media(max-width:700px){section{grid-template-columns:1fr}.company{display:none}}""")
(ui / "README.md").write_text("""# DCtuneRstudio UI\n\nStatic branded shell for the DC Laboratory identity. ECU communication, maps, autotune, calculations and data I/O remain implemented by the Java console in `java_console/ui`.\n""")

# Deterministic branded raster assets (logos/icons/splash/banner), replacing only brand artwork.
font_candidates = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
font_path = next((p for p in font_candidates if Path(p).exists()), None)
def font(size): return ImageFont.truetype(font_path, size) if font_path else ImageFont.load_default()
def make_logo(path, size=(900, 240), icon=False):
    im = Image.new("RGBA", size, (5,5,8,255)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((8,8,size[0]-8,size[1]-8), radius=28, outline=(0,204,255,255), width=4)
    d.ellipse((28,28,180,180), outline=(255,34,68,255), width=8)
    d.text((66,66), "DC", fill=(0,204,255,255), font=font(48))
    if not icon: d.text((210,65), "tuneR", fill=(255,68,102,255), font=font(72)); d.text((595,82), "studio", fill=(232,232,240,255), font=font(38))
    im.save(path)
def make_splash(path):
    im = Image.new("RGBA", (1280,720), (5,5,8,255)); d=ImageDraw.Draw(im)
    for x in range(1280):
        t=x/1279; c=(int(0*(1-t)+255*t),int(204*(1-t)+34*t),int(255*(1-t)+68*t),255); d.line((x,0,x,16),fill=c,width=16)
    d.text((130,270),"DCtuneRstudio",fill=(232,232,240,255),font=font(86)); d.text((135,390),"Diagnóstico y Sintonización Automotriz",fill=(0,204,255,255),font=font(32)); d.text((135,470),"DC Laboratory — Versión PC",fill=(255,68,102,255),font=font(30)); im.save(path)

autoupdate = ROOT / "java_console/autoupdate/src/main/resources/com/rusefi"; autoupdate.mkdir(parents=True, exist_ok=True)
core = ROOT / "java_console/core_ui/src/main/resources/com/rusefi"; core.mkdir(parents=True, exist_ok=True)
trigger = ROOT / "java_console/trigger-ui/src/main/resources/com/rusefi"; trigger.mkdir(parents=True, exist_ok=True)
web = ui / "public"
make_logo(autoupdate/"logo.png"); make_logo(core/"appicon.png", (256,256), True); make_logo(trigger/"logo.png"); make_logo(trigger/"logo_alphax.png"); make_logo(trigger/"logo_mre.png"); make_logo(trigger/"logo_proteus.png"); make_logo(trigger/"logo_tutomo.png")
make_splash(ROOT / "java_console/ui/src/main/resources/com/rusefi/splash.png")
make_logo(ROOT / "java_console/ui/src/main/resources/com/rusefi/banner.png", (1200,260))
make_logo(web/"favicon.ico", (256,256), True)
make_logo(web/"logo-dctuner.png")

print("DCtuneRstudio branding applied")
""
