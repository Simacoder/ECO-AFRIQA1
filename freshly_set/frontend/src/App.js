import './App.css';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import About from './components/pages/about-us/About';
import Home from "./components/pages/homepage/Home"
import SignUp from './components/pages/login/LoginSignup';
import Blogs from "./components/pages/blogs/Blogs";

function App() {
  return (
    <Router>
    <Routes>
        <Route path="/signup" element={<SignUp />} />
        <Route path="/" element={<Home />} />
        <Route path="/blogs" element={<Blogs />} />
        <Route path="/about-us" element={<About />} />
    </Routes>
</Router>

  );
}

export default App;
