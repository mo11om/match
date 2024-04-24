import React from 'react';

const OrderList = ({ orders }) => {
  return (
    <>
      <h2>Orders</h2>
      <ul>
        {orders.map((order) => (
          <li key={order.id}>{order.name} (quantity: {order.quantity})</li>
        ))}
      </ul>
    </>
  );
};

export default OrderList;
