import React, {useState} from 'react';
import { Helmet } from 'react-helmet';
import PropTypes from 'prop-types';

async function loginUser(creds) {
    return fetch('/logs', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(creds)
    })
    .then(response => response.json())
}
export default function Login ({ setLogs }) {
    const TITLE = 'Apache Struts Scanner';
    const [message, setMessage] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    console.log(typeof(setLogs));
    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');
        setSubmitting(true);
        const logs = await loginUser({username, password});
        console.log(logs);
        if (!logs.status) {
            setSubmitting(false);
            setLogs(logs);
        }
        else {
            setSubmitting(false);
            setMessage(logs.data.status);
        }
    }

    return (
        <div className="App">
            <Helmet>
                <title>{ TITLE }</title>
            </Helmet>
            <header className="App-header">
                <form onSubmit={handleSubmit}>
                    <h3>Login</h3>
                    <input type="text" placeholder="Enter username" onChange={e => setUsername(e.target.value)}/>
                    <input type="text" placeholder="Enter password" onChange={e => setPassword(e.target.value)}/>
                    <button type="submit">Submit</button>
                    <div className='message'>
                        <p>{submitting &&
                        <span>Submitting.....</span>
                        }</p>
                        <p>{message}</p>
                    </div>
                </form>
            </header>
        </div>
    );
}

Login.propTypes = {
    setLogs: PropTypes.func.isRequired
}