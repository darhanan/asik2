# Clean Code evidence

Five practices, each with an excerpt from the submitted code and the specific benefit.
Practices 4 and 5 are the two explanations connected to *Clean Code*, Chapter 6
(Objects and Data Structures).

---

## 1. Meaningful names

Names identify both the domain and the pattern role, so a reader can tell what a class *is*
in the pattern just from its name.

```java
// src/main/java/aitu/sdp/assignment2/factory/logistics/Logistics.java
public abstract class Logistics {
    protected abstract Transport createTransport();
    public String planDelivery(String cargo, String destination) { ... }
}

// src/main/java/aitu/sdp/assignment2/factory/logistics/RoadLogistics.java
public final class RoadLogistics extends Logistics { ... }
```

**Benefit.** `Logistics` / `RoadLogistics` / `SeaLogistics` name the creator role, `Transport` /
`Truck` / `Ship` name the product role, and `GUIFactory` / `WindowsFactory` name the factory role.
The parameters `cargo` and `destination` say what the values mean rather than `String a, String b`.
During the defense the class name alone answers "which pattern role is this?", and no comment is
needed to explain the mapping.

---

## 2. Small methods with one responsibility

Input handling, selection, construction, rendering, and delivery are separate methods in
separate classes instead of one long `main`.

```java
// src/main/java/aitu/sdp/assignment2/app/Main.java
public static void main(String[] args) {
    try (Scanner scanner = new Scanner(System.in)) {
        String deliveryMode = readChoice(args, 0, "...", scanner);   // input only
        String platform     = readChoice(args, 1, "...", scanner);   // input only
        start(deliveryMode, platform);                               // wiring + output
    } catch (UnsupportedChoiceException invalidChoice) {
        System.out.println(invalidChoice.getMessage());              // error reporting only
        System.out.println("Stopping without running the delivery.");
        System.exit(EXIT_INVALID_INPUT);
    }
}
```

**Benefit.** Each method does one thing at one level of abstraction: `readChoice` only obtains a
raw string, `LogisticsSelector.select` / `GUIFactorySelector.select` only validate and choose,
`DeliveryApplication.run` only renders and delivers. Changing how input arrives (for example,
reading from a file) touches `readChoice` alone; the pattern code is untouched.

---

## 3. Avoid duplicated logic

The delivery workflow exists once, in the base creator, instead of being copied into each
concrete creator.

```java
// src/main/java/aitu/sdp/assignment2/factory/logistics/Logistics.java
public String planDelivery(String cargo, String destination) {
    Transport transport = createTransport();          // varies by subclass
    return transport.deliver(cargo, destination);     // identical for every subclass
}
```

**Benefit.** `RoadLogistics` and `SeaLogistics` contain only the line that actually differs -
which transport to instantiate. The workflow steps (obtain a transport, hand it the cargo and
destination) are written once, so a change to the workflow cannot fall out of sync between the
road and sea branches. The same reasoning applies to the UI side: repeated component creation
lives inside `WindowsFactory` / `MacOSFactory` rather than being repeated at every call site.

---

## 4. Data abstraction (*Clean Code*, Chapter 6)

Callers depend on abstract contracts and never see a concrete implementation type. Chapter 6
argues that a class should *expose abstract interfaces that let users manipulate the essence of
the data without having to know its implementation*.

```java
// src/main/java/aitu/sdp/assignment2/app/DeliveryApplication.java
public final class DeliveryApplication {

    private final GUIFactory guiFactory;   // abstraction, not WindowsFactory
    private final Logistics logistics;     // abstraction, not RoadLogistics
    private final Button button;           // abstraction, not WindowsButton
    private final Checkbox checkbox;       // abstraction, not WindowsCheckbox

    public DeliveryApplication(GUIFactory guiFactory, Logistics logistics) {
        this.guiFactory = guiFactory;
        this.logistics  = logistics;
        this.button     = guiFactory.createButton();     // obtained from the factory
        this.checkbox   = guiFactory.createCheckbox();   // never `new WindowsButton()`
    }

    public String[] run(String cargo, String destination) {
        return new String[] {
            "UI family: " + guiFactory.platformName(),
            button.paint(),                                   // through the interface
            checkbox.paint(),                                 // through the interface
            logistics.planDelivery(cargo, destination)        // through the abstract creator
        };
    }
}
```

**Benefit.** Every field is declared as an interface or abstract class, so the client has no way
to depend on `WindowsButton` or `Truck`. There is no `instanceof`, no cast, and no branching on a
concrete type anywhere in the client: the implementation is genuinely hidden, not merely wrapped
in getters. Adding a Linux UI family therefore requires no change to this class at all.

---

## 5. Objects and encapsulation (*Clean Code*, Chapter 6)

Behaviour is expressed as a method; internal state stays private and is not exposed through
accessors that no caller needs.

```java
// src/main/java/aitu/sdp/assignment2/factory/transport/Truck.java
public final class Truck implements Transport {

    private static final String ROAD_ROUTE = "highway route";   // private, no getter

    @Override
    public String deliver(String cargo, String destination) {   // behaviour, not data
        return "Truck delivers " + cargo + " to " + destination + " by " + ROAD_ROUTE;
    }
}
```

**Benefit.** Chapter 6 contrasts an *object*, which hides its data and exposes behaviour, with a
*data structure*, which exposes its data and has no meaningful behaviour. `Truck` is an object in
that sense: the route is private with no `getRoadRoute()`, and the only thing a caller can ask is
"deliver this cargo". Had the class instead exposed `getRoadRoute()`, callers would begin
assembling delivery messages themselves, and the delivery rule would leak out of the class. The
same holds for `DeliveryApplication`, whose `button` and `checkbox` fields are private and are
used only inside `run(...)`.

> Note on stateless classes: `WindowsFactory`, `MacOSFactory`, `RoadLogistics`, and
> `SeaLogistics` hold no state at all. That is intentional - they exist purely to make a creation
> decision - and the rubric explicitly accepts stateless classes.
