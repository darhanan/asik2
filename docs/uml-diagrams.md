# UML Class Diagrams

The diagrams that appear in the submitted report PDF are drawn as vector graphics by
`tools/umldiag.py` and embedded directly by `tools/md2pdf.py` (see Section 2 of the report).

Equivalent PlantUML sources are kept in `uml-factory-method.puml` and
`uml-abstract-factory.puml` for anyone who prefers to render them with the PlantUML plugin
in IntelliJ IDEA or the `plantuml` CLI. The ASCII versions below make the structure readable
without any tooling at all.

## Diagram 1 - Factory Method (Part A)

```
        <<interface>>                              abstract
         Transport            <<Product>>          Logistics          <<Creator>>
    +---------------------+                  +---------------------------------+
    | + deliver(cargo,    |<- - - - - - - - -| + planDelivery(cargo, dest):Str |
    |     destination):Str|      creates &   | # createTransport(): Transport  | {abstract}
    +---------------------+      uses        +---------------------------------+
            ^        ^                              ^                 ^
            |        |                              |                 |
     implements   implements                    extends           extends
            |        |                              |                 |
    +-------+--+  +--+---------+        +-----------+-----+  +--------+--------+
    |  Truck   |  |   Ship     |        | RoadLogistics   |  |  SeaLogistics   |
    |----------|  |------------|        |-----------------|  |-----------------|
    | -ROAD_   |  | -SEA_ROUTE |        | # createTrans-  |  | # createTrans-  |
    |  ROUTE   |  | +paint...  |        |   port():       |  |   port():       |
    | +deliver |  | +deliver   |        |   Transport     |  |   Transport     |
    +----------+  +------------+        +-----------------+  +-----------------+
         ^                ^                      :                    :
         |                |                      : <<creates>>        : <<creates>>
         +----------------|----------------------+                    |
                          +---------------------------------------- --+

    DeliveryApplication  <<Client>>  ----> Logistics : calls planDelivery(cargo, destination)
    (depends on the abstract Logistics type only - never on Truck or Ship)

    Runtime path:
      DeliveryApplication.run(...)
        -> Logistics.planDelivery(cargo, destination)      [shared workflow]
          -> createTransport()                             [overridden in the subclass]
            -> new Truck()  /  new Ship()
          -> Transport.deliver(cargo, destination)         [called through the contract]
```

## Diagram 2 - Abstract Factory (Part B)

```
     <<interface>>            <<interface>>              <<interface>>
        Button                  Checkbox                  GUIFactory     <<AbstractFactory>>
   +--------------+         +--------------+     +------------------------------+
   | + paint():Str|         | + paint():Str|     | + createButton(): Button     |
   +--------------+         +--------------+     | + createCheckbox(): Checkbox |
      ^        ^               ^        ^        | + platformName(): String     |
      |        |               |        |        +------------------------------+
      |        |               |        |              ^                  ^
      |        |               |        |         implements         implements
      |        |               |        |              |                  |
+-----+----+ +-+--------+ +----+-----+ +-+---------+  |                  |
| Windows  | | MacOS    | | Windows   | | MacOS     |  |                  |
| Button   | | Button   | | Checkbox  | | Checkbox  |  |                  |
|----------| |----------| |-----------| |-----------|  |                  |
| +paint() | | +paint() | | +paint()  | | +paint()  |  |                  |
+----------+ +----------+ +-----------+ +-----------+  |                  |
      ^            ^            ^             ^        |                  |
      |            |            |             |   +----+----------+  +----+----------+
      |            |            |             |   | WindowsFactory|  | MacOSFactory  |
      |            |            |             |   |---------------|  |---------------|
      |            |            |             |   | +createButton |  | +createButton |
      +--<<creates>>------------|-------------|---| +createCheckbox| | +createCheckbox|
                   |            |             |   | +platformName |  | +platformName |
                   +--<<creates>>-------------+   +---------------+  +---------------+
                                (WindowsFactory -> WindowsButton + WindowsCheckbox)
                                (MacOSFactory   -> MacOSButton   + MacOSCheckbox)

   DeliveryApplication  <<Client>>
   +------------------------------------------------------+
   | - guiFactory: GUIFactory   (injected in constructor)  |
   | - button: Button           (= guiFactory.createButton())
   | - checkbox: Checkbox       (= guiFactory.createCheckbox())
   | + run(cargo, destination): String[]                   |
   +------------------------------------------------------+
      |                |                 |
      +--> GUIFactory  +--> Button       +--> Checkbox
           (injected)       (interface)       (interface)

   The client never calls a concrete component constructor and never casts.
   Because one factory supplies both products, a mixed-family pair is impossible.
```
