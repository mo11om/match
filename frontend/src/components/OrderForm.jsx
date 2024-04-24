import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS

const OrderForm = ({ }) => {
  const [product, setProduct] = useState({
    user: 'mo', // Set a default user
    order_type: 'buy', // Use orderType for consistency
    price: 0.00,
    quantity: 1,
    condition: '', // Optional condition
    market: false, // Optional market type
  });
  const [showConfirm, setShowConfirm] = useState(false); // State for confirmation dialog


  const handleChange = (event) => {
    const { name, value } = event.target;
    setProduct((prevProduct) => ({ ...prevProduct, [name]: value }));
    
  };
  const handleintChange = (event) => {
    const { name, value } = event.target;
    const newValue = parseInt(value, 10); // Parse to integer (optional)
    setProduct((prevProduct) => ({ ...prevProduct, [name]: newValue }));
     

  };
  // const handleConfirm = () => {
  //   // onSubmit(product); // Pass the entire product object on confirmation
  //   console.log (product)
  //   setShowConfirm(false); // Close confirmation dialog
    
  // };
  const handleConfirm = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(product),
      });

      if (response.ok) {
        // Handle successful submission (e.g., show success message)
        console.log('Order submitted successfully!');
        setShowConfirm(false); // Close confirmation dialog
      } else {
        // Handle failed submission (e.g., show error message)
        console.error('Error submitting order:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };
  const handleSubmit = (event) => {
    event.preventDefault();
    setShowConfirm(true); // Open confirmation dialog before submitting
  };
  return (
    <div className="order-form"> {/* Add a class for styling */}
      <h2>Place Order</h2>
      <form onSubmit={handleSubmit} className="row mb-3"> {/* Add Bootstrap classes */}
      <div className="col-md-4">
          <label htmlFor="type" className="form-label">
            type:
          </label>
          <select
            name="order_type"
            id="order_type"
            value={product.order_type}
            onChange={handleChange}
            className="form-control"
          >
            <option value="">Select </option>

            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
          </select>
        </div> 
        <div className="col-md-10">
          <label htmlFor="condition" className="form-label">
            Condition:
          </label>
          <select
            name="condition"
            id="condition"
            value={product.condition}
            onChange={handleChange}
            className="form-control"
          >
            <option value="">Select Condition</option>
            <option value="ROD">ROD  </option>
            <option value="IOC">IOC (Instant or Cancel)</option>
            <option value="FOK">FOK (Fill or Kill)</option>
          </select>
        </div>
        <div className="col-md-6">
          <label htmlFor="price" className="form-label">
            Price:
          </label>
          <input
            type='number'
            name="price"
            id="price"
            required
            min={1}
            step="1"
            value={product.price}
            onChange={handleintChange}
            className="form-control"
          />
        </div>

        <div className="col-md-6"> {/* Use grid system for responsive layout */}
          <label htmlFor="quantity" className="form-label">
            Quantity:
          </label>
          <input
            type="number"
            name="quantity"
            id="quantity"
            required
            min={1}
            value={product.quantity}
            onChange={handleintChange}
            className="form-control"
          />
        </div>
        <div className="col-12"> {/* Full width for button */}
          <button type="submit" className="btn btn-primary">
            Submit Order
          </button>
        </div>
      </form>
      
      {showConfirm && ( // Conditionally render confirmation dialog
        <div className="confirmation-modal">
          <p>Are you sure you want to submit this order?</p>
          <button onClick={handleConfirm} className="btn btn-success">
            Confirm
          </button>
          <button onClick={() => setShowConfirm(false)} className="btn btn-light">
            Cancel
          </button>
        </div>
      )}
    </div>
  );
};

export default OrderForm;
