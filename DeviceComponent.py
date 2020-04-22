# uncompyle6 version 3.6.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.17 (default, Nov  7 2019, 10:07:09)
# [GCC 7.4.0]
# Embedded file name: /Applications/Ableton Live 10 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Launchkey_MK2/DeviceComponent.py
# Compiled at: 2020-04-18 08:28:38
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Generic.Devices import DEVICE_DICT, BANK_NAME_DICT, DEVICE_BOB_DICT, parameter_banks, parameter_bank_names
from _Framework.Control import ButtonControl
from _Framework.DeviceComponent import DeviceComponent as DeviceComponentBase
BOB_BANK_NAME = b'Best of Parameters'
NavDirection = Live.Application.Application.View.NavDirection

class DeviceComponent(DeviceComponentBase):
    device_nav_left_button = ButtonControl()
    device_nav_right_button = ButtonControl()

    def __init__(self, *a, **k):
        super(DeviceComponent, self).__init__(*a, **k)
        new_banks = {}
        new_bank_names = {}
        self._device_banks = DEVICE_DICT
        self._device_bank_names = BANK_NAME_DICT
        self._device_best_banks = DEVICE_BOB_DICT
        for device_name, current_banks in self._device_banks.iteritems():
            if len(current_banks) > 1:
                assert device_name in self._device_best_banks.keys(), b"Could not find best-of-banks for '%s'" % device_name
                assert device_name in self._device_bank_names.keys(), b"Could not find bank names for '%s'" % device_name
                current_banks = self._device_best_banks[device_name] + current_banks
                new_bank_names[device_name] = (
                 BOB_BANK_NAME,) + self._device_bank_names[device_name]
            new_banks[device_name] = current_banks

        self._device_banks = new_banks
        self._device_bank_names = new_bank_names

    @device_nav_left_button.pressed
    def device_nav_left_button(self, value):
        self._scroll_device_chain(NavDirection.left)

    @device_nav_right_button.pressed
    def device_nav_right_button(self, value):
        self._scroll_device_chain(NavDirection.right)

    def _scroll_device_chain(self, direction):
        view = self.application().view
        if not view.is_view_visible(b'Detail') or not view.is_view_visible(b'Detail/DeviceChain'):
            view.show_view(b'Detail')
            view.show_view(b'Detail/DeviceChain')
        else:
            view.scroll_view(direction, b'Detail/DeviceChain', False)

    def _is_banking_enabled(self):
        return True

    def _number_of_parameter_banks(self):
        result = 0
        if self._device != None:
            if self._device.class_name in self._device_banks.keys():
                result = len(self._device_banks[self._device.class_name])
            else:
                result = DeviceComponentBase._number_of_parameter_banks(self)
        return result

    def _parameter_banks(self):
        return parameter_banks(self._device, self._device_banks)

    def _parameter_bank_names(self):
        return parameter_bank_names(self._device, self._device_bank_names)

    def _update_device_bank_buttons(self):
        if self.is_enabled():
            bank_length = len(self._parameter_banks())
            for index, button in enumerate(self._bank_buttons or []):
                if button:
                    value_to_send = False
                    if index == self._bank_index and self._device:
                        value_to_send = b'Device.BankSelected'
                    else:
                        if index == 0:
                            value_to_send = b'Device.BestOfBank'
                        else:
                            if index in xrange(bank_length):
                                value_to_send = b'Device.Bank'
                    button.set_light(value_to_send)
