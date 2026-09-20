package aitu.sdp.assignment2.app;

import aitu.sdp.assignment2.abstractfactory.factories.GUIFactory;
import aitu.sdp.assignment2.abstractfactory.ui.Button;
import aitu.sdp.assignment2.abstractfactory.ui.Checkbox;
import aitu.sdp.assignment2.factory.logistics.Logistics;

/**
 * Client of both patterns.
 *
 * <p>It receives a {@link GUIFactory} and a {@link Logistics} through its constructor and uses
 * them only through those abstractions: it never calls a concrete component constructor, never
 * casts, and never inspects a concrete class to decide what to do.</p>
 */
public final class DeliveryApplication {

    private final GUIFactory guiFactory;
    private final Logistics logistics;
    private final Button button;
    private final Checkbox checkbox;

    /**
     * @param guiFactory supplies the matching pair of UI components
     * @param logistics  supplies the delivery workflow for the chosen delivery mode
     */
    public DeliveryApplication(GUIFactory guiFactory, Logistics logistics) {
        this.guiFactory = guiFactory;
        this.logistics = logistics;
        this.button = guiFactory.createButton();
        this.checkbox = guiFactory.createCheckbox();
    }

    /**
     * Renders both UI components and then runs the delivery workflow.
     *
     * @param cargo       description of the goods to move
     * @param destination where the cargo has to arrive
     * @return the lines the application produced, in the order they were produced
     */
    public String[] run(String cargo, String destination) {
        return new String[] {
            "UI family: " + guiFactory.platformName(),
            button.paint(),
            checkbox.paint(),
            logistics.planDelivery(cargo, destination)
        };
    }
}
