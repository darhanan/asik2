package aitu.sdp.assignment2.abstractfactory.ui;

/** Abstract product: a clickable button, rendered by the platform that owns it. */
public interface Button {

    /**
     * Renders the button.
     *
     * @return one line naming the platform and the component type
     */
    String paint();
}
