"""Sensor platform for stiebel_eltron_isg."""
"""Change 18.02.2025 JG - V.2025.2.0 - Extended register scope"""
import datetime
import logging

import homeassistant.util.dt as dt_util
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.stiebel_eltron_isg.data import (
    StiebelEltronISGIntegrationConfigEntry,
)

from .const import (
    ACTIVE_ERROR,
    ACTUAL_HUMIDITY,
    ACTUAL_HUMIDITY_HK1,
    ACTUAL_HUMIDITY_HK2,
    ACTUAL_HUMIDITY_HK3,
    ACTUAL_MODE_EVE,
    ACTUAL_MODE_IWS,
    ACTUAL_ROOM_TEMPERATURE_HK1,
    ACTUAL_ROOM_TEMPERATURE_HK2,
    ACTUAL_ROOM_TEMPERATURE_HK3,
    ACTUAL_TEMPERATURE,
    ACTUAL_TEMPERATURE_BUFFER,
    ACTUAL_TEMPERATURE_COOLING_FANCOIL,
    ACTUAL_TEMPERATURE_COOLING_SURFACE,
    ACTUAL_TEMPERATURE_FEK,
    ACTUAL_TEMPERATURE_HK1,
    ACTUAL_TEMPERATURE_HK2,
    ACTUAL_TEMPERATURE_HK3,
    ACTUAL_TEMPERATURE_WATER,
    COLLECTOR_TEMPERATURE,
    COMMUTE_REL,
    COMPRESSOR_COOLING,
    COMPRESSOR_CURRENT,
    COMPRESSOR_FAULT,
    COMPRESSOR_HEATING,
    COMPRESSOR_HEATING_WATER,
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
    DEVICE_ID,
    DEWPOINT_TEMPERATURE_HK1,
    DEWPOINT_TEMPERATURE_HK2,
    DEWPOINT_TEMPERATURE_HK3,
    DIFFERENT_PRESSURE_TXT,
    DOMAIN,
    DOM_SENSOR,
    DYNAMIC_FACTOR,
    D_FACTOR,
    ELECTRICAL_BOOSTER_HEATING,
    ELECTRICAL_BOOSTER_HEATING_WATER,
    ERROR_NUMBER,
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
    FAN_PRZ,
    FLOW_TEMPERATURE,
    FLOW_TEMPERATURE_NHZ,
    FLOW_TEMPERATURE_WP1,
    FLOW_TEMPERATURE_WP2,
    HEATER_PRESSURE,
    HEATING_COOLING_POWER,
    HEATPOWER_RELATIV,
    HEAT_LEVEL,
    HIGH_PRESSURE,
    HIGH_PRESSURE_WP1,
    HIGH_PRESSURE_WP2,
    HOT_GAS_TEMPERATURE,
    HOT_GAS_TEMPERATURE_WP1,
    HOT_GAS_TEMPERATURE_WP2,
    I_FACTOR,
    LOW_PRESSURE,
    LOW_PRESSURE_WP1,
    LOW_PRESSURE_WP2,
    MIXED_WATER_QUANTITY,
    ND_FILTERED,
    OPENING_EXV,
    OPENING_EXV_COOLING,
    OPENING_EXV_PRE,
    OUTDOOR_TEMPERATURE,
    OVERHEAT_COMPRESSOR_ACTUAL,
    OVERHEAT_COMPRESSOR_TARGET,
    OVERHEAT_RECUP_ACTUAL,
    PRODUCED_ELECTRICAL_HEAT_TOTAL,
    PRODUCED_ELECTRICAL_WATER_TOTAL,
    PRODUCED_HEATING,
    PRODUCED_HEATING_TODAY,
    PRODUCED_HEATING_TODAY_VS_CONSUMED_HEATING_TODAY,
    PRODUCED_HEATING_TOTAL,
    PRODUCED_HEATING_TOTAL_VS_CONSUMED_HEATING_TOTAL,
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
    PWM_HEAT_PUMP,
    PWM_MIXER_PUMP,
    PWM_SOLAR_PUMP,
    P_FACTOR,
    RETURN_TEMPERATURE,
    RETURN_TEMPERATURE_WP1,
    RETURN_TEMPERATURE_WP2,
    SG_READY_STATE,
    SOFTWARE_ID,
    SOFTWARE_REVISION,
    SOURCE_PRESSURE,
    SOLAR_COLLECTOR_TEMPERATURE,
    SOLAR_CYLINDER_TEMPERATURE,
    SOLAR_RUNTIME,
    SOURCE_TEMPERATURE,
    TARGET_ROOM_TEMPERATURE_HK1,
    TARGET_ROOM_TEMPERATURE_HK2,
    TARGET_ROOM_TEMPERATURE_HK3,
    TARGET_TEMPERATURE,
    TARGET_TEMPERATURE_BUFFER,
    TARGET_TEMPERATURE_COOLING_FANCOIL,
    TARGET_TEMPERATURE_COOLING_SURFACE,
    TARGET_TEMPERATURE_FEK,
    TARGET_TEMPERATURE_HK1,
    TARGET_TEMPERATURE_HK2,
    TARGET_TEMPERATURE_HK3,
    TARGET_TEMPERATURE_WATER,
    VALVE_POSITION,
    VENTILATION_AIR_ACTUAL_FAN_SPEED,
    VENTILATION_AIR_TARGET_FLOW_RATE,
    VOLUME_STREAM,
    VOLUME_STREAM_WP1,
    VOLUME_STREAM_WP2,
    WW_2_ACTUAL_TEMP,
)
from .entity import StiebelEltronISGEntity

_LOGGER = logging.getLogger(__name__)


def create_temperature_entity_description(name, key):
    """Create an entry description for a temperature sensor."""
    return SensorEntityDescription(
        key=key,
        name=name,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        has_entity_name=True,
    )


def create_energy_entity_description(name, key, visible_default=True):
    """Create an entry description for a energy sensor."""
    return SensorEntityDescription(
        key=key,
        name=name,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        icon="mdi:meter-electric",
        has_entity_name=True,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        entity_registry_visible_default=visible_default,
    )


def create_daily_energy_entity_description(name, key, visible_default=True):
    """Create an entry description for a energy sensor."""
    return SensorEntityDescription(
        key=key,
        name=name,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        icon="mdi:meter-electric",
        has_entity_name=True,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
        entity_registry_visible_default=visible_default,
    )


def create_humidity_entity_description(name, key):
    """Create an entry description for a humidity sensor."""
    return SensorEntityDescription(
        key=key,
        name=name,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:water-percent",
        state_class=SensorStateClass.MEASUREMENT,
        has_entity_name=True,
    )


def create_pressure_entity_description(name, key):
    """Create an entry description for a pressure sensor."""
    return SensorEntityDescription(
        key=key,
        name=name,
        native_unit_of_measurement=UnitOfPressure.BAR,
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
        has_entity_name=True,
    )


def create_volume_stream_entity_description(name, key):
    """Create an entry description for a volume stream sensor."""
    return SensorEntityDescription(
        key=key,
        name=name,
        native_unit_of_measurement="l/min",
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
        has_entity_name=True,
    )


