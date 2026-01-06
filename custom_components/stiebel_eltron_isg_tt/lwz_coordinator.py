"""Data Coordinator for the LWZ Stiebel Eltron heat pumps."""
"""Change 18.02.2025 JG - V.2025.2.0 - Extended register scope"""

"""For more details about this integration, please refer to
https://github.com/pail23/stiebel_eltron_isg
"""

# Stiebel Eltron ISG Ergaenzung auf erweiterten Registerumfang
# Tecalor THZ5.5 / THZ504 / Stiebel Eltron LWZ504
# Regler 504INV
# JG 12/2024
import logging

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from custom_components.stiebel_eltron_isg.coordinator import (
    StiebelEltronModbusDataCoordinator,
    get_isg_scaled_value,
)

from .const import (

    ACTIVE_ERROR,
    ACTUAL_HUMIDITY,
    ACTUAL_HUMIDITY_HK1,
    ACTUAL_HUMIDITY_HK2,
    ACTUAL_MODE_EVE,
    ACTUAL_MODE_IWS,
    ACTUAL_ROOM_TEMPERATURE_HK1,
    ACTUAL_ROOM_TEMPERATURE_HK2,
    ACTUAL_TEMPERATURE,
    ACTUAL_TEMPERATURE_FEK,
    ACTUAL_TEMPERATURE_HK1,
    ACTUAL_TEMPERATURE_HK2,
    ACTUAL_TEMPERATURE_WATER,
    COMFORT_COOLING_TEMPERATURE_TARGET_HK1,
    COMFORT_COOLING_TEMPERATURE_TARGET_HK2,
    COMFORT_TEMPERATURE_TARGET_HK1,
    COMFORT_TEMPERATURE_TARGET_HK2,
    COMFORT_WATER_TEMPERATURE_TARGET,
    COMMUTE_REL,
    COMPRESSOR_COOLING,
    COMPRESSOR_CURRENT,
    COMPRESSOR_FAULT,
    COMPRESSOR_HEATING,
    COMPRESSOR_HEATING_WATER,
    COMPRESSOR_ON,
    COMPRESSOR_PERFORMANCE_TARGET,
    COMPRESSOR_POWER,
    COMPRESSOR_SPEED,
    COMPRESSOR_STARTS,
    COMPRESSOR_TARGET_CALCULATED,
    COMPRESSOR_TARGET_SENT,
    COMPRESSOR_TEMPERATURE,
    COMPRESSOR_VOLTAGE,
    CONDENSER_TEMPERATURE,
    CONSUMED_HEATING,
    CONSUMED_HEATING_TODAY,
    CONSUMED_HEATING_TOTAL,
    CONSUMED_WATER_HEATING,
    CONSUMED_WATER_HEATING_TODAY,
    CONSUMED_WATER_HEATING_TOTAL,
    COOLING_TEMPERATURE,
    DEFROST_LL_WT,
    DEFROST_STATUS,
    DEVICE_ID,
    DEWPOINT_TEMPERATURE_HK1,
    DEWPOINT_TEMPERATURE_HK2,
    DOM_SENSOR,
    DYNAMIC_FACTOR,
    ECO_COOLING_TEMPERATURE_TARGET_HK1,
    ECO_COOLING_TEMPERATURE_TARGET_HK2,
    ECO_TEMPERATURE_TARGET_HK1,
    ECO_TEMPERATURE_TARGET_HK2,
    ECO_WATER_TEMPERATURE_TARGET,
    ELECTRICAL_BOOSTER_HEATING,
    ELECTRICAL_BOOSTER_HEATING_WATER,
    ELECTRIC_REHEATING,
    ENERGYMANAGEMENT,
    ERROR_STATUS,
    EVAPORATOR_DEFROST,
    EVAPORATOR_DIFFERENCE_PRESSURE,
    EVAPORATOR_OUTPUT_TEMPERATURE,
    EVAPORATOR_TEMPERATURE,
    EXHAUST_AIR_ACTUAL_FAN_SPEED,
    EXHAUST_AIR_TARGET_FLOW_RATE,
    EXTRACT_AIR_ACTUAL_FAN_SPEED,
    EXTRACT_AIR_DEW_POINT,
    EXTRACT_AIR_HUMIDITY,
    EXTRACT_AIR_TARGET_FLOW_RATE,
    EXTRACT_AIR_TEMPERATURE,
    FAN_LEVEL_DAY,
    FAN_LEVEL_NIGHT,
    FILTER,
    FILTER_EXTRACT_AIR,
    FILTER_VENTILATION_AIR,
    FLOW_TEMPERATURE,
    HEATER_PRESSURE,
    HEATING_COOLING_POWER,
    HEATING_CURVE_LOW_END_HK1,
    HEATING_CURVE_LOW_END_HK2,
    HEATING_CURVE_RISE_HK1,
    HEATING_CURVE_RISE_HK2,
    HEATPOWER_RELATIV,
    HEAT_LEVEL,
    HEAT_UP_PROGRAM,
    HIGH_PRESSURE,
    HOT_GAS_TEMPERATURE,
    IS_COOLING,
    IS_HEATING,
    IS_HEATING_WATER,
    IS_SUMMER_MODE,
    LOW_PRESSURE,
    MIXED_WATER_QUANTITY,
    OPENING_EXV_COOLING,
    OPERATION_MODE,
    OUTDOOR_TEMPERATURE,
    OVEN_FIREPLACE_ACTIV,
    OVERHEAT_COMPRESSOR_ACTUAL,
    OVERHEAT_COMPRESSOR_TARGET,
    OVERHEAT_RECUP_ACTUAL,
    POWER_OFF,
    PRODUCED_ELECTRICAL_HEAT_TOTAL,
    PRODUCED_ELECTRICAL_WATER_TOTAL,
    PRODUCED_HEATING,
    PRODUCED_HEATING_TODAY,
    PRODUCED_HEATING_TODAY_VS_CONSUMED_HEATING_TODAY,
    PRODUCED_HEATING_TOTAL,
    PRODUCED_HEATING_TOTAL_VS_CONSUMED_HEATING_TOTAL,
    P_FACTOR,
    PRODUCED_RECOVERY,
    PRODUCED_RECOVERY_TODAY,
    PRODUCED_RECOVERY_TOTAL,
    PRODUCED_SOLAR_HEATING,
    PRODUCED_SOLAR_HEATING_TODAY,
    PRODUCED_SOLAR_HEATING_TOTAL,
    PRODUCED_SOLAR_WATER_HEATING,
    PRODUCED_SOLAR_WATER_HEATING_TODAY,
    PRODUCED_SOLAR_WATER_HEATING_TOTAL,
    PRODUCED_WATER_HEATING,
    PRODUCED_WATER_HEATING_TODAY,
    PRODUCED_WATER_HEATING_TODAY_VS_CONSUMED_WATER_HEATING_TODAY,
    PRODUCED_WATER_HEATING_TOTAL,
    PRODUCED_WATER_HEATING_TOTAL_VS_CONSUMED_WATER_HEATING_TOTAL,
    PUMP_ON_HK1,
    PWM_HEAT_PUMP,
    PWM_MIXER_PUMP,
    PWM_SOLAR_PUMP,
    RETURN_TEMPERATURE,
    SERVICE,
    SG_READY_ACTIVE,
    SG_READY_INPUT_1,
    SG_READY_INPUT_2,
    SOFTWARE_ID,
    SOFTWARE_REVISION,
    SOURCE_TEMPERATURE,
    SOLAR_COLLECTOR_TEMPERATURE,
    SWITCHING_PROGRAM_ENABLED,
    TARGET_ROOM_TEMPERATURE_HK1,
    TARGET_ROOM_TEMPERATURE_HK2,
    TARGET_TEMPERATURE,
    TARGET_TEMPERATURE_FEK,
    TARGET_TEMPERATURE_HK1,
    TARGET_TEMPERATURE_HK2,
    TARGET_TEMPERATURE_WATER,
    VALVE_POSITION,
    VENTILATION,
    VENTILATION_AIR_ACTUAL_FAN_SPEED,
    VENTILATION_AIR_TARGET_FLOW_RATE,
    VOLUME_STREAM,
    I_FACTOR,
    D_FACTOR,
    OPENING_EXV_PRE,
    OPENING_EXV,
    FAN_PRZ,
    ND_FILTERED,
    WW_2_ACTUAL_TEMP,
    DIFFERENT_PRESSURE_TXT,
    CAN_BUS_STATUS_OK,
    CAN_BUS_STATUS_FAULT,
    CAN_BUS_STATUS_ERROR_1,
    CAN_BUS_STATUS_ERROR_2,
    CAN_BUS_STATUS_LINE_FAULT,
    DEVICE_TYPE_504INV,
    DEVICE_TYPE_5CS,
    DEVICE_TYPE_8CS,
    DEVICE_TYPE_8CSE,
    ERROR_NUMBER,

)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class StiebelEltronModbusLWZDataCoordinator(StiebelEltronModbusDataCoordinator):
    """Thread safe wrapper class for pymodbus. Communicates with LWZ or LWA controller models."""

    async def read_modbus_data(self) -> dict:
        """Read the ISG data through modbus."""
        return {
            **await self.read_modbus_energy(),
            **await self.read_modbus_system_state(),
            **await self.read_modbus_system_values(),
            **await self.read_modbus_system_paramter(),
            **await self.read_modbus_sg_ready(),
        }

    async def read_modbus_system_state(self) -> dict:
        """Read the system state values from the ISG."""
        result = {}
        inverter_data = await self.read_input_registers(slave=1, address=2000, count=7)
        if not inverter_data.isError():
            decoder = BinaryPayloadDecoder.fromRegisters(
                inverter_data.registers,
                byteorder=Endian.BIG,
            )
            # REGISTER OFFSET -1
            # 2001 THZ504 BETRIEBSSTATUS_TEXT_1 [B0] SCHALTPROGRAMM-AKTIV [B1] VERDICHTER [B2]  HEIZEN [B3] KUEHLEN [B4]WARMWASSERBEREITUNG [B5] ELEKTRISCHE-NACHERWAERMUNG [B6] SERVICE [B7] EVU-SPERRE  [B8] FILTERWECHSEL  [B9] LUEFTUNG [B10] HEIZKREISPUMPE [B11] ABTAUEN-VERDAMPFER [B12] FILTERWECHSEL-ABLUFT   [B13] FILTERWECHSEL-ZULUFT [B14] TROCKENHEIZPROGRAMM [B15] ENERGIEMANAGEMENT
            state = decoder.decode_16bit_uint()
            # SCHALTPROGRAMM-AKTIV
            result[SWITCHING_PROGRAM_ENABLED] = (state & 1) != 0
            # VERDICHTER
            result[COMPRESSOR_ON] = (state & (1 << 1)) != 0
            # HEIZEN
            result[IS_HEATING] = (state & (1 << 2)) != 0
            # KUEHLEN
            result[IS_COOLING] = (state & (1 << 3)) != 0
            # WARMWASSERBEREITUNG
            result[IS_HEATING_WATER] = (state & (1 << 4)) != 0
            # ELEKTRISCHE-NACHERWAERMUNG
            result[ELECTRIC_REHEATING] = (state & (1 << 5)) != 0
            # SERVICE
            result[SERVICE] = (state & (1 << 6)) != 0
            # EVU-SPERRE
            result[POWER_OFF] = (state & (1 << 7)) != 0
            # FILTERWECHSEL-BEIDE
            result[FILTER] = (state & (1 << 8)) != 0
            # LUETUNG
            result[VENTILATION] = (state & (1 << 9)) != 0
            # HEIZKREISPUMPE
            result[PUMP_ON_HK1] = (state & (1 << 10)) != 0
            # ABTAUEN-VERDAMPFER
            result[EVAPORATOR_DEFROST] = (state & (1 << 11)) != 0
            # FILTERWECHSEL-ABLUFT
            result[FILTER_EXTRACT_AIR] = (state & (1 << 12)) != 0
            # FILTERWECHSEL-ZULUFT
            result[FILTER_VENTILATION_AIR] = (state & (1 << 13)) != 0
            # TROCKENHEIZPROGRAMM-AKTIV
            result[HEAT_UP_PROGRAM] = (state & (1 << 14)) != 0
            # ENERGIEMANAGEMENT
            result[ENERGYMANAGEMENT] = (state & (1 << 15)) != 0
            # 2002 THZ504 FEHLERSTATUS
            result[ERROR_STATUS] = decoder.decode_16bit_uint()
            # decoder.skip_bytes(4)
            # 2003 THZ504 CAN-BUS-STATUS [0] OK [-1] STOERUNG [-2] CAN_FEHLER [-3] CAN_FEHLER [-4] LEITUNGSFEHLER
            state = decoder.decode_16bit_uint()
            # CAN-BUS-STATUS OK
            result[CAN_BUS_STATUS_OK] = (state & 1) != 0
            # CAN-STATUS STOERUNG
            result[CAN_BUS_STATUS_FAULT] = (state & 1) != -1
            # CAN-STATUS CAN_FEHLER
            result[CAN_BUS_STATUS_ERROR_1] = (state & 1) != -2
            # CAN-STATUS CAN_FEHLER
            result[CAN_BUS_STATUS_ERROR_2] = (state & 1) != -3
            # CAN-STATUS LEITUNGSFEHLER
            result[CAN_BUS_STATUS_LINE_FAULT] = (state & 1) != -4
            # 2004 THZ504 ABTAUEN EINGELEITET
            result[DEFROST_STATUS] = decoder.decode_16bit_uint()
            # 2005 THZ504 BETRIEBSSTATUS_TEXT_2 [B0] SOMMERBETRIEB [B1] OFEN-KAMIN-AKTIV
            state = decoder.decode_16bit_uint()
            # SOMMERBETRIEB
            result[IS_SUMMER_MODE] = (state & 1) != 0
            # OFEN-KAMIN-AKTIV
            result[OVEN_FIREPLACE_ACTIV] = (state & (1 << 1)) != 0
            # 2006 THZ504 FEHLER NUMMER
            result[ERROR_NUMBER] = decoder.decode_16bit_uint()
            # 2007 THZ504 GERAETETYP [7] 504INV [16] 5CS [17] 8CS [18] 8CSE
            state = decoder.decode_16bit_uint()
            # 504INV
            result[DEVICE_TYPE_504INV] = (state & 1) != 7
            # 5CS
            result[DEVICE_TYPE_5CS] = (state & 1) != 16
            # 8CS
            result[DEVICE_TYPE_8CS] = (state & 1) != 17
            # 8CSE
            result[DEVICE_TYPE_8CSE] = (state & 1) != 18

            # 2008 THZ504 PROZESSSTATUS_TEXT [B0] HD WAECHTER [B1] MOTORSCHUTZ [B2] ABTAUSIGNAL [B4] VERDICHTER [B5] DHC1 [B6] DHC2 [B7] DHC3 [B8] ABTAUVENTIL [B9] LUEFTER [B10] KUEHLEN [B11] EVU-SPERRE [B12] OFEN KAMIN

            # 2009 THZ504 HAUPTVERSIONSNUMMER

            # 2010 THZ504 NEBENVERSIONSNUMMER

            # 2011 THZ504 REVISIONSNUMMER

            # 2012 THZ504 LAUFZEIT-TAGE-?
            # 2013 THZ504 LAUFZEIT-STUNDEN-?
            # 2014 THZ504 FEHLER TIMESTAMP
            # 2015 THZ504 FATALER FEHLER TIMESTAMP
            # 2016 THZ504 ERWEITERUNG [1] SG-READY [2] KNX [3] EMI [4] MODBUS [9] TEST
            # 2017 THZ504 DAY_DBL
            # 2018 THZ504 WM_HZ_DBL
            # 2019 THZ504 WM_WW_DBL
            # 2020 THZ504 AUSSENTEMP_MAX_DBL
            # 2021 THZ504 AUSSENTEMP_AVG_DBL
            # 2022 THZ504 AUSSENTEMP_MIN_DBL
            # 2023 THZ504 BUILDNUMMER
            # 2024 THZ504 PV-LEISTUNG
            # 2025 THZ504 EMI-STATUS [0] EMI-NO-CONNECTION [1] EMI-OK [2] EMI-ACTIVE-ECO [3] EMI-ACTIVE-COMFORT [4] EMI-ACTIVE-HIGH [10] EMI-ERROR [11] EMI-ERROR

        return result

    async def read_modbus_system_values(self) -> dict:
        """Read the system related values from the ISG."""
        result: dict = {}
        inverter_data = await self.read_input_registers(slave=1, address=0, count=85)
        if not inverter_data.isError():
            decoder = BinaryPayloadDecoder.fromRegisters(
                inverter_data.registers,
                byteorder=Endian.BIG,
            )
            # REGISTER OFFSET -1
            # 1 actual room temperature for HC1
            # THZ504 RAUMISTTEMP HK1
            result[ACTUAL_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            result[ACTUAL_ROOM_TEMPERATURE_HK1] = result[ACTUAL_TEMPERATURE]
            # 2 actual room setpoint for HC1
            # THZ504 RAUMSOLLTEMP HK1
            result[TARGET_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            result[TARGET_ROOM_TEMPERATURE_HK1] = result[TARGET_TEMPERATURE]
            # 3 actual room humidity for HC1
            # THZ504 RAUMFEUCHTE HK1
            result[ACTUAL_HUMIDITY] = get_isg_scaled_value(decoder.decode_16bit_int())
            result[ACTUAL_HUMIDITY_HK1] = result[ACTUAL_HUMIDITY]
            # 4 actual room temperature for HC2 - Should not refer to FEK
            # THZ504 RAUMISTTEMP HK2
            result[ACTUAL_TEMPERATURE_FEK] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            result[ACTUAL_ROOM_TEMPERATURE_HK2] = result[ACTUAL_TEMPERATURE_FEK]
            # 5 actual room setpoint for HC2 - Should not refer to FEK
            # THZ504 RAUMSOLLTEMP HK2
            result[TARGET_TEMPERATURE_FEK] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            result[TARGET_ROOM_TEMPERATURE_HK2] = result[TARGET_TEMPERATURE_FEK]
            # 6 actual room humidity for HC2
            # THZ504 RAUMFEUCHTE HK2
            result[ACTUAL_HUMIDITY_HK2] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 7 outside temperature
            # THZ504 AUSSENTEMPERATUR
            result[OUTDOOR_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 8
            # THZ504 ISTWERT HK1
            result[ACTUAL_TEMPERATURE_HK1] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 9
            # THZ504 SOLLWERT HK1
            result[TARGET_TEMPERATURE_HK1] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 10
            # THZ504 ISTWERT HK2
            result[ACTUAL_TEMPERATURE_HK2] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 11
            # THZ504 SOLLWERT HK2
            result[TARGET_TEMPERATURE_HK2] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 12
            # THZ504 VORLAUFTEMP
            result[FLOW_TEMPERATURE] = get_isg_scaled_value(decoder.decode_16bit_int())
            # 13
            # THZ504 RUECKLAUFTEMP
            result[RETURN_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 14
            # THZ504 DRUCK HEIZKREIS
            result[HEATER_PRESSURE] = get_isg_scaled_value(decoder.decode_16bit_int())
            # 15
            # THZ504 VOLUMENSTROM
            result[VOLUME_STREAM] = get_isg_scaled_value(decoder.decode_16bit_int())
            # 16
            # THZ504 WW IST TEMPERATUR
            result[ACTUAL_TEMPERATURE_WATER] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 17
            # THZ504 WW SOLL TEMPERATUR
            result[TARGET_TEMPERATURE_WATER] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 18
            # THZ504 ZULUFT IST LUEFTER DREHZAHL
            result[VENTILATION_AIR_ACTUAL_FAN_SPEED] = decoder.decode_16bit_uint()
            # 19
            # THZ504 ZULUFT SOLL VOLUMENSTROM
            result[VENTILATION_AIR_TARGET_FLOW_RATE] = decoder.decode_16bit_uint()
            # 20
            # THZ504 ABULUFT IST LUEFTER DREHZAHL
            result[EXTRACT_AIR_ACTUAL_FAN_SPEED] = decoder.decode_16bit_uint()
            # 21
            # THZ504 ABLUFT SOLL VOLUMENSTROM
            result[EXTRACT_AIR_TARGET_FLOW_RATE] = decoder.decode_16bit_uint()
            # 22
            # THZ504 ABLUFTFEUCHTE
            result[EXTRACT_AIR_HUMIDITY] = decoder.decode_16bit_uint()
            # 23
            # THZ504 ABLUFTTEMPERATUR
            result[EXTRACT_AIR_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_uint()
            )
            # 24
            # THZ504 ABLUFTTAUPUNKT
            result[EXTRACT_AIR_DEW_POINT] = get_isg_scaled_value(
                decoder.decode_16bit_uint()
            )
            # 25
            # THZ504 TAUPUNKTTEMPERATUR HK1
            result[DEWPOINT_TEMPERATURE_HK1] = get_isg_scaled_value(
                decoder.decode_16bit_int()
            )
            # 26
            # THZ504 TAUPUNKTTEMPERATUR HK2
            result[DEWPOINT_TEMPERATURE_HK2] = get_isg_scaled_value(
                decoder.decode_16bit_int()
            )
            # 27
            # THZ504 KOLLEKTORTEMP
            result[SOLAR_COLLECTOR_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int()
            )
            # 28
            # THZ504 HEISSGASTEMP
            result[HOT_GAS_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int()
            )
            # 29
            # THZ504 HOCHDRUCK
            result[HIGH_PRESSURE] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 100
            )
            # 30
            # THZ504 NIEDERDRUCK
            result[LOW_PRESSURE] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 100
            )
            # 31
            # THZ504 VERDICHTERSTARTS HIGH
            compressor_starts_high = decoder.decode_16bit_uint()
            # 32
            # THZ504 VERDICHTERDREHZAHL
            result[COMPRESSOR_SPEED] = decoder.decode_16bit_uint()
            # 33
            # THZ504 MISCHWASSERMENGE
            result[MIXED_WATER_QUANTITY] = decoder.decode_16bit_uint()
            # 34
            # THZ504 VERDICHTERSTARTS LOW
            compressor_starts_low = decoder.decode_16bit_uint()
            if compressor_starts_high == 32768:
                result[COMPRESSOR_STARTS] = compressor_starts_high
            else:
                result[COMPRESSOR_STARTS] = (
                        compressor_starts_low + compressor_starts_high * 1000
                )
            # 35
            # THZ504 VERDAMPFERTEMP
            result[EVAPORATOR_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int()
            )
            # 36
            # THZ504 SOFTWARESTAND
            result[SOFTWARE_REVISION] = decoder.decode_16bit_uint()
            # 37
            # THZ504 FORTLUFT SOLL VOLUMENSTROM
            result[EXHAUST_AIR_TARGET_FLOW_RATE] = decoder.decode_16bit_uint()
            # 38
            # THZ504 FORTLUFT IST LUEFTERDREHZAHL
            result[EXHAUST_AIR_ACTUAL_FAN_SPEED] = decoder.decode_16bit_uint()
            # 39
            # THZ504 VERFLUESSIGERTEMP
            result[CONDENSER_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int()
            )
            # 40
            # THZ504 HEIZSTUFE
            result[HEAT_LEVEL] = decoder.decode_16bit_uint()
            # decoder.skip_bytes(18)
            # 41
            # THZ504 ABTAUEN LL WT
            result[DEFROST_LL_WT] = decoder.decode_16bit_uint()
            # 42
            # THZ504 FEHLERLISTE
            result[ACTIVE_ERROR] = decoder.decode_16bit_uint()
            # skip 43-47
            decoder.skip_bytes(10)
            # 48
            # THZ504 GERAETEKENNUNG
            result[DEVICE_ID] = decoder.decode_16bit_uint()
            # 49
            # THZ504 KUEHLUNGSTEMP
            result[COOLING_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 10
            )
            # 50
            # THZ504 POSITION VENTIL
            result[VALVE_POSITION] = decoder.decode_16bit_uint()
            # 51
            # THZ504 VERDAMPFERAUSG TEMP
            result[EVAPORATOR_OUTPUT_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int()
            )
            # 52
            # THZ504 OEFNUNG EXV KUEHLEN
            result[OPENING_EXV_COOLING] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 10
            )
            # 53
            # THZ504 SOFTWARE ID
            result[SOFTWARE_ID] = decoder.decode_16bit_uint()
            # 54
            # THZ504 DOMSENSOR
            result[DOM_SENSOR] = decoder.decode_16bit_uint()
            # 55
            # THZ504 OELSUMPFTEMP
            result[SOURCE_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 10
            )
            # 56
            # THZ504 DIFF.DRUCK VERDAMPFER
            result[EVAPORATOR_DIFFERENCE_PRESSURE] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 10
            )
            # 57
            # THZ504 PWM SOLARPUMPE
            result[PWM_SOLAR_PUMP] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 10
            )
            # 58
            # THZ504 PWM HEIZKREISPUMPE
            result[PWM_HEAT_PUMP] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 10
            )
            # 59
            # THZ504 PWM MISCHERPUMPE
            result[PWM_MIXER_PUMP] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 10
            )
            # 60
            # THZ504 HEIZLEISTUNG RELATIV
            result[HEATPOWER_RELATIV] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 1
            )
            # decoder.skip_bytes(6)
            # 61
            # THZ504 LEISTUNGSVORGABE VERDICHTER
            result[COMPRESSOR_PERFORMANCE_TARGET] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 1
            )
            # 62
            # THZ504 VERDICHTER SOLL ERRECHNET
            result[COMPRESSOR_TARGET_CALCULATED] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 1
            )
            # 63
            # THZ504 VERDICHTER SOLL GESENDET
            result[COMPRESSOR_TARGET_SENT] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 1
            )
            # 64
            # THZ504 HEIZ/KUEHL-LEISTUNG GEMESSEN
            result[HEATING_COOLING_POWER] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 100
            )
            # 65
            # THZ504 MOTORSTROM
            result[COMPRESSOR_CURRENT] = get_isg_scaled_value(
                decoder.decode_16bit_int()
            )
            # 66
            # THZ504 MOTORLEISTUNG
            result[COMPRESSOR_POWER] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 100
            )
            # 67
            # THZ504 MOTORSPANNUNG
            result[COMPRESSOR_VOLTAGE] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 1
            )
            # 68
            # THZ504 INVERTERTEMP.
            result[COMPRESSOR_TEMPERATURE] = get_isg_scaled_value(
                decoder.decode_16bit_int()
            )
            # 69
            # THZ504 INVERTERFEHLER
            result[COMPRESSOR_FAULT] = decoder.decode_16bit_uint()
            # 70
            # THZ504 AKT.MODE IWS
            result[ACTUAL_MODE_IWS] = decoder.decode_16bit_uint()
            # 71
            # THZ504 AKT.MODE EVE
            result[ACTUAL_MODE_EVE] = decoder.decode_16bit_uint()
            # 72
            # THZ504 UEBERH.VERD.SOLL
            result[OVERHEAT_COMPRESSOR_TARGET] = get_isg_scaled_value(
                decoder.decode_16bit_uint(), 10
            )
            # 73
            # THZ504 UEBERH.VERD.IST
            result[OVERHEAT_COMPRESSOR_ACTUAL] = get_isg_scaled_value(
                decoder.decode_16bit_uint(), 10
            )
            # 74
            # THZ504 UEBERH.REKUP.IST
            result[OVERHEAT_RECUP_ACTUAL] = get_isg_scaled_value(
                decoder.decode_16bit_uint(), 10
            )
            # decoder.skip_bytes(2)
            # 75
            # THZ504 PENDELN REL.
            result[COMMUTE_REL] = get_isg_scaled_value(
                decoder.decode_16bit_uint(), 10
            )
            # 76
            # THZ504 DYNAMIK-FAKTOR
            result[DYNAMIC_FACTOR] = get_isg_scaled_value(
                decoder.decode_16bit_uint(), 100
            )
            # 77
            # THZ504 P-FAKTOR
            result[P_FACTOR] = get_isg_scaled_value(
                decoder.decode_16bit_uint(), 100
            )
            # 78
            # THZ504 I-FAKTOR
            result[I_FACTOR] = get_isg_scaled_value(
                decoder.decode_16bit_uint(), 100
            )
            # 79
            # THZ504 D-FAKTOR
            result[D_FACTOR] = get_isg_scaled_value(
                decoder.decode_16bit_uint(), 100
            )
            # 80
            # THZ504 OEFNUNG EXV VORST.
            result[OPENING_EXV_PRE] = get_isg_scaled_value(
                decoder.decode_16bit_uint(), 10
            )  # 81
            # THZ504 OEFNUNG EXV
            result[OPENING_EXV] = get_isg_scaled_value(
                decoder.decode_16bit_uint(), 10
            )  # 82
            # THZ504 LUEFTER_PRZ
            result[FAN_PRZ] = decoder.decode_16bit_uint()
            # 83
            # THZ504 ND GEFILTERT
            result[ND_FILTERED] = get_isg_scaled_value(
                decoder.decode_16bit_int(), 100
            )
            # 84
            # THZ504 WW-2-ISTTEMP
            result[WW_2_ACTUAL_TEMP] = decoder.decode_16bit_uint()
            # 85
            # THZ504 DIFFERENZDRUCK_TEXT
            result[DIFFERENT_PRESSURE_TXT] = decoder.decode_16bit_uint()

            result["system_values"] = list(inverter_data.registers)
        return result

    async def read_modbus_system_paramter(self) -> dict:
        """Read the system paramters from the ISG."""
        result: dict = {}
        inverter_data = await self.read_holding_registers(
            slave=1,
            address=1000,
            count=25,
        )
        if not inverter_data.isError():
            decoder = BinaryPayloadDecoder.fromRegisters(
                inverter_data.registers,
                byteorder=Endian.BIG,
            )
            # 1001
            # THZ504 BETRIEBSART
            result[OPERATION_MODE] = decoder.decode_16bit_uint()
            # 1002
            # THZ504 RAUMTEMP KOMFORT/TAG SOLL HK1
            result[COMFORT_TEMPERATURE_TARGET_HK1] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 1003
            # THZ504 RAUMTEMP ECO/NACHT SOLL HK1
            result[ECO_TEMPERATURE_TARGET_HK1] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 1004
            decoder.skip_bytes(2)
            # 1005
            # THZ504 RAUMTEMP KOMFORT/TAG SOLL HK2
            result[COMFORT_TEMPERATURE_TARGET_HK2] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 1006
            # THZ504 RAUMTEMP ECO/NACHT SOLL HK2
            result[ECO_TEMPERATURE_TARGET_HK2] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 1007
            decoder.skip_bytes(2)
            # 1008
            # THZ504 HEIZKURVE STEIGUNG HK1
            result[HEATING_CURVE_RISE_HK1] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
                100,
            )
            # 1009
            # THZ504 HEIZKURVE FUSSPUNKT HK1
            result[HEATING_CURVE_LOW_END_HK1] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
                100,
            )
            # 1010
            # THZ504 HEIZKURVE STEIGUNG HK2
            result[HEATING_CURVE_RISE_HK2] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
                100,
            )
            # 1011
            # THZ504 HEIZKURVE FUSSPUNKT HK2
            result[HEATING_CURVE_LOW_END_HK2] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
                100,
            )
            # 1012
            # THZ504 WASSERTEMP KOMFORT SOLL
            result[COMFORT_WATER_TEMPERATURE_TARGET] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 1013
            # THZ504 WASSERTEMP ECO SOLL
            result[ECO_WATER_TEMPERATURE_TARGET] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 1014-1017
            decoder.skip_bytes(8)
            # 1018
            # THZ504 LUEFTUNG STUFE TAG
            result[FAN_LEVEL_DAY] = decoder.decode_16bit_uint()
            # 1019
            # THZ504 LUEFTUNG STUFE NACHT
            result[FAN_LEVEL_NIGHT] = decoder.decode_16bit_uint()
            # 1020-1021
            decoder.skip_bytes(4)
            # 1022
            # THZ504 KÜHLTEMP KOMFORT SOLL HK1
            result[COMFORT_COOLING_TEMPERATURE_TARGET_HK1] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 1023
            # THZ504 KÜHLTEMP ECO SOLL HK1
            result[ECO_COOLING_TEMPERATURE_TARGET_HK1] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 1024
            # THZ504 KÜHLTEMP KOMFORT SOLL HK2
            result[COMFORT_COOLING_TEMPERATURE_TARGET_HK2] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )
            # 1025
            # THZ504 KÜHLTEMP ECO SOLL HK2
            result[ECO_COOLING_TEMPERATURE_TARGET_HK2] = get_isg_scaled_value(
                decoder.decode_16bit_int(),
            )

            result["system_paramaters"] = list(inverter_data.registers)
        return result

    async def read_modbus_energy(self) -> dict:
        """Read the energy consumption related values from the ISG."""
        result = {}
        inverter_data = await self.read_input_registers(slave=1, address=3000, count=37)

        if not inverter_data.isError():
            decoder = BinaryPayloadDecoder.fromRegisters(
                inverter_data.registers,
                byteorder=Endian.BIG,
            )
            # 3001
            # THZ504 WM HEIZEN TAG KWH
            produced_heating_today_high = decoder.decode_16bit_uint()
            # 3002
            # THZ504 WM HEIZEN SUMME KWH
            produced_heating_total_low = decoder.decode_16bit_uint()
            # 3003
            # THZ504 WM HEIZEN SUMME MWH
            produced_heating_total_high = decoder.decode_16bit_uint()
            # 3004
            # THZ504 WM WW TAG KWH
            produced_water_today_high = decoder.decode_16bit_uint()
            # 3005
            # THZ504 WM WW SUMME KWH
            produced_water_total_low = decoder.decode_16bit_uint()
            # 3006
            # THZ504 WM WW SUMME MWH
            produced_water_total_high = decoder.decode_16bit_uint()
            # 3007
            # THZ504 WM NE HEIZEN SUMME KWH
            produced_electrical_heat_total_low = decoder.decode_16bit_uint()
            # 3008
            # THZ504 WM NE HEIZEN SUMME MWH
            produced_electrical_heat_total_high = decoder.decode_16bit_uint()
            # 3009
            # THZ504 WM NE WW SUMME KWH
            produced_electrical_water_total_low = decoder.decode_16bit_uint()
            # 3010
            # THZ504 WM NE WW SUMME MWH
            produced_electrical_water_total_high = decoder.decode_16bit_uint()
            # 3011
            # THZ504 WM WRG TAG KWH
            produced_recovery_today_high = decoder.decode_16bit_uint()
            # 3012
            # THZ504 WM WRG SUMME KWH
            produced_recovery_total_low = decoder.decode_16bit_uint()
            # 3013
            # THZ504 WM WRG SUMME MWH
            produced_recovery_total_high = decoder.decode_16bit_uint()
            # 3014
            # THZ504 WM SOLAR HZ TAG
            produced_solar_heating_today = self.assign_if_increased(
                decoder.decode_16bit_uint(),
                PRODUCED_SOLAR_HEATING_TODAY,
            )
            # 3015
            # THZ504 WM SOLAR HZ SUMME KWH
            produced_solar_heating_total_low = decoder.decode_16bit_uint()
            # 3016
            # THZ504 WM SOLAR HZ SUMME MWH
            produced_solar_heating_total_high = decoder.decode_16bit_uint()
            # 3017
            # THZ504 WM SOLAR WW TAG
            produced_solar_water_heating_today = self.assign_if_increased(
                decoder.decode_16bit_uint(),
                PRODUCED_SOLAR_WATER_HEATING_TODAY,
            )
            # 3018
            # THZ504 WM SOLAR WW SUMME KWH
            produced_solar_water_heating_total_low = decoder.decode_16bit_uint()
            # 3019
            # THZ504 WM SOLAR WW SUMME MWH
            produced_solar_water_heating_total_high = decoder.decode_16bit_uint()
            # 3020 - 3021
            decoder.skip_bytes(4)
            # 3020
            # THZ504 WM KUEHLEN SUMME KWH
            # 3021
            # THZ504 WM KUEHLEN SUMME MWH
            # 3022
            # THZ504 P HEIZUNG TAG KWH
            consumed_heating_today_high = decoder.decode_16bit_uint()
            # 3023
            # THZ504 P HEIZUNG SUMME KWH
            consumed_heating_total_low = decoder.decode_16bit_uint()
            # 3024
            # THZ504 P HEIZUNG SUMME MWH
            consumed_heating_total_high = decoder.decode_16bit_uint()
            # 3025
            # THZ504 P WW TAG KWH
            consumed_water_today_high = decoder.decode_16bit_uint()
            # 3026
            # THZ504 P WW SUMME KWH
            consumed_water_total_low = decoder.decode_16bit_uint()
            # 3027
            # THZ504 P WW SUMME MWH
            consumed_water_total_high = decoder.decode_16bit_uint()
            # 3028
            # THZ504 VERDICHTER HEIZEN
            result[COMPRESSOR_HEATING] = decoder.decode_16bit_uint()
            # 3029
            # THZ504 VERDICHTER KUEHLEN
            result[COMPRESSOR_COOLING] = decoder.decode_16bit_uint()
            # 3030
            # THZ504 VERDICHTER WW
            result[COMPRESSOR_HEATING_WATER] = decoder.decode_16bit_uint()
            # 3031
            # THZ504 ELEKTR NE HEIZEN
            result[ELECTRICAL_BOOSTER_HEATING] = decoder.decode_16bit_uint()
            # 3032
            # THZ504 ELEKTR NE WW
            result[ELECTRICAL_BOOSTER_HEATING_WATER] = decoder.decode_16bit_uint()
            # 3033
            # THZ504 WM HEIZEN TAG WH
            produced_heating_today_low = decoder.decode_16bit_uint()
            # 3034
            # THZ504 WM WW TAG WH
            produced_water_today_low = decoder.decode_16bit_uint()
            # 3035
            # THZ504 P HEIZUNG TAG WH
            consumed_heating_today_low = decoder.decode_16bit_uint()
            # 3036
            # THZ504 P WW TAG WH
            consumed_water_today_low = decoder.decode_16bit_uint()
            # 3037
            # THZ504 WM WRG TAG WH
            produced_recovery_today_low = decoder.decode_16bit_uint()

            # Energy Calculation
            result[PRODUCED_HEATING_TOTAL] = (
                    produced_heating_total_high * 1000 + produced_heating_total_low
            )

            result[PRODUCED_HEATING_TODAY] = (
                    produced_heating_today_high + produced_heating_today_low * 0.001
            )

            result[PRODUCED_HEATING] = self.assign_if_increased(
                result[PRODUCED_HEATING_TOTAL] + result[PRODUCED_HEATING_TODAY],
                PRODUCED_HEATING,
            )

            result[PRODUCED_WATER_HEATING_TOTAL] = (
                    produced_water_total_high * 1000 + produced_water_total_low
            )

            result[PRODUCED_WATER_HEATING_TODAY] = (
                    produced_water_today_high + produced_water_today_low * 0.001
            )
            result[PRODUCED_WATER_HEATING] = self.assign_if_increased(
                result[PRODUCED_WATER_HEATING_TOTAL] + result[PRODUCED_WATER_HEATING_TODAY],
                PRODUCED_WATER_HEATING,
            )

            result[CONSUMED_HEATING_TOTAL] = (
                    consumed_heating_total_high * 1000 + consumed_heating_total_low
            )

            result[CONSUMED_HEATING_TODAY] = (
                    consumed_heating_today_high + consumed_heating_today_low * 0.001
            )

            result[CONSUMED_HEATING] = self.assign_if_increased(
                result[CONSUMED_HEATING_TOTAL] + result[CONSUMED_HEATING_TODAY],
                CONSUMED_HEATING,
            )

            result[CONSUMED_WATER_HEATING_TOTAL] = (
                    consumed_water_total_high * 1000 + consumed_water_total_low
            )

            result[CONSUMED_WATER_HEATING_TODAY] = (
                    consumed_water_today_high + consumed_water_today_low * 0.001
            )

            result[CONSUMED_WATER_HEATING] = self.assign_if_increased(
                result[CONSUMED_WATER_HEATING_TOTAL]
                + result[CONSUMED_WATER_HEATING_TODAY],
                CONSUMED_WATER_HEATING,
            )

            result[PRODUCED_RECOVERY_TOTAL] = (
                    produced_recovery_total_high * 1000 + produced_recovery_total_low
            )

            result[PRODUCED_RECOVERY_TODAY] = (
                    produced_recovery_today_high + produced_recovery_today_low * 0.001
            )

            result[PRODUCED_RECOVERY] = self.assign_if_increased(
                result[PRODUCED_RECOVERY_TOTAL] + result[PRODUCED_RECOVERY_TODAY],
                PRODUCED_RECOVERY,
            )

            result[PRODUCED_ELECTRICAL_HEAT_TOTAL] = (
                    produced_electrical_heat_total_high * 1000 + produced_electrical_heat_total_low
            )

            result[PRODUCED_ELECTRICAL_WATER_TOTAL] = (
                    produced_electrical_water_total_high * 1000 + produced_electrical_water_total_low
            )

            result[PRODUCED_SOLAR_HEATING_TOTAL] = (
                    produced_solar_heating_total_high * 1000 + produced_solar_heating_total_low
            )

            result[PRODUCED_SOLAR_HEATING_TODAY] = produced_solar_heating_today

            result[PRODUCED_SOLAR_HEATING] = self.assign_if_increased(
                result[PRODUCED_SOLAR_HEATING_TOTAL]
                + result[PRODUCED_SOLAR_HEATING_TODAY],
                PRODUCED_SOLAR_HEATING,
            )

            result[PRODUCED_SOLAR_WATER_HEATING_TOTAL] = (
                    produced_solar_water_heating_total_high * 1000 + produced_solar_water_heating_total_low
            )

            result[PRODUCED_SOLAR_WATER_HEATING_TODAY] = (
                produced_solar_water_heating_today
            )

            result[PRODUCED_SOLAR_WATER_HEATING] = self.assign_if_increased(
                result[PRODUCED_SOLAR_WATER_HEATING_TOTAL]
                + result[PRODUCED_SOLAR_WATER_HEATING_TODAY],
                PRODUCED_SOLAR_WATER_HEATING,
            )

            # Energy Ratio
            # Heating Ratio Today
            result[PRODUCED_HEATING_TODAY_VS_CONSUMED_HEATING_TODAY] = (
                    (produced_heating_today_high + produced_heating_today_low * 0.001) / (
                        consumed_heating_today_high + consumed_heating_today_low * 0.001)
            )

            # Heating Ratio Total
            result[PRODUCED_HEATING_TOTAL_VS_CONSUMED_HEATING_TOTAL] = (
                    (produced_heating_total_high * 1000 + produced_heating_total_low) / (
                        consumed_heating_total_high * 1000 + consumed_heating_total_low)
            )

            # Water Heating Ratio Today
            result[PRODUCED_WATER_HEATING_TODAY_VS_CONSUMED_WATER_HEATING_TODAY] = (
                    (produced_water_today_high + produced_water_today_low * 0.001) / (
                        consumed_water_today_high + consumed_water_today_low * 0.001)
            )

            # Water Heating Ratio Total
            result[PRODUCED_WATER_HEATING_TOTAL_VS_CONSUMED_WATER_HEATING_TOTAL] = (
                    (produced_water_total_high * 1000 + produced_water_total_low) / (
                        consumed_water_total_high * 1000 + consumed_water_total_low)
            )

        return result

    async def set_data(self, key, value) -> None:
        """Write the data to the modbus."""
        _LOGGER.debug(f"set modbus register for {key} to {value}")
        if key == SG_READY_ACTIVE:
            await self.write_register(address=4000, value=value, slave=1)
        elif key == SG_READY_INPUT_1:
            await self.write_register(address=4001, value=value, slave=1)
        elif key == SG_READY_INPUT_2:
            await self.write_register(address=4002, value=value, slave=1)
        elif key == OPERATION_MODE:
            await self.write_register(address=1000, value=value, slave=1)
        elif key == COMFORT_TEMPERATURE_TARGET_HK1:
            await self.write_register(address=1001, value=int(value * 10), slave=1)
        elif key == ECO_TEMPERATURE_TARGET_HK1:
            await self.write_register(address=1002, value=int(value * 10), slave=1)
        elif key == HEATING_CURVE_RISE_HK1:
            await self.write_register(address=1007, value=int(value * 100), slave=1)
        elif key == HEATING_CURVE_LOW_END_HK1:
            await self.write_register(address=1008, value=int(value * 100), slave=1)
        elif key == COMFORT_TEMPERATURE_TARGET_HK2:
            await self.write_register(address=1004, value=int(value * 10), slave=1)
        elif key == ECO_TEMPERATURE_TARGET_HK2:
            await self.write_register(address=1005, value=int(value * 10), slave=1)
        elif key == HEATING_CURVE_RISE_HK2:
            await self.write_register(address=1009, value=int(value * 100), slave=1)
        elif key == HEATING_CURVE_LOW_END_HK2:
            await self.write_register(address=1010, value=int(value * 100), slave=1)
        elif key == COMFORT_WATER_TEMPERATURE_TARGET:
            await self.write_register(address=1011, value=int(value * 10), slave=1)
        elif key == ECO_WATER_TEMPERATURE_TARGET:
            await self.write_register(address=1012, value=int(value * 10), slave=1)
        elif key == FAN_LEVEL_DAY:
            await self.write_register(address=1017, value=int(value), slave=1)
        elif key == FAN_LEVEL_NIGHT:
            await self.write_register(address=1018, value=int(value), slave=1)
        elif key == COMFORT_COOLING_TEMPERATURE_TARGET_HK1:
            await self.write_register(address=1021, value=int(value * 10), slave=1)
        elif key == ECO_COOLING_TEMPERATURE_TARGET_HK1:
            await self.write_register(address=1022, value=int(value * 10), slave=1)
        elif key == COMFORT_COOLING_TEMPERATURE_TARGET_HK2:
            await self.write_register(address=1023, value=int(value * 10), slave=1)
        elif key == ECO_COOLING_TEMPERATURE_TARGET_HK2:
            await self.write_register(address=1024, value=int(value * 10), slave=1)
        else:
            return
        self.data[key] = value

    async def async_reset_heatpump(self) -> None:
        """Reset the heat pump."""
        _LOGGER.debug("Reset the heat pump is not implemented of LWZ/LWA")