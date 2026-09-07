### String-Editor-Sonic-Unleashed-PS2

Esta herramienta de Python permite visualizar y editar los strings del juego Sonic Unleashed-PS2 de forma organizada, cómoda y segura, ideal para mods o traducciones, está inspirada en otras herramientas de Sonic Unleashed de otras plataformas.

El programa funciona a partir de un archivo XML que contiene los strings codificados en hex, por lo que no trabaja directamente sobre los archivos del juego.

**Dependencia:**
Para obtener el archivo XML necesario, se debe usar la herramienta **FCO_Tool (Full Release)** compartida en github por el usuario **Hedgeturd**.

Todo el crédito por la extracción de strings de un FCO a un XML va para él y su herramienta.

**Uso:**
1. Genere por aparte el archivo **XML** a partir de un **FCO** usando la herramienta **FCO_Tool (Full Release)** de **Hedgeturd**.
2. Abre el XML con el String Editor.
3. El programa visualizará todos los textos codificados.
4. Para decodificar los textos use el botón **Editor Tabla** y cree una tabla a partir de la fuente **SVR** que acompaña el **FCO**, si la fuente contiene mas de un estilo use el símbolo **$** como separador (Puede usar herramientas como **Puyo Tools** para visualizar la fuente).
6. Abra la tabla creada y automáticamente se visualizarán los textos, si no se aprecian correctamente verifique y edite la tabla y con el botón **Actualizar Tabla** podrá actualizar los cambios en tiempo real.
7. Edita a tu gusto
8. Guarda los cambios y el XML quedará listo para ser convertido nuevamente a FCO con FCO_Tool.

**IMPORTANTE**
El carácter **/** representa un salto de línea y se carga por defecto

El checkbox de **Triple Espacio (Auto)** se usa para los subtítulos

Sólamente se puede editar con los caracteres disponibles de la fuente, si desea usar mas caracteres puede usar otra fuente pero deberá asociar esa fuente al FCO.

**Nota:**
Este programa fue desarrollado con asistencia de IA, utilizando **Gemini AI de Google** para la estructuración y corrección del código, el código es completamente libre pero si hace alguna correción o lo comparte en algún otro lado mantén los créditos.
