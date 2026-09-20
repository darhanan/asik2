package aitu.sdp.assignment2.factory.transport;

/**
 * Concrete product: road delivery.
 *
 * <p>The route is internal state of the truck. It is private and has no accessor, because no
 * caller needs the raw value - callers only need the delivery result (Clean Code, Chapter 6).</p>
 */
public final class Truck implements Transport {

    private static final String ROAD_ROUTE = "highway route";

    @Override
    public String deliver(String cargo, String destination) {
        return "Truck delivers " + cargo + " to " + destination + " by " + ROAD_ROUTE;
    }
}
