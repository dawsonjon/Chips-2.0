Schematix - a graphical front end for Chips
===========================================

Schematix is a schematic editor that creates chips. The schematic primitives 
are derived from Chips modules.

Features Implemented
--------------------

* Component selector.
* Component creation, deletion and parameter editing.
* Interconnecting components.
* Loading and Saving Schematics.
* Undo, Redo.

Features Yet to be Implemented
------------------------------

* Integrate user defined editor for chips code.
* Generate Chips code.
* Import Chips code as component.
* Import a sub-schematic as a component.

Techinical Details
------------------

* Implemented in Python.
* Uses wxPython for gui framework.
* Schematic editor is based on wxPython FloatCanvas.
* Dependencies are Python, wxPython, NumPy (required by floatcanvas)
