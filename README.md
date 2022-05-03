## **Interconnect plugin V1**
This plugin simulates data transmission energy in on-chip wires in the Accelergy+Timeloop infrastructure. State of the art accelerators may consume up to 5% of overall system energy moving data through on-chip wiring, so modeling all components of the system is vital for tools such as Accelergy+Timeloop to find optimal accelerator designs and workload mappings.

This plugin uses the equations in [1] to simulate the transfer energy in networks and between local buffers. Networking energy is determined by the length of NoC wires, while inter-buffer data movement energy is determined assuming data traverses entire components according to Accelergy's area model.

# Intall me:
We install automatically via pip. From inside this directory, run
```
pip install .
```
# Run me:
Under the "local" heading of highest architecture level of any architecture specification in Timeloop+Accelergy, add the following component. This will instantiate a wire primitive component for use by Timeloop.
```
    local:
        - name: wire
          class: wire
          attributes:
            delay_penalty: 0          # Required: Permitted delay. 0 for min-delay wire, 1 for 2x delay...
            technology: 32            # REQUIRED: Technology node in nm
            voltage: 0.5              # OPTIONAL: Swing voltage of wire. Default low-swing 0.5V
            switching_activity: 0.25  # OPTIONAL: Switching activity of wire. Generally somewhere between
                                      #           0 and 0.5. Dependent on the workload: For probability P
                                      #           of a single bit being on in the workload of interest,
                                      #           Sw_Activity = (P)(1-P).
```

References:
[1] K. Banerjee and A. Mehrotra, “A power-optimal repeater insertion methodology for global interconnects in nanometer designs,” IEEE Transactions on Electron Devices, vol. 49, no. 11, pp. 2001–2007, 2002
