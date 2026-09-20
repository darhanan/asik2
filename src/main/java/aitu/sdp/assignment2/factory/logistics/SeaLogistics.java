package aitu.sdp.assignment2.factory.logistics;

import aitu.sdp.assignment2.factory.transport.Ship;
import aitu.sdp.assignment2.factory.transport.Transport;

/** Concrete creator: the sea branch always produces a {@link Ship}. */
public final class SeaLogistics extends Logistics {

    @Override
    protected Transport createTransport() {
        return new Ship();
    }
}
