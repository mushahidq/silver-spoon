import React, {useState} from 'react';
import axios from 'axios';
import { Helmet } from 'react-helmet';

const Home = () => {

    const [url, setURL] = useState('');
    const [message, setMessage] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [type, setType] = useState('');
    const TITLE = 'Apache Struts and Log4J Scanner';

    let handleSubmit = (e) => {
        e.preventDefault();
        setMessage('');
        setSubmitting(true);
        axios.get('/scan?url=' + url + '&type=' + type).then(response => {
            setSubmitting(false);
            setMessage(response.data.status);
        }).catch(() => {
            setSubmitting(false);
            setMessage("Failed to submit URL");
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
                <label for="scan">Choose scan type:</label>
                <select onChange={(e) => setType(e.target.value)}>
                    <option value="struts">Apache Struts</option>
                    <option value="log4shell">Log4shell</option>
                </select>
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