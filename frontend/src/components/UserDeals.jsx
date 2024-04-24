import React from 'react';

const UserDeals = ({ user, setUser, deals, onGetDeals }) => {
  return (
    <>
      <h2>User Deals</h2>
      <label>
        User:
        <input type="text" value={user} onChange={(e) => setUser(e.target.value)} />
      </label>
      <button onClick={onGetDeals}>Get Deals</button>
      {deals.length > 0 && (
        <ul>
          {deals.map((deal) => (
            <li key={deal.id}>{deal.name} (details...)</li>
          ))}
        </ul>
      )}
    </>
  );
};

export default UserDeals;
