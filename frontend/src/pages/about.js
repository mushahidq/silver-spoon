import React from "react";
import { Helmet } from 'react-helmet';

const About = () => {
    const TITLE = 'Apache Struts Scanner';
    return (
        <div className="App">
            <Helmet>
                <title>{ TITLE }</title>
            </Helmet>
            <header className="App-header">
                <div className="container">
                    <h3>About Apache Struts RCE Vulnerability</h3>
                    <p>
                        Apache Struts is a Java web framework that is used to build web applications.
                        It is a Java-based web framework that is used to build web applications.
                    </p>
                </div>
            </header>
        </div>
    );
}

export default About;