# Assignment 2 - Factory Method and Abstract Factory

**Course:** ShP-2216 Software Design Patterns  
**Institution:** Astana IT University, School of Software Engineering  
**Academic year:** 2026-2027 | Programme 6B06102 Software Engineering, Year 2, Trimester 4  
**Student:** Darkhan Tynyshtyk  
**Group:** SE-2523  
**GitHub repository:** https://github.com/darhanan/asik2  
**Submitted commit:** tag `submission-v1` (see README for the exact hash)

---

## 1. Introduction

The application is a console logistics program. In a single run it does two things: it plans a
delivery using either a truck or a ship, and it renders a button and a checkbox belonging to
either the Windows or the macOS UI family. The delivery mode and the UI platform are chosen
independently at startup, so all four combinations run without any code change.

**Why Factory Method fits the transport part.** There is a single product hierarchy - a
`Transport` - and one varying decision: which concrete transport a given logistics branch uses.
The steps around that decision (obtain a transport, hand it the cargo and destination, report the
result) are identical for road and sea. Factory Method is designed exactly for this shape: the
shared steps live in the creator's `planDelivery(...)`, and the single varying step is deferred to
subclasses through `createTransport()`. A Simple Factory would place that decision in one
conditional, which would have to be edited every time a transport is added; with Factory Method a
new transport is a new subclass instead.

**Why Abstract Factory fits the UI part.** Here there is not one product hierarchy but two -
`Button` and `Checkbox` - and the products must be *consistent*: a Windows button must never
appear next to a macOS checkbox. Abstract Factory expresses precisely that constraint. Because one
`GUIFactory` implementation supplies both creation methods, choosing `WindowsFactory` makes a
mixed pair structurally impossible; the client cannot produce one even by mistake, because it
never calls a component constructor at all.

The two patterns are complementary and not interchangeable: the transport side varies along one
axis (one product, several implementations), while the UI side varies along two (several products
that must belong to the same family).

---

## 2. UML class diagrams

> Insert the rendered images here. Sources: `docs/uml-factory-method.puml` and
> `docs/uml-abstract-factory.puml`; a readable ASCII version of both is in `docs/uml-diagrams.md`.

### 2.1 Factory Method (Part A)

Roles shown in the diagram:

| Pattern role      | Class in the code                       |
|-------------------|-----------------------------------------|
| Product           | `Transport` (interface)                 |
| Concrete products | `Truck`, `Ship`                         |
| Creator           | `Logistics` (abstract)                  |
| Concrete creators | `RoadLogistics`, `SeaLogistics`         |
| Client            | `DeliveryApplication`                   |

Relationships: `Truck` and `Ship` implement `Transport`; `RoadLogistics` and `SeaLogistics`
extend `Logistics`; `Logistics` depends on `Transport` (it creates and uses one); each concrete
creator has a `<<creates>>` dependency on its own transport; `DeliveryApplication` depends on the
abstract `Logistics` type only.

Runtime path, matching the code exactly:

```
DeliveryApplication.run(cargo, destination)
  -> Logistics.planDelivery(cargo, destination)     shared workflow, no concrete type named
       -> createTransport()                         overridden by RoadLogistics / SeaLogistics
            -> new Truck()  |  new Ship()
       -> Transport.deliver(cargo, destination)     invoked through the contract
```

### 2.2 Abstract Factory (Part B)

| Pattern role       | Class in the code                                                   |
|--------------------|---------------------------------------------------------------------|
| Abstract products  | `Button`, `Checkbox` (interfaces, each with `paint()`)               |
| Concrete products  | `WindowsButton`, `WindowsCheckbox`, `MacOSButton`, `MacOSCheckbox`   |
| Abstract factory   | `GUIFactory` with `createButton()` and `createCheckbox()`            |
| Concrete factories | `WindowsFactory`, `MacOSFactory`                                     |
| Client             | `DeliveryApplication` (constructor injection of `GUIFactory`)        |

`createButton()` is declared as returning `Button` and `createCheckbox()` as returning `Checkbox`,
so the client is never handed a concrete type. `WindowsFactory` creates the Windows pair,
`MacOSFactory` the macOS pair; the family grouping is visible in the diagram as the two
`<<creates>>` dependencies leaving each factory.

