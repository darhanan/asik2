package aitu.sdp.assignment2.app;

import aitu.sdp.assignment2.abstractfactory.factories.GUIFactory;
import aitu.sdp.assignment2.factory.logistics.Logistics;
import java.util.Scanner;

/**
 * Entry point. Collects the two independent choices, validates them, wires the selected creator
 * and factory into {@link DeliveryApplication}, and prints the result.
 *
 * <p>Usage:</p>
 * <pre>
 *   java -cp out aitu.sdp.assignment2.app.Main ROAD WINDOWS
 *   java -cp out aitu.sdp.assignment2.app.Main            (then answer the two prompts)
 * </pre>
 */
public final class Main {

    private static final String CARGO = "laboratory equipment";
    private static final String DESTINATION = "Aktau warehouse";
    private static final int EXIT_INVALID_INPUT = 1;

    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            String deliveryMode = readChoice(args, 0, "Delivery mode (" + LogisticsSelector.SUPPORTED_MODES + "): ", scanner);
            String platform = readChoice(args, 1, "UI platform (" + GUIFactorySelector.SUPPORTED_PLATFORMS + "): ", scanner);
            start(deliveryMode, platform);
        } catch (UnsupportedChoiceException invalidChoice) {
            System.out.println(invalidChoice.getMessage());
            System.out.println("Stopping without running the delivery.");
            System.exit(EXIT_INVALID_INPUT);
        }
    }

    /**
     * Takes the choice from the arguments when it is present, otherwise asks the user once.
     *
     * @throws UnsupportedChoiceException if no argument was given and the console input has ended
     */
    private static String readChoice(String[] args, int index, String prompt, Scanner scanner) {
        if (index < args.length) {
            return args[index];
        }
        System.out.print(prompt);
        if (!scanner.hasNextLine()) {
            System.out.println();
            throw new UnsupportedChoiceException("Missing input: no value was provided.");
        }
        return scanner.nextLine();
    }

    /** Validates both choices, builds the application, and prints every line it produces. */
    private static void start(String deliveryMode, String platform) {
        Logistics logistics = LogisticsSelector.select(deliveryMode);
        GUIFactory guiFactory = GUIFactorySelector.select(platform);

        System.out.println("Delivery mode: " + deliveryMode.trim().toUpperCase());
        System.out.println("UI platform: " + platform.trim().toUpperCase());

        DeliveryApplication application = new DeliveryApplication(guiFactory, logistics);
        for (String line : application.run(CARGO, DESTINATION)) {
            System.out.println(line);
        }
    }
}
