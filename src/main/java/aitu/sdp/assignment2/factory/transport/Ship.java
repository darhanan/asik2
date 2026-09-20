package aitu.sdp.assignment2.factory.transport;

/**
 * Concrete product: sea delivery.
 *
 * <p>Visibly different from {@link Truck}: it moves cargo in containers over a sea route.</p>
 */
public final class Ship implements Transport {

    private static final String SEA_ROUTE = "sea route";

    @Override
    public String deliver(String cargo, String destination) {
        return "Ship delivers " + cargo + " to " + destination + " in containers by " + SEA_ROUTE;
    }
}
