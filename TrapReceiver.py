from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c
from Email import send_notification

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('50.0.0.2', 162))
)

# SNMPv3/USM setup

# user: usr-md5-none, auth: MD5, priv NONE, securityEngineId: 8000000001020304
# this USM entry is used for TRAP receiving purposes
config.addV3User(
    snmpEngine, 'demo',
    config.usmHMACMD5AuthProtocol, 'password',
    securityEngineId=v2c.OctetString(hexValue='800000090300CA0153900000')
)

f = open("OIDs", "r")
oids = f.readlines()


def analize(name, valor):

    for i in oids:
        oid, desc = i.rstrip('\n').split("|")
        if name.find(oid) != -1:
            mensaje = desc + ": " + valor
            send_notification("sonia_gtz05@hotmail.com","Alerta SNMP", mensaje)


# Callback function for receiving notifications
# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
          varBinds, cbCtx):
    print('Notification from ContextEngineId "%s", ContextName "%s"' % (contextEngineId.prettyPrint(),
                                                                        contextName.prettyPrint()))
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        analize(str(name.prettyPrint()), str(val.prettyPrint()))


# Register SNMP Application at the SNMP engine
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1)  # this job would never finish

# Run I/O dispatcher which would receive queries and send confirmations
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise