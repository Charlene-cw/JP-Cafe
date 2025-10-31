CREATE TABLE 'Inventory' (
    'ItemID' TEXT,
    'ItemName' TEXT,
    'Description' TEXT,
    'Price' TEXT,
    'Quantity' NUM,
    'Image' TEXT,
    PRIMARY KEY('ItemID')
);

CREATE TABLE 'Member' (
    'MemName' TEXT,
    'MemEmail' TEXT,
    'Password' TEXT,
    'Mobile' TEXT,
    PRIMARY KEY ('MemEmail')
);

CREATE TABLE 'Orders' (
    'OrderID' TEXT,
    'CustomerName' TEXT,
    'Date' TEXT,
    'IsMem' NUM,
    'TotalPayable' NUM,
    PRIMARY KEY ('OrderID')
);

CREATE TABLE 'ItemOrdered' (
    'OrderID' TEXT,
    'ItemID' TEXT,
    'Quantity' NUM,
    FOREIGN KEY('OrderID') REFERENCES 'Order'('OrderID'),
    FOREIGN KEY('ItemID') REFERENCES 'Inventory'('ItemID')
);
