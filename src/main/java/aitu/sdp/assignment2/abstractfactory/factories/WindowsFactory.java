package aitu.sdp.assignment2.abstractfactory.factories;

import aitu.sdp.assignment2.abstractfactory.ui.Button;
import aitu.sdp.assignment2.abstractfactory.ui.Checkbox;
import aitu.sdp.assignment2.abstractfactory.ui.WindowsButton;
import aitu.sdp.assignment2.abstractfactory.ui.WindowsCheckbox;

/** Concrete factory producing the complete Windows component family. */
public final class WindowsFactory implements GUIFactory {

    @Override
    public Button createButton() {
        return new WindowsButton();
    }

    @Override
    public Checkbox createCheckbox() {
        return new WindowsCheckbox();
    }

    @Override
    public String platformName() {
        return "WINDOWS";
    }
}
