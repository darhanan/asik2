package aitu.sdp.assignment2.factory.transport;

/**
 * Product role of the Factory Method pattern.
 *
 * <p>Declares the only delivery behaviour the rest of the application is allowed to depend on.
 * Creators and clients talk to this contract, never to {@code Truck} or {@code Ship} directly.</p>
 */
public interface Transport {

    /**
     * Carries the given cargo to the given destination and reports what happened.
     *
     * @param cargo       human readable description of the goods being moved
     * @param destination where the cargo has to arrive
     * @return a single line describing the completed delivery
     */
    String deliver(String cargo, String destination);
}