---

## 3. Clean Code evidence

Five practices with annotated excerpts are documented in full in `docs/clean-code-evidence.md`;
the same content is reproduced in Section 3 of this report. Summary:

| # | Practice                                  | Where it is shown                               |
|---|-------------------------------------------|-------------------------------------------------|
| 1 | Meaningful names                          | `Logistics`, `RoadLogistics`, `Transport`, `GUIFactory` |
| 2 | Small methods, one responsibility each    | `Main.main`<br>`readChoice`<br>`start`             |
| 3 | No duplicated logic                       | `Logistics.planDelivery(...)` written once       |
| 4 | **Data abstraction (Chapter 6)**          | `DeliveryApplication` fields typed as interfaces |
| 5 | **Objects and encapsulation (Chapter 6)** | `Truck.deliver(...)`, private `ROAD_ROUTE`       |

Items 4 and 5 are the two explanations connected to *Clean Code*, Chapter 6.

---

## 4. Verification evidence

All checks were run on one machine with the commands from the README. The full console transcript
is in `docs/verification-transcript.txt`.

| # | Input | Expected result | Actual result | Status |
|---|-------|-----------------|---------------|--------|
| 1 | `ROAD WINDOWS` | Truck delivery; Windows button and checkbox | `UI family: WINDOWS`<br>`Rendering Windows button`<br>`Rendering Windows checkbox`<br>`Truck delivers laboratory equipment to Aktau warehouse by highway route` | PASS |
| 2 | `SEA WINDOWS` | Ship delivery; Windows button and checkbox | `UI family: WINDOWS`<br>`Rendering Windows button`<br>`Rendering Windows checkbox`<br>`Ship delivers laboratory equipment to Aktau warehouse in containers by sea route` | PASS |
| 3 | `ROAD MACOS` | Truck delivery; macOS button and checkbox | `UI family: MACOS`<br>`Rendering macOS button`<br>`Rendering macOS checkbox`<br>`Truck delivers laboratory equipment to Aktau warehouse by highway route` | PASS |
| 4 | `SEA MACOS` | Ship delivery; macOS button and checkbox | `UI family: MACOS`<br>`Rendering macOS button`<br>`Rendering macOS checkbox`<br>`Ship delivers laboratory equipment to Aktau warehouse in containers by sea route` | PASS |
| 5 | `AIR WINDOWS` | Clear validation message; no delivery | `Unsupported delivery mode: 'AIR'. Supported values: ROAD, SEA.`<br>`Stopping without running the delivery.` Exit code 1; no UI rendered, no delivery performed | PASS |
| 6 | `ROAD LINUX` | Clear validation message; no UI construction | `Unsupported UI platform: 'LINUX'. Supported values: WINDOWS, MACOS.`<br>`Stopping without running the delivery.` Exit code 1; no components created | PASS |

**Missing-input behaviour.** Documented in the README: when a value is not supplied as an
argument, the program prompts for it; if no console input is available, or the value is blank, it
prints `Missing delivery mode. Supported values: ROAD, SEA.` (or the corresponding platform
message) and stops with exit code 1. Verified: running `java -cp out aitu.sdp.assignment2.app.Main`
with no arguments and no input printed `Missing input: no value was provided.` followed by
`Stopping without running the delivery.` No default was substituted and no factory was left null.

**Cross-platform note.** Check 3 and Check 4 were executed on a single machine. Selecting the
macOS family does not require a computer running macOS, because the components only print their
platform and component type.

Additional observation: input is accepted case-insensitively (`road` / `macos` work), which is
documented in the README as supported behaviour.

---

## 5. Conclusion

### 5.1 Comparing the two patterns

Factory Method and Abstract Factory both remove `new` from the client, but they answer different
questions.

*Factory Method* concerns **one product hierarchy**. A single creation step inside an otherwise
fixed algorithm is deferred to a subclass. The variation is expressed through inheritance: each
subclass overrides one method. In this project that is the transport - `RoadLogistics` and
`SeaLogistics` differ in exactly one line, and everything else is shared in `planDelivery(...)`.

