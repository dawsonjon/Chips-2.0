Schematix
=========


Introduction
------------

Schematix is a graphical program for designing FPGAs using schematic entry. FPGA designs can be created graphically by placing components, and connecting them together using standardised buses. Schematix includes many predefined components. You can add your own componentsby:

+ Creating them in a schematic.
+ Creating them from a C program.
+ Writing them yourself in VHDL.

Screenshots
-----------

.. image:: https://raw.github.com/dawsonjon/Schematix/master/screenshots.png


What is Implemented
-------------------

+ A tree based component manager using meta-tags to categorise components.
+ A schematic editor.
+ Automatic generation of VHDL.
+ GHDL and gtkWave integration.
+ A base set of components.
+ C based component description.
+ Integrated reStructuredText based documentation browser.

What is not Implemented
-----------------------

+ Better GUI features.

  - Documentation Editor.
  - Preferences dialog.

+ Synthesisable floating point.
+ More built in components.
