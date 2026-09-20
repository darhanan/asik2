package aitu.sdp.assignment2.app;

import aitu.sdp.assignment2.factory.logistics.Logistics;
import aitu.sdp.assignment2.factory.logistics.RoadLogistics;
import aitu.sdp.assignment2.factory.logistics.SeaLogistics;

/**
 * Startup selection for the delivery mode.
 *
 * <p>The switch below is the only place in the program that maps a text choice to a concrete
 * creator. Everything after startup works with the abstract {@link Logistics} type.</p>
 */
final class LogisticsSelector {

    static final String SUPPORTED_MODES = "ROAD, SEA";

    private LogisticsSelector() {
    }

    /**
     * @param deliveryMode raw user choice, in any letter case
     * @return the concrete creator for that mode
     * @throws UnsupportedChoiceException if the mode is missing, blank, or not supported
     */
    static Logistics select(String deliveryMode) {
        String normalized = normalize(deliveryMode, "delivery mode");
        return switch (normalized) {
            case "ROAD" -> new RoadLogistics();
            case "SEA" -> new SeaLogistics();
            default -> throw new UnsupportedChoiceException(
                "Unsupported delivery mode: '" + normalized + "'. Supported values: " + SUPPORTED_MODES + ".");
        };
    }

    private static String normalize(String choice, String fieldName) {
        if (choice == null || choice.isBlank()) {
            throw new UnsupportedChoiceException(
                "Missing " + fieldName + ". Supported values: " + SUPPORTED_MODES + ".");
        }
        return choice.trim().toUpperCase();
    }
}
