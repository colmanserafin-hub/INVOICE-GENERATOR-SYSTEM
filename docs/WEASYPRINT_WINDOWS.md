WeasyPrint on Windows — quick notes

WeasyPrint relies on native libraries (GTK, Cairo, Pango, GObject/GLib). On Windows the easiest way to get these is via MSYS2 packages.

1) Install MSYS2
- Download and install from https://www.msys2.org/

2) Open "MSYS2 MinGW 64-bit" shell and update packages:

```bash
pacman -Syu
# restart the shell if prompted
pacman -Su
```

3) Install required libs (64-bit):

```bash
pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-cairo mingw-w64-x86_64-pango mingw-w64-x86_64-glib mingw-w64-x86_64-libffi
```

4) Add the MSYS2 `mingw64\bin` directory to your PATH (or run scripts from MSYS2 environment). Example path:

```
C:\msys64\mingw64\bin
```

5) Reinstall WeasyPrint in your virtualenv (if previously installed):

```powershell
& .venv\Scripts\Activate.ps1
pip install --force-reinstall weasyprint
```

6) Test a simple conversion (from venv):

```powershell
python -c "from weasyprint import HTML; HTML(string='<p>test</p>').write_pdf('test.pdf')"
```

If you prefer not to install native libs, the project already provides a ReportLab fallback which generates PDFs without needing platform native libraries.

More info and troubleshooting:
- Official first-steps: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html
- Windows troubleshooting: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows