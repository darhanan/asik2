# Assignment 2 - Factory Method and Abstract Factory

Astana IT University | School of Software Engineering
Course: ShP-2216 Software Design Patterns | Academic year 2026-2027
Individual work | Java, JDK 17

## Project purpose

One console logistics application that combines two creational patterns in a single run:

- **Factory Method** creates the transport. An abstract `Logistics` creator declares
  `createTransport()` and owns the shared `planDelivery(cargo, destination)` workflow;
  `RoadLogistics` and `SeaLogistics` override the factory method to produce a `Truck` or a `Ship`.
- **Abstract Factory** creates a matching pair of UI components. `GUIFactory` declares
  `createButton()` and `createCheckbox()`; `WindowsFactory` and `MacOSFactory` each produce a
  complete, consistent family.

The delivery mode and the UI platform are chosen independently at runtime, so all four
combinations work without editing any code.

## Package structure

```
src/main/java/aitu/sdp/assignment2/
├── factory/                                   Part A - Factory Method
│   ├── transport/
│   │   ├── Transport.java                     Product      (interface)
│   │   ├── Truck.java                         Concrete product - road
│   │   └── Ship.java                          Concrete product - sea
│   └── logistics/
│       ├── Logistics.java                     Creator      (abstract, holds planDelivery)
│       ├── RoadLogistics.java                 Concrete creator -> Truck
│       └── SeaLogistics.java                  Concrete creator -> Ship
├── abstractfactory/                           Part B - Abstract Factory
│   ├── ui/
│   │   ├── Button.java                        Abstract product
│   │   ├── Checkbox.java                      Abstract product
│   │   ├── WindowsButton.java                 Windows family
│   │   ├── WindowsCheckbox.java               Windows family
│   │   ├── MacOSButton.java                   macOS family
│   │   └── MacOSCheckbox.java                 macOS family
│   └── factories/
│       ├── GUIFactory.java                    Abstract factory
│       ├── WindowsFactory.java                Concrete factory
│       └── MacOSFactory.java                  Concrete factory
└── app/                                       Startup and client
    ├── Main.java                              Entry point, input handling
    ├── LogisticsSelector.java                 Startup selection: text -> concrete creator
    ├── GUIFactorySelector.java                Startup selection: text -> concrete factory
    ├── UnsupportedChoiceException.java        Signals an invalid or missing choice
    └── DeliveryApplication.java               Client of both patterns

docs/
├── uml-factory-method.puml                    UML source - Factory Method
├── uml-abstract-factory.puml                  UML source - Abstract Factory
├── uml-diagrams.md                            Readable ASCII version of both diagrams
├── verification-transcript.txt                Evidence for the six required checks
└── clean-code-evidence.md                     Annotated Clean Code excerpts
```

## Prerequisites

- JDK 17 or newer (`javac` and `java` on the PATH). The sources are compiled with
  `--release 17`, so the bytecode is JDK 17 compatible even on a newer JDK.
- No Maven, Gradle, database, or network access is required.

## Build

From the repository root:

```bash
javac --release 17 -d out $(find src -name '*.java')
```

On Windows PowerShell:

```powershell
javac --release 17 -d out (Get-ChildItem -Recurse -Filter *.java src).FullName
```

## Run

Two independent choices: delivery mode and UI platform.

**With command-line arguments:**

```bash
java -cp out aitu.sdp.assignment2.app.Main ROAD WINDOWS
```

**With console input** (the program prompts for each value):

```bash
java -cp out aitu.sdp.assignment2.app.Main
Delivery mode (ROAD, SEA): ROAD
UI platform (WINDOWS, MACOS): WINDOWS
```

## Supported input values

| Choice        | Accepted values      | Notes                                        |
|---------------|----------------------|----------------------------------------------|
| Delivery mode | `ROAD`, `SEA`        | Case-insensitive, surrounding spaces trimmed  |
| UI platform   | `WINDOWS`, `MACOS`   | Case-insensitive, surrounding spaces trimmed  |

Validation behaviour: an unsupported value, an empty value, or missing input prints a clear
message naming the supported values, then stops cleanly with exit code `1`. The program never
falls back to a silent default and never continues with a null factory. Selecting `MACOS` does
not require a computer running macOS - the components only print their platform.

## Sample run

```
$ java -cp out aitu.sdp.assignment2.app.Main ROAD WINDOWS
Delivery mode: ROAD
UI platform: WINDOWS
UI family: WINDOWS
Rendering Windows button
Rendering Windows checkbox
Truck delivers laboratory equipment to Aktau warehouse by highway route
```

Changing only the platform replaces both UI components and keeps the transport:

```
$ java -cp out aitu.sdp.assignment2.app.Main ROAD MACOS
Delivery mode: ROAD
UI platform: MACOS
UI family: MACOS
Rendering macOS button
Rendering macOS checkbox
Truck delivers laboratory equipment to Aktau warehouse by highway route
```

Invalid choice:

```
$ java -cp out aitu.sdp.assignment2.app.Main AIR WINDOWS
Unsupported delivery mode: 'AIR'. Supported values: ROAD, SEA.
Stopping without running the delivery.
```

The full transcript of all six required checks is in `docs/verification-transcript.txt`.

## Assessed commit

<!-- Fill this in after your final push, and copy the same value into the report. -->
Submitted commit: `<commit-hash>`

## References

- Lecture 2: Factory Method and Abstract Factory, ShP-2216 Software Design Patterns, AITU.
- E. Freeman, E. Robson. *Head First Design Patterns*, Chapter 4 (Factory Pattern).
- R. C. Martin. *Clean Code*, Chapter 6 (Objects and Data Structures).
