// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vitejs.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>
//       </div>
//       <h1>Vite + React</h1>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/App.jsx</code> and save to test HMR
//         </p>
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//     </>
//   )
// }

// export default App

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import OrderList from './components/Orderlist'; // Import OrderList component
import OrderForm from './components/OrderForm'; // Import OrderForm component 
 
import TradePrice from './components/TradePrice'; // Import TradePrice component
// import TradeInfo from './components/TradeInfo'; // Import TradePrice component
import './style.css'; // Import CSS file
import TransactionList from './components/TransactionList';

const API_URL = 'http://localhost:5000'; // Replace with your Flask app's URL

function App() {
  const [orders, setOrders] = useState([]);
  const [user, setUser] = useState('');
  const [deals, setDeals] = useState([]);
  const [tradePrice, setTradePrice] = useState(null);

  // ... rest of the code remains the same (useEffect, handle functions) ...

  return (
    <div > 
      <h1>Trade App</h1>
      
      {/* <OrderList orders={orders} /> */}
      <div style={{ display: 'flex' }}>
        <OrderForm style={{ flex: 1 }} />  {/* Set flex: 1 for OrderForm */}
        <TradePrice   style={{ flex: 100  }} /> {/* Set specific width for TradePrice */}
        <TransactionList/>
      </div>

     </div>
    
   
  );
}

export default App;
