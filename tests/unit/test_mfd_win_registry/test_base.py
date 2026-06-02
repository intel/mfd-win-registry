# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Tests for `mfd_win_registry` package."""

import pytest
from textwrap import dedent
from unittest.mock import patch
from mfd_connect import RPyCConnection
from mfd_connect.base import ConnectionCompletedProcess
from mfd_typing import OSName
from mfd_win_registry.base import WindowsRegistry
from mfd_win_registry.constants import PropertyType, BuffersAttribute
from mfd_win_registry.exceptions import WindowsRegistryException


class TestMfdWinRegistry:
    expected = {
        "DriverDesc": "Broadcom NetXtreme Gigabit Ethernet",
        "ProviderName": "Broadcom",
        "DriverDateData": "{0, 0, 31, 192}",
        "DriverDate": "2-20-2018",
        "DriverVersion": "20.8.0.0",
        "InfPath": "oem13.inf",
        "InfSection": "BCM5703G_LHinst.NTamd64.6.1",
        "MatchingDeviceId": "PCI\\VEN_14E4&DEV_165F&SUBSYS_1F5B1028",
        "*TransmitBuffers": "200",
        "*ReceiveBuffers": "200",
        "RxCoalescingTicks": "10",
        "TxCoalescingTicks": "30",
        "RxMaxCoalescedFrames": "5",
        "TxMaxCoalescedFrames": "200",
        "AdminSettingsLevel": "2",
        "JumboPacketMode": "1",
        "*IfType": "6",
        "*MediaType": "0",
        "*PhysicalMediaType": "0",
        "BusType": "5",
        "Characteristics": "132",
        "*InterruptModeration": "1",
        "*TCPUDPChecksumOffloadIPv4": "3",
        "*PriorityVLANTag": "3",
        "VlanID": "0",
        "*FlowControl": "4",
        "*JumboPacket": "1500",
        "*SpeedDuplex": "0",
        "*WakeOnMagicPacket": "1",
        "*WakeOnPattern": "1",
        "WolSpeed": "0",
        "WireSpeed": "1",
        "IfTypePreStart": "6",
        "NetworkInterfaceInstallTimestamp": "133188066793669822",
        "InstallTimeStamp": "{231, 7, 1, 0}",
        "DeviceInstanceID": "PCI\\VEN_14E4&DEV_165F&SUBSYS_1F5B1028&REV_00\\0000B083FECFA1AA00",
        "ComponentId": "PCI\\VEN_14E4&DEV_165F&SUBSYS_1F5B1028",
        "NetCfgInstanceId": "{E4D3514E-4003-48CA-A268-7BF63596CEA4}",
        "NetLuidIndex": "32775",
        "PSPath": "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\Current\
        ControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0011",
        "PSParentPath": "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\Current\
        ControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}",
        "PSChildName": "0011",
        "PSDrive": "HKLM",
        "PSProvider": "Microsoft.PowerShell.Core\\Registry",
    }
    output = dedent(
        """\nName                      DisplayName                    DisplayValue                   \
        RegistryKeyword RegistryValue  \n----                      -----------                    \
        ------------                   --------------- -------------  \nNIC2                      \
        Speed & Duplex                 10 Mbps Half Duplex            *SpeedDuplex    {1}            \n\n\n"""
    )
    interface_id = "11"
    new_feature_list = {
        "DriverDesc": "Intel(R) Ethernet Network Adapter E810-C-Q2",
        "ProviderName": "Intel",
        "DriverDateData": "{0, 64, 246, 183}",
        "DriverDate": "4-18-2023",
        "DriverVersion": "1.13.236.0",
        "InfPath": "oem12.inf",
        "InfSection": "F1592",
        "IncludedInfs": "{pci.inf}",
        "MatchingDeviceId": "PCI\\VEN_8086&DEV_1592&SUBSYS_00028086",
        "LogLinkStateEvent": "51",
        "UniversalInstall": "1",
        "IceaInstallDir": "C:\\Windows\\System32\\DriverStore\\FileRepository\\icea68.inf_amd64_842fd73bafcfa6da",
        "VMQSupported": "1",
        "CoInstallFlag": "539492416",
        "*IfType": "6",
        "*MediaType": "0",
        "*PhysicalMediaType": "14",
        "BusType": "5",
        "Characteristics": "132",
        "Port1FunctionNumber": "0",
        "*FlowControl": "0",
        "*TransmitBuffers": "512",
        "*ReceiveBuffers": "512",
        "*TCPChecksumOffloadIPv4": "3",
        "*TCPChecksumOffloadIPv6": "3",
        "*UDPChecksumOffloadIPv4": "3",
        "*UDPChecksumOffloadIPv6": "3",
        "*IPChecksumOffloadIPv4": "3",
        "ITR": "65535",
        "*PriorityVLANTag": "3",
        "*InterruptModeration": "1",
        "*LsoV2IPv4": "1",
        "*LsoV2IPv6": "1",
        "*JumboPacket": "1514",
        "LinkOnIntDown": "1",
        "AllowNoFECModulesInAuto": "0",
        "*NumRssQueues": "16",
        "MaxNumRssQueuesPerVPort": "4",
        "*RSSProfile": "4",
        "*RSS": "1",
        "*RssBaseProcNumber": "0",
        "*NumaNodeId": "65535",
        "*MaxRssProcessors": "32",
        "*NetworkDirect": "1",
        "*NetworkDirectTechnology": "1",
        "RdmaRoceFrameSize": "1024",
        "RdmaMaxVfsEnabled": "0",
        "RdmaVfPreferredResourceProfile": "0",
        "VlanId": "0",
        "*QOS": "1",
        "*SRIOV": "1",
        "MDDAutoResetVFs": "0",
        "*EncapsulatedPacketTaskOffload": "1",
        "*EncapsulatedPacketTaskOffloadNvgre": "1",
        "*EncapsulatedPacketTaskOffloadVxlan": "1",
        "*VxlanUDPPortNumber": "4789",
        "*EncapOverhead": "0",
        "*VMQ": "1",
        "*VMQVlanFiltering": "1",
        "*RssOnHostVPorts": "1",
        "*UsoIPv4": "1",
        "*UsoIPv6": "1",
        "*PtpHardwareTimestamp": "0",
        "*SoftwareTimestamp": "0",
        "*SpeedDuplex": "0",
        "FecMode": "2",
        "IfTypePreStart": "6",
        "NetworkInterfaceInstallTimestamp": "133268775009839512",
        "InstallTimeStamp": "{231, 7, 4, 0}",
        "DeviceInstanceID": "PCI\\VEN_8086&DEV_1592&SUBSYS_00028086&REV_01\\000100FFFF00000001",
        "ComponentId": "PCI\\VEN_8086&DEV_1592&SUBSYS_00028086",
        "NetCfgInstanceId": "{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}",
        "NetLuidIndex": "32773",
        "Port": "1",
        "CoInstallFlagSet": "1",
        "IntelDCBxInstalled": "1",
        "PerformanceProfile": "7",
        "Version": "43",
        "PSPath": "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\Current\
        ControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005",
        "PSParentPath": "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\Current\
        ControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}",
        "PSChildName": "0005",
        "PSDrive": "HKLM",
        "PSProvider": "Microsoft.PowerShell.Core\\Registry",
    }
    child_items = {
        (
            "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\"
            "AdditionalConfiguration"
        ): {
            "WPP_GUID": "{BDD04ED8-F4BB-4B36-BB76-D2FFC123EC67}",
            "FW_LOG_NAME": "E810_Log",
            "PSPath": (
                "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet"
                "\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\AdditionalConfiguration"
            ),
            "PSParentPath": (
                "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\"
                "CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
            ),
            "PSChildName": "AdditionalConfiguration",
            "PSDrive": "HKLM",
            "PSProvider": "Microsoft.PowerShell.Core\\Registry",
        },
        "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\DcbCfg": {
            "DcbPfcAdvertise": "1",
            "DcbPfcEnable": "1",
            "DcbPfcWilling": "1",
            "DcbPgAdvertise": "1",
            "DcbPgEnable": "1",
            "DcbPgWilling": "1",
            "Bw0DetailTx": "Bandwidth Group 0",
            "Bw0DetailRx": "Bandwidth Group 0",
            "Bw0PercentageRx": "13",
            "Bw0PercentageTx": "13",
            "Bw1DetailTx": "Bandwidth Group 1",
            "Bw1DetailRx": "Bandwidth Group 1",
            "Bw1PercentageRx": "13",
            "Bw1PercentageTx": "13",
            "Bw2DetailTx": "Bandwidth Group 2",
            "Bw2DetailRx": "Bandwidth Group 2",
            "Bw2PercentageRx": "13",
            "Bw2PercentageTx": "13",
            "Bw3DetailTx": "Bandwidth Group 3",
            "Bw3DetailRx": "Bandwidth Group 3",
            "Bw3PercentageRx": "13",
            "Bw3PercentageTx": "13",
            "Bw4DetailTx": "Bandwidth Group 4",
            "Bw4DetailRx": "Bandwidth Group 4",
            "Bw4PercentageRx": "12",
            "Bw4PercentageTx": "12",
            "Bw5DetailTx": "Bandwidth Group 5",
            "Bw5DetailRx": "Bandwidth Group 5",
            "Bw5PercentageRx": "12",
            "Bw5PercentageTx": "12",
            "Bw6DetailTx": "Bandwidth Group 6",
            "Bw6DetailRx": "Bandwidth Group 6",
            "Bw6PercentageRx": "12",
            "Bw6PercentageTx": "12",
            "Bw7DetailTx": "Bandwidth Group 7",
            "Bw7DetailRx": "Bandwidth Group 7",
            "Bw7PercentageRx": "12",
            "Bw7PercentageTx": "12",
            "DcbxSubtype": "3",
            "OperDcbxSubtype": "3",
            "OsControlled": "0",
            "PSPath": (
                "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet"
                "\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\DcbCfg"
            ),
            "PSParentPath": (
                "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\"
                "CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
            ),
            "PSChildName": "DcbCfg",
            "PSDrive": "HKLM",
            "PSProvider": "Microsoft.PowerShell.Core\\Registry",
        },
        ("hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Linkage"): {
            "RootDevice": "{{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}}",
            "Export": "{\\Device\\{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}}",
            "UpperBind": "{lltdio, MsLldp, Ndisuio, RasPppoe}",
            "FilterList": (
                "{{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}-{EA24CD6C-D17A-4348-9190-09F0D5BE83DD}-0000, "
                "{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}-{3BFD7820-D65C-4C1B-9FEA-983A019639EA}-0000, "
                "{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}-{EA24CD6C-D17A-4348-9190-09F0D5BE83DD}-0001, "
                "{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}-{7DAF2AC8-E9F6-4765-A842-F1F5D2501341}-0000}"
            ),
            "PSPath": (
                "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\"
                "control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Linkage"
            ),
            "PSParentPath": (
                "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\"
                "CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
            ),
            "PSChildName": "Linkage",
            "PSDrive": "HKLM",
            "PSProvider": "Microsoft.PowerShell.Core\\Registry",
        },
        "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi": {
            "Service": "icea",
            "PSPath": (
                "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\"
                "control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi"
            ),
            "PSParentPath": (
                "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\"
                "CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
            ),
            "PSChildName": "Ndi",
            "PSDrive": "HKLM",
            "PSProvider": "Microsoft.PowerShell.Core\\Registry",
        },
        (
            "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\"
            "0005\\NicSwitches"
        ): {},
        (
            "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\"
            "0005\\PROSetNdi"
        ): {},
    }
    proset_registry = {
        "HKLM:\\Software\\Intel\\Basedrivers": {},
        "HKLM:\\Software\\Intel\\NETWORK_SERVICES": {
            "Sync": (
                "Sync\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            ),
            "Timeout": "3000",
            "PSPath": "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\Software\\Intel\\NETWORK_SERVICES",
            "PSParentPath": "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\Software\\Intel",
            "PSChildName": "NETWORK_SERVICES",
            "PSDrive": "HKLM",
            "PSProvider": "Microsoft.PowerShell.Core\\Registry",
        },
        "HKLM:\\Software\\Intel\\Prounstl": {},
        "HKLM:\\Software\\Intel\\PSIS": {},
    }
    path = r"hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"

    @pytest.fixture()
    def winreg(self, mocker):
        conn = mocker.create_autospec(RPyCConnection)
        conn.get_os_name.return_value = OSName.WINDOWS
        winreg_obj = WindowsRegistry(connection=conn)
        mocker.stopall()
        return winreg_obj

    def test_get_registry_path(self, winreg):
        output = dedent(
            """
            \n\n
            DriverDesc                          : Intel(R) Ethernet Network Adapter E810-C-Q2
            ProviderName                        : Intel
            DriverDateData                      : {0, 64, 246, 183...}
            DriverDate                          : 4-18-2023
            DriverVersion                       : 1.13.236.0
            InfPath                             : oem12.inf
            InfSection                          : F1592
            IncludedInfs                        : {pci.inf}
            MatchingDeviceId                    : PCI\\VEN_8086&DEV_1592&SUBSYS_00028086
            LogLinkStateEvent                   : 51
            UniversalInstall                    : 1
            IceaInstallDir                      : C:\\Windows\\System32\\DriverStore\
\\FileRepository\\icea68.inf_amd64_842fd73bafcfa6da
            VMQSupported                        : 1
            CoInstallFlag                       : 539492416
            *IfType                             : 6
            *MediaType                          : 0
            *PhysicalMediaType                  : 14
            BusType                             : 5
            Characteristics                     : 132
            Port1FunctionNumber                 : 0
            *FlowControl                        : 0
            *TransmitBuffers                    : 512
            *ReceiveBuffers                     : 512
            *TCPChecksumOffloadIPv4             : 3
            *TCPChecksumOffloadIPv6             : 3
            *UDPChecksumOffloadIPv4             : 3
            *UDPChecksumOffloadIPv6             : 3
            *IPChecksumOffloadIPv4              : 3
            ITR                                 : 65535
            *PriorityVLANTag                    : 3
            *InterruptModeration                : 1
            *LsoV2IPv4                          : 1
            *LsoV2IPv6                          : 1
            *JumboPacket                        : 1514
            LinkOnIntDown                       : 1
            AllowNoFECModulesInAuto             : 0
            *NumRssQueues                       : 16
            MaxNumRssQueuesPerVPort             : 4
            *RSSProfile                         : 4
            *RSS                                : 1
            *RssBaseProcNumber                  : 0
            *NumaNodeId                         : 65535
            *MaxRssProcessors                   : 32
            *NetworkDirect                      : 1
            *NetworkDirectTechnology            : 1
            RdmaRoceFrameSize                   : 1024
            RdmaMaxVfsEnabled                   : 0
            RdmaVfPreferredResourceProfile      : 0
            VlanId                              : 0
            *QOS                                : 1
            *SRIOV                              : 1
            MDDAutoResetVFs                     : 0
            *EncapsulatedPacketTaskOffload      : 1
            *EncapsulatedPacketTaskOffloadNvgre : 1
            *EncapsulatedPacketTaskOffloadVxlan : 1
            *VxlanUDPPortNumber                 : 4789
            *EncapOverhead                      : 0
            *VMQ                                : 1
            *VMQVlanFiltering                   : 1
            *RssOnHostVPorts                    : 1
            *UsoIPv4                            : 1
            *UsoIPv6                            : 1
            *PtpHardwareTimestamp               : 0
            *SoftwareTimestamp                  : 0
            *SpeedDuplex                        : 0
            FecMode                             : 1
            IfTypePreStart                      : 6
            NetworkInterfaceInstallTimestamp    : 133268775009839512
            InstallTimeStamp                    : {231, 7, 4, 0...}
            DeviceInstanceID                    : PCI\\VEN_8086&DEV_1592&SUBSYS_00028086&REV_01\\000100FFFF00000001
            ComponentId                         : PCI\\VEN_8086&DEV_1592&SUBSYS_00028086
            NetCfgInstanceId                    : {81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}
            NetLuidIndex                        : 32773
            Port                                : 1
            CoInstallFlagSet                    : 1
            IntelDCBxInstalled                  : 1
            PerformanceProfile                  : 7
            PSPath                              : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system
                                                  \\CurrentControlSet\\control\\class\
                                                  \\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005
            PSParentPath                        : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system
                                                  \\CurrentControlSet\\control\\class\
                                                  \\{4D36E972-E325-11CE-BFC1-08002BE10318}
            PSChildName                         : 0005
            PSDrive                             : HKLM
            PSProvider                          : Microsoft.PowerShell.Core\\Registry"""
        )
        expected = {
            "DriverDesc": "Intel(R) Ethernet Network Adapter E810-C-Q2",
            "ProviderName": "Intel",
            "DriverDateData": "{0, 64, 246, 183, 94, 20, 219, 1}",
            "DriverDate": "4-18-2023",
            "DriverVersion": "1.13.236.0",
            "InfPath": "oem12.inf",
            "InfSection": "F1592",
            "IncludedInfs": "{pci.inf}",
            "MatchingDeviceId": "PCI\\VEN_8086&DEV_1592&SUBSYS_00028086",
            "LogLinkStateEvent": "51",
            "UniversalInstall": "1",
            "IceaInstallDir": "C:\\Windows\\System32\\DriverStore\\FileRepository\\icea68.inf_amd64_842fd73bafcfa6da",
            "VMQSupported": "1",
            "CoInstallFlag": "539492416",
            "*IfType": "6",
            "*MediaType": "0",
            "*PhysicalMediaType": "14",
            "BusType": "5",
            "Characteristics": "132",
            "Port1FunctionNumber": "0",
            "*FlowControl": "0",
            "*TransmitBuffers": "512",
            "*ReceiveBuffers": "512",
            "*TCPChecksumOffloadIPv4": "3",
            "*TCPChecksumOffloadIPv6": "3",
            "*UDPChecksumOffloadIPv4": "3",
            "*UDPChecksumOffloadIPv6": "3",
            "*IPChecksumOffloadIPv4": "3",
            "ITR": "65535",
            "*PriorityVLANTag": "3",
            "*InterruptModeration": "1",
            "*LsoV2IPv4": "1",
            "*LsoV2IPv6": "1",
            "*JumboPacket": "1514",
            "LinkOnIntDown": "1",
            "AllowNoFECModulesInAuto": "0",
            "*NumRssQueues": "16",
            "MaxNumRssQueuesPerVPort": "4",
            "*RSSProfile": "4",
            "*RSS": "1",
            "*RssBaseProcNumber": "0",
            "*NumaNodeId": "65535",
            "*MaxRssProcessors": "32",
            "*NetworkDirect": "1",
            "*NetworkDirectTechnology": "1",
            "RdmaRoceFrameSize": "1024",
            "RdmaMaxVfsEnabled": "0",
            "RdmaVfPreferredResourceProfile": "0",
            "VlanId": "0",
            "*QOS": "1",
            "*SRIOV": "1",
            "MDDAutoResetVFs": "0",
            "*EncapsulatedPacketTaskOffload": "1",
            "*EncapsulatedPacketTaskOffloadNvgre": "1",
            "*EncapsulatedPacketTaskOffloadVxlan": "1",
            "*VxlanUDPPortNumber": "4789",
            "*EncapOverhead": "0",
            "*VMQ": "1",
            "*VMQVlanFiltering": "1",
            "*RssOnHostVPorts": "1",
            "*UsoIPv4": "1",
            "*UsoIPv6": "1",
            "*PtpHardwareTimestamp": "0",
            "*SoftwareTimestamp": "0",
            "*SpeedDuplex": "0",
            "FecMode": "1",
            "IfTypePreStart": "6",
            "NetworkInterfaceInstallTimestamp": "133268775009839512",
            "InstallTimeStamp": "{231, 7, 4, 0, 5, 0, 11, 0, 17, 0, 36, 28, 0, 249, 0}",
            "DeviceInstanceID": "PCI\\VEN_8086&DEV_1592&SUBSYS_00028086&REV_01\\000100FFFF00000001",
            "ComponentId": "PCI\\VEN_8086&DEV_1592&SUBSYS_00028086",
            "NetCfgInstanceId": "{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}",
            "NetLuidIndex": "32773",
            "Port": "1",
            "CoInstallFlagSet": "1",
            "IntelDCBxInstalled": "1",
            "PerformanceProfile": "7",
            "PSPath": r"Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\system\CurrentControlSet\control"
            r"\class\{4D36E972-E325-11CE-BFC1-08002BE10318}\0005",
            "PSParentPath": r"Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\system\CurrentControlSet"
            r"\control\class\{4D36E972-E325-11CE-BFC1-08002BE10318}",
            "PSChildName": "0005",
            "PSDrive": "HKLM",
            "PSProvider": "Microsoft.PowerShell.Core\\Registry",
        }
        _reg_path = "hklm:\\system\\CurrentControlSet\\control\\class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\0011"
        r_comm = ConnectionCompletedProcess(return_code=0, args="command", stdout=output, stderr="stderr")
        # retrieve all data from registries
        r_ddd = ConnectionCompletedProcess(
            return_code=0, args="command", stdout="\n0\n64\n246\n183\n94\n20\n219\n1", stderr="stderr"
        )
        r_its = ConnectionCompletedProcess(
            return_code=0, args="command", stdout="\n231\n7\n4\n0\n5\n0\n11\n0\n17\n0\n36\n28\n0\n249\n0"
        )
        with patch.object(winreg._connection, "execute_powershell", side_effect=[r_comm, r_ddd, r_its]):
            result = winreg.get_registry_path(path=_reg_path)
            assert expected == result

    def test_get_registry_path_if_key_or_value_contains_space(self, winreg):
        output = dedent(
            """\n\n
            Initialization  : 0
            NVM             : 1
            IO              : 2
            Link Management : 3
            AQ Interface    : 4
            Manageability   : 5
            Infrastructure  : 6
            PSPath          : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\
\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\0005\\AdditionalConfiguration\\INTEL_LOG_CONFIGURATIONS
            PSParentPath    : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\
\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\0005\\AdditionalConfiguration
            PSChildName     : INTEL_LOG_CONFIGURATIONS
            PSDrive         : HKLM
            PSProvider      : Microsoft.PowerShell.Core\\Registry
            Test Key        : Test Value"""
        )
        expected = {
            "Initialization": "0",
            "NVM": "1",
            "IO": "2",
            "Link Management": "3",
            "AQ Interface": "4",
            "Manageability": "5",
            "Infrastructure": "6",
            "PSPath": (
                "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class"
                "\\{4d36e972-e325-11ce-bfc1-08002be10318}\\0005\\AdditionalConfiguration\\INTEL_LOG_CONFIGURATIONS"
            ),
            "PSParentPath": (
                "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class"
                "\\{4d36e972-e325-11ce-bfc1-08002be10318}\\0005\\AdditionalConfiguration"
            ),
            "PSChildName": "INTEL_LOG_CONFIGURATIONS",
            "PSDrive": "HKLM",
            "PSProvider": "Microsoft.PowerShell.Core\\Registry",
            "Test Key": "Test Value",
        }
        winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
            return_code=0, args="command", stdout=output, stderr="stderr"
        )
        assert expected == winreg.get_registry_path(
            path=r"hklm:\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\0005"
            r"\AdditionalConfiguration\INTEL_LOG_CONFIGURATIONS"
        )

    def test_get_registry_path_if_more_registry_value_available(self, winreg):
        output = dedent(
            """
            \n\n
            DriverDesc                          : Intel(R) Ethernet Network Adapter E810-C-Q2
            ProviderName                        : Intel
            DriverDateData                      : {0, 64, 246, 183...}
            InstallTimeStamp                    : {231, 7, 4, 0...}
            PSPath                              : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system
                                                  \\CurrentControlSet\\control\\class\
                                                  \\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005
            PSParentPath                        : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system
                                                  \\CurrentControlSet\\control\\class\
                                                  \\{4D36E972-E325-11CE-BFC1-08002BE10318}"""
        )
        expected = {
            "DriverDesc": "Intel(R) Ethernet Network Adapter E810-C-Q2",
            "ProviderName": "Intel",
            "DriverDateData": "{0, 64, 246, 183, 94, 20, 219, 1}",
            "InstallTimeStamp": "{231, 7, 4, 0, 5, 0, 11, 0, 17, 0, 36, 28, 0, 249, 0}",
            "PSPath": (
                r"Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\system\CurrentControlSet\control\class"
                r"\{4D36E972-E325-11CE-BFC1-08002BE10318}\0005"
            ),
            "PSParentPath": (
                r"Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\system\CurrentControlSet\control\class"
                r"\{4D36E972-E325-11CE-BFC1-08002BE10318}"
            ),
        }
        _reg_path = "hklm:\\system\\CurrentControlSet\\control\\class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\0011"
        r_comm = ConnectionCompletedProcess(return_code=0, args="command", stdout=output, stderr="stderr")
        # retrieve all data from registries
        r_ddd = ConnectionCompletedProcess(
            return_code=0, args="command", stdout="\n0\n64\n246\n183\n94\n20\n219\n1", stderr="stderr"
        )
        r_its = ConnectionCompletedProcess(
            return_code=0, args="command", stdout="\n231\n7\n4\n0\n5\n0\n11\n0\n17\n0\n36\n28\n0\n249\n0"
        )
        with patch.object(winreg._connection, "execute_powershell", side_effect=[r_comm, r_ddd, r_its]):
            result = winreg.get_registry_path(path=_reg_path)
            assert expected == result

    def test_check_registry_key(self, winreg):
        with (
            patch.object(winreg, "get_registry_path", return_value=self.expected),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            output = dedent(
                """\nName                      DisplayName                    DisplayValue                   \
                RegistryKeyword RegistryValue  \n----                      -----------                    \
                ------------                   --------------- -------------  \nNIC2                      \
                Speed & Duplex                 10 Mbps Half Duplex            *SpeedDuplex    {1}            \n\n\n"""
            )
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            winreg.check_registry_key(interface="NIC2", feature="*SpeedDuplex", value="1")

    def test_check_registry_key_not_set(self, winreg):
        with (
            patch.object(winreg, "get_registry_path", return_value=self.expected),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            output = dedent(
                """\nName                      DisplayName                    DisplayValue                   \
                RegistryKeyword RegistryValue  \n----                      -----------                    \
                ------------                   --------------- -------------  \nNIC2                      \
                Speed & Duplex                 10 Mbps Half Duplex            *SpeedDuplex    {1}            \n\n\n"""
            )
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            with pytest.raises(WindowsRegistryException, match="Failed: The value 0 is not set for \\*SpeedDuplex"):
                winreg.check_registry_key(interface="NIC2", feature="*SpeedDuplex", value="0")

    def test_add_registry_key(self, winreg):
        with (
            patch.object(winreg, "get_registry_path", return_value=self.expected),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
            patch.object(winreg, "check_registry_key", return_value=self.output),
        ):
            output = dedent(
                """\nName                      DisplayName                    DisplayValue                   \
                RegistryKeyword RegistryValue  \n----                      -----------                    \
                ------------                   --------------- -------------  \nNIC2                      \
                Speed & Duplex                 10 Mbps Half Duplex            *SpeedDuplex    {1}            \n\n\n"""
            )
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            winreg.add_registry_key(interface="NIC2", feature="*SpeedDuplex", value="0")

    def test_remove_registry_key_remove(self, winreg):
        with (
            patch.object(winreg, "get_registry_path", return_value=self.expected),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
            patch.object(winreg, "check_registry_key", return_value=self.output),
        ):
            output = dedent(
                """\nName                      DisplayName                    DisplayValue                   \
                RegistryKeyword RegistryValue  \n----                      -----------                    \
                ------------                   --------------- -------------  \nNIC2                      \
                Speed & Duplex                 10 Mbps Half Duplex            *SpeedDuplex    {1}            \n\n\n"""
            )
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            winreg.remove_registry_key(interface="NIC2", feature="*SpeedDuplex")

    def test_registry_exists(self, winreg):
        winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
            return_code=0, args="command", stdout="True\n", stderr="stderr"
        )
        assert winreg.registry_exists(
            path="hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}"
        )

    def test_registry_exists_fail(self, winreg):
        winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
            return_code=0, args="command", stdout="False\n", stderr="stderr"
        )
        assert not winreg.registry_exists(
            path="hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0100"
        )

    def test_set_feature(self, winreg):
        with (
            patch.object(winreg, "get_registry_path", return_value=self.expected),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="stdout", stderr="stderr"
            )
            winreg.set_feature(interface="SLOT 4 Port 2", feature="VlanID", value="2000")

    def test_set_feature_new(self, winreg):
        with (
            patch.object(winreg, "get_feature_list", return_value=self.expected),
            patch.object(winreg, "get_registry_path", return_value=self.new_feature_list),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="stdout", stderr=""
            )
            winreg.set_feature(
                interface="SLOT 4 Port 2",
                feature="Version",
                value="2000",
                prop_type=PropertyType.DWORD,
            )

    def test_set_feature_base_path(self, winreg):
        with (
            patch.object(winreg, "get_registry_path", return_value=self.new_feature_list),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="stdout", stderr="stderr"
            )
            winreg.set_feature(
                interface="SLOT 4 Port 2",
                feature="Version",
                value="2000",
                base_path=(
                    "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
                ),
            )

    def test_set_feature_new_fail(self, winreg):
        with (
            patch.object(winreg, "get_registry_path", return_value=self.new_feature_list),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=1, args="command", stdout="stdout", stderr="stderr"
            )
            with pytest.raises(
                WindowsRegistryException,
                match="Error in creating the feature: Version1",
            ):
                winreg.set_feature(interface="SLOT 4 Port 2", feature="Version1", value="2000")

    def test_remove_feature(self, winreg):
        with (
            patch.object(winreg, "get_registry_path", return_value=self.new_feature_list),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="stdout", stderr=""
            )
            winreg.remove_feature(interface="SLOT 4 Port 2", feature="Version")

    def test_remove_feature_fail(self, winreg):
        output_error = dedent(
            """remove-itemproperty : Property Version does not exist at path HKEY_LOCAL_MACHINE\
            \\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\
            \\0005.\nAt line:1 char:89\n+ ... e(512,3000);remove-itemproperty -path 'hklm:\\system\\CurrentControlSet ...
            +                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            + CategoryInfo          : InvalidArgument: (Version:String) [Remove-ItemProperty], PSArgumentException
            + FullyQualifiedErrorId : System.Management.Automation.PSArgumentException,Microsoft.PowerShell.\
            Commands.RemoveItemPropertyCommand\n \n", stdout_bytes=b'', stderr_bytes=b"remove-itemproperty : Property\
             Version does not exist at path HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\control\\class\
            \\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005.\nAt line:1 char:89\n+ ... e(512,3000);remove-itemproperty\
             -path 'hklm:\\system\\CurrentControlSet ...
            +                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            + CategoryInfo          : InvalidArgument: (Version:String) [Remove-ItemProperty], PSArgumentException
            + FullyQualifiedErrorId : System.Management.Automation.PSArgumentException,Microsoft.PowerShell.\
            Commands.RemoveItemPropertyCommand

            """  # noqa: E501
        )
        with (
            patch.object(winreg, "get_registry_path", return_value=self.new_feature_list),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=1, args="command", stdout="stdout", stderr=output_error
            )
            with pytest.raises(
                WindowsRegistryException,
                match="Error while removing the feature: Version on SLOT 4 Port 2 adapter.",
            ):
                winreg.remove_feature(interface="SLOT 4 Port 2", feature="Version")

    def test_remove_feature_base_path(self, winreg):
        with (
            patch.object(winreg, "get_registry_path", return_value=self.new_feature_list),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="stdout", stderr=""
            )
            winreg.remove_feature(
                interface="SLOT 4 Port 2",
                feature="Version",
                base_path=(
                    "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
                ),
            )

    def test_get_feature_possible_values_not_match(self, winreg):
        output_error = dedent(
            """Set-NetAdapterAdvancedProperty : No matching keyword value found. The following are valid keyword\
             values: 0, 1, 2, 3 At line:1 char:89
             + ... e(512,3000);Set-NetAdapterAdvancedProperty -Name "SLOT 4 Port 2" -Reg ...
            +                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                + CategoryInfo          : InvalidArgument: (MSFT_NetAdapter...D0023336D}:...):ROOT/\
                StandardCi...ertySettingData) [Set-NetAdapterAdvancedProperty], CimException\n    \
                + FullyQualifiedErrorId : Windows System Error 87,Set-NetAdapterAdvancedProperty\n \n"""
        )
        output = "0\n1\n2\n3\n"
        expected = [0, 1, 2, 3]
        winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
            return_code=0, args="command", stdout=output, stderr=output_error
        )
        assert expected == winreg.get_feature_possible_values(interface="SLOT 4 Port 2", feature="FecMode")

    def test_get_feature_possible_values_match_range_step(self, winreg):
        output_error = dedent(
            """
            Set-NetAdapterAdvancedProperty : Value must be within the range 0 - 256, in increments of 32
            At line:1 char:89
            + ... e(512,3000);Set-NetAdapterAdvancedProperty -Name "SLOT 4 Port 2" -Reg ...
            +                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
                + CategoryInfo          : InvalidArgument: (MSFT_NetAdapter...D0023336D}\
            :...):ROOT/StandardCi...ertySettingData) [Set-NetAdapterAdvancedProperty], CimException
                + FullyQualifiedErrorId : Windows System Error 87,Set-NetAdapterAdvancedProperty
            """
        )
        expected = [0, 32, 64, 96, 128, 160, 192, 224, 256]
        winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
            return_code=1, args="command", stdout="stdout", stderr=output_error
        )
        assert expected == winreg.get_feature_possible_values(interface="SLOT 4 Port 2", feature="*EncapOverhead")

    def test_get_feature_possible_values_match_range(self, winreg):
        output_error = dedent(
            """Set-NetAdapterAdvancedProperty : Value must be within the range 0 - 4096
            At line:1 char:89
            + ... e(512,3000);Set-NetAdapterAdvancedProperty -Name "SLOT 4 Port 2" -Reg ...
            +                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                + CategoryInfo          : InvalidArgument: (MSFT_NetAdapter...D0023336D}:...):/
            ROOT/StandardCi...ertySettingData) [Set-NetAdapterAdvancedProperty], CimException
                + FullyQualifiedErrorId : Windows System Error 87,Set-NetAdapterAdvancedProperty\n \n"""
        )
        expected = list(range(0, 4097, 1))
        winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
            return_code=1, args="command", stdout="stdout", stderr=output_error
        )
        assert expected == winreg.get_feature_possible_values(interface="SLOT 4 Port 2", feature="VlanId")

    def test_get_registry_childitems(self, winreg):
        with patch.object(
            winreg,
            "get_registry_path",
            side_effect=[each for each in self.child_items.values()],
        ):
            output = (
                "\nName                                                                        "
                "                                                 \n----                                    "
                "                                                                                     "
                "\nHKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-"
                "08002BE10318}\\0005\\AdditionalConfiguration\nHKEY_LOCAL_MACHINE\\system\\CurrentControlSet"
                "\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\DcbCfg                 \n"
                "HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}"
                "\\0005\\Linkage                \nHKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\control\\class\\"
                "{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi                    \nHKEY_LOCAL_MACHINE\\system"
                "\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\"
                "NicSwitches            \nHKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\control\\"
                "class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\PROSetNdi"
            )
            expected = {
                (
                    "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\"
                    "AdditionalConfiguration"
                ): {
                    "WPP_GUID": "{BDD04ED8-F4BB-4B36-BB76-D2FFC123EC67}",
                    "FW_LOG_NAME": "E810_Log",
                    "PSPath": (
                        "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet"
                        "\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\AdditionalConfiguration"
                    ),
                    "PSParentPath": (
                        "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\"
                        "CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
                    ),
                    "PSChildName": "AdditionalConfiguration",
                    "PSDrive": "HKLM",
                    "PSProvider": "Microsoft.PowerShell.Core\\Registry",
                },
                (
                    "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}"
                    "\\0005\\DcbCfg"
                ): {
                    "DcbPfcAdvertise": "1",
                    "DcbPfcEnable": "1",
                    "DcbPfcWilling": "1",
                    "DcbPgAdvertise": "1",
                    "DcbPgEnable": "1",
                    "DcbPgWilling": "1",
                    "Bw0DetailTx": "Bandwidth Group 0",
                    "Bw0DetailRx": "Bandwidth Group 0",
                    "Bw0PercentageRx": "13",
                    "Bw0PercentageTx": "13",
                    "Bw1DetailTx": "Bandwidth Group 1",
                    "Bw1DetailRx": "Bandwidth Group 1",
                    "Bw1PercentageRx": "13",
                    "Bw1PercentageTx": "13",
                    "Bw2DetailTx": "Bandwidth Group 2",
                    "Bw2DetailRx": "Bandwidth Group 2",
                    "Bw2PercentageRx": "13",
                    "Bw2PercentageTx": "13",
                    "Bw3DetailTx": "Bandwidth Group 3",
                    "Bw3DetailRx": "Bandwidth Group 3",
                    "Bw3PercentageRx": "13",
                    "Bw3PercentageTx": "13",
                    "Bw4DetailTx": "Bandwidth Group 4",
                    "Bw4DetailRx": "Bandwidth Group 4",
                    "Bw4PercentageRx": "12",
                    "Bw4PercentageTx": "12",
                    "Bw5DetailTx": "Bandwidth Group 5",
                    "Bw5DetailRx": "Bandwidth Group 5",
                    "Bw5PercentageRx": "12",
                    "Bw5PercentageTx": "12",
                    "Bw6DetailTx": "Bandwidth Group 6",
                    "Bw6DetailRx": "Bandwidth Group 6",
                    "Bw6PercentageRx": "12",
                    "Bw6PercentageTx": "12",
                    "Bw7DetailTx": "Bandwidth Group 7",
                    "Bw7DetailRx": "Bandwidth Group 7",
                    "Bw7PercentageRx": "12",
                    "Bw7PercentageTx": "12",
                    "DcbxSubtype": "3",
                    "OperDcbxSubtype": "3",
                    "OsControlled": "0",
                    "PSPath": (
                        "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet"
                        "\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\DcbCfg"
                    ),
                    "PSParentPath": (
                        "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\"
                        "CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
                    ),
                    "PSChildName": "DcbCfg",
                    "PSDrive": "HKLM",
                    "PSProvider": "Microsoft.PowerShell.Core\\Registry",
                },
                (
                    "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}"
                    "\\0005\\Linkage"
                ): {
                    "RootDevice": "{{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}}",
                    "Export": "{\\Device\\{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}}",
                    "UpperBind": "{lltdio, MsLldp, Ndisuio, RasPppoe}",
                    "FilterList": (
                        "{{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}-{EA24CD6C-D17A-4348-9190-09F0D5BE83DD}-0000, "
                        "{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}-{3BFD7820-D65C-4C1B-9FEA-983A019639EA}-0000, "
                        "{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}-{EA24CD6C-D17A-4348-9190-09F0D5BE83DD}-0001, "
                        "{81C379EE-5F3E-4BE8-B2CC-AF2D0023336D}-{7DAF2AC8-E9F6-4765-A842-F1F5D2501341}-0000}"
                    ),
                    "PSPath": (
                        "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\"
                        "control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Linkage"
                    ),
                    "PSParentPath": (
                        "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\"
                        "CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
                    ),
                    "PSChildName": "Linkage",
                    "PSDrive": "HKLM",
                    "PSProvider": "Microsoft.PowerShell.Core\\Registry",
                },
                "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi": {
                    "Service": "icea",
                    "PSPath": (
                        "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\"
                        "control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi"
                    ),
                    "PSParentPath": (
                        "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\"
                        "CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
                    ),
                    "PSChildName": "Ndi",
                    "PSDrive": "HKLM",
                    "PSProvider": "Microsoft.PowerShell.Core\\Registry",
                },
                (
                    "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\"
                    "0005\\NicSwitches"
                ): {},
                (
                    "hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\"
                    "0005\\PROSetNdi"
                ): {},
            }
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            assert expected == winreg.get_registry_childitems(
                path="hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
            )

    def test_check_proset_registry(self, winreg):
        with patch.object(winreg, "get_registry_childitems", return_value=self.proset_registry):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="stdout", stderr="stderr"
            )
            assert winreg.check_proset_registry()

    def test_check_proset_registry_key_not_present(self, winreg):
        with patch.object(winreg, "get_registry_childitems", return_value=self.child_items):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="stdout", stderr="stderr"
            )
            assert not winreg.check_proset_registry()

    def test_remove_registry_subkeys_registry_not_exists(self, winreg):
        with patch.object(winreg, "registry_exists", return_value=False):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="", stderr=""
            )
            with pytest.raises(WindowsRegistryException, match=f"Registry Path: {self.path} does not exist."):
                winreg.remove_registry_subkeys(
                    path=r"hklm:\system\CurrentControlSet\control\class\{4D36E972-E325-11CE-BFC1-08002BE10318}\0005"
                )

    def test_remove_registry_subkeys(self, winreg):
        with patch.object(winreg, "registry_exists", return_value=True):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="", stderr=""
            )
            winreg.remove_registry_subkeys(
                path="hklm:\\system\\CurrentControlSet\\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005"
            )

    def test_remove_registry_subkeys_fail(self, winreg):
        with patch.object(winreg, "registry_exists", return_value=True):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=1, args="command", stdout="", stderr="stderr"
            )
            with pytest.raises(
                WindowsRegistryException, match=f"Error while removing the registry subkeys from path: {self.path}"
            ):
                winreg.remove_registry_subkeys(
                    path=r"hklm:\system\CurrentControlSet\control\class\{4D36E972-E325-11CE-BFC1-08002BE10318}\0005"
                )

    def test_get_rx_buffers(self, winreg):
        with patch.object(winreg, "get_feature_list", return_value=self.new_feature_list):
            expected = 512
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="", stderr=""
            )
            assert expected == winreg.get_rx_buffers("SLOT 4 Port 2")

    def test_get_rx_buffers_attr(self, winreg):
        with patch.object(winreg, "_get_feature_attribute", return_value="4096"):
            expected = 4096
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="", stderr=""
            )
            assert expected == winreg.get_rx_buffers("SLOT 4 Port 2", BuffersAttribute.MAX)

    def test_get_tx_buffers(self, winreg):
        with patch.object(winreg, "get_feature_list", return_value=self.new_feature_list):
            expected = 512
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="", stderr=""
            )
            assert expected == winreg.get_tx_buffers("SLOT 4 Port 2")

    def test_get_tx_buffers_attr(self, winreg):
        with patch.object(winreg, "_get_feature_attribute", return_value="128"):
            expected = 128
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="", stderr=""
            )
            assert expected == winreg.get_tx_buffers("SLOT 4 Port 2", BuffersAttribute.MIN)

    def test_get_feature_attributes(self, winreg):
        with (
            patch.object(winreg, "_get_saved_params_path", return_value="Params"),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            output = dedent(
                """
                ParamDesc    : EncapOverhead
                default      : 0
                min          : 0
                max          : 256
                base         : 10
                step         : 32
                type         : int
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\*EncapOverhead
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapOverhead
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry

                ParamDesc    : Encapsulated Task Offload
                default      : 1
                type         : enum
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\
                \\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\\
                *EncapsulatedPacketTaskOffload
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapsulatedPacketTaskOffload
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry

                ParamDesc    : NVGRE Encapsulated Task Offload
                default      : 1
                type         : enum
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\\
                *EncapsulatedPacketTaskOffloadNvgre
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapsulatedPacketTaskOffloadNvgre
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry

                ParamDesc    : VXLAN Encapsulated Task Offload
                default      : 1
                type         : enum
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\\
                *EncapsulatedPacketTaskOffloadVxlan
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapsulatedPacketTaskOffloadVxlan
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry"""
            )
            expected = "enum"
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            assert expected == winreg._get_feature_attribute(
                interface="SLOT 4 Port 2", feature="*EncapsulatedPacketTaskOffloadVxlan", attribute_name="type"
            )

    def test_get_feature_not_present(self, winreg):
        with (
            patch.object(winreg, "_get_saved_params_path", return_value="Params"),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            output = dedent(
                """
                ParamDesc    : EncapOverhead
                default      : 0
                min          : 0
                max          : 256
                base         : 10
                step         : 32
                type         : int
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\*EncapOverhead
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapOverhead
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry

                ParamDesc    : Encapsulated Task Offload
                default      : 1
                type         : enum
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\
                \\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\\
                *EncapsulatedPacketTaskOffload
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapsulatedPacketTaskOffload
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry

                ParamDesc    : NVGRE Encapsulated Task Offload
                default      : 1
                type         : enum
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\\
                *EncapsulatedPacketTaskOffloadNvgre
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapsulatedPacketTaskOffloadNvgre
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry

                ParamDesc    : VXLAN Encapsulated Task Offload
                default      : 1
                type         : enum
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\\
                *EncapsulatedPacketTaskOffloadVxlan
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapsulatedPacketTaskOffloadVxlan
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry"""
            )
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            with pytest.raises(
                WindowsRegistryException, match="Cannot find the FecMode feature on SLOT 4 Port 2 adapter"
            ):
                winreg._get_feature_attribute(interface="SLOT 4 Port 2", feature="FecMode", attribute_name="type")

    def test_get_feature_attributes_not_present(self, winreg):
        with (
            patch.object(winreg, "_get_saved_params_path", return_value="Params"),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            output = dedent(
                """
                ParamDesc    : EncapOverhead
                default      : 0
                min          : 0
                max          : 256
                base         : 10
                step         : 32
                type         : int
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\*EncapOverhead
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapOverhead
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry

                ParamDesc    : Encapsulated Task Offload
                default      : 1
                type         : enum
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\
                \\control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\\
                *EncapsulatedPacketTaskOffload
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapsulatedPacketTaskOffload
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry

                ParamDesc    : NVGRE Encapsulated Task Offload
                default      : 1
                type         : enum
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\\
                *EncapsulatedPacketTaskOffloadNvgre
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapsulatedPacketTaskOffloadNvgre
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry

                ParamDesc    : VXLAN Encapsulated Task Offload
                default      : 1
                type         : enum
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\\
                *EncapsulatedPacketTaskOffloadVxlan
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params
                PSChildName  : *EncapsulatedPacketTaskOffloadVxlan
                PSDrive      : HKLM
                PSProvider   : Microsoft.PowerShell.Core\\Registry"""
            )
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            with pytest.raises(
                WindowsRegistryException,
                match="Cannot find attributes enum for \\*EncapOverhead feature on SLOT 4 Port 2 adapter",
            ):
                winreg._get_feature_attribute(
                    interface="SLOT 4 Port 2", feature="*EncapOverhead", attribute_name="enum"
                )

    def test_get_saved_params_path(self, winreg):
        with patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id):
            output = "\n\nPSChildName : Interfaces\n\nPSChildName : Params\n\n\n\n"
            expected = "Params"
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            assert expected == winreg._get_saved_params_path(interface="SLOT 4 Port 2")

    def test_get_saved_params_path_savedparams(self, winreg):
        with patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id):
            output = "\n\nPSChildName : Interfaces\n\nPSChildName : savedParams\n\n\n\n"
            expected = "savedParams"
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            assert expected == winreg._get_saved_params_path(interface="SLOT 4 Port 2")

    def test_get_saved_params_path_empty(self, winreg):
        with patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id):
            output = "\n\nPSChildName : Interfaces\n\n\n\n"
            expected = None
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr="stderr"
            )
            assert expected == winreg._get_saved_params_path(interface="SLOT 4 Port 2")

    def test_get_feature_enum(self, winreg):
        with (
            patch.object(winreg, "get_feature_list", return_value=self.expected),
            patch.object(winreg, "_get_saved_params_path", return_value="Params"),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            output = dedent(
                """
                0            : Auto Negotiation
                25000        : 25 Gbps Full Duplex
                50000        : 50 Gbps Full Duplex
                10           : 100 Gbps Full Duplex
                PSPath       : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\*SpeedDuplex\\enum
                PSParentPath : Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\
                control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\*SpeedDuplex
                PSChildName  : enum
                PSDrive      : HKLM\nPSProvider   : Microsoft.PowerShell.Core\\Registry\n\n\n\n"""
            )
            expected = {
                "0": "Auto Negotiation",
                "25000": "25 Gbps Full Duplex",
                "50000": "50 Gbps Full Duplex",
                "10": "100 Gbps Full Duplex",
                "PSPath": (
                    "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\control"
                    "\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\*SpeedDuplex\\enum"
                ),
                "PSParentPath": (
                    "Microsoft.PowerShell.Core\\Registry::HKEY_LOCAL_MACHINE\\system\\CurrentControlSet\\"
                    "control\\class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0005\\Ndi\\Params\\*SpeedDuplex"
                ),
                "PSChildName": "enum",
                "PSDrive": "HKLM",
                "PSProvider": "Microsoft.PowerShell.Core\\Registry",
            }
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout=output, stderr=""
            )
            assert expected == winreg.get_feature_enum("SLOT 4 Port 2", "*SpeedDuplex")

    def test_get_feature_enum_empty(self, winreg):
        with (
            patch.object(winreg, "get_feature_list", return_value=""),
            patch.object(winreg, "_get_saved_params_path", return_value="Params"),
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
        ):
            winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
                return_code=0, args="command", stdout="", stderr=""
            )
            with pytest.raises(
                WindowsRegistryException, match="Feature \\*SpeedDuplex not present on interface: SLOT 4 Port 2"
            ):
                assert winreg.get_feature_enum("SLOT 4 Port 2", "*SpeedDuplex")

    def test_get_feature_list(self, winreg):
        with (
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
            patch.object(winreg, "get_registry_path", return_value=self.expected),
        ):
            assert self.expected == winreg.get_feature_list("SLOT 4 Port 2")

    def test_get_feature_list_uncached(self, winreg):
        with (
            patch.object(winreg, "_convert_interface_to_index", return_value=self.interface_id),
            patch.object(winreg, "get_registry_path", return_value=self.expected),
        ):
            assert self.expected == winreg.get_feature_list("SLOT 4 Port 2", False)

    def test_set_itemproperty(self, winreg):
        path = (
            r"hklm:\system\CurrentControlSet\enum\PCI\VEN_8086&DEV_1892&"
            r"SUBSYS_00028086&REV_01\000100FFFF00000001\Device "
            r"Parameters\Interrupt Management\MessageSignaledInterruptProperties"
        )
        winreg._connection.execute_powershell.return_value = ConnectionCompletedProcess(
            return_code=0, args="command", stdout="", stderr="stderr"
        )
        assert winreg.set_itemproperty(path=path, name="MessageNumberLimit", value="33") is None
        winreg._connection.execute_powershell.assert_called_with(
            r"set-itemproperty -path 'hklm:\system\CurrentControlSet\enum\PCI\VEN_8086&DEV_1892&SUBSYS_00028086&REV_01"
            r"\000100FFFF00000001\Device Parameters\Interrupt Management\MessageSignaledInterruptProperties' "
            r"-Name MessageNumberLimit -Value 33",
            expected_return_codes=[0],
        )
