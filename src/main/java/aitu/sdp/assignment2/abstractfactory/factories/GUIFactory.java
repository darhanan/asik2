package aitu.sdp.assignment2.abstractfactory.factories;

import aitu.sdp.assignment2.abstractfactory.ui.Button;
import aitu.sdp.assignment2.abstractfactory.ui.Checkbox;

/**
 * Abstract factory role.
 *
 * <p>Declares one creation method per product type. Because a single implementation supplies both
 * methods, a client that uses one factory can never end up with a mixed pair of components.</p>
 */
public interface GUIFactory {

    /** @return a button belonging to this factory's platform family */
    Button createButton();

    /** @return a checkbox belonging to this factory's platform family */
    Checkbox createCheckbox();

    /** @return the family name, used for reporting which UI family was selected */
    String platformName();
}
