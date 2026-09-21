package com.rusefi;

import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.LineBorder;
import java.awt.*;

/** Visual identity constants only; ECU behavior and communication remain unchanged. */
public final class DCtuneRstudioBrand {
    public static final String APP_NAME = "DCtuneRstudio";
    public static final String COMPANY = "DC Laboratory";
    public static final String STARTUP_TITLE = APP_NAME + " — Diagnóstico y Sintonización Automotriz";
    public static final String STARTUP_SUBTITLE = COMPANY + " — Versión PC";
    public static final String ABOUT_URL = "https://github.com/dcg0/DC-tuner-studio-";
    public static final Color NEON_BLUE = Color.decode("#00ccff");
    public static final Color NEON_BLUE_DARK = Color.decode("#0099ff");
    public static final Color NEON_RED = Color.decode("#ff2244");
    public static final Color NEON_RED_LIGHT = Color.decode("#ff4466");
    public static final Color BACKGROUND = Color.decode("#050508");
    public static final Color SURFACE = Color.decode("#0f0f1a");
    public static final Color TEXT = Color.decode("#e8e8f0");
    public static final Color HIGHLIGHT = Color.decode("#00ff99");
    public static final Color BORDER = Color.decode("#1a1a2e");

    private DCtuneRstudioBrand() {}

    public static void applyTheme() {
        UIManager.put("Panel.background", SURFACE);
        UIManager.put("OptionPane.background", SURFACE);
        UIManager.put("MenuBar.background", BACKGROUND);
        UIManager.put("Menu.background", BACKGROUND);
        UIManager.put("MenuItem.background", SURFACE);
        UIManager.put("Menu.foreground", TEXT);
        UIManager.put("MenuItem.foreground", TEXT);
        UIManager.put("Button.background", NEON_BLUE_DARK);
        UIManager.put("Button.foreground", Color.WHITE);
        UIManager.put("Button.focusedBorderColor", NEON_RED);
        UIManager.put("Component.borderColor", BORDER);
        UIManager.put("TitlePane.background", BACKGROUND);
        UIManager.put("TitlePane.foreground", TEXT);
        UIManager.put("TabbedPane.selectedBackground", NEON_RED);
        UIManager.put("TabbedPane.underlineColor", NEON_BLUE);
        UIManager.put("TabbedPane.selectedUnderlineColor", NEON_RED_LIGHT);
    }

    public static Border themedBorder() {
        return new LineBorder(NEON_BLUE, 1, true);
    }
}
