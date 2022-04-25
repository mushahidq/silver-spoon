import './App.css';
import React, {useState} from 'react';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages';
import About_Struts from './pages/about_struts';
import Contact from './pages/contact';
import Logs from './pages/logs';
import About_log4j from './pages/about_log4j';

function App() {

  const [logs, setLogs] = useState();

  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path='/' exact element={<Home />} />
        <Route path='/about_struts' element={<About_Struts />} />
        <Route path='/about_log4j' element={<About_log4j />} />
        <Route path='/contact' element={<Contact />} />
        <Route path='/logs' element={<Logs logs={logs} setLogs={setLogs}/>} />
        <Route path='*' exact={true} element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
