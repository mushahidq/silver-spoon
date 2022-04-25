import React, {useState} from 'react';
import axios from 'axios';
import { Helmet } from 'react-helmet';

const About = () => {
    const [email, setEmail] = useState('');
    const [feedback, setFeedback] = useState('');
    const [message, setMessage] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const TITLE = 'Apache Struts Scanner';

    let handleSubmit = async (e) => {
        e.preventDefault();
        const loginFormData = new FormData();
        loginFormData.append('email', email);
        loginFormData.append('feedback', feedback);
        setMessage('');
        setSubmitting(true);
        try {
            // make axios post request
            await axios({
              method: "post",
              url: "/feedback",
              data: loginFormData,
              headers: { "Content-Type": "multipart/form-data" },
            }).then(response => {
                setSubmitting(false);
                if (response.data.status === 'success') {
                    setMessage('Successfully submitted feedback');
                } else {
                    setMessage('Failed to submit feedback');
                }
            }).catch(error => {
                setSubmitting(false);
                setMessage("Failed to submit feedback");
                console.log(error)
            });
          } catch(error) {
            setSubmitting(false);
            setMessage("Failed to submit feedback");
            console.log(error)
        }
    }
    
    return (
        <div className="App">
            <Helmet>
                <title>{ TITLE }</title>
            </Helmet>
            <header className="App-header">
            <form onSubmit={handleSubmit}>
                <h3>Provide Feedback</h3>
                <input type="text" placeholder="Enter email" value={email} onChange={(e) => setEmail(e.target.value)}/>
                <input type="text" placeholder="Enter feedback" value={feedback} onChange={(e) => setFeedback(e.target.value)}/>
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

export default About;