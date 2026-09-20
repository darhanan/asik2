package aitu.sdp.assignment2.abstractfactory.factories;

import aitu.sdp.assignment2.abstractfactory.ui.Button;
import aitu.sdp.assignment2.abstractfactory.ui.Checkbox;
import aitu.sdp.assignment2.abstractfactory.ui.MacOSButton;
import aitu.sdp.assignment2.abstractfactory.ui.MacOSCheckbox;

/**
 * Concrete factory producing the complete macOS component family.
 *
 * <p>The components only print their platform, so this factory runs on any operating system.</p>
 */
public final class MacOSFactory implements GUIFactory {

    @Override
    public Button createButton() {
        return new MacOSButton();
    }

    @Override
    public Checkbox createCheckbox() {
        return new MacOSCheckbox();
    }

    @Override
    public String platformName() {
        return "MACOS";
    }
}
