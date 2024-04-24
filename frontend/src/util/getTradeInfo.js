import axios from 'axios';

export async function getTradeInfo() {
  try {
    const response = await axios.get('http://127.0.0.1:5000/trade_info');
    return response.data;
  } catch (error) {
    console.error('Error fetching trade info:', error);
    return null; // Handle errors by returning null or a default value
  }
}
