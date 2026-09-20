package aitu.sdp.assignment2.factory.logistics;

import aitu.sdp.assignment2.factory.transport.Transport;

/**
 * Creator role of the Factory Method pattern.
 *
 * <p>Holds the delivery workflow that every logistics branch shares, but leaves the decision of
 * <em>which</em> transport to use to its subclasses. This is the difference from a Simple Factory:
 * there is no conditional here, the choice is made by overriding {@link #createTransport()}.</p>
 */
public abstract class Logistics {

    /**
     * Factory method. Subclasses decide which concrete transport is produced.
     *
     * @return a transport seen only through its {@link Transport} contract
     */
    protected abstract Transport createTransport();

    /**
     * Shared workflow: obtains a transport through the factory method and runs the delivery
     * through the {@link Transport} contract. It never mentions a concrete transport class.
     *
     * @param cargo       description of the goods to move
     * @param destination where the cargo has to arrive
     * @return the delivery report produced by the created transport
     */
    public String planDelivery(String cargo, String destination) {
        Transport transport = createTransport();
        return transport.deliver(cargo, destination);
    }
}
