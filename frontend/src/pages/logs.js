import React from 'react';
import { Helmet } from 'react-helmet';
import Login from './login';
import PropTypes from 'prop-types';
import Log from '../components/log';

const Logs = ({logs, setLogs}) => {
    const TITLE = 'Apache Struts Scanner';

    if (!logs) {
        return <Login setLogs={setLogs} />;
    }

    const logsList = logs.logs;
    const feedback = logs.feedbacks;

    return (
        <div className='Table-Container'>
            <Helmet>
                <title>{ TITLE }</title>
            </Helmet>
            <section>
                <h1>Apache Struts Scanner Logs</h1>
                <div class="tbl-header">
                    <table cellpadding="0" cellspacing="0" border="0">
                    <thead>
                        <tr>
                            <th>Request IP</th>
                            <th>Target URL</th>
                            <th>Result</th>
                            <th>Timestamp</th>
                        </tr>
                    </thead>
                    </table>
                </div>
                <div class="tbl-content">
                    <table cellpadding="0" cellspacing="0" border="0">
                        <tbody>
                            { logsList.map((log)=> (<Log log={log} />)) }
                        </tbody>
                    </table>
                </div>
            </section>

            <section>
                <h1>Feedback</h1>
                <div class="tbl-header">
                    <table cellpadding="0" cellspacing="0" border="0">
                    <thead>
                        <tr>
                            <th>Request IP</th>
                            <th>Feedback</th>
                            <th>Email</th>
                            <th>Timestamp</th>
                        </tr>
                    </thead>
                    </table>
                </div>
                <div class="tbl-content">
                    <table cellpadding="0" cellspacing="0" border="0">
                        <tbody>
                            { feedback.map((feedback) => (<Log log={feedback} />)) }
                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    );
}

Logs.propTypes = {
    logs: PropTypes.object.isRequired,
    setLogs: PropTypes.func.isRequired
}

export default Logs;