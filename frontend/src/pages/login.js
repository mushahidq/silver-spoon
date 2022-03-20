import React, {useState} from 'react';
import axios from 'axios';
import { Helmet } from 'react-helmet';

const Login = () => {
    const TITLE = 'Apache Struts Scanner';

    return (
        <div className="App">
            <Helmet>
                <title>{ TITLE }</title>
            </Helmet>
            <header className="App-header">
                <form method='POST' action='http://localhost:5000/logs'>
                    <h3>Login</h3>
                    <input type="text" placeholder="Enter username" name='username'/>
                    <input type="text" placeholder="Enter password" name='password'/>
                    <button type="submit">Submit</button>
                </form>
            </header>
        </div>
    );
}

export default Login;