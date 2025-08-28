# Disclaimer

The Code as well as the contents of the README after this Disclaimer is more than 99% AI generated, using the Coursor fork of Visual Studio Code and Claude Sonnet 4 as the underlying LLM.

# Theme Color Editor

A Python GUI application for editing Windows Forms control color themes. This program provides a visual interface to modify color definitions for various UI controls and export the changes as a JSON file.

## Features

- **Visual Color Table**: Displays all available controls in a table format with their current color values
- **Interactive Color Picker**: Double-click on any color cell to open a color picker dialog
- **Theme Name Editing**: Modify the theme name through a text field
- **Export Functionality**: Save modified themes as JSON files in the exact format as the original
- **Reset Capability**: Reset all changes back to the original theme
- **Error Handling**: Graceful handling of file loading and saving errors

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python installation)

## Usage

1. **Run the Program**:
   ```bash
   python theme_editor.py
   ```

2. **Load Theme**: The program automatically loads `sample-theme.json` from the same directory

3. **Edit Colors**:
   - Double-click on any color cell in the table
   - Use the color picker dialog to select a new color
   - Click "OK" to apply the change

4. **Modify Theme Name**: Edit the theme name in the text field at the top

5. **Export Theme**: Click "Export Theme" to save your changes as a new JSON file

6. **Reset Changes**: Click "Reset to Original" to revert all changes

## File Format

The program works with JSON files in the following format:

```json
{
    "Name": "Theme Name",
    "Theme": {
        "ControlName.Property": {
            "R": 255,
            "G": 128,
            "B": 64
        },
        "AnotherControl.Property": {
            "Name": "NamedColor"
        }
    }
}
```

## Supported Color Formats

- **RGB Values**: `{"R": 255, "G": 128, "B": 64}`
- **Named Colors**: `{"Name": "DimGray"}` (converted to RGB when edited)

## Controls Supported

The program supports all controls found in the sample theme:
- Default colors (BackColor, ForeColor)
- LinkLabel colors (ActiveLinkColor, DisabledLinkColor, LinkColor)
- Form controls (CheckBox, ComboBox, TextBox, Button, etc.)
- DataGridView colors
- Custom controls (ColourableTabControl, ExpanderTile, etc.)

## Error Handling

- Missing `sample-theme.json` file
- Invalid JSON format
- File save errors
- Color picker cancellation

## Notes

- Named colors are converted to RGB format when edited
- The program preserves the exact JSON structure of the original file
- All changes are made in memory until exported
- The original file is never modified directly

