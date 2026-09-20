package aitu.sdp.assignment2.app;

import aitu.sdp.assignment2.abstractfactory.factories.GUIFactory;
import aitu.sdp.assignment2.abstractfactory.factories.MacOSFactory;
import aitu.sdp.assignment2.abstractfactory.factories.WindowsFactory;

/**
 * Startup selection for the UI platform.
 *
 * <p>The switch below is the only place that maps a text choice to a concrete factory. From then
 * on the application depends on the {@link GUIFactory} abstraction alone.</p>
 */
final class GUIFactorySelector {

    static final String SUPPORTED_PLATFORMS = "WINDOWS, MACOS";

    private GUIFactorySelector() {
    }

    /**
     * @param platform raw user choice, in any letter case
     * @return the concrete factory for that platform
     * @throws UnsupportedChoiceException if the platform is missing, blank, or not supported
     */
    static GUIFactory select(String platform) {
        String normalized = normalize(platform, "UI platform");
        return switch (normalized) {
            case "WINDOWS" -> new WindowsFactory();
            case "MACOS" -> new MacOSFactory();
            default -> throw new UnsupportedChoiceException(
                "Unsupported UI platform: '" + normalized + "'. Supported values: " + SUPPORTED_PLATFORMS + ".");
        };
    }

    private static String normalize(String choice, String fieldName) {
        if (choice == null || choice.isBlank()) {
            throw new UnsupportedChoiceException(
                "Missing " + fieldName + ". Supported values: " + SUPPORTED_PLATFORMS + ".");
        }
        return choice.trim().toUpperCase();
    }
}
