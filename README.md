### String-Editor-Sonic-Unleashed-PS2

Esta herramienta permite visualizar y editar los strings del juego de forma organizada y segura, ideal para mods o traducciones.

El programa funciona a partir de un archivo XML que contiene los strings codificados en hex, por lo que no trabaja directamente sobre los archivos del juego.

**Dependencia:**
Para obtener el archivo XML necesario, se debe usar la herramienta **FCO_Tool (Full Release)** compartida en github por el usuario **Hedgeturd**.

Todo el crédito por la extracción de strings de un FCO a un XML va para él y su herramienta.

**Uso:**
1. Genera el archivo XML usando la herramienta **FCO_Tool (Full Release)** de **Hedgeturd**.
2. Abre el XML con el String Editor.
3. El programa visualizará todos los textos codificados.
4. Para decodificar los textos use el botón **Editor Tabla** y cree una tabla a partir de la fuente que acompaña el **FCO**, si la fuente contiene mas de un estilo use el símbolo **$** como separador (Puede usar herramientas como **Puyo Tools** para visualizar la fuente).
6. Abra la tabla creada
7. Edita a tu gusto
8. Guarda los cambios y el XML quedará listo para ser convertido nuevamente a FCO con FCO_Tool.

**IMPORTANTE**
Sólamente se puede editar con los caracteres disponibles de la fuente, si desea usar mas caracteres deberá usar otra fuente pero deberá asociar esa fuente al FCO.

**Nota sobre el desarrollo:**
Este programa fue desarrollado con asistencia de IA, utilizando **Gemini AI de Google** para la estructuración y corrección del código.
