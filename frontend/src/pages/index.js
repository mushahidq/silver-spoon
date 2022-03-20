import React, {useState} from 'react';
import axios from 'axios';
import { Helmet } from 'react-helmet';

const Home = () => {

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
        }).catch(() => {
            setSubmitting(false);
            setMessage("Failed to submit feedback");
        })
    }

    return (
        <div className="App">
            <Helmet>
                <title>{ TITLE }</title>
            </Helmet>
            <header className="App-header">
            <form onSubmit={handleSubmit}>
                <h3>Apache Struts Scanner</h3>
                <input type="text" placeholder="Enter URL" value={url} onChange={(e) => setURL(e.target.value)}/>
                <button type="submit">Submit</button>
                <div className='message'>
                    <p>{submitting &&
                    <span>Scanning......</span>
                    }</p>
                    <p>{message}</p>
                </div>
            </form>
            </header>
        </div>
    );
}

export default Home;