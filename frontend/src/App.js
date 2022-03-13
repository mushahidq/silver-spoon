import logo from './logo.svg';
import './App.css';
import React, {useState} from 'react';
import { Helmet } from 'react-helmet';
import axios from 'axios';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  const [url, setURL] = useState('');
  const [message, setMessage] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const TITLE = 'Apache Struts Scanner';

  let handleSubmit = (e) => {
    e.preventDefault();
    setMessage('');
    setSubmitting(true);
    axios.get('http://localhost:5000/scan?url=' + url).then(response => {
      setSubmitting(false);
      setMessage(response.data.status);
    }).catch(error => {
      console.log(error)
    })
  }

  return (
    <div className="App">
      <Helmet>
          <title>{ TITLE }</title>
        </Helmet>
        <Router>
          <Navbar />
        </Router>
      <header className="App-header">
        <h3>Apache Struts Scanner</h3>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Enter URL" value={url} onChange={(e) => setURL(e.target.value)}/>
          <button type="submit">Submit</button>
        </form>
        <div className='message'>
          <p>{submitting &&
            <span>Scanning......</span>
          }</p>
          <p>{message}</p>
        </div>
      </header>
    </div>
  );
}

export default App;
