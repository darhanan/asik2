package aitu.sdp.assignment2.abstractfactory.ui;

/** Abstract product: a checkbox, rendered by the platform that owns it. */
public interface Checkbox {

    /**
     * Renders the checkbox.
     *
     * @return one line naming the platform and the component type
     */
    String paint();
}
