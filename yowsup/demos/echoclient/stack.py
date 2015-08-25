from yowsup.stacks import YowStack
from .layer import EchoLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.layers.stanzaregulator             import YowStanzaRegulator
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.logger                      import YowLoggerLayer
from yowsup.layers.protocol_iq                 import YowIqProtocolLayer
from yowsup.layers.protocol_calls              import YowCallsProtocolLayer
from yowsup.layers.protocol_groups             import YowGroupsProtocolLayer
from yowsup.common import YowConstants
from yowsup import env

class YowsupEchoStack(object):
    def __init__(self, credentials, log_path, encryptionEnabled = False):
        protocol_layers = (
            YowAuthenticationProtocolLayer,
            YowMessagesProtocolLayer,
            YowReceiptProtocolLayer,
            YowAckProtocolLayer,
            YowMediaProtocolLayer,
            YowIqProtocolLayer,
            YowCallsProtocolLayer,
            YowGroupsProtocolLayer
        )

        if encryptionEnabled:
            from yowsup.layers.axolotl import YowAxolotlLayer
            layers = (
                EchoLayer,
                protocol_layers,
                YowAxolotlLayer,
                YowLoggerLayer(log_path=log_path),
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )
        else:
            layers = (
                EchoLayer,
                protocol_layers,
                YowLoggerLayer(log_path=log_path),
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )

        self.stack = YowStack(layers)
        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
