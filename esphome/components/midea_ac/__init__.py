import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate, sensor
from esphome.components.midea_dongle import CONF_MIDEA_DONGLE_ID, MideaDongle
from esphome.const import (CONF_BOOST, CONF_ECO, CONF_ID, CONF_SLEEP,
                           ICON_THERMOMETER, UNIT_CELSIUS)

DEPENDENCIES = ['midea_dongle']
AUTO_LOAD = ['climate', 'sensor']
CODEOWNERS = ['@dudanov']

CONF_BEEPER = 'beeper'
CONF_OUTDOOR_TEMPERATURE = 'outdoor_temperature'
midea_ac_ns = cg.esphome_ns.namespace('midea_ac')
MideaAC = midea_ac_ns.class_('MideaAC', climate.Climate, cg.Component)

CONFIG_SCHEMA = cv.All(climate.CLIMATE_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(MideaAC),
    cv.GenerateID(CONF_MIDEA_DONGLE_ID): cv.use_id(MideaDongle),
    cv.Optional(CONF_BEEPER): cv.boolean,
    cv.Optional(CONF_BOOST): cv.boolean,
    cv.Optional(CONF_ECO): cv.boolean,
    cv.Optional(CONF_SLEEP): cv.boolean,
    cv.Optional(CONF_OUTDOOR_TEMPERATURE): sensor.sensor_schema(UNIT_CELSIUS, ICON_THERMOMETER, 0),
}).extend(cv.COMPONENT_SCHEMA))


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield climate.register_climate(var, config)
    paren = yield cg.get_variable(config[CONF_MIDEA_DONGLE_ID])
    cg.add(var.set_midea_dongle_parent(paren))
    if CONF_BEEPER in config:
        cg.add(var.set_beeper_feedback(config[CONF_BEEPER]))
    if CONF_OUTDOOR_TEMPERATURE in config:
        sens = yield sensor.new_sensor(config[CONF_OUTDOOR_TEMPERATURE])
        cg.add(var.set_outdoor_temperature_sensor(sens))
    if CONF_BOOST in config:
        cg.add(var.set_supports_boost(config[CONF_BOOST]))
    if CONF_SLEEP in config:
        cg.add(var.set_supports_sleep_(config[CONF_SLEEP]))
    if CONF_ECO in config:
        cg.add(var.set_supports_eco(config[CONF_ECO]))