import React from 'react';

export default function Log ({ log }) {
    return (
        <tr>
            <td>{log[1]}</td>
            <td>{log[2]}</td>
            <td>{log[3]}</td>
            <td>{log[4]}</td>
        </tr>
    );
}