 
import {React,useState,useEffect,useRef} from 'react';
import axios from 'axios';
const TransactionList = ({}) => {
  const [transactions, setTransactions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);
  const fetchTransactions = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://127.0.0.1:5000/deals', {
        user: 'mo', // Assuming the required user data
      });
       
      setTransactions(response.data.sort((a, b) => b[4] - a[4])); // Sort by time (index 4) descending
      // setTransactions(response.data);  
    } catch (error) {
      console.error('Error fetching transactions:', error);
      setError(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
    intervalRef.current = setInterval(fetchTransactions, 10000); // Check every 5 seconds

    return () => {
      // Clear the interval when the component unmounts
      clearInterval(intervalRef.current);
    };
  }, []);

// ... rest of the component code

return (
  <div className="transaction-list table-responsive">
    <h2>Transaction History</h2>
    {isLoading ? (
      <p>Loading transactions...</p>
    ) : error ? (
      <p className="alert alert-danger" role="alert">
        Error fetching transactions: {error.message}
      </p>
    ) : (
      <table className="table table-striped">
        <thead>
          <tr>
            {/* Removed ID column */}
            <th scope="col">Type</th>
            <th scope="col">Price</th>
            <th scope="col">Quantity</th>
            <th scope="col">Time</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction[0]}>
              {/* Removed ID from cell */}
              <td>{transaction[1]}</td>
              <td>${transaction[2].toFixed(2)}</td>
              <td>{transaction[3]}</td>
              <td>{transaction[4]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    )}
  </div>
);
};

export default TransactionList;

 
