Physical Interface
==================

`Input`, `Output` and `Wire` objects within a chip are implemented using a
synchronous interconnect bus. The details of the interconnect bus are described
here. This section will be of most use to developers who want to integrate a
*Chips* design into a larger design, or to generate an HDL wrapper to support a
*Chips* design in new hardware.

.. aafig::
 
  rst >-o------------------------------+
        |                              |
  clk >-+--o------------------------+  |
        |  |                        |  |
        |  |   +-----------+        |  |      +--------------+
        |  |   | TX        |        |  |      | RX           |
        |  +-->+           |        |  +----->+              |
        |      |           |        |         |              |
        +----->+           |        +-------->+              |
               |           |                  |              |
               |           | "<bus_name>"     |              |
               |           +=================>+              |
               |           | "<bus_name>_stb" |              |
               |           +----------------->+              |
               |           | "<bus_name>_ack" |              |
               |           +<-----------------+              |
               |           |                  |              |
               +-----------+                  +--------------+
 
Global Signals
--------------
 
+------+-----------+------+-------------+
| Name | Direction | Type | Description |
+------+-----------+------+-------------+
| clk  |   input   | bit  |    Clock    |
+------+-----------+------+-------------+
| rst  |   input   | bit  |    Reset    |
+------+-----------+------+-------------+

 
Interconnect Signals
--------------------

+----------------+-----------+------+-----------------------------------------------------------+
|      Name      | Direction | Type |                        Description                        |
+----------------+-----------+------+-----------------------------------------------------------+
|   <bus_name>   |  TX to RX | bus  |                        Payload Data                       |
+----------------+-----------+------+-----------------------------------------------------------+
| <bus_name>_stb |  TX to RX | bit  | '1' indicates that payload data is valid and TX is ready. |
+----------------+-----------+------+-----------------------------------------------------------+
| <bus_name>_ack |  TX to RX | bit  |              '1' indicates that RX is ready.              |
+----------------+-----------+------+-----------------------------------------------------------+

 
Interconnect Bus Transaction
----------------------------
 
1. Both transmitter and receiver **shall** be synchronised to the 0 to 1 transition of `clk`.
#. If `rst` is set to 1, upon the 0 to 1 transition of `clk` the transmitter **shall** terminate any active bus transaction and set `<bus_name>_stb` to 0.
#. If `rst` is set to 1, upon the 0 to 1 transition of `clk` the receiver **shall** terminate any active bus transaction and set `<bus_name>_ack` to 0.
#. If `rst` is set to 0, normal operation **shall** commence.
#. The transmitter **may** insert wait states on the bus by setting `<bus_name>_stb` to 0.
#. The transmitter **shall** set `<bus_name>_stb` to 1 to signify that data is valid.
#. Once `<bus_name>_stb` has been set to 1, it **shall** remain at 1 until the transaction completes.
#. The transmitter **shall** ensure that `<bus_name>` contains valid data for the entire period that `<bus_name>_stb` is 1.
#. The transmitter **may** set `<bus_name>` to any value when `<bus_name>_stb` is 0.
#. The receiver **may** insert wait states on the bus by setting `<bus_name>_ack` to 0.
#. The receiver **shall** set `<bus_name>_ack` to 1 to signify that it is ready to receive data.
#. Once `<bus_name>_ack` has been set to 1, it **shall** remain at 1 until the transaction completes.
#. Whenever `<bus_name>_stb` is 1 and `<bus_name>_ack` are 1, a bus transaction **shall** complete on the following 0 to 1 transition of `clk`.
#. Both the transmitter and receiver **may** commence a new transaction without inserting any wait states.
#. The receiver **may** delay a transaction by inserting wait states until the transmitter indicates that data is available.
#. The transmitter **shall** not delay a transaction by inserting wait states until the receiver is ready to accept data. Deadlock would occur if both the transmitter and receiver delayed a transaction until the other was ready.
 
.. aafig::
 
        "rst"            _______________________________________
                           _   _   _   _   _   _   _   _   _   _ 
        "clk"            _| |_| |_| |_| |_| |_| |_| |_| |_| |_| 
                         _______________________________________                       
       "<bus_name>"           | VALID |                                                         
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                               _______
       "<bus_name>_stb"  _____|       |_________________________
                                   ___
       "<bus_name>_ack"  _________|   |_________________________
         
                               ^^^^ "RX adds wait states"
                               ||||
         
                                   ^^^^  "Data transfers"
                                   ||||
         
        "rst"            _______________________________________
                           _   _   _   _   _   _   _   _   _   _
        "clk"            _| |_| |_| |_| |_| |_| |_| |_| |_| |_| 
                         _______________________________________                       
       "<bus_name>"           | VALID |                         
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                   ___
       "<bus_name>_stb"  _________|   |_________________________
                               _______
       "<bus_name>_ack"  _____|       |_________________________
         
         
                               ^^^^ "TX adds wait states"
                               ||||
         
                                   ^^^^  "Data transfers"
                                   ||||


        "rst"            _______________________________________
                           __    __    __    __    __    __    _
        "clk"            _|  |__|  |__|  |__|  |__|  |__|  |__|
         
                         _______________________________________                       
       "<bus_name>"             | D0        | D1  | D2  |       
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                       _________________
       "<bus_name>_stb"  _____________|                 |_______
                                 _______________________
       "<bus_name>_ack"  _______|                       |_______
         
                                ^^^^ "TX adds wait states"
                                ||||
                                       ^^^^  "Data transfers"
                                       ||||
                                            ^^^^ "stb and ack needn't return to 0 between data words"
                                            ||||

..
 
 
