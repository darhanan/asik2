package aitu.sdp.assignment2.abstractfactory.ui;

/** Concrete product of the Windows family. */
public final class WindowsCheckbox implements Checkbox {

    @Override
    public String paint() {
        return "Rendering Windows checkbox";
    }
}
