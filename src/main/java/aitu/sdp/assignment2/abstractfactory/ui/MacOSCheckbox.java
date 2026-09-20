package aitu.sdp.assignment2.abstractfactory.ui;

/** Concrete product of the macOS family. */
public final class MacOSCheckbox implements Checkbox {

    @Override
    public String paint() {
        return "Rendering macOS checkbox";
    }
}
