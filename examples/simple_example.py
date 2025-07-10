# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Simple example of usage."""

from mfd_connect import RPyCConnection
from mfd_win_registry import WindowsRegistry, PropertyType, BuffersAttribute

conn = RPyCConnection(ip="x.x.x.x")
winreg_obj = WindowsRegistry(connection=conn)
print(
    winreg_obj.get_registry_path(
        path="hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
    )
)
print(winreg_obj.add_registry_key("SLOT 2 Port 1", "FecMode", "2"))
print(winreg_obj.remove_registry_key("SLOT 2 Port 1", "FecMode"))
print(winreg_obj.check_registry_key("SLOT 2 Port 1", "FecMode", "0"))
print(
    winreg_obj.registry_exists(
        path="hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}"
    )
)
print(winreg_obj.set_feature("SLOT 4 Port 2", "FecMode", "1"))
print(winreg_obj.set_feature("SLOT 4 Port 2", "Version", "42", PropertyType.DWORD))
print(winreg_obj.remove_feature("SLOT 4 Port 2", "Version"))
print(winreg_obj.get_feature_possible_values("SLOT 4 Port 2", "FecMode"))
print(
    winreg_obj.get_registry_childitems(
        path="hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
    )
)
print(winreg_obj.check_proset_registry())
print(
    winreg_obj.remove_registry_subkeys(
        path="hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\icea"
    )
)
print(winreg_obj.get_rx_buffers("SLOT 4 Port 2"))
print(winreg_obj.get_rx_buffers("SLOT 4 Port 2", BuffersAttribute.MIN))
print(winreg_obj.get_tx_buffers("SLOT 4 Port 2"))
print(winreg_obj.get_tx_buffers("SLOT 4 Port 2", BuffersAttribute.MAX))
print(winreg_obj.get_feature_enum("SLOT 4 Port 2", "*SpeedDuplex"))
print(winreg_obj.get_feature_list("SLOT 4 Port 2"))
print(winreg_obj.get_feature_list("SLOT 4 Port 2", False))
print(
    winreg_obj.set_itemproperty(
        path="hklm:\\system\\CurrentControlSet\\enum\\PCI\\VEN_8086&DEV_1592&SUBSYS_00028086&REV_01\\000100FFFF\
                00000001\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties",
        name="MessageNumberLimit",
        value="33",
    )
)
