 
import React, { useState, useEffect } from 'react';
import { Spinner } from 'react-bootstrap'; // Assuming you're using Bootstrap

import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
async function getTradeInfo(setTradePrice,setTradeInfo) {
  try {
    const response = await axios.get('http://127.0.0.1:5000/trade_info');
    // console.log(response.data)
    setTradePrice(response.data.price); // Update component state with the fetched price

    setTradeInfo(response.data.info)
    // console.log(response.data.info.buy)

    
  } catch (error) {
    console.error('Error fetching trade info:', error);
  }
}

const TradePrice = ( ) => {
  const [tradePrice, setTradePrice] = useState(null); // Initialize state for trade price
  
  const [tradeInfo, setTradeInfo] = useState(null);
  useEffect(() => {
    const fetchData = async () => {
      await getTradeInfo(setTradePrice,setTradeInfo); // Update component state on mount
    };
    const intervalId = setInterval(fetchData, 3000); // Update every 5 seconds

    return () => clearInterval(intervalId); // Cleanup function to stop interval on unmount
  }, []); // Empty dependency array to run only once on mount
  const slicedBuyPrices = Object.keys(tradeInfo.buy)
  .filter((buyPrice) => tradeInfo.buy[buyPrice] > 0)
  .reverse()
  .slice(0, 5); // Limit to top 5 elements
  const slicedSellPrices = Object.keys(tradeInfo.sell)
  .filter((sellPrice) => tradeInfo.sell[sellPrice] > 0)
   
  .slice(0, 5); // Limit to top 5 elements
  return (
    <div className="trade-price mb-3">
      

      {/* Display Buy and Sell Information */}
      {tradeInfo && ( // Check if tradeInfo is available
        <div style={{ display: 'flex' }}>
          <div>
          <h4>Buy Orders</h4>
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Price</th>
                <th>Volume</th>
              </tr>
            </thead>
            <tbody>
              {/* Loop through buy orders */}
              {slicedBuyPrices.map((buyPrice) => (
                  <tr key={buyPrice}>
                    <td>{buyPrice}</td>
                    <td>{tradeInfo.buy[buyPrice]}</td>
                  </tr>
                ))}
            </tbody>
          </table>
          </div>
          
            <div>
            <h4>Sell Orders</h4>
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Price</th>
                <th>Volume</th>
              </tr>
            </thead>
            <tbody>
              {/* Loop through sell orders */}
              {slicedSellPrices.map((sellPrice) => (
                  <tr key={sellPrice}>
                    <td>{sellPrice}</td>
                    <td>{tradeInfo.sell[sellPrice]}</td>
                  </tr>
                ))}

            </tbody>
          </table>
            </div>
         
        </div>
      )}
      <h2>Trade Price</h2>

      {tradePrice === null ? (
        <div className="trade-price-value">
          <Spinner size="sm" variant="primary" /> Loading trade price...
        </div>
      ) : (
        <p className="trade-price-value">Price: {tradePrice}</p>
      )}
      {/* Button logic here (if applicable) */}
    </div>
  );
};

export default TradePrice;
