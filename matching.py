import sortedcontainers 
class order:
    def __init__(self,owner,price,qunantity) -> None:
        self.owner=owner
        self.price= price
        self.quantity =qunantity
class  orderbook:
    def __init__(self) -> None:
        self.orderbook= sortedcontainers.SortedDict( )
        self.orderlist= sortedcontainers.SortedDict()
    def add_order(self,price:float ,owner:str,quantity:int)->None:
        if price in self.orderbook :
            self.orderbook[price]+= quantity
        else :
            self.orderbook[price]=quantity
        if price in self.orderlist:
            self.orderlist[price] .append ({owner: quantity })
        else : 
            self.orderlist [price]=  [{owner: quantity} ]

test = orderbook()
test.add_order(45.0,"asdf",45) 
test.add_order(45.0,"asdf",45) 
print(test.orderbook,test.orderlist )   

