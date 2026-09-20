package aitu.sdp.assignment2.factory.logistics;

import aitu.sdp.assignment2.factory.transport.Transport;
import aitu.sdp.assignment2.factory.transport.Truck;

/** Concrete creator: the road branch always produces a {@link Truck}. */
public final class RoadLogistics extends Logistics {

    @Override
    protected Transport createTransport() {
        return new Truck();
    }
}
