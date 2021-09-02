# coding: utf-8
# @package TLC59208
#  This is a FaBo7Seg_TLC59208 library for the FaBo 7seg I2C Brick.
#
#  http://fabo.io/211.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

# Default I2C slave address
SLAVE_ADDRESS = 0x20

# PWM output value
# PWM_VALUE     = 0x02
# PWM_VALUE = 0xFF
PWM_VALUE = 0xFF


# Auto-Increment on PWM Registers
AUTO_INCREMENT_REG = 0xA2
SET_ONLY_REG = 0x05
# LED点灯パターン1
# LED点灯パターン定義(数字)
LED_0 = 0x77
LED_1 = 0x14
LED_2 = 0xB3
LED_3 = 0xB6
LED_4 = 0xD4
LED_5 = 0xE6
LED_6 = 0xE7
LED_7 = 0x74
LED_8 = 0xF7
LED_9 = 0xF6

# LED点灯パターン2
# LED点灯パターン定義(アルファベット)
LED_A = 0xB7
LED_B = 0xC7
LED_C = 0x63
LED_D = 0x97
LED_E = 0xE3
LED_F = 0xE1
LED_H = 0xD5

# LED点灯パターン3
# LED点灯パターン定義(ドット,消灯)
LED_DP = 0x08
LED_OFF = 0x00

# PWMレジスタ
LED_PWM0 = 0x01
LED_PWM1 = 0x02
LED_PWM2 = 0x04

LED_PWM3 = 0x08
LED_PWM4 = 0x10
LED_PWM5 = 0x20
LED_PWM6 = 0x40
LED_PWM7 = 0x80

# 7Segment LED PINアサイン定義
LED_PIN_A = 0x20
LED_PIN_B = 0x10
LED_PIN_C = 0x04
LED_PIN_D = 0x02
LED_PIN_E = 0x01
LED_PIN_F = 0x40
LED_PIN_G = 0x80
LED_PIN_DP = 0x08

# smbus
bus = smbus.SMBus(1)

# TLC59208 I2C Controll class


class TLC59208(object):
    address = []

    # Constructor
    #  @param [in] address TLC59208 i2c slave_address default:0x20
    def __init__(self, addr=[SLAVE_ADDRESS]):
        print("led control init\r\n")
        # type check
        if isinstance(addr, list):
            address = addr
        else:
            address = [addr]

        # address set
        for num in address:
            self.address += [num]

        self.digits = len(address)

        self.configure()

    # Configuring TLC59208F Device
    #  @retval true normaly done
    #  @retval false device error
    def configure(self):

        set_data = [
            0x81,   # 00h: MODE1
            0x03,   # 01h: MODE2
            0x00,   # 02h: PWM0
            0x00,   # 03h: PWM1
            0x00,   # 04h: PWM2
            0x00,   # 05h: PWM3
            0x00,   # 06h: PWM4
            0x00,   # 07h: PWM5
            0x00,   # 08h: PWM6
            0x00,   # 09h: PWM7
            0xFF,   # 0Ah: GRPPWM
            0x00,   # 0Bh: GRPFREQ
            0xAA,   # 0Ch: LEDOUT0
            0xAA,   # 0Dh: LEDOUT1
            0x92,   # 0Eh: SUBADR1
            0x94,   # 0Fh: SUBADR2
            0x98,   # 10h: SUBADR3
            0xD0    # 11h: ALLCALLADR
        ]

        for i in range(self.digits):
            bus.write_i2c_block_data(self.address[i], 0x80, set_data)

    # show a number
    #  @param [in] number show number
    #  @param [in] digit digit number
    def showNumber(self, number, digit=0):
        print("turn on led: ", number)
        if number == 0:
            # bus.write_byte_data(self.address[digit], LED_PWM0, PWM_VALUE)
             self.writePattern(self.address[digit], LED_PWM0)
        elif number == 1:
            # bus.write_byte_data(self.address[digit], LED_PWM1, PWM_VALUE)
            self.writePattern(self.address[digit], LED_PWM1)
        elif number == 2:
            self.writePattern(self.address[digit], LED_PWM2)
        elif number == 3:
            self.writePattern(self.address[digit], LED_PWM3)
        elif number == 4:
            self.writePattern(self.address[digit], LED_PWM4)
        elif number == 5:
            self.writePattern(self.address[digit], LED_PWM5)
        elif number == 6:
            self.writePattern(self.address[digit], LED_PWM6)
        elif number == 7:
            self.writePattern(self.address[digit], LED_PWM7)
        else:
            self.writePattern(self.address[digit], LED_OFF)
    # led off
    #  @param [in] digit digit number
    def clearNumber(self, digit=0):
        print("clean led")
        self.writePattern(self.address[digit], LED_OFF)

    # show a number use full digit
    #  @param [in] number show number(int)

    def showNumberFullDigit(self, number):
        minus_flg = 0

        if number < 0:
            minus_flg = 1
            number *= -1

        for i in range(self.digits):
            if number == 0:
                if minus_flg == 1:
                    self.showPattern(LED_PIN_G, i)
                    minus_flg = 0
                elif i == 0:
                    self.showNumber(number)
                else:
                    self.clearNumber(i)
            else:
                self.showNumber(number % 10, i)

            number = int(number / 10)

    # show dot
    #  @param [in] digit digit number
    def showDot(self, digit=0):
        # DP on
        # bus.write_byte_data(self.address[digit], SET_ONLY_REG, PWM_VALUE)
        print("show dot led")
        bus.write_byte_data(self.address[digit], SET_ONLY_REG, LED_DP)

    # off dot
    #  @param [in] digit digit number
    def clearDot(self, digit=0):
        # DP off
        bus.write_byte_data(self.address[digit], SET_ONLY_REG, LED_OFF)

    # show pattern
    #  @param [in] data pattern data
    #  @param [in] digit digit number

    def showPattern(self, data, digit=0):
        self.writePattern(self.address[digit], data)

    # write Pattern
    #  @param [in] data data
    #  @param [in] address register address
    def writePattern(self, address, data):
        pattern = []
        for i in range(8):
            if (data >> i) & 0x01:
                pattern += [PWM_VALUE]
            else:
                pattern += [LED_OFF]
        try:
            bus.write_i2c_block_data(address, AUTO_INCREMENT_REG, pattern)
        except:
            # 7seg write error
            pass
