package aitu.sdp.assignment2.abstractfactory.ui;

/** Concrete product of the Windows family. */
public final class WindowsButton implements Button {

    @Override
    public String paint() {
        return "Rendering Windows button";
    }
}
