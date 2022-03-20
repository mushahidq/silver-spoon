import './App.css';
import React, {useState} from 'react';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages';
import About from './pages/about';
import Contact from './pages/contact';
import Login from './pages/login';
import Logs from './pages/logs';

function App() {

  const [logs, setLogs] = useState();

  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path='/' exact element={<Home />} />
        <Route path='/about' element={<About />} />
        <Route path='/contact' element={<Contact />} />
        <Route path='/login' element={<Login setLogs={setLogs} />} />
        <Route path='/logs' element={<Logs logs={logs} setLogs={setLogs}/>} />
        <Route path='*' exact={true} element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
