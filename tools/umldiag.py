"""Layouts for the two assignment UML diagrams (y grows upward, reportlab convention)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from umlpdf import Box, conn, note, UML

FS = 7.4
FM_W, FM_H = 560, 340
AF_W, AF_H = 640, 430


def factory_method(c):
    transport = Box('Transport', '<<Product>> interface',
                    ops=['+ deliver(cargo, destination): String'], italic=True)
    truck = Box('Truck', '<<ConcreteProduct>>', attrs=['- ROAD_ROUTE: String'],
                ops=['+ deliver(cargo, destination): String'])
    ship = Box('Ship', '<<ConcreteProduct>>', attrs=['- SEA_ROUTE: String'],
               ops=['+ deliver(cargo, destination): String'])
    logistics = Box('Logistics', '<<Creator>> abstract',
                    ops=['+ planDelivery(cargo, destination): String',
                         '# createTransport(): Transport {abstract}'], italic=True)
    road = Box('RoadLogistics', '<<ConcreteCreator>>', ops=['# createTransport(): Transport'])
    sea = Box('SeaLogistics', '<<ConcreteCreator>>', ops=['# createTransport(): Transport'])
    client = Box('DeliveryApplication', '<<Client>>', attrs=['- logistics: Logistics'],
                 ops=['+ run(cargo, destination): String[]'])

    for b in (transport, truck, ship, logistics, road, sea, client):
        b.measure(c, FS)

    transport.place(8, FM_H - transport.h - 18)
    logistics.place(FM_W - logistics.w - 6, FM_H - logistics.h - 18)
    truck.place(8, 168)
    ship.place(8, 92)
    road.place(FM_W - road.w - 38, 168)
    sea.place(FM_W - sea.w - 38, 92)
    client.place(FM_W - client.w - 38, 8)

    # Products implement the Transport contract.
    conn(c, truck.T(.22), transport.B(.22), 'implements')
    conn(c, ship.T(.62), transport.B(.62), 'implements')
    # Creators extend the abstract Logistics.
    conn(c, road.T(.3), logistics.B(.3), 'extends')
    conn(c, sea.T(.75), logistics.B(.75), 'extends')
    # The creator creates and uses a Transport.
    conn(c, logistics.L(), transport.R(), 'depends', 'creates and uses', ly=3)
    # Each concrete creator instantiates its own product.
    conn(c, road.L(), truck.R(), 'depends', '<<creates>>', ly=3)
    conn(c, sea.L(), ship.R(), 'depends', '<<creates>>', ly=3)
    # The client depends on the abstract creator only.
    conn(c, client.T(.18), sea.B(.18), 'assoc', 'planDelivery(...)', lx=44, ly=1)

    for b in (transport, truck, ship, logistics, road, sea, client):
        b.draw(c, FS)

    note(c, 8, 8, ['planDelivery(cargo, destination) {',
                   '    Transport t = createTransport();  // subclass decides',
                   '    return t.deliver(cargo, destination);  // via contract',
                   '}'])


def abstract_factory(c):
    button = Box('Button', '<<AbstractProduct>>', ops=['+ paint(): String'], italic=True)
    checkbox = Box('Checkbox', '<<AbstractProduct>>', ops=['+ paint(): String'], italic=True)
    gui = Box('GUIFactory', '<<AbstractFactory>>',
              ops=['+ createButton(): Button', '+ createCheckbox(): Checkbox',
                   '+ platformName(): String'], italic=True)
    wb = Box('WindowsButton', '<<ConcreteProduct>>', ops=['+ paint(): String'])
    wc = Box('WindowsCheckbox', '<<ConcreteProduct>>', ops=['+ paint(): String'])
    mb = Box('MacOSButton', '<<ConcreteProduct>>', ops=['+ paint(): String'])
    mc = Box('MacOSCheckbox', '<<ConcreteProduct>>', ops=['+ paint(): String'])
    wf = Box('WindowsFactory', '<<ConcreteFactory>>',
             ops=['+ createButton(): Button', '+ createCheckbox(): Checkbox'])
    mf = Box('MacOSFactory', '<<ConcreteFactory>>',
             ops=['+ createButton(): Button', '+ createCheckbox(): Checkbox'])
    client = Box('DeliveryApplication', '<<Client>>',
                 attrs=['- guiFactory: GUIFactory', '- button: Button', '- checkbox: Checkbox'],
                 ops=['+ run(cargo, destination): String[]'])

    for b in (button, checkbox, gui, wb, wc, mb, mc, wf, mf, client):
        b.measure(c, FS)

    top = AF_H - 18
    # Abstract products on the left, abstract factory on the right.
    button.place(8, top - button.h)
    checkbox.place(8, top - button.h - checkbox.h - 14)
    gui.place(AF_W - gui.w - 6, top - gui.h + 4)

    # Windows family column, then macOS family column - each under its own factory.
    col1 = 140
    col2 = col1 + max(wb.w, wc.w, wf.w) + 30
    wb.place(col1, 236)
    wc.place(col1, 236 - wc.h - 12)
    mb.place(col2, 236)
    mc.place(col2, 236 - mc.h - 12)

    wf.place(col1, 236 + wb.h + 40)
    mf.place(col2, 236 + mb.h + 40)
    client.place(AF_W - client.w - 6, 14)

    # Concrete components implement their abstract product (left-hand interfaces).
    conn(c, wb.L(.7), button.B(.35), 'implements')
    conn(c, mb.T(.5), button.R(.25), 'implements')
    conn(c, wc.L(.55), checkbox.B(.35), 'implements')
    conn(c, mc.L(.3), checkbox.R(.4), 'implements')

    # Concrete factories implement the abstract factory.
    conn(c, wf.T(.55), gui.L(.8), 'extends')
    conn(c, mf.T(.75), gui.L(.25), 'extends')

    # Each factory creates its own family pair - short vertical links inside the column.
    conn(c, wf.B(.25), wb.T(.25), 'depends', '<<creates>>', lx=-24, ly=2)
    conn(c, wf.B(.62), wb.T(.75), 'depends')
    conn(c, wb.B(.85), wc.T(.85), 'depends')
    conn(c, mf.B(.25), mb.T(.25), 'depends', '<<creates>>', lx=-24, ly=2)
    conn(c, mf.B(.62), mb.T(.75), 'depends')
    conn(c, mb.B(.85), mc.T(.85), 'depends')

    # Client: constructor injection of the factory, use through product interfaces.
    conn(c, client.T(.4), mf.R(.2), 'assoc', 'injected', lx=26, ly=2)
    conn(c, client.L(.5), mc.B(.75), 'depends', 'uses', lx=6, ly=3)

    for b in (button, checkbox, gui, wb, wc, mb, mc, wf, mf, client):
        b.draw(c, FS)

    note(c, 8, 14, ['DeliveryApplication(GUIFactory f, Logistics l) {',
                    '    this.button   = f.createButton();    // one family,',
                    '    this.checkbox = f.createCheckbox();  // no casts',
                    '}'])


def fm_flowable(width):
    return UML(width, FM_W, FM_H, factory_method)


def af_flowable(width):
    return UML(width, AF_W, AF_H, abstract_factory)
