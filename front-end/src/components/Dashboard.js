import React, {useState} from 'react'
import axios from 'axios';

const Dashboard = ({token, logout}) => {
    const [amount, setAmount] = useState('');
    const [service, setService] = useState('');
    const [feedback, setFeedback] = useState('');

    const submitPayment = async () => {
        await axios.post('/payment', {amount}, {headers: {'x-access-token': token}});
        alert('Payment processed successfully');
    };

    const submitServiceRequest = async () => {
        await axios.post('/service-request', {service}, {headers: {'x-access-token': token}});
        alert('Service request submitted successfully');
    };

    const submitFeedback = async () => {
        await axios.post('/feedback', {feedback}, {headers: {'x-access-token': token}});
        alert('Feedback submitted successfully');
    };

    return (
        <div>
            <h1>Dashboard</h1>
            <button onClick={logout}>Logout</button>
            <div>
                <h2>Payment</h2>
                <input type='text' placeholder='Amount' value={amount} onChange={(e) => setAmount(e.target.value)} />
                <button onClick={submitPayment}>Submit Payment</button>
            </div>
            <div>
                <h2>Service Request</h2>
                <input type="text" placeholder="Service" value={service} onChange={(e) => setService(e.target.value)} />
                <button onClick={submitServiceRequest}>Submit Service Request</button>
            </div>
            <div>
                <h2>Feedback</h2>
                <input type="text" placeholder="Feedback" value={feedback} onChange={(e) => setFeedback(e.target.value)} />
                <button onClick={submitFeedback}>Submit Feedback</button>
            </div>
        </div>
    );
};

export default Dashboard;