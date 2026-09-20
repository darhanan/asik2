package aitu.sdp.assignment2.app;

/** Raised when the user supplies a delivery mode or UI platform the application does not support. */
public final class UnsupportedChoiceException extends RuntimeException {

    public UnsupportedChoiceException(String message) {
        super(message);
    }
}