SYSTEM_VALUES_SENSOR_TYPES = [
    create_temperature_entity_description("Actual Temperature", ACTUAL_TEMPERATURE),
    create_temperature_entity_description("Target Temperature", TARGET_TEMPERATURE),
    create_temperature_entity_description(
        "Actual Temperature FEK",
        ACTUAL_TEMPERATURE_FEK,
    ),
    create_temperature_entity_description(
        "Target Temperature FEK",
        TARGET_TEMPERATURE_FEK,
    ),
    create_humidity_entity_description("Humidity", ACTUAL_HUMIDITY),
    create_humidity_entity_description("Humidity HK 1", ACTUAL_HUMIDITY_HK1),
    create_humidity_entity_description("Humidity HK 2", ACTUAL_HUMIDITY_HK2),
    create_humidity_entity_description("Humidity HK 3", ACTUAL_HUMIDITY_HK3),
    create_temperature_entity_description(
        "Dew Point Temperature HK 1",
        DEWPOINT_TEMPERATURE_HK1,
    ),
    create_temperature_entity_description(
        "Dew Point Temperature HK 2",
        DEWPOINT_TEMPERATURE_HK2,
    ),
    create_temperature_entity_description(
        "Dew Point Temperature HK 3",
        DEWPOINT_TEMPERATURE_HK3,
    ),
    create_temperature_entity_description(
        "Cooling Temperature",
        COOLING_TEMPERATURE,
    ),
    create_temperature_entity_description("Outdoor Temperature", OUTDOOR_TEMPERATURE),
    create_temperature_entity_description(
        "Actual Temperature HK 1",
        ACTUAL_TEMPERATURE_HK1,
    ),
    create_temperature_entity_description(
        "Target Temperature HK 1",
        TARGET_TEMPERATURE_HK1,
    ),
    create_temperature_entity_description(
        "Actual Temperature HK 2",
        ACTUAL_TEMPERATURE_HK2,
    ),
    create_temperature_entity_description(
        "Target Temperature HK 2",
        TARGET_TEMPERATURE_HK2,
    ),
    create_temperature_entity_description(
        "Actual Temperature HK 3",
        ACTUAL_TEMPERATURE_HK3,
    ),
    create_temperature_entity_description(
        "Target Temperature HK 3",
        TARGET_TEMPERATURE_HK3,
    ),
    create_temperature_entity_description(
        "Actual Temperature Cooling Fancoil",
        ACTUAL_TEMPERATURE_COOLING_FANCOIL,
    ),
    create_temperature_entity_description(
        "Target Temperature Cooling Fancoil",
        TARGET_TEMPERATURE_COOLING_FANCOIL,
    ),
    create_temperature_entity_description(
        "Actual Temperature Cooling Surface",
        ACTUAL_TEMPERATURE_COOLING_SURFACE,
    ),
    create_temperature_entity_description(
        "Target Temperature Cooling Surface",
        TARGET_TEMPERATURE_COOLING_SURFACE,
    ),
    create_temperature_entity_description(
        "Solar Collector Temperature", SOLAR_COLLECTOR_TEMPERATURE
    ),
    create_temperature_entity_description(
        "Solar Cylinder Temperature", SOLAR_CYLINDER_TEMPERATURE
    ),
    SensorEntityDescription(
        key=SOLAR_RUNTIME,
        name="Solar Runtime",
        has_entity_name=True,
        icon="mdi:hours-24",
        native_unit_of_measurement="h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    create_temperature_entity_description(
        "Actual Room Temperature HK 1",
        ACTUAL_ROOM_TEMPERATURE_HK1,
    ),
    create_temperature_entity_description(
        "Target Room Temperature HK 1",
        TARGET_ROOM_TEMPERATURE_HK1,
    ),
    create_temperature_entity_description(
        "Actual Room Temperature HK 2",
        ACTUAL_ROOM_TEMPERATURE_HK2,
    ),
    create_temperature_entity_description(
        "Target Room Temperature HK 2",
        TARGET_ROOM_TEMPERATURE_HK2,
    ),
    create_temperature_entity_description(
        "Actual Room Temperature HK 3",
        ACTUAL_ROOM_TEMPERATURE_HK3,
    ),
    create_temperature_entity_description(
        "Target Room Temperature HK 3",
        TARGET_ROOM_TEMPERATURE_HK3,
    ),
    create_temperature_entity_description("Flow Temperature", FLOW_TEMPERATURE),
    create_temperature_entity_description("Flow Temperature NHZ", FLOW_TEMPERATURE_NHZ),
    create_temperature_entity_description("Return Temperature", RETURN_TEMPERATURE),
    create_temperature_entity_description(
        "Actual Temperature Buffer",
        ACTUAL_TEMPERATURE_BUFFER,
    ),
    create_temperature_entity_description(
        "Target Temperature Buffer",
        TARGET_TEMPERATURE_BUFFER,
    ),
    create_pressure_entity_description("Heater Pressure", HEATER_PRESSURE),
    create_volume_stream_entity_description("Volume Stream", VOLUME_STREAM),
    create_temperature_entity_description(
        "Actual Temperature Water",
        ACTUAL_TEMPERATURE_WATER,
    ),
    create_temperature_entity_description(
        "Target Temperature Water",
        TARGET_TEMPERATURE_WATER,
    ),
    create_temperature_entity_description(
        "Solar Collector Temperature",
        SOLAR_COLLECTOR_TEMPERATURE,
    ),
    create_temperature_entity_description("Source Temperature", SOURCE_TEMPERATURE),
    create_pressure_entity_description("Source Pressure", SOURCE_PRESSURE),
    create_temperature_entity_description("Hot Gas Temperature", HOT_GAS_TEMPERATURE),
    create_pressure_entity_description("High Pressure", HIGH_PRESSURE),
    create_pressure_entity_description("Low Pressure", LOW_PRESSURE),
    create_pressure_entity_description("ND Filtered", ND_FILTERED),
    create_temperature_entity_description(
        "Return Temperature WP1",
        RETURN_TEMPERATURE_WP1,
    ),
    create_temperature_entity_description("Flow Temperature WP1", FLOW_TEMPERATURE_WP1),
    create_temperature_entity_description(
        "Hot Gas Temperature WP1",
        HOT_GAS_TEMPERATURE_WP1,
    ),
    create_pressure_entity_description("Low Pressure WP1", LOW_PRESSURE_WP1),
    create_pressure_entity_description("High Pressure WP1", HIGH_PRESSURE_WP1),
    create_volume_stream_entity_description("Volume Stream WP1", VOLUME_STREAM_WP1),
    create_temperature_entity_description(
        "Return Temperature WP2",
        RETURN_TEMPERATURE_WP2,
    ),
    create_temperature_entity_description("Flow Temperature WP2", FLOW_TEMPERATURE_WP2),
    create_temperature_entity_description(
        "Hot Gas Temperature WP2",
        HOT_GAS_TEMPERATURE_WP2,
    ),
    create_pressure_entity_description("Low Pressure WP2", LOW_PRESSURE_WP2),
    create_pressure_entity_description("High Pressure WP2", HIGH_PRESSURE_WP2),
    create_volume_stream_entity_description("Volume Stream WP2", VOLUME_STREAM_WP2),
    create_temperature_entity_description("Collector Temperature", COLLECTOR_TEMPERATURE),
    create_temperature_entity_description("Evaporator Temperature", EVAPORATOR_TEMPERATURE),
    create_temperature_entity_description("Evaporator Output Temperature", EVAPORATOR_OUTPUT_TEMPERATURE),
    create_temperature_entity_description("Condenser Temperature", CONDENSER_TEMPERATURE),
    create_temperature_entity_description("Compressor Temperature", COMPRESSOR_TEMPERATURE),
    SensorEntityDescription(
        key=ACTIVE_ERROR,
        name="Active Error",
        has_entity_name=True,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:alert-circle",
    ),
    SensorEntityDescription(
        DEVICE_ID,
        name="Device ID",
        has_entity_name=True,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:information",
    ),
    SensorEntityDescription(
        SOFTWARE_REVISION,
        name="Software Revision",
        has_entity_name=True,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:information",
    ),
    SensorEntityDescription(
        SOFTWARE_ID,
        name="Software ID",
        has_entity_name=True,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:information",
    ),
    SensorEntityDescription(
        MIXED_WATER_QUANTITY,
        name="Mixed Water Quantity",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        OPENING_EXV_COOLING,
        name="Opening EXV Cooling",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        PWM_SOLAR_PUMP,
        name="PWM Solar Pump",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        PWM_HEAT_PUMP,
        name="PWM Heat Pump",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        PWM_MIXER_PUMP,
        name="PWM Mixer Pump",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        EXHAUST_AIR_TARGET_FLOW_RATE,
        name="Exhaust Air Target Flow Rate",
        icon="mdi:fan",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        EXHAUST_AIR_ACTUAL_FAN_SPEED,
        name="Exhaust Air Actual Fan Speed",
        icon="mdi:speedometer",
        has_entity_name=True,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        HEAT_LEVEL,
        name="Heat Level",
        icon="mdi:heat-wave",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        PRODUCED_HEATING_TODAY_VS_CONSUMED_HEATING_TODAY,
        name="Ratio Heating Today",
        icon="mdi:set-left",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        PRODUCED_HEATING_TOTAL_VS_CONSUMED_HEATING_TOTAL,
        name="Ratio Heating Total",
        icon="mdi:set-left",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        PRODUCED_WATER_HEATING_TODAY_VS_CONSUMED_WATER_HEATING_TODAY,
        name="Ratio Water Heating Today",
        icon="mdi:set-left",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        PRODUCED_WATER_HEATING_TOTAL_VS_CONSUMED_WATER_HEATING_TOTAL,
        name="Ratio Water Heating Total",
        icon="mdi:set-left",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        VALVE_POSITION,
        name="Valve Position",
        icon="mdi:information",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        DOM_SENSOR,
        name="DOM Sensor",
        icon="mdi:information",
        has_entity_name=True,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        HEATPOWER_RELATIV,
        name="Heatpower relativ",
        icon="mdi:flash",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        COMPRESSOR_FAULT,
        name="Compressor Fault",
        icon="mdi:information",
        has_entity_name=True,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        ACTUAL_MODE_IWS,
        name="Actual Mode IWS",
        icon="mdi:information",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        ACTUAL_MODE_EVE,
        name="Actual Mode EVE",
        icon="mdi:information",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        OVERHEAT_COMPRESSOR_TARGET,
        name="Overheat Compressor Target",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement="K",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        OVERHEAT_COMPRESSOR_ACTUAL,
        name="Overheat Compressor Actual",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement="K",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        OVERHEAT_RECUP_ACTUAL,
        name="Overheat Recup Actual",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement="K",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        DYNAMIC_FACTOR,
        name="Dynamic Factor",
        icon="mdi:information",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        P_FACTOR,
        name="P-Factor",
        icon="mdi:information",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        I_FACTOR,
        name="I-Factor",
        icon="mdi:information",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        D_FACTOR,
        name="D-Factor",
        icon="mdi:information",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        OPENING_EXV_PRE,
        name="Opening EXV Pre",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        OPENING_EXV,
        name="Opening EXV",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        FAN_PRZ,
        name="Fan PRZ",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        WW_2_ACTUAL_TEMP,
        name="WW-2 actual temp",
        icon="mdi:information",
        has_entity_name=True,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        DIFFERENT_PRESSURE_TXT,
        name="Different Pressure Text",
        icon="mdi:information",
        has_entity_name=True,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        EVAPORATOR_DIFFERENCE_PRESSURE,
        name="Evaporator Difference Pressure",
        icon="mdi:gauge",
        has_entity_name=True,
        native_unit_of_measurement="Pa",
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        COMMUTE_REL,
        name="Commute Rel",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        HEATING_COOLING_POWER,
        name="Heating/Cooling Power",
        icon="mdi:flash",
        has_entity_name=True,
        native_unit_of_measurement="kW",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        COMPRESSOR_PERFORMANCE_TARGET,
        name="Compressor Performance Target",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        COMPRESSOR_TARGET_CALCULATED,
        name="Compressor Target Calculated",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        COMPRESSOR_TARGET_SENT,
        name="Compressor Target Sent",
        icon="mdi:information",
        has_entity_name=True,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        ERROR_NUMBER,
        name="Error Number",
        icon="mdi:information",
        has_entity_name=True,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]

ENERGYMANAGEMENT_SENSOR_TYPES = [
    SensorEntityDescription(
        key=SG_READY_STATE,
        name="SG Ready State",
        icon="mdi:solar-power",
        has_entity_name=True,
    ),
]


ENERGY_SENSOR_TYPES = [
    create_energy_entity_description(
        "Produced Electrical Heating Total",
        PRODUCED_ELECTRICAL_HEAT_TOTAL,
    ),
    create_energy_entity_description(
        "Produced Electrical Water Total",
        PRODUCED_ELECTRICAL_WATER_TOTAL,
    ),
    create_energy_entity_description(
        "Produced Heating Total",
        PRODUCED_HEATING_TOTAL,
    ),
    create_energy_entity_description(
        "Produced Heating",
        PRODUCED_HEATING,
    ),
    create_energy_entity_description(
        "Produced Water Heating Total",
        PRODUCED_WATER_HEATING_TOTAL,
    ),
    create_energy_entity_description("Produced Water Heating", PRODUCED_WATER_HEATING),
    create_energy_entity_description(
        "Produced Recovery",
        PRODUCED_RECOVERY,
    ),
    create_energy_entity_description(
        "Produced Recovery Total",
        PRODUCED_RECOVERY_TOTAL,
    ),
    create_energy_entity_description(
        "Produced Solar Heating",
        PRODUCED_SOLAR_HEATING,
    ),
    create_energy_entity_description(
        "Produced Solar Heating Total",
        PRODUCED_SOLAR_HEATING_TOTAL,
    ),
    create_energy_entity_description(
        "Produced Solar Water Heating Total",
        PRODUCED_SOLAR_WATER_HEATING_TOTAL,
    ),
    create_energy_entity_description(
        "Produced Solar Water Heating",
        PRODUCED_SOLAR_WATER_HEATING,
    ),
    create_energy_entity_description(
        "Consumed Heating Total",
        CONSUMED_HEATING_TOTAL,
    ),
    create_energy_entity_description(
        "Consumed Heating",
        CONSUMED_HEATING,
    ),
    create_energy_entity_description(
        "Consumed Water Heating Total",
        CONSUMED_WATER_HEATING_TOTAL,
    ),
    create_energy_entity_description(
        "Consumed Water Heating",
        CONSUMED_WATER_HEATING,
    ),
]

ENERGY_DAILY_SENSOR_TYPES = [
    create_daily_energy_entity_description(
        "Produced Heating Today",
        PRODUCED_HEATING_TODAY,
    ),
    create_daily_energy_entity_description(
        "Produced Water Heating Today",
        PRODUCED_WATER_HEATING_TODAY,
    ),
    create_daily_energy_entity_description(
        "Produced Recovery Today",
        PRODUCED_RECOVERY_TODAY,
    ),
    create_daily_energy_entity_description(
        "Produced Solar Heating Today",
        PRODUCED_SOLAR_HEATING_TODAY,
    ),
    create_daily_energy_entity_description(
        "Produced Solar Water Heating Today",
        PRODUCED_SOLAR_WATER_HEATING_TODAY,
    ),
    create_daily_energy_entity_description(
        "Consumed Heating Today",
        CONSUMED_HEATING_TODAY,
    ),
    create_daily_energy_entity_description(
        "Consumed Water Heating Today",
        CONSUMED_WATER_HEATING_TODAY,
    ),
]


COMPRESSOR_SENSOR_TYPES = [
    SensorEntityDescription(
        key=COMPRESSOR_STARTS,
        name="Compressor starts",
        icon="mdi:restart",
        has_entity_name=True,
    ),
    SensorEntityDescription(
        COMPRESSOR_COOLING,
        name="Compressor cooling",
        icon="mdi:hours-24",
        has_entity_name=True,
        native_unit_of_measurement="h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=COMPRESSOR_HEATING,
        name="Compressor heating",
        icon="mdi:hours-24",
        has_entity_name=True,
        native_unit_of_measurement="h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=COMPRESSOR_HEATING_WATER,
        name="Compressor heating water",
        icon="mdi:hours-24",
        has_entity_name=True,
        native_unit_of_measurement="h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        COMPRESSOR_SPEED,
        name="Compressor speed",
        icon="mdi:speedometer",
        has_entity_name=True,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        COMPRESSOR_CURRENT,
        name="Compressor current",
        icon="mdi:current-ac",
        has_entity_name=True,
        native_unit_of_measurement="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        COMPRESSOR_VOLTAGE,
        name="Compressor voltage",
        icon="mdi:sine-wave",
        has_entity_name=True,
        native_unit_of_measurement="V",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        COMPRESSOR_POWER,
        name="Compressor power",
        icon="mdi:flash",
        has_entity_name=True,
        native_unit_of_measurement="kW",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ELECTRICAL_BOOSTER_HEATING,
        name="Electrical booster heating",
        icon="mdi:hours-24",
        has_entity_name=True,
        native_unit_of_measurement="h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ELECTRICAL_BOOSTER_HEATING_WATER,
        name="Electrical booster heating water",
        icon="mdi:hours-24",
        has_entity_name=True,
        native_unit_of_measurement="h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
]

VENTILATION_SENSOR_TYPES = [
    SensorEntityDescription(
        key=VENTILATION_AIR_ACTUAL_FAN_SPEED,
        name="Ventilation air actual fan speed",
        icon="mdi:fan",
        has_entity_name=True,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=VENTILATION_AIR_TARGET_FLOW_RATE,
        name="Ventilation air target fan speed",
        icon="mdi:fan",
        has_entity_name=True,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=EXTRACT_AIR_ACTUAL_FAN_SPEED,
        name="Extract air actual fan speed",
        icon="mdi:fan",
        has_entity_name=True,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=EXTRACT_AIR_TARGET_FLOW_RATE,
        name="Extract air target fan speed",
        icon="mdi:fan",
        has_entity_name=True,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    create_temperature_entity_description(
        "Extract air dew point", EXTRACT_AIR_DEW_POINT
    ),
    create_humidity_entity_description("Extract air humidity", EXTRACT_AIR_HUMIDITY),
    create_temperature_entity_description(
        "Extract air temperature", EXTRACT_AIR_TEMPERATURE
    ),
]


async def async_setup_entry(
    _hass: HomeAssistant,  # Unused function argument: `hass`
    entry: StiebelEltronISGIntegrationConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data.coordinator

    entities = []
    for description in SYSTEM_VALUES_SENSOR_TYPES:
        sensor = StiebelEltronISGSensor(
            coordinator,
            entry,
            description,
        )
        entities.append(sensor)

    for description in ENERGYMANAGEMENT_SENSOR_TYPES:
        sensor = StiebelEltronISGSensor(
            coordinator,
            entry,
            description,
        )
        entities.append(sensor)

    for description in ENERGY_SENSOR_TYPES:
        sensor = StiebelEltronISGSensor(
            coordinator,
            entry,
            description,
        )
        entities.append(sensor)

    for description in ENERGY_DAILY_SENSOR_TYPES:
        sensor = StiebelEltronISGEnergySensor(
            coordinator,
            entry,
            description,
        )
        entities.append(sensor)

    if not coordinator.is_wpm:
        for description in COMPRESSOR_SENSOR_TYPES:
            sensor = StiebelEltronISGSensor(
                coordinator,
                entry,
                description,
            )
            entities.append(sensor)
        for description in VENTILATION_SENSOR_TYPES:
            sensor = StiebelEltronISGSensor(
                coordinator,
                entry,
                description,
            )
            entities.append(sensor)

    async_add_devices(entities)


class StiebelEltronISGSensor(StiebelEltronISGEntity, SensorEntity):
    """stiebel_eltron_isg Sensor class."""

    def __init__(
        self,
        coordinator,
        config_entry,
        description,
    ):
        """Initialize the sensor."""
        self.entity_description = description
        super().__init__(coordinator, config_entry)

    @property
    def unique_id(self) -> str | None:
        """Return the unique id of the sensor."""
        return f"{DOMAIN}_{self.coordinator.name}_{self.entity_description.key}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data.get(self.entity_description.key) is not None


class StiebelEltronISGEnergySensor(StiebelEltronISGEntity, SensorEntity):
    """stiebel_eltron_isg Energy Sensor class."""

    def __init__(
        self,
        coordinator,
        config_entry,
        description,
    ):
        """Initialize the sensor."""
        self.entity_description = description
        super().__init__(coordinator, config_entry)

    @property
    def unique_id(self) -> str | None:
        """Return the unique id of the sensor."""
        return f"{DOMAIN}_{self.coordinator.name}_{self.entity_description.key}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data.get(self.entity_description.key) is not None

    @property
    def last_reset(self) -> datetime.datetime | None:
        """Set Last Reset to now, if value is 0."""
        value = self.coordinator.data.get(self.entity_description.key)
        if value is not None and value == 0:
            return dt_util.utcnow()
        return None