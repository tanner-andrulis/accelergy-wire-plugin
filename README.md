## **Interconnect plugin V1**
TODO TODO TODO

# Intall me:

cd into this directory

pip install .

# Run me:
1. Add the file wire.yaml to your components directory in an Accelery/Timeloop design

2. Add something like this somewhere in your .yaml arch spec:
```
    local:
        - name: wire
          class: wire
          attributes:
            delay_penalty: 1
            technology: 32
```
