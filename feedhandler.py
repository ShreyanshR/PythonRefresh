from dataclasses import dataclass
from enum import Enum, auto
from statistics import quantiles

type Quantity = int
type Price = float
type SeqNo = int

class Event(Enum):
    DISCONNECT = auto()
    ADD = auto()
    CHANGE = auto()
    DELETE = auto()

@dataclass
class DataBlock:
    event: Event
    price: Price | None
    quantity: Quantity | None
    seqNo: SeqNo
    isBuy: bool | None

@dataclass
class OrderBook:
    bids: dict[Price, Quantity]
    asks: dict[Price, Quantity]

@dataclass
class Snapshot:
    book: OrderBook
    asOfSeqNo: SeqNo

class EventStream:
    def __init__(self):
        self.orderBook: OrderBook = OrderBook({}, {})
        self.next_expected_seqNo = 1
        self.buffer = {}
        self.disconnect : bool = False
    
    def processMessage(self, msg: DataBlock | Snapshot) -> None:
        if isinstance(msg, DataBlock):
            if msg.event == Event.DISCONNECT:
                self.disconnect = True
                self.orderBook = OrderBook({}, {})
                self.next_expected_seqNo = msg.seqNo + 1

            elif msg.seqNo == self.next_expected_seqNo:
                if not self.disconnect:
                    self._processDataBlock(msg)
                    self.next_expected_seqNo += 1
                    while self.next_expected_seqNo in self.buffer:
                        buffered_block = self.buffer[self.next_expected_seqNo]
                        self._processDataBlock(buffered_block)
                        self.buffer.pop(self.next_expected_seqNo)
                        self.next_expected_seqNo += 1

                else:
                    self.next_expected_seqNo += 1

            else:
                self.buffer[msg.seqNo] = msg

        elif isinstance(msg, Snapshot):
            self.orderBook = msg.book
            self.next_expected_seqNo = msg.asOfSeqNo
            self.disconnect = False

            while self.next_expected_seqNo in self.buffer:
                buffered_block = self.buffer[self.next_expected_seqNo]
                self._processDataBlock(buffered_block)
                self.buffer.pop(self.next_expected_seqNo)
                self.next_expected_seqNo += 1

    def _processDataBlock(self, block: DataBlock) -> None:
        if block.event == Event.ADD:
            if block.isBuy:
                self.orderBook.bids[block.price] = block.quantity
            else:
                self.orderBook.asks[block.price] = block.quantity
        
        elif block.event == Event.CHANGE:
            if block.isBuy:
                self.orderBook.bids[block.price] = block.quantity
            else:
                self.orderBook.asks[block.price] = block.quantity
        
        elif block.event == Event.DELETE:
            if block.isBuy:
                self.orderBook.bids.pop(block.price)
            else:
                self.orderBook.asks.pop(block.price)


if __name__ == "__main__":
    eventStream = EventStream()
    snapShot_1 = Snapshot(OrderBook({1:2}, {5:3}), 1) 
    dataBlock_1 = DataBlock(Event.ADD, 2, 5, 1, True) 
    dataBlock_2 = DataBlock(Event.DELETE, 5, None, 2, False)

    eventStream.processMessage(snapShot_1)
    eventStream.processMessage(dataBlock_1)
    eventStream.processMessage(dataBlock_2)
    print(eventStream.orderBook)