*Abstract Factory* concerns **several related product families**. It groups multiple creation
methods behind one interface so that the products a client receives are guaranteed to be
consistent with one another. The variation is expressed through composition: the client is handed
an object. In this project that is the UI - `WindowsFactory` supplies both a Windows button and a
Windows checkbox, and family consistency is the whole point.

The relationship to *Simple Factory* is also worth stating: a Simple Factory concentrates the
decision in one conditional inside a single `create(type)` method. Adding a product means editing
that conditional, so the creation code is not closed to modification. Factory Method replaces the
conditional with subclass overrides, so adding a product means adding a class. The small `switch`
in `LogisticsSelector` and `GUIFactorySelector` is *not* a Simple Factory in this sense: it runs
once at startup to translate a user's text choice into an object, and after that no branching on
type occurs anywhere. Some mapping from external input to an object is unavoidable in any program
that takes user input; what matters is that the delivery and rendering logic below it contains no
conditionals, casts, or `instanceof` checks on product types.

### 5.2 Design reflection - what would change for three extensions

**(a) Adding one more transport, e.g. `Drone` for air delivery.**

- *Add:* `Drone implements Transport` (one new class) and `AirLogistics extends Logistics`
  overriding `createTransport()` to return a `Drone` (one new class).
- *Change:* one line in `LogisticsSelector.select(...)` to map `"AIR"` to `AirLogistics`, and the
  `SUPPORTED_MODES` constant so the validation message stays accurate.
- *Unchanged:* `Logistics.planDelivery(...)`, `Transport`, `Truck`, `Ship`, the entire Abstract
  Factory side, and `DeliveryApplication` - which depends only on the abstract `Logistics` type
  and therefore cannot notice a new subclass. This is the payoff of Factory Method: the shared
  workflow is closed to modification.

**(b) Adding one more UI family, e.g. Linux.**

- *Add:* `LinuxButton implements Button`, `LinuxCheckbox implements Checkbox`, and
  `LinuxFactory implements GUIFactory` returning that pair (three new classes).
- *Change:* one line in `GUIFactorySelector.select(...)` plus the `SUPPORTED_PLATFORMS` constant.
- *Unchanged:* `Button`, `Checkbox`, `GUIFactory`, the existing Windows and macOS classes, and
  `DeliveryApplication`, which receives a `GUIFactory` and calls `createButton()` /
  `createCheckbox()` without knowing which family answered. Adding a *family* is the cheap
  direction for Abstract Factory.

**(c) Adding one more UI product type, e.g. a text field.**

This is the expensive direction, and it is a known trade-off of Abstract Factory rather than a
flaw in this implementation.

- *Add:* a `TextField` interface with `paint()`, plus one implementation per family
  (`WindowsTextField`, `MacOSTextField`).
- *Change:* `GUIFactory` must declare `createTextField(): TextField` - and because that is a new
  method on the interface, **every** existing concrete factory must implement it. With two
  families that is two edits; with ten families it would be ten. `DeliveryApplication` must also
  change if the new component is to be rendered, since it decides which components the screen
  contains.
- *Unchanged:* `Button`, `Checkbox`, all four existing component classes, the selectors (no new
  input value is introduced), and the whole Factory Method side.

In short: **new families are cheap, new product types are expensive.** Both extension directions
leave the startup selection code as the only place that mentions concrete classes, and leave the
delivery and rendering logic untouched.

### 5.3 References

1. Lecture 2: Factory Method and Abstract Factory (Logistics and GUI examples; Clean Code,
   Chapter 6 slides), ShP-2216 Software Design Patterns, Astana IT University, 2026-2027.
2. E. Freeman, E. Robson. *Head First Design Patterns*, 2nd ed., O'Reilly, Chapter 4 - The Factory
   Pattern.
3. R. C. Martin. *Clean Code: A Handbook of Agile Software Craftsmanship*, Prentice Hall,
   Chapter 6 - Objects and Data Structures.
4. E. Gamma, R. Helm, R. Johnson, J. Vlissides. *Design Patterns: Elements of Reusable
   Object-Oriented Software*, Addison-Wesley - Factory Method and Abstract Factory.
5. Software Design Patterns syllabus 2026-2027 and the official course calendar in Moodle.
