import React from "react";
import { Helmet } from 'react-helmet';

const About_log4j = () => {
    const TITLE = 'Apache Struts Scanner';
    return (
        <div className="App">
            <Helmet>
                <title>{ TITLE }</title>
            </Helmet>
            <header className="App-header">
                <div className="container" style={{transform: "translate(-50%,-60%)"}}>
                    <h3>About Log4Shell Vulnerability</h3>
                    <p>
                        Log4Shell (CVE-2021-44228) was a zero-day vulnerability in Log4j,
                        a popular Java logging framework, involving arbitrary code execution.
                    </p>
                </div>
            </header>
        </div>
    );
}

export default About_log4j;